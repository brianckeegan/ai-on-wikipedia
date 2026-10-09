"""Draw a simple random sample of frame items for hand-coding topical relevance.

Coders fill `relevant` (1/0) and `notes`; the coded file is saved as a new file (never
overwrite the sample) and reported as the frame's precision with a 95% interval.

Usage: python -m ai_on_wikipedia.audit <frame.parquet> <relevance_audit_sample.csv>
"""

from __future__ import annotations

import sys

import pandas as pd

from .settings import load_config


def main(frame_path: str, out: str) -> None:
    cfg = load_config()
    frame = pd.read_parquet(frame_path)
    items = frame.drop_duplicates("qid")[
        ["qid", "wp1_title", "wp1_quality", "wp1_importance", "core_importance"]
    ]
    n = min(cfg["frame"]["audit_sample_size"], len(items))
    sample = items.sample(n, random_state=cfg["seed"]).sort_values("qid")
    sample["relevant"] = ""
    sample["notes"] = ""
    sample.to_csv(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
