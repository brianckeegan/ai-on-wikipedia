"""Draw a stratified random sample of frame items for hand-coding topical relevance.

Strata: narrow-only, broad-only, both. Coders fill `relevant` (1/0) and `notes`; the coded
file is saved as a new file (never overwrite the sample) and reported as precision per bound.

Usage: python -m ai_on_wikipedia.audit <frame.parquet> <relevance_audit_sample.csv>
"""

from __future__ import annotations

import sys

import pandas as pd

from .settings import load_config


def stratum(row: pd.Series) -> str:
    if row["in_narrow"] and row["in_broad"]:
        return "both"
    return "narrow_only" if row["in_narrow"] else "broad_only"


def main(frame_path: str, out: str) -> None:
    cfg = load_config()
    n = cfg["frame"]["audit_sample_per_bound"]
    frame = pd.read_parquet(frame_path)
    # One row per item; prefer the English title for coding, else any available title.
    items = (
        frame.assign(_en=frame["wiki"].eq("en"))
        .sort_values(["qid", "_en"], ascending=[True, False])
        .drop_duplicates("qid")
        .drop(columns="_en")
    )
    items["stratum"] = items.apply(stratum, axis=1)
    sample = pd.concat(
        g.sample(min(n, len(g)), random_state=cfg["seed"]) for _, g in items.groupby("stratum")
    )
    sample = sample[["stratum", "qid", "wiki", "title", "wp1_quality", "broad_anchor_wikis"]]
    sample["relevant"] = ""
    sample["notes"] = ""
    sample.to_csv(out, index=False)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
