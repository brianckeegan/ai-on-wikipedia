"""Build the sampling frame and map it across languages through Wikidata.

The frame is the set of main-namespace articles assessed by English WikiProject Artificial
Intelligence (WP1 snapshot). Each article is resolved to its Wikidata item, and every item is
located in all analysis wikis through its sitelinks, so every edition is measured on the same
set of topics.

Lookups go to the Wikidata Query Service (WDQS) in bulk: English titles are matched exactly
against sitelink names, then sitelinks are fetched for all items. The Action APIs are used
only where WDQS cannot answer: resolving the few WP1 titles that are redirects or need
normalization; fetching sitelinks for items the main WDQS graph does not hold (since the 2025
graph split, scholarly works such as "Attention Is All You Need" live in a separate graph);
and looking up local page IDs (which join the frame to the revision dumps).

Usage: python -m ai_on_wikipedia.frame <wp1.tsv> <frame.parquet> [--skip-page-ids]
"""

from __future__ import annotations

import argparse
import re
import sys
from string import Template

import pandas as pd

from .client import batched, get_json, mw_query, sparql
from .settings import api_url, load_config
from .wp1 import frame_titles, load_wp1

WIKIDATA_API = "https://www.wikidata.org/w/api.php"
TITLE_BATCH = 200
ITEM_BATCH = 400

# string.Template keeps SPARQL's literal braces readable (no f-string brace escaping).
TITLES_QUERY = Template(
    "SELECT ?name ?item WHERE { VALUES ?name { $values } "
    "?article schema:name ?name; schema:isPartOf <https://$wiki.wikipedia.org/>; "
    "schema:about ?item }"
)
SITELINKS_QUERY = Template(
    "SELECT ?item ?site ?title WHERE { VALUES ?item { $values } "
    "?article schema:about ?item; schema:isPartOf ?site; schema:name ?title. "
    "FILTER(?site IN ($sites)) }"
)


def sparql_string(text: str, lang: str) -> str:
    """A SPARQL language-tagged string literal, with backslashes and quotes escaped."""
    escaped = text.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"@{lang}'


def titles_query(titles: list[str], wiki: str) -> str:
    """WDQS query matching exact article titles in one wiki to their Wikidata items."""
    values = " ".join(sparql_string(t, wiki) for t in titles)
    return TITLES_QUERY.substitute(values=values, wiki=wiki)


def sitelinks_query(qids: list[str], wikis: list[str]) -> str:
    """WDQS query returning each item's article title in each of the given wikis."""
    values = " ".join(f"wd:{q}" for q in qids)
    sites = ", ".join(f"<https://{w}.wikipedia.org/>" for w in wikis)
    return SITELINKS_QUERY.substitute(values=values, sites=sites)


def qid_from_iri(iri: str) -> str:
    return iri.rsplit("/", 1)[1]


def wiki_from_site(site: str) -> str:
    match = re.match(r"https://([a-z0-9-]+)\.wikipedia\.org/", site)
    if not match:
        raise ValueError(f"Not a Wikipedia site IRI: {site}")
    return match.group(1)


def wdqs_titles_to_qids(wiki: str, titles: list[str]) -> dict[str, str]:
    """Exact title -> QID through WDQS. Redirects and non-normalized titles are not matched."""
    out: dict[str, str] = {}
    for batch in batched(titles, TITLE_BATCH):
        for row in sparql(titles_query(batch, wiki)):
            out[row["name"]] = qid_from_iri(row["item"])
    return out


def api_titles_to_qids(wiki: str, titles: list[str]) -> dict[str, str]:
    """Title -> QID through the Action API, following redirects and normalization."""
    out: dict[str, str] = {}
    for batch in batched(titles, 50):
        for chunk in mw_query(
            api_url(wiki),
            {
                "prop": "pageprops",
                "ppprop": "wikibase_item",
                "redirects": "1",
                "titles": "|".join(batch),
            },
        ):
            back = {}
            for r in chunk.get("normalized", []) + chunk.get("redirects", []):
                back[r["to"]] = back.get(r["from"], r["from"])
            for p in chunk.get("pages", []):
                qid = p.get("pageprops", {}).get("wikibase_item")
                if qid:
                    out[back.get(p["title"], p["title"])] = qid
    return out


def api_sitelinks(qids: list[str], wikis: list[str]) -> list[dict]:
    """Sitelinks through the Wikidata Action API, for items WDQS does not return."""
    sites = {f"{w}wiki": w for w in wikis}
    rows = []
    for batch in batched(qids, 50):
        data = get_json(
            WIKIDATA_API,
            {
                "action": "wbgetentities",
                "ids": "|".join(batch),
                "props": "sitelinks",
                "format": "json",
            },
        )
        for qid, entity in data.get("entities", {}).items():
            for site, link in entity.get("sitelinks", {}).items():
                if site in sites:
                    rows.append({"qid": qid, "wiki": sites[site], "title": link["title"]})
    return rows


def sitelinks(qids: list[str], wikis: list[str]) -> pd.DataFrame:
    """One row per (qid, wiki) where the item has an article in that wiki."""
    rows = []
    for batch in batched(qids, ITEM_BATCH):
        for row in sparql(sitelinks_query(batch, wikis)):
            rows.append(
                {
                    "qid": qid_from_iri(row["item"]),
                    "wiki": wiki_from_site(row["site"]),
                    "title": row["title"],
                }
            )
    found = {r["qid"] for r in rows}
    missing = [q for q in qids if q not in found]
    if missing:
        print(f"Sitelinks via the Wikidata API for {len(missing)} items", file=sys.stderr)
        rows += api_sitelinks(missing, wikis)
    return pd.DataFrame(rows, columns=["qid", "wiki", "title"])


def title_page_ids(wiki: str, titles: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for batch in batched(titles, 50):
        for chunk in mw_query(api_url(wiki), {"titles": "|".join(batch)}):
            for p in chunk.get("pages", []):
                if "pageid" in p:
                    out[p["title"]] = p["pageid"]
    return out


def build_frame(wp1_path: str, *, resolve_page_ids: bool = True) -> pd.DataFrame:
    cfg = load_config()
    wikis = cfg["languages"]["wikis"]
    core = set(cfg["frame"]["core_importance"])

    wp1 = frame_titles(load_wp1(wp1_path))
    qids = wdqs_titles_to_qids("en", wp1["title"].tolist())
    missing = [t for t in wp1["title"] if t not in qids]
    qids.update(api_titles_to_qids("en", missing))
    wp1["qid"] = wp1["title"].map(qids)
    print(
        f"WP1 titles: {len(wp1)}; matched by WDQS: {len(wp1) - len(missing)}; "
        f"via redirects: {wp1['qid'].notna().sum() - (len(wp1) - len(missing))}; "
        f"without a Wikidata item: {wp1['qid'].isna().sum()}",
        file=sys.stderr,
    )
    wp1 = wp1.dropna(subset=["qid"]).drop_duplicates("qid")

    frame = sitelinks(sorted(wp1["qid"]), wikis)
    frame["page_id"] = pd.NA
    if resolve_page_ids:
        for wiki, grp in frame.groupby("wiki"):
            ids = title_page_ids(wiki, grp["title"].tolist())
            frame.loc[grp.index, "page_id"] = grp["title"].map(ids)

    frame = frame.merge(
        wp1[["qid", "title", "quality", "importance"]].rename(
            columns={
                "title": "wp1_title",
                "quality": "wp1_quality",
                "importance": "wp1_importance",
            }
        ),
        on="qid",
        how="left",
    )
    frame["core_importance"] = frame["wp1_importance"].isin(core)
    frame["page_id"] = frame["page_id"].astype("Int64")
    print(
        f"Frame: {frame['qid'].nunique()} items, {len(frame)} articles; "
        f"core-importance: {frame.loc[frame['core_importance'], 'qid'].nunique()} items, "
        f"{int(frame['core_importance'].sum())} articles",
        file=sys.stderr,
    )
    return frame.sort_values(["qid", "wiki"]).reset_index(drop=True)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    ap.add_argument("wp1")
    ap.add_argument("out")
    ap.add_argument(
        "--skip-page-ids",
        action="store_true",
        help="leave page_id empty (no Action API lookups); join to dumps by title instead",
    )
    args = ap.parse_args()
    build_frame(args.wp1, resolve_page_ids=not args.skip_page_ids).to_parquet(args.out, index=False)


if __name__ == "__main__":
    main()
