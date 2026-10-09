"""Assemble the article-month panel (aggregate only; no editor identifiers leave this stage).

STUB — to implement once revisions.py exists. Output grain: one row per (qid, wiki, month)
from the later of window start or article creation through window end. Columns are specified
in DATA-DICTIONARY.md (dataset `article_month`). Months with no activity are explicit zeros,
not missing rows.

Usage: python -m ai_on_wikipedia.panel <frame.parquet> <out.parquet>
       --revisions <revisions/*.parquet...> --pageviews <pageviews/*.parquet...>
"""

from __future__ import annotations

import argparse


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("frame")
    ap.add_argument("out")
    ap.add_argument("--revisions", nargs="+", required=True)
    ap.add_argument("--pageviews", nargs="+", required=True)
    ap.parse_args()
    raise NotImplementedError("panel stage is a stub; see the module docstring and ROADMAP.md")


if __name__ == "__main__":
    main()
