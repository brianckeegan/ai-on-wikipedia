# Design memo — AI on Wikipedia

Working research design for the JQD:DM Special Workflow Issue. This is the brainstorm, refined. The LOI-length version is `docs/loi-draft.md`. Decisions recorded here are logged with rationale in `decision-log.md`.

## Venue constraints that shape the design

The *Journal of Quantitative Description: Digital Media* publishes quantitative description and **no causal claims**. LOIs are judged by humans on four questions answered in order: the research question in one sentence, what is described, how the sample is constructed, and how it pertains to digital media. Reviewers "pay special attention to sampling and weighting." In the Special Workflow Issue, the full manuscript must pass an LLM check (via a skill file distributed on 2026-11-01). The check covers fit with the descriptive mandate (no causal claims slipped in), documentation of data, sampling, and measurement, appropriate statistics with reported uncertainty, internal consistency between text, tables, and figures, and self-contained presentation. Human reviewers then judge theoretical value, conceptual coherence, and contribution. Each author may appear on only one submission. Timeline: LOI 2026-10-25, manuscript 2027-01-15, reviews 2027-02-15, revisions 2027-03-08, publication 2027-03-15.

Implications: November 2022 is a **period boundary, not a treatment**. Every number must trace to a pipeline output. Every comparison should carry an interval. The sampling frame needs to be defensible on its face: one editor-curated topic set, measured identically in every edition, with its English-defined scope stated plainly.

## Research question (one sentence)

How did the production (article creation, revision, coauthorship) and consumption (pageviews) of AI-related Wikipedia articles change across the 20 most-read language editions after November 2022, relative to each edition's own pre-period trajectory and its edition-wide activity?

Sub-questions that organize the descriptive results:

1. **Coverage.** Which AI topics exist in which editions, and how did the stock grow? Compare incumbents (articles that existed before the boundary) with entrants (articles created after it), and English-anchored items with items native to each language.
2. **Production intensity.** How did edits, distinct editors, newcomer share, bot and anonymous share, and identity-revert rates change on AI articles across periods and editions?
3. **Coauthorship structure.** Did authorship of AI articles concentrate (fewer editors doing more of the work) or diffuse? How much do editors overlap across AI articles and across editions?
4. **Attention.** How did user pageviews to AI articles, and their share of each edition's total traffic, change? Where is attention high but production low, or the reverse?
5. **Production–consumption alignment.** Within each edition, does growth in AI attention match growth in AI authorship? Rank editions by the gap.

## What is described

The unit is the **Wikidata item × language edition**, observed monthly from 2020-11 to 2026-09. Measures:

| Concept | Measure | Source |
| --- | --- | --- |
| Coverage | article exists; creation month; incumbent/entrant cohort; bytes; Content Translation origin | `mediawiki_history`, Wikidata |
| Revision | edits/month; identity-revert share; bytes changed | `mediawiki_history` |
| Coauthorship | distinct editors/month; new-editor share; Gini of edits across editors; anonymous/temporary/bot shares; cross-article and cross-wiki editor overlap (pseudonymized) | `mediawiki_history` |
| Consumption | daily user pageviews → monthly; share of edition-wide user views | Wikimedia REST pageviews |
| Frame metadata | WikiProject quality/importance; core-importance flag | WP1 |

## How the sample is constructed

The frame is a single, editor-curated topic set, measured identically in every edition (PI decision, 2026-10-09; see `decision-log.md`).

- **Frame: English WikiProject Artificial Intelligence, mapped across languages.** The WP1 assessment export, frozen on 2026-10-09, has 1,882 tagged pages. 1,246 are in the main namespace (488 Start, 388 C, 112 B, 107 Stub, 29 List, 5 GA, 43 unassessed, and 74 NA-class rows that are mostly redirects). The rest are 463 drafts, 136 categories, 26 templates, and 11 files. The main-namespace titles resolve (following redirects) to 1,212 Wikidata items, with 27 unmapped. Through sitelinks, those items have 5,914 articles across the 20 editions, from 1,209 in English to 115 in Swedish. 39% of items exist only in English, the median item appears in 2 editions, and 49 appear in all 20.
- **Why one frame.** Holding the topic set fixed makes the editions comparable: differences between them cannot come from different definitions of "AI." The cross-edition comparison stands in for a non-AI baseline. Edition-wide totals (`view_share`, AI share of edition edits) give each edition its own denominator.
- **Scope condition.** The topic set is defined by English Wikipedia. An exploratory crawl of each edition's own AI category and its immediate subcategories (`exploratory/frame_counts_2026-10-09/`) found that 17% of the topics filed there have no English article. These are out of scope and are stated as a limitation, not corrected for. The two-frame design using that crawl was considered and dropped.
- **Relevance audit.** A simple random sample of 200 items (seed 42) is hand-coded for topical relevance, and the frame's precision is reported with a 95% interval. WikiProject tagging is noisy at the margins (for example, "Batik shirt" is tagged).
- **Robustness subset.** Main results are re-run on the 184 items rated Top, High, or Mid importance (2,142 articles). 705 items have no importance rating, so the subset is small but cleanly on-topic.
- **Languages.** The top 20 editions by user pageviews in 2022-10, the last full pre-period month: en, ja, es, ru, fr, de, it, zh, pt, ar, fa, pl, tr, nl, id, uk, sv, cs, vi, ko (ru verified at 945M, rank 4). Ranks 19–22 (vi, ko, he, hi) are within 12% of each other, so the 20th slot is fragile. Report this, and consider a robustness swap.
- **Weighting.** The frame is a census of the WikiProject's topics, not a probability sample. Results are reported unweighted at the article level, plus attention-weighted (by pageviews) where the question is about what readers encounter. Edition-level summaries are not pooled across editions without stating the weights.
- **Known frame limitations** (state them in the paper): the frame is observed in 2026, so pages deleted before then are missing (survivorship); entrants exist only post-boundary by construction; WikiProject tagging itself grew over the window; per-article pageviews are keyed to the current title.

## How it pertains to digital media

Wikipedia is a core piece of public information infrastructure. It is a top destination for search and a primary training and grounding corpus for large language models. AI is therefore both a *topic* that Wikipedia's language communities must document and a *technology* that reshapes how readers reach Wikipedia. Describing how 20 language communities produced and consumed knowledge about AI during its mass-market arrival shows which publics had current, well-maintained, collaboratively authored reference information about a fast-moving technology, and where attention outpaced authorship. The design does not claim that AI caused any change.

## Threats to description (what reviewers will probe)

1. **Platform-wide trends.** Edition-wide pageviews and editing fell during the window, and Wikimedia reclassified automated traffic. Mitigation: edition-wide denominators (`view_share`, AI share of edition edits), and explicit notes on the classifier changes. A matched non-AI sample was considered and deferred (see `decision-log.md`).
2. **Measurement breaks.** Temporary accounts replaced IP editing on many wikis in 2025. Report per-wiki rollout dates and avoid reading the anonymous-share series across them.
3. **Frame dependence.** The frame is English-defined. This is handled by the stated scope condition, the relevance audit, and the core-importance robustness subset.
4. **Multiple comparisons across 20 editions × many measures.** Lead with a small set of pre-specified headline measures. Present the rest as small multiples with intervals and no significance stars.

## Literature to position against (verify each before citing)

These are pointers from memory and must be checked before citing: Hecht & Gergle (2010) on cross-language content diversity; Keegan, Gergle & Contractor (2013) on breaking-news collaboration on Wikipedia; McMahon, Johnson & Hecht (2017) and Vincent, Johnson & Hecht (2018) on Wikipedia's interdependence with search and other platforms; Reeves, Yin & Simperl (2024) on ChatGPT and Wikipedia engagement; Lyu et al. (2025) on Wikipedia contributions after ChatGPT; Brooks, Eggert & Peskoff (2024) on AI-generated content in new Wikipedia articles; and the Wikimedia Foundation's 2025 reporting on human pageview declines after its bot-detection update. The contribution relative to these: they study Wikipedia *in general* after ChatGPT, mostly in English, whereas this project describes Wikipedia's coverage *of AI itself* across 20 editions, separating production from consumption.

## Open questions for the PI

- Coauthors? Each author can appear on only one submission in this issue.
- Report Draft-namespace AI submissions (463 in WP1) as a side measure of production pressure?
