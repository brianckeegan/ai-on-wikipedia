# AGENTS.md — guidance for agents and humans working in this repo

Read this first. It states the non-negotiables and points you at the right place for each task. This repo was scaffolded with the CUPIDS Lab `data-project` skill at level **L2 (Reproduce)**.

## Non-negotiables

- **Raw data is immutable.** Never edit anything under `data/raw/` in place. Read it, write derived data to `data/interim/` or `data/processed/`. Anything derived must be reproducible from raw. **Bulk or re-downloadable** raw (category crawls, `mediawiki_history` dumps, pageview pulls) stays git-ignored; the small **curated source-of-record** `data/raw/wp1_artificial_intelligence_2026-10-09.tsv` (the WikiProject AI article list as of that date) is tracked via a `.gitignore` carve-out and documented in `DATA-DICTIONARY.md` as immutable. A newer snapshot is a *new dated file*, never an overwrite.
- **Open, version-controllable formats.** Prefer plain text, CSV/Parquet, Markdown, and text-based pipeline definitions. Do not introduce a vendor-locked artifact as a required dependency; anything a hosted tool produces must be exportable.
- **Provenance lives with the data.** Record where data came from, its license, and any transformations in `DATA-DICTIONARY.md` and `decision-log.md`.
- **Secrets and sensitive data never land in the repo.** Keep credentials out of code and notebooks. Editor usernames and IP addresses are personal data even though Wikipedia publishes them: hash them with the salt in `.env` (`EDITOR_ID_SALT`) at ingest, never write raw identifiers to `data/interim/` or `data/processed/`, and release only aggregates.
- **Describe, don't infer causes.** The target venue (JQD:DM) does not publish causal claims. November 2022 is a period boundary, not a treatment. Avoid "effect of", "impact of", "caused", "led to" in code comments, figure titles, and manuscript text.
- **Be polite to Wikimedia infrastructure.** Every request sends the `user_agent` from `config.yaml`, uses `src/ai_on_wikipedia/client.py` (which backs off on 429/5xx), and prefers dumps over API calls for bulk data.

## Where things are

- Source data and derived outputs: `data/`. Schema (and project terms): `DATA-DICTIONARY.md`.
- Pipeline: `Snakefile` + `config.yaml` at the repo root; stage code in `src/ai_on_wikipedia/`.
- Exploration: `exploratory/` (notebooks stay here; package reusable code into `src/`).
- Research design and LOI: `docs/design-memo.md`, `docs/loi-draft.md`. Manuscript: `manuscript/`.
- What's planned but not built yet: `ROADMAP.md`; the handoff memo is `NEXT-STEPS.md`.

## How we work

Explore in `exploratory/`, then package code into `src/` at the exploration boundary. Pipelines are code (re-runnable), not cleaned snapshots. Pin environments so others — and other agents — can reproduce results. Notebooks are kept **output-free** in version control: run `nbstripout --install` once per clone to activate the git filter that `.gitattributes` declares (the `nbstripout` pre-commit hook is a backstop). Clones that skip this still work — they just won't auto-strip outputs. Before pushing, run `ruff check .`, `pytest`, and `snakemake -n`.
