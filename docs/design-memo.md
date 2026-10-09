# Design memo — AI on Wikipedia

Working research design for the JQD:DM Special Workflow Issue. This is the brainstorm, refined. The LOI-length version is `docs/loi-draft.md`. Decisions recorded here are logged with rationale in `decision-log.md`.

## Venue constraints that shape the design

The *Journal of Quantitative Description: Digital Media* publishes quantitative description and **no causal claims**. LOIs are judged by humans on four questions answered in order: the research question in one sentence, what is described, how the sample is constructed, and how it pertains to digital media. Reviewers "pay special attention to sampling and weighting." In the Special Workflow Issue, the full manuscript must pass an LLM check (via a skill file distributed on 2026-11-01). The check covers fit with the descriptive mandate (no causal claims slipped in), documentation of data, sampling, and measurement, appropriate statistics with reported uncertainty, internal consistency between text, tables, and figures, and self-contained presentation. Human reviewers then judge theoretical value, conceptual coherence, and contribution. Each author may appear on only one submission. Timeline: LOI 2026-10-25, manuscript 2027-01-15, reviews 2027-02-15, revisions 2027-03-08, publication 2027-03-15.

Implications: November 2022 is a **period boundary, not a treatment**. Every number must trace to a pipeline output. Every comparison should carry an interval. The sampling frame needs to be defensible on its face, which is why it is bracketed.

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
| Frame metadata | WikiProject quality/importance; anchor wikis; category depth | WP1, category crawl |

## How the sample is constructed (bracketed frame)

The frame has two bounds. Every result is reported for both.

- **Narrow bound: English WikiProject Artificial Intelligence.** The WP1 assessment export, frozen on 2026-10-09, has 1,882 tagged pages. 1,246 are in the main namespace (488 Start, 388 C, 112 B, 107 Stub, 29 List, 5 GA, 43 unassessed, and 74 NA-class rows that are mostly redirects). The rest are 463 drafts, 136 categories, 26 templates, and 11 files. Main-namespace titles are resolved through redirects to Wikidata items, then to their sitelinks in the 20 editions. This bound is editor-curated and high-precision, but English-anchored.
- **Broad bound: multi-anchored category union.** Each edition's local root category for artificial intelligence (from the Wikidata item for Category:Artificial intelligence) is crawled to depth 2. Article members are mapped to Wikidata items and unioned across editions. The English root alone has 36 direct subcategories, several of which drift off-topic (people, fiction, robots, philosophy). The depth cap and a relevance audit keep that drift in check. This bound captures AI articles that exist only in non-English editions.
- **Relevance audit.** A stratified random sample (narrow-only, broad-only, both; 200 items each, seed 42) is hand-coded for topical relevance. Precision per stratum, with 95% intervals, is reported in the paper.
- **Languages.** The top 20 editions by user pageviews in 2022-10, the last full pre-period month: en, ja, es, ru, fr, de, it, zh, pt, ar, fa, pl, tr, nl, id, uk, sv, cs, vi, ko. ru is pending verification. Ranks 19–22 (vi, ko, he, hi) are within 12% of each other, so the 20th slot is fragile. Report this, and consider a robustness swap.
- **Weighting.** The frame is a census of each bound, not a probability sample. Results are reported unweighted at the article level, plus attention-weighted (by pageviews) where the question is about what readers encounter. Edition-level summaries are not pooled across editions without stating the weights.
- **Known frame limitations** (state them in the paper): the frame is observed in 2026, so pages deleted before then are missing (survivorship); entrants exist only post-boundary by construction; WikiProject tagging itself grew over the window; per-article pageviews are keyed to the current title.

## How it pertains to digital media

Wikipedia is a core piece of public information infrastructure. It is a top destination for search and a primary training and grounding corpus for large language models. AI is therefore both a *topic* that Wikipedia's language communities must document and a *technology* that reshapes how readers reach Wikipedia. Describing how 20 language communities produced and consumed knowledge about AI during its mass-market arrival shows which publics had current, well-maintained, collaboratively authored reference information about a fast-moving technology, and where attention outpaced authorship. The design does not claim that AI caused any change.

## Threats to description (what reviewers will probe)

1. **Platform-wide trends.** Edition-wide pageviews and editing fell during the window, and Wikimedia reclassified automated traffic. Mitigation: edition-wide denominators (`view_share`, AI share of edition edits), and explicit notes on the classifier changes. A matched non-AI sample was considered and deferred (see `decision-log.md`).
2. **Measurement breaks.** Temporary accounts replaced IP editing on many wikis in 2025. Report per-wiki rollout dates and avoid reading the anonymous-share series across them.
3. **Frame dependence.** Handled by bracketing and the audit.
4. **Multiple comparisons across 20 editions × many measures.** Lead with a small set of pre-specified headline measures. Present the rest as small multiples with intervals and no significance stars.

## Literature to position against (verify each before citing)

These are pointers from memory and must be checked before citing: Hecht & Gergle (2010) on cross-language content diversity; Keegan, Gergle & Contractor (2013) on breaking-news collaboration on Wikipedia; McMahon, Johnson & Hecht (2017) and Vincent, Johnson & Hecht (2018) on Wikipedia's interdependence with search and other platforms; Reeves, Yin & Simperl (2024) on ChatGPT and Wikipedia engagement; Lyu et al. (2025) on Wikipedia contributions after ChatGPT; Brooks, Eggert & Peskoff (2024) on AI-generated content in new Wikipedia articles; and the Wikimedia Foundation's 2025 reporting on human pageview declines after its bot-detection update. The contribution relative to these: they study Wikipedia *in general* after ChatGPT, mostly in English, whereas this project describes Wikipedia's coverage *of AI itself* across 20 editions, separating production from consumption.

## Open questions for the PI

- Coauthors? Each author can appear on only one submission in this issue.
- Should the paper lead with the narrow bound and treat the broad bound as robustness, or present them side by side?
- Report Draft-namespace AI submissions (463 in WP1) as a side measure of production pressure?
- Is depth 2 right for every edition? Category hierarchies vary in granularity, so a per-edition depth or a relevance-calibrated depth may be fairer.
