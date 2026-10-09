# Changelog

All notable changes to AI on Wikipedia are recorded here. Format follows [Keep a Changelog](https://keepachangelog.com/); this project aims to use semantic versioning for data and code releases.

## [Unreleased]

### Added
- Initial project scaffold (level L2) via the CUPIDS Lab `data-project` skill.
- Bracketed sampling-frame design (WikiProject AI narrow bound; multi-language category union broad bound) and the pinned WP1 snapshot `data/raw/wp1_artificial_intelligence_2026-10-09.tsv`.
- Snakemake pipeline with working stages for language ranking, category crawl, frame construction, relevance-audit sampling, dump download, and pageviews; stubs for revisions, panel, and describe.
- Research design memo, LOI draft, and the JQD:DM LaTeX manuscript template.

### Changed

### Deprecated

### Removed

### Fixed

### Security
- Editor identifiers are pseudonymized with a keyed hash at ingest (`src/ai_on_wikipedia/privacy.py`).
