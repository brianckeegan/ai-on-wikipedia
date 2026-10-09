"""Build the bracketed sampling frame and map it across languages through Wikidata.

narrow: main-namespace articles assessed by English WikiProject Artificial Intelligence (WP1).
broad:  union of every analysis wiki's local AI category tree (depth-capped).
Every Wikidata item in either bound is then located in all analysis wikis via its sitelinks.

Usage: python -m ai_on_wikipedia.frame <wp1.tsv> <frame.parquet> <categories/*.jsonl...>
"""

from __future__ import annotations

import sys

import pandas as pd

from .client import batched, get_json, mw_query
from .settings import api_url, load_config
from .wp1 import load_wp1, narrow_titles

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


def pageids_to_qids(wiki: str, page_ids: list[int]) -> dict[int, str]:
    out: dict[int, str] = {}
    for batch in batched(page_ids, 50):
        for chunk in mw_query(
            api_url(wiki),
            {"prop": "pageprops", "ppprop": "wikibase_item", "pageids": "|".join(map(str, batch))},
        ):
            for p in chunk.get("pages", []):
                qid = p.get("pageprops", {}).get("wikibase_item")
                if qid:
                    out[p["pageid"]] = qid
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


def main(wp1_path: str, out: str, *category_files: str) -> None:
    wikis = load_config()["languages"]["wikis"]

    narrow = narrow_titles(load_wp1(wp1_path))
    narrow["qid"] = narrow["title"].map(titles_to_qids("en", narrow["title"].tolist()))
    narrow = narrow.dropna(subset=["qid"]).drop_duplicates("qid")

    broad_parts = []
    for path in category_files:
        cats = pd.read_json(path, lines=True)
        if cats.empty:
            continue
        wiki = cats["wiki"].iloc[0]
        cats["qid"] = cats["page_id"].map(pageids_to_qids(wiki, cats["page_id"].tolist()))
        broad_parts.append(cats.dropna(subset=["qid"])[["qid", "wiki", "depth"]])
    empty = pd.DataFrame(columns=["qid", "wiki", "depth"])
    broad = pd.concat(broad_parts) if broad_parts else empty
    anchors = (
        broad.groupby("qid")
        .agg(
            broad_anchor_wikis=("wiki", lambda s: ",".join(sorted(set(s)))),
            broad_min_depth=("depth", "min"),
        )
        .reset_index()
    )

    qids = sorted(set(narrow["qid"]) | set(anchors["qid"]))
    frame = sitelinks(qids, wikis)
    frame["page_id"] = pd.NA
    for wiki, grp in frame.groupby("wiki"):
        ids = title_page_ids(wiki, grp["title"].tolist())
        frame.loc[grp.index, "page_id"] = grp["title"].map(ids)

    frame = frame.merge(
        narrow[["qid", "quality", "importance"]].rename(
            columns={"quality": "wp1_quality", "importance": "wp1_importance"}
        ),
        on="qid",
        how="left",
    )
    frame = frame.merge(anchors, on="qid", how="left")
    frame["in_narrow"] = frame["qid"].isin(set(narrow["qid"]))
    frame["in_broad"] = frame["qid"].isin(set(anchors["qid"]))
    frame["page_id"] = frame["page_id"].astype("Int64")
    frame.to_parquet(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], *sys.argv[3:])
