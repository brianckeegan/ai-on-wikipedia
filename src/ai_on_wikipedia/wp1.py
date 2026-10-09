"""Parse the WikiProject Artificial Intelligence (WP1) assessment snapshot: the sampling frame.

Source: https://api.wp1.openzim.org/v1/projects/Artificial_Intelligence/articles?format=tsv
"""

from __future__ import annotations

import pandas as pd

# Non-article namespaces that appear in the WP1 export (drafts, categories, templates, files...).
NON_ARTICLE_PREFIXES = (
    "Draft:",
    "Category:",
    "Template:",
    "File:",
    "Portal:",
    "Wikipedia:",
    "Module:",
    "Book:",
    "User:",
    "Help:",
)


def load_wp1(path: str) -> pd.DataFrame:
    """All rows of the snapshot with a namespace flag; never drops rows silently."""
    df = pd.read_csv(path, sep="\t", dtype=str, keep_default_na=False)
    df["is_article_ns"] = ~df["article"].str.startswith(NON_ARTICLE_PREFIXES)
    df["quality"] = df["quality"].str.removesuffix("-Class")
    df["importance"] = df["importance"].str.removesuffix("-Class")
    return df


def frame_titles(df: pd.DataFrame) -> pd.DataFrame:
    """Main-namespace rows: the frame (redirects among NA-class rows resolve later)."""
    return df.loc[df["is_article_ns"], ["article", "quality", "importance"]].rename(
        columns={"article": "title"}
    )
