"""Build the sampling frame and map it across languages through Wikidata.

The frame is the set of main-namespace articles assessed by English WikiProject Artificial
Intelligence (WP1 snapshot). Each article is resolved to its Wikidata item, and every item is
located in all analysis wikis through its sitelinks, so every edition is measured on the same
set of topics.

Usage: python -m ai_on_wikipedia.frame <wp1.tsv> <frame.parquet>
"""

from __future__ import annotations

import sys

import pandas as pd

from .client import batched, get_json, mw_query
from .settings import api_url, load_config
from .wp1 import frame_titles, load_wp1

WIKIDATA_API = "https://www.wikidata.org/w/api.php"


def titles_to_qids(wiki: str, titles: list[str]) -> dict[str, str]:
    """Title -> Wikidata QID, following redirects (a moved WP1 title maps to its target)."""
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


def sitelinks(qids: list[str], wikis: list[str]) -> pd.DataFrame:
    """One row per (qid, wiki) where the item has an article in that wiki."""
    rows = []
    sites = {f"{w}wiki": w for w in wikis}
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
        for qid, ent in data.get("entities", {}).items():
            for site, link in ent.get("sitelinks", {}).items():
                if site in sites:
                    rows.append({"qid": qid, "wiki": sites[site], "title": link["title"]})
    return pd.DataFrame(rows, columns=["qid", "wiki", "title"])


def title_page_ids(wiki: str, titles: list[str]) -> dict[str, int]:
    out: dict[str, int] = {}
    for batch in batched(titles, 50):
        for chunk in mw_query(api_url(wiki), {"titles": "|".join(batch)}):
            for p in chunk.get("pages", []):
                if "pageid" in p:
                    out[p["title"]] = p["pageid"]
    return out


def main(wp1_path: str, out: str) -> None:
    cfg = load_config()
    wikis = cfg["languages"]["wikis"]
    core = set(cfg["frame"]["core_importance"])

    wp1 = frame_titles(load_wp1(wp1_path))
    wp1["qid"] = wp1["title"].map(titles_to_qids("en", wp1["title"].tolist()))
    unmapped = wp1["qid"].isna().sum()
    wp1 = wp1.dropna(subset=["qid"]).drop_duplicates("qid")
    print(f"WP1 titles without a Wikidata item: {unmapped}", file=sys.stderr)

    frame = sitelinks(sorted(wp1["qid"]), wikis)
    frame["page_id"] = pd.NA
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
    frame.to_parquet(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
