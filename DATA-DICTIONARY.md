# Data dictionary — AI on Wikipedia

Documentation is half the work: a dataset without this file is a private spreadsheet. Keep this current and co-located with the data. One `Dataset` block per dataset the pipeline holds; one variable per row within each table. Blocks marked *(planned)* describe the target schema of stages that are still stubs — update them when the stage lands.

## Dataset: `wp1_artificial_intelligence_2026-10-09.tsv` (raw, curated source-of-record, tracked)

- **Grain (unit of observation):** one row per page tagged by English WikiProject Artificial Intelligence, across all namespaces.
- **Source / provenance:** WP1 assessment API, `https://api.wp1.openzim.org/v1/projects/Artificial_Intelligence/articles?format=tsv`, retrieved 2026-10-09 by the PI's session; SHA-256 `07a72603ec016e09f9e920613e70565f5543bcc8e3668f304828e0dda30d1688`. Mirrors the talk-page banners of [Wikipedia:WikiProject Artificial Intelligence](https://en.wikipedia.org/wiki/Wikipedia:WikiProject_Artificial_Intelligence).
- **Input license:** Wikipedia metadata, CC BY-SA 4.0.
- **Sensitivity:** public.
- **Update cadence:** live upstream; this file is a **frozen, immutable snapshot**. A refresh is a new dated file plus a decision-log entry, never an overwrite.
- **Row count (as obtained):** 1,882 rows: 1,246 main-namespace, 463 `Draft:`, 136 `Category:`, 26 `Template:`, 11 `File:`. Checked in `tests/test_basics.py`.

| Variable | Type | Units | Allowed values / range | Description | Missingness |
| --- | --- | --- | --- | --- | --- |
| `article` | string | — | page title with namespace prefix | Page tagged by the WikiProject | none observed |
| `article_link` | string | — | URL | Link to the page on en.wikipedia.org | none observed |
| `importance` | category | — | `Top-Class`, `High-Class`, `Mid-Class`, `Low-Class`, `NA-Class`, `Unknown-Class` | WikiProject importance rating | `Unknown-Class` = not yet rated; `NA-Class` = non-article page |
| `importance_updated` | datetime | ISO 8601 UTC | — | When the importance rating was last updated | — |
| `quality` | category | — | `GA`, `B`, `C`, `Start`, `Stub`, `List`, `NA`, `Unassessed` (each with `-Class` suffix) | WikiProject quality rating | `Unassessed-Class` = not rated; `NA-Class` main-namespace rows are mostly redirects |
| `quality_updated` | datetime | ISO 8601 UTC | — | When the quality rating was last updated | — |

## Dataset: `data/processed/frame.parquet`

- **Grain:** one row per (Wikidata item, analysis wiki) where the item has an article in that wiki.
- **Source / provenance:** built by `src/ai_on_wikipedia/frame.py` from the WP1 snapshot, MediaWiki `pageprops` (English title → QID, following redirects), Wikidata `wbgetentities` sitelinks, and MediaWiki title → page ID lookups.
- **Input license:** CC BY-SA 4.0 (Wikipedia) and CC0 (Wikidata). **Sensitivity:** public. **Update cadence:** per run.
- **Row count (as obtained):** expected from the 2026-10-09 exploratory counts: 1,212 items / 5,914 rows (en 1,209 · zh 370 · ko 365 · fr 357 · es 346 · fa 319 · ar 312 · ja 281 · ru 273 · pt 270 · uk 260 · de 259 · id 221 · it 182 · pl 178 · tr 168 · vi 149 · cs 141 · nl 139 · sv 115); 184 core-importance items / 2,142 rows. Re-record from the pipeline's own output.

| Variable | Type | Units | Allowed values / range | Description | Missingness |
| --- | --- | --- | --- | --- | --- |
| `qid` | string | — | `Q[0-9]+` | Wikidata item; the cross-language unit of analysis | none (unmapped titles are dropped and counted) |
| `wiki` | string | — | language code | Edition where the article exists | none |
| `title` | string | — | — | Local title from the sitelink at build time | none |
| `page_id` | Int64 | — | > 0 | Local page ID; joins to revisions | `<NA>` if the title did not resolve |
| `wp1_title` | string | — | — | English title as listed in the WP1 snapshot (before redirect resolution) | none |
| `wp1_quality` | category | — | as in the WP1 snapshot, without `-Class` | English WikiProject quality rating | none |
| `wp1_importance` | category | — | as in the WP1 snapshot, without `-Class` | English WikiProject importance rating | none (`Unknown` = not rated) |
| `core_importance` | bool | — | — | `wp1_importance` is in `frame.core_importance` (Top, High, Mid); the robustness subset | none |

## Dataset: `data/interim/revisions/<wiki>.parquet` *(planned)*

- **Grain:** one row per revision to a frame page in that wiki.
- **Source / provenance:** `mediawiki_history` dump, snapshot `mediawiki_history.snapshot` in `config.yaml`, filtered by `src/ai_on_wikipedia/revisions.py`.
- **Sensitivity:** pseudonymized. Editor identifiers are keyed hashes. Raw usernames and IPs are **never** written here. This dataset is **not for release**.

| Variable | Type | Units | Allowed values / range | Description | Missingness |
| --- | --- | --- | --- | --- | --- |
| `page_id` | int | — | — | Local page ID | none |
| `revision_id` | int | — | — | Revision ID | none |
| `timestamp` | datetime | UTC | window | Revision time | none |
| `editor_key` | string | — | 16 hex chars | HMAC-SHA256 pseudonym of user ID or IP (`privacy.editor_key`) | null for suppressed editors |
| `editor_type` | category | — | `registered`, `anonymous`, `temporary`, `bot` | Editor class at edit time | — |
| `bytes` | int | bytes | ≥ 0 | Page size after the revision | — |
| `bytes_diff` | int | bytes | — | Size change from the parent revision | — |
| `is_reverted` | bool | — | — | Revision was later identity-reverted | — |
| `is_revert` | bool | — | — | Revision restores an earlier identical version | — |
| `is_content_translation` | bool | — | — | Revision tagged `contenttranslation` | — |

## Dataset: `data/interim/pageviews/<wiki>.parquet`

- **Grain:** one row per (frame item, day) for articles in that wiki, plus one `__WIKI_TOTAL__` row per day holding the wiki-wide total.
- **Source / provenance:** Wikimedia REST pageviews API, `per-article` and `aggregate` endpoints, `agent=user`, `access=all-access`, daily, window from `config.yaml`.
- **Input license:** CC0. **Sensitivity:** public.

| Variable | Type | Units | Allowed values / range | Description | Missingness |
| --- | --- | --- | --- | --- | --- |
| `wiki` | string | — | — | Edition | none |
| `qid` | string | — | `Q…` or `__WIKI_TOTAL__` | Item, or the wiki-total sentinel | none |
| `page_id` | Int64 | — | — | Local page ID | `<NA>` on wiki-total rows |
| `date` | date | — | window | Day (UTC) | days with zero views are **absent**; fill with 0 in the panel |
| `views` | int | count | ≥ 0 | User-agent pageviews | — |

## Dataset: `data/processed/article_month.parquet` *(planned)*

- **Grain:** one row per (qid, wiki, month), from the later of window start or article creation through window end. Months without activity are explicit zeros.
- **Sensitivity:** public aggregate; no editor identifiers. This is the releasable dataset.

| Variable | Type | Units | Allowed values / range | Description | Missingness |
| --- | --- | --- | --- | --- | --- |
| `qid`, `wiki` | string | — | — | Keys | none |
| `month` | date | first of month | window | Calendar month | none |
| `period` | category | — | `pre`, `post` | Relative to `window.boundary` | none |
| `cohort` | category | — | `incumbent`, `entrant` | Article created before / on-or-after the boundary | none |
| `edits` | int | count | ≥ 0 | Revisions in the month | 0 |
| `editors` | int | count | ≥ 0 | Distinct editor keys in the month | 0 |
| `new_editors` | int | count | ≥ 0 | Editors whose first edit to this article is in the month | 0 |
| `anon_edit_share` | float | proportion 0–1 | — | Share of edits by anonymous or temporary accounts | null if `edits` = 0 |
| `bot_edit_share` | float | proportion 0–1 | — | Share of edits by bots | null if `edits` = 0 |
| `reverted_share` | float | proportion 0–1 | — | Share of edits later identity-reverted | null if `edits` = 0 |
| `bytes_end` | int | bytes | ≥ 0 | Page size at month end | carried forward |
| `views` | int | count | ≥ 0 | User pageviews | 0 |
| `view_share` | float | proportion 0–1 | — | `views` / wiki-wide user views in the month | — |

### Derived variables

- `period` = `post` if `month` ≥ `window.boundary` else `pre`. See `settings.period`.
- `cohort` = `entrant` if the article's first revision is on or after `window.boundary`.
- `view_share` = article `views` / `__WIKI_TOTAL__` views for the same wiki and month. This reads each edition's AI attention against its own overall traffic; the cross-edition comparison on a fixed topic set stands in for a non-AI baseline (see `decision-log.md`).
- `editor_key` = `HMAC-SHA256(EDITOR_ID_SALT, identifier)[:16]`.

### Known issues & caveats

- **The frame is today's snapshot.** WikiProject tags and category membership are observed in 2026, not as they stood in 2020–2022. Articles deleted or merged before the snapshot are invisible (survivorship). Entrant articles exist only in the post-period by construction.
- **The frame is English-defined.** Topics are those English WikiProject AI tags; cross-language coverage depends on Wikidata sitelinks. AI topics covered only in other editions are out of scope (an exploratory crawl found 17% of topics in other editions' AI categories, at depth 1, have no English article). 39% of frame items exist only in English.
- **WikiProject tagging is noisy at the margins** (e.g. `Batik shirt` is tagged). Relevance is measured on a hand-coded random sample of 200 items, not assumed.
- **Pageviews are by current title.** Views recorded under an earlier title (before a page move) are missed. Add redirect/move-log aggregation before trusting pre-period views for renamed pages.
- **Automated-traffic classification changed** during the window. `agent=user` is the best available filter, not a clean measure of humans.
- **Temporary accounts** replaced IP editing on many wikis in 2025. That breaks the `anon_edit_share` series. Report the rollout dates per wiki.
- **Supports description, not causation.** The data can describe level and trajectory differences between periods, wikis, and frame bounds. It cannot attribute them to ChatGPT or any other event.

## Glossary

| Term / acronym | Definition |
| --- | --- |
| QID | Wikidata item identifier; the language-independent unit that links the same topic across editions |
| sitelink | The link from a Wikidata item to its article in a specific wiki |
| WP1 | The Wikipedia 1.0 assessment tool that exports WikiProject quality and importance ratings |
| frame | The English WikiProject Artificial Intelligence article set, mapped through Wikidata to the 20 analysis editions |
| core-importance subset | Frame items the WikiProject rates Top, High, or Mid importance; used as a robustness check |
| incumbent / entrant | Article that existed before / was created on or after the period boundary |
| identity revert | A revision whose content hash matches an earlier revision, restoring it exactly |
| user agent (pageviews) | Wikimedia's classification of traffic not identified as spiders or automated |
