# Frame counts for the LOI (2026-10-09)

**Status:** the broad category-union frame these scripts also measured was dropped on 2026-10-09 (`decision-log.md`). Only the WikiProject frame (`narrow_fix.py`) is used. The depth-1 crawl survives as the source of the scope-condition figure (17% of topics in other editions' AI categories have no English article).

These scripts produced the frame sizes quoted in `docs/loi-draft.md` and `decision-log.md`. The sandbox's IP was rate-limited (HTTP 429) by the MediaWiki Action API, so they use services that query Wikipedia server-side: the Wikidata Query Service (title → item, item → sitelinks) and PetScan (category trees with Wikidata items). Run from the repo root with an output directory as the only argument, e.g. `python exploratory/frame_counts_2026-10-09/narrow_fix.py /tmp/out`.

- `frame_counts.py` resolves the seed category's sitelinks (Q558331 links to all 20 editions), makes a first narrow mapping by article IRI (an undercount, superseded), and runs the depth-2 PetScan crawl.
- `narrow_fix.py` gives the final narrow mapping: exact title match through WDQS `schema:name`, then redirect and normalization resolution through the Action API for the remainder, then sitelinks.
- `depth_sweep.py` runs PetScan at depths 0 and 1.

Results (2026-10-09): narrow 1,246 pages → 1,219 mapped (27 without a Wikidata item) → 1,212 distinct items → 5,914 articles across the 20 editions. Broad at depth 0 / 1 / 2: 1,922 / 6,610 / 16,859 distinct items, containing 31.8% / 58.5% / 73.7% of the narrow items. At depth 1 there are 42,961 articles; 17.4% of items have no English article, and 65.0% appear in only one edition's tree.

These are exploratory. Fold the WDQS and PetScan backends into `src/ai_on_wikipedia/` (see `ROADMAP.md`) so that the pipeline itself reproduces these numbers.
