"""Daily user-agent pageviews for every frame article in one wiki, plus the wiki-wide total.

Per-article views are queried by *current* title, so views recorded under earlier titles
(before a page move) are missed; see DATA-DICTIONARY.md known issues.

Usage: python -m ai_on_wikipedia.pageviews <wiki> <frame.parquet> <out.parquet>
"""

from __future__ import annotations

import sys
from urllib.parse import quote

import pandas as pd

from .client import get_json
from .settings import load_config, project_domain

REST = "https://wikimedia.org/api/rest_v1/metrics/pageviews"


def _stamp(day: str) -> str:
    return day.replace("-", "") + "00"


def article_views(wiki: str, title: str, start: str, end: str, cfg: dict) -> list[dict]:
    article = quote(title.replace(" ", "_"), safe="")
    url = (
        f"{REST}/per-article/{project_domain(wiki)}/{cfg['access']}/{cfg['agent']}/"
        f"{article}/{cfg['granularity']}/{_stamp(start)}/{_stamp(end)}"
    )
    items = get_json(url, min_interval=1 / cfg["max_requests_per_second"]).get("items", [])
    return [{"timestamp": i["timestamp"], "views": i["views"]} for i in items]


def wiki_total_views(wiki: str, start: str, end: str, cfg: dict) -> list[dict]:
    url = (
        f"{REST}/aggregate/{project_domain(wiki)}/{cfg['access']}/{cfg['agent']}/"
        f"{cfg['granularity']}/{_stamp(start)}/{_stamp(end)}"
    )
    return [
        {"timestamp": i["timestamp"], "views": i["views"]} for i in get_json(url).get("items", [])
    ]


def main(wiki: str, frame_path: str, out: str) -> None:
    cfg = load_config()
    pv, win = cfg["pageviews"], cfg["window"]
    frame = pd.read_parquet(frame_path)
    pages = frame.loc[frame["wiki"].eq(wiki), ["qid", "page_id", "title"]].drop_duplicates("qid")
    rows = []
    for page in pages.itertuples(index=False):
        for r in article_views(wiki, page.title, win["start"], win["end"], pv):
            rows.append({"wiki": wiki, "qid": page.qid, "page_id": page.page_id, **r})
    for r in wiki_total_views(wiki, win["start"], win["end"], pv):
        rows.append({"wiki": wiki, "qid": "__WIKI_TOTAL__", "page_id": pd.NA, **r})
    df = pd.DataFrame(rows, columns=["wiki", "qid", "page_id", "timestamp", "views"])
    df["date"] = pd.to_datetime(df["timestamp"].str[:8], format="%Y%m%d")
    df.drop(columns="timestamp").to_parquet(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
