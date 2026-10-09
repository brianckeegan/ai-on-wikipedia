"""Filter one wiki's mediawiki_history dump to frame pages and pseudonymize editors.

STUB — to implement:
  1. Pin the dump's column list from the README shipped with the snapshot
     (https://dumps.wikimedia.org/other/mediawiki_history/) — do not guess column order.
  2. Stream each *.tsv.bz2, keep event_entity == "revision" rows whose page_id is in the
     frame for this wiki, within config window (plus page creation events for all time).
  3. Keep: page_id, revision_id, event_timestamp, editor (-> privacy.editor_key), editor type
     (registered / anonymous / temporary account / bot via user groups and is_bot_by),
     revision_text_bytes, revision_text_bytes_diff, revision_is_identity_reverted,
     revision_is_identity_revert, revision_tags (for Content Translation), page creation timestamp.
  4. Never write the raw username or IP; write data/interim/revisions/<wiki>.parquet.

Usage: python -m ai_on_wikipedia.revisions <wiki> <frame.parquet> <dump_dir> <out.parquet>
"""

from __future__ import annotations

import sys


def main(wiki: str, frame_path: str, dump_dir: str, out: str) -> None:
    raise NotImplementedError("revisions stage is a stub; see the module docstring and ROADMAP.md")


if __name__ == "__main__":
    main(*sys.argv[1:5])
