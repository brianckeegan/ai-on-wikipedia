# ROADMAP — this level's work and what's deferred

This project was scaffolded at level **L2 (Reproduce)** and is deliberately right-sized. This file records the work the current level created (assignable, below) and the concerns deferred to later levels, so nothing important is lost and the next maintainer or agent knows what to do now and what to add later. Building less now and documenting the rest here is the intended workflow, not a shortcut.

Key dates (JQD:DM Special Workflow Issue): LOI due **2026-10-25**, LOI decisions 2026-11-01, LLM-approved manuscript due **2027-01-15**, revisions due 2027-03-08.

## This level's work (assignable)

The tasks the current level created. Each row is a checkbox you can assign and track. Check it when its definition of done is met.

| ✓ | Task | Owner | Priority | Size | Definition of done | Blocking? | Level | Links |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [ ] | Draft and submit the LOI | PI | high | S | The four questions are answered in order in `docs/loi-draft.md`, the frame sizes from the next two tasks are filled in, and the LOI is submitted at journalqd.org by 2026-10-25 | yes — deadline | L2 | `docs/loi-draft.md` |
| [x] | Verify the top-20 language ranking | PI | high | S | `snakemake results/tables/language_ranking.csv` returns values for all candidates (including ru and ro), `config.yaml` `languages.wikis` matches the ranking, and the ranks 19–22 near-tie is recorded in `decision-log.md` | no | L2 | `config.yaml`, `decision-log.md` |
| [x] | Pin the seed category and crawl the broad bound | Data engineer | high | M | `frame.seed_category_qid` is set and verified, root categories resolve for all 20 wikis (add overrides for any without a sitelink), `data/raw/categories/*.jsonl` exist, and per-wiki counts are recorded in `DATA-DICTIONARY.md` | no | L2 | `src/ai_on_wikipedia/categories.py` |
| [ ] | Port the frame stages to WDQS + PetScan | Data engineer | high | M | `categories.py` uses PetScan and `frame.py` maps titles by exact `schema:name` through WDQS (Action API only for redirects); the pipeline reproduces the 2026-10-09 counts in `exploratory/frame_counts_2026-10-09/README.md` | no | L2 | `src/ai_on_wikipedia/frame.py` |
| [x] | Build the frame and report bound sizes | Data engineer | high | M | `data/processed/frame.parquet` exists, and the counts of distinct QIDs (narrow, broad, both) and of unmapped WP1 titles are recorded in `DATA-DICTIONARY.md` and the LOI | no | L2 | `src/ai_on_wikipedia/frame.py` |
| [ ] | Hand-code the relevance audit | PI | high | M | Every row of `results/tables/relevance_audit_sample.csv` is coded, saved as a separate coded file, and precision per stratum is reported with 95% intervals | no | L2 | `src/ai_on_wikipedia/audit.py` |
| [ ] | Pseudonymize editor identifiers at ingest | Data engineer | high | S | `revisions.py` writes only `editor_key` (never usernames or IPs), `.env` holds `EDITOR_ID_SALT`, and a test asserts no raw-identifier column exists in interim outputs | **yes** — before any revision data is written | L2 | `src/ai_on_wikipedia/privacy.py` |
| [ ] | Implement the revisions stage | Data engineer | high | L | Column list pinned from the dump README, `data/interim/revisions/<wiki>.parquet` for all 20 wikis, and row counts reconciled for 3 sample articles against the page histories | no | L2 | `src/ai_on_wikipedia/revisions.py` |
| [ ] | Collect pageviews and verify them | Data engineer | high | M | `data/interim/pageviews/<wiki>.parquet` for all wikis, and 5 spot-checked articles match pageviews.wmcloud.org | no | L2 | `src/ai_on_wikipedia/pageviews.py` |
| [ ] | Implement the panel and describe stages | Data engineer | high | L | `article_month.parquet` matches the schema in `DATA-DICTIONARY.md`, and `summary_by_wiki_period.csv` reports bootstrap intervals | no | L2 | `src/ai_on_wikipedia/panel.py`, `describe.py` |
| [x] | Get CI green | Data engineer | med | S | The token guard, ruff, pytest, and `snakemake -n` pass on the PR | no | L2 | `.github/workflows/ci.yml` |
| [ ] | Fill the data dictionary after the first full run | PI | med | S | Every `<N …>` placeholder in `DATA-DICTIONARY.md` is replaced with observed counts | no | L2 | `DATA-DICTIONARY.md` |

**Tracking:** this checklist is the source of truth for the current level's work.

## Deferred items

Concerns that are real but above the current level. They are added when you climb.

| Concern | Why deferred | Adds it (template / level) | Blocking? |
| --- | --- | --- | --- |
| Governance for editor-level data (access tiers, salt custody and retention, remedy process) | Only aggregates are released now. Becomes sensitive-human **when** editor-level revision tables or coauthorship networks are shared or deposited | `GOVERNANCE.md` + `data-management-plan.md` (L3/L4) | **yes** — conditional: before releasing any editor-level or network data |
| Matched non-AI baseline sample | PI decision (2026-10-09). Wiki-wide denominators are used instead | New `baseline` rule (L2 extension) | no |
| Responsible-data, bulletproofing, and data-quality checklists; data card | Single-PI project with public inputs. Needed before public data release | `docs/checklists/*`, `docs/data-card.md` (L4) | no |
| Collaboration files (CONTRIBUTING, CODE_OF_CONDUCT, CODEOWNERS, CHARTER) and GitHub issues/Project from this checklist | No coauthors yet. Add when collaborators join | L3 + `data-project track` | no |
| Replication deposit (processed aggregates, code, docs) with DOI | Needed at acceptance, not now | `dataverse/` kit (L5) | no |
| FAIR self-assessment | Do it before the deposit | `docs/FAIR-CHECKLIST.md` (L4) | no |
| Page-move and redirect aggregation for pageviews | Pre-period views for renamed articles are undercounted | `pageviews.py` extension (L2) | no |
| Time-varying narrow frame (when each WikiProject banner was added) | Requires talk-page histories. The current frame is a 2026 snapshot | `frame.py` extension (L2) | no |
| Clickstream referrers (search vs. internal vs. external) | Available only for a subset of wikis. Scope creep for this manuscript | New stage (L2) | no |
| Content Translation and AI-cleanup-template measures | Optional measures of cross-language diffusion and LLM-text maintenance | `revisions.py` tag fields (L2) | no |
| AI drafts in Draft: namespace (463 in WP1) | Drafts are not articles, but they describe production pressure | New stage (L2) | no |

## How to climb a level

Re-run the `data-project` skill in this directory and ask to climb to the next level (e.g. "take this to L3"). The skill adds only the new level's artifacts, refreshes this roadmap, and (if the project is on GitHub) files the new level's tasks as issues. Items marked **blocking** must be resolved, or explicitly acknowledged, before the project does the thing they guard and before climbing. Some blocking items are **conditional**: they come due only when a named event occurs (here, *before editor-level or network data leaves the controlled tier*). Treat the trigger as the gate.
