# Decision log — AI on Wikipedia

A running, dated record of design and data decisions and *why* they were made — the provenance of the project's choices, legible to people who join later. Add an entry whenever you make a non-obvious choice (a filtering rule, a definition, a tool, a tradeoff). Newest first.

## 2026-10-09 — Single frame: WikiProject AI articles mapped across languages; no non-AI baseline

- **Context:** After seeing the frame counts, the PI chose to drop the two-frame (bracketed) design.
- **Decision:** The frame is the English WikiProject Artificial Intelligence article set (WP1 snapshot 2026-10-09), mapped through Wikidata to the corresponding articles in the 20 analysis editions: 1,212 items, 5,914 articles. The broad category-union frame is dropped, and `categories.py` and its pipeline rule are removed. No matched non-AI baseline will be built.
- **Why:** A fixed topic set measured identically in every edition makes the multilingual comparison the comparative device. Differences between editions cannot be artifacts of different topic definitions, and the editions serve as comparison cases for one another in place of a non-AI baseline. Edition-wide denominators still separate AI activity from each edition's overall trend.
- **Consequences:** English-defined scope is stated as a limitation: an exploratory crawl found 17% of topics in other editions' AI categories (depth 1) have no English article. The relevance audit becomes a simple random sample of 200 items. A core-importance robustness subset (Top/High/Mid: 184 items, 2,142 articles) replaces the bracket as the frame-sensitivity check. The entries below on the bracketed frame and category depth are superseded and kept for provenance.

## 2026-10-09 — (Superseded) Broad frame limited to category depth 1; frame sizes for the LOI

- **Context:** A depth sweep of each edition's AI category tree (PetScan, all 20 roots resolved from Q558331) gave 1,922 / 6,610 / 16,859 distinct Wikidata items at depth 0 / 1 / 2, containing 31.8% / 58.5% / 73.7% of the narrow frame's items. Random draws at depth 2 were visibly off-topic (Sieve of Eratosthenes and a low-pass filter in ar, a video-game character in ko, a video-game series in en). At depth 1, most draws were on-topic, with some noise (Tower of Hanoi, Chinese Library Classification, focus group).
- **Decision:** Set `frame.category_depth` to 1. Keep depth 2 only as an outer sensitivity bound if reviewers ask.
- **Why:** Depth 2 nearly triples the frame and mostly adds drift. Depth 1 still adds coverage the narrow frame lacks (17.4% of its items have no English article).
- **Consequences:** LOI frame sizes. Narrow: 1,246 pages → 1,212 distinct items (27 pages unmapped) → 5,914 articles across 20 editions, from en 1,209 down to sv 115. Broad at depth 1: 6,610 items → 42,961 articles; 65.0% of items are anchored by one edition only. The relevance audit must still quantify the precision of depth 1. These numbers came from exploratory WDQS/PetScan scripts (`exploratory/frame_counts_2026-10-09/`) because the Action API rate-limited the sandbox, so the pipeline must be ported to those backends to reproduce them.

## 2026-10-09 — (Superseded) Bracketed sampling frame: WikiProject AI (narrow) and multi-language category union (broad)

- **Context:** JQD:DM reviewers "pay special attention to sampling." A single English category tree is both noisy (it drifts off-topic with depth) and English-anchored (it misses AI articles that exist only in other languages).
- **Decision:** Report every measure for two bounds. **Narrow:** the main-namespace articles in the WikiProject Artificial Intelligence WP1 snapshot (1,246 main-namespace rows of 1,882 total on 2026-10-09), mapped to Wikidata and their sitelinks. **Broad:** the union of each analysis wiki's local AI category tree (root from the Wikidata item for Category:Artificial intelligence, Q558331, which links to all 20 editions; depth 1 — see the depth entry above), mapped to Wikidata. Record which wikis anchor each item, and hand-code a stratified relevance sample (narrow-only, broad-only, both).
- **Why:** The narrow bound is high-precision and editor-curated but English-anchored. The broad bound has higher recall across languages but is noisier. Findings that hold across both bounds are robust to frame choice. Where they diverge, the divergence is itself descriptive evidence about how language communities organize AI knowledge. The share of each wiki's AI articles that are English-anchored versus native is a finding.
- **Consequences:** Set `frame.seed_category_qid` before running and verify it. The relevance audit must be coded before the frames are reported. The WP1 snapshot is frozen, and refreshes are new dated files.

## 2026-10-09 — Language editions: top 20 by user pageviews in October 2022

- **Context:** Ranking "largest" wikis by article count includes bot-generated editions (Cebuano, Waray, Egyptian Arabic). The PI chose readership as the criterion.
- **Decision:** Rank candidate wikis by `agent=user` pageviews in the last full pre-period month (2022-10) and pin the top 20 in `config.yaml`.
- **Why:** This measures each edition's audience at the boundary, before the post-period could change it.
- **Consequences:** The preliminary ranking (REST `aggregate` endpoint, retrieved 2026-10-09; several calls were rate-limited) is: en 7.49B, ja 985M, es 952M, fr 880M, de 828M, it 471M, zh 408M, pt 266M, ar 247M, fa 240M, pl 222M, tr 138M, nl 122M, id 118M, uk 110M, sv 76.5M, cs 72.9M, vi 68.9M, **ko 63.6M, he 62.6M, hi 61.4M**, fi 54.8M, hu 53.7M. Retries confirmed **ru 945M (rank 4)** and **ro 40.8M** (below the cutoff), so the pinned list stands. Ranks 19–22 (vi, ko, he, hi) lie within 12% of each other, so the 20th slot is fragile. Report this, and consider a robustness check that swaps ko for he and hi.

## 2026-10-09 — No matched non-AI baseline sample

- **Context:** Wikipedia-wide pageviews and editing are declining, and traffic classification changed during the window, so raw AI-article trends mix topic-specific change with platform-wide change.
- **Decision:** No matched non-AI article sample (PI decision; cost and time before the 2027-01-15 manuscript deadline). Instead, normalize attention by wiki-wide user pageviews (`view_share`) and compare AI-article editing to edition-level totals from the same dumps.
- **Why:** A wiki-wide denominator costs one extra API call per wiki and separates the AI share from platform trends at the edition level.
- **Consequences:** Article-level comparisons to "similar" non-AI articles cannot be made. The PI confirmed on 2026-10-09 that the multilingual comparison serves this role (see the single-frame entry above), so the baseline is not planned.

## 2026-10-09 — Observation window and period boundary

- **Context:** The JQD:DM mandate excludes causal claims.
- **Decision:** Window 2020-11-01 to 2026-09-30. Pre-period: Nov 2020–Oct 2022 (24 months). Post-period: Nov 2022–Sep 2026 (47 months). November 2022 is a descriptive marker (ChatGPT's public release on 2022-11-30 falls in the first post month).
- **Why:** A symmetric-enough pre-period describes trajectories, not just levels, without implying an intervention.
- **Consequences:** Text, figures, and code use "before/after" and "changed", never "effect" or "impact".

## 2026-10-09 — Editor identifiers are pseudonymized at ingest

- **Context:** Coauthorship measures need editor identity, but usernames and IPs are personal data even though Wikipedia publishes them.
- **Decision:** Hash identifiers with HMAC-SHA256 under a secret salt (`EDITOR_ID_SALT` in `.env`) before writing `data/interim/`. Release only aggregate tables.
- **Why:** The analysis needs only "same editor or not." Pseudonymizing at ingest keeps identifiers out of every downstream artifact.
- **Consequences:** Releasing editor-level or network data is a blocking `ROADMAP.md` item that needs governance first.

## 2026-10-09 — Project scaffolded

- **Context:** Project started with the CUPIDS Lab `data-project` skill at level L2 for a JQD:DM Special Workflow Issue submission (LOI due 2026-10-25).
- **Decision:** Adopt the standard layout, the immutable-raw-data convention, a Python/Snakemake pipeline, and the deferred-work roadmap.
- **Why:** The manuscript must pass an automated check of methods, uncertainty, and internal consistency, and a re-runnable pipeline makes every reported number traceable.
- **Consequences:** See `ROADMAP.md` for deferred concerns.
