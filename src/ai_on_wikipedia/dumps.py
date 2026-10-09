"""Download one wiki's mediawiki_history dump files (bulk, git-ignored).

Dumps: https://dumps.wikimedia.org/other/mediawiki_history/<snapshot>/<wiki>wiki/
Large wikis are split by time range; every *.tsv.bz2 file for the wiki is fetched.

Usage: python -m ai_on_wikipedia.dumps <wiki> data/raw/mediawiki_history/<wiki>
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

from .client import session
from .settings import load_config


def main(wiki: str, out_dir: str) -> None:
    cfg = load_config()["mediawiki_history"]
    index = f"{cfg['base_url']}/{cfg['snapshot']}/{wiki}wiki/"
    html = session().get(index, timeout=60)
    html.raise_for_status()
    files = sorted(set(re.findall(r'href="([^"]+\.tsv\.bz2)"', html.text)))
    if not files:
        raise SystemExit(f"No dump files listed at {index}")
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for name in files:
        target = out / name
        if target.exists():
            continue
        with session().get(index + name, stream=True, timeout=600) as resp:
            resp.raise_for_status()
            tmp = target.with_suffix(".part")
            with open(tmp, "wb") as fh:
                for block in resp.iter_content(1 << 20):
                    fh.write(block)
            tmp.rename(target)
        print(f"{wiki}: {name}", file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
