# Changelog

All notable changes to AI on Wikipedia are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/); this project aims to use semantic versioning for data and code releases.

## [Unreleased]

### Added
- Initial project scaffold (level L2) via the CUPIDS Lab `data-project` skill.
- Sampling frame built from the pinned WP1 snapshot `data/raw/wp1_artificial_intelligence_2026-10-09.tsv`.
- Snakemake pipeline with working stages for language ranking, category crawl, frame construction, relevance-audit sampling, dump download, and pageviews; stubs for revisions, panel, and describe.
- Research design memo, LOI draft, and the JQD:DM LaTeX manuscript template.

### Changed
- Frame stage ported to the Wikidata Query Service: exact-title matching and sitelinks in bulk SPARQL queries, with the Action API only for redirects, out-of-graph (scholarly) items, and page IDs (`--skip-page-ids` to omit). The pipeline frame is 1,211 items / 5,928 articles; the LOI and design memo now cite it.
- Sampling frame narrowed to the English WikiProject Artificial Intelligence article set mapped across 20 editions (PI decision, 2026-10-09). The category-union frame, `categories.py`, and its pipeline rule are removed. The relevance audit is now a 200-item simple random sample, with a core-importance robustness subset. No non-AI baseline: the cross-edition comparison on a fixed topic set serves that role.

### Deprecated

### Removed

### Fixed

### Security
- Editor identifiers are pseudonymized with a keyed hash at ingest (`src/ai_on_wikipedia/privacy.py`).
