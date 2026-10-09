"""Rank candidate wikis by user pageviews in the reference month.

Usage: python -m ai_on_wikipedia.languages results/tables/language_ranking.csv
"""

from __future__ import annotations

import calendar
import sys

import pandas as pd

from .client import get_json
from .settings import load_config, project_domain

AQS = "https://wikimedia.org/api/rest_v1/metrics/pageviews/aggregate"


def monthly_user_views(wiki: str, month: str, access: str = "all-access") -> int | None:
    year, mon = (int(x) for x in month.split("-"))
    last = calendar.monthrange(year, mon)[1]
    url = (
        f"{AQS}/{project_domain(wiki)}/{access}/user/monthly/"
        f"{year}{mon:02d}0100/{year}{mon:02d}{last}00"
    )
    items = get_json(url, min_interval=1.0).get("items", [])
    return items[0]["views"] if items else None


def main(out: str) -> None:
    cfg = load_config()["languages"]
    rows = [
        {"wiki": w, "user_pageviews": monthly_user_views(w, cfg["rank_month"])}
        for w in cfg["candidates"]
    ]
    df = pd.DataFrame(rows).sort_values("user_pageviews", ascending=False, na_position="last")
    df["rank"] = range(1, len(df) + 1)
    df["in_analysis"] = df["wiki"].isin(cfg["wikis"])
    df["rank_month"] = cfg["rank_month"]
    df.to_csv(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1])
