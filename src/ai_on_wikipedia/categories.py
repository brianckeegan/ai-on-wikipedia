"""Crawl one wiki's local AI category tree to a fixed depth: the broad frame bound.

Usage: python -m ai_on_wikipedia.categories <wiki> data/raw/categories/<wiki>.jsonl
"""

from __future__ import annotations

import json
import sys
from collections import deque

from .client import get_json, mw_query
from .settings import api_url, load_config

WIKIDATA_API = "https://www.wikidata.org/w/api.php"


def root_category(wiki: str) -> str | None:
    """Local title of the AI root category, from overrides or the seed item's sitelinks."""
    fcfg = load_config()["frame"]
    if wiki in (fcfg.get("root_category_overrides") or {}):
        return fcfg["root_category_overrides"][wiki]
    qid = fcfg.get("seed_category_qid")
    if not qid:
        raise SystemExit("Set frame.seed_category_qid in config.yaml (verify the Wikidata item).")
    data = get_json(
        WIKIDATA_API,
        {"action": "wbgetentities", "ids": qid, "props": "sitelinks", "format": "json"},
    )
    link = data.get("entities", {}).get(qid, {}).get("sitelinks", {}).get(f"{wiki}wiki")
    return link["title"] if link else None


def crawl(wiki: str, root: str, depth: int) -> list[dict]:
    """Breadth-first walk; records each article (ns 0) with the depth and category it came via."""
    api = api_url(wiki)
    seen_cats, seen_pages, rows = {root}, set(), []
    queue = deque([(root, 0)])
    while queue:
        cat, d = queue.popleft()
        for chunk in mw_query(
            api,
            {
                "list": "categorymembers",
                "cmtitle": cat,
                "cmlimit": "max",
                "cmtype": "page|subcat",
                "cmnamespace": "0|14",
                "cmprop": "ids|title|type",
            },
        ):
            for m in chunk.get("categorymembers", []):
                if m["type"] == "subcat" and d < depth and m["title"] not in seen_cats:
                    seen_cats.add(m["title"])
                    queue.append((m["title"], d + 1))
                elif m["type"] == "page" and m["pageid"] not in seen_pages:
                    seen_pages.add(m["pageid"])
                    rows.append(
                        {
                            "wiki": wiki,
                            "page_id": m["pageid"],
                            "title": m["title"],
                            "depth": d,
                            "via_category": cat,
                        }
                    )
    return rows


def main(wiki: str, out: str) -> None:
    root = root_category(wiki)
    rows = [] if root is None else crawl(wiki, root, load_config()["frame"]["category_depth"])
    with open(out, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"{wiki}: root={root!r} articles={len(rows)}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
