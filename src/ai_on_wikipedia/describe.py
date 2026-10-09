"""Descriptive summaries for the manuscript: pre vs. post period, by wiki.

STUB — to implement once panel.py exists. For each wiki x period (pre, post), for all frame
items and for the core-importance subset (WikiProject Top/High/Mid): articles existing,
articles created, edits, distinct editors, newcomer share, identity-revert rate, median bytes,
user pageviews, and AI share of wiki-wide pageviews, with bootstrap intervals over articles.
Report uncertainty; describe, do not attribute causes.

Usage: python -m ai_on_wikipedia.describe <article_month.parquet> <summary.csv>
"""

from __future__ import annotations

import sys


def main(panel_path: str, out: str) -> None:
    raise NotImplementedError("describe stage is a stub; see the module docstring and ROADMAP.md")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
