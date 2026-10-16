# PNAS research article — outline

Working outline for a PNAS Direct Submission research article built on this repository's pipeline. The LaTeX skeleton is `main.tex` in this folder (PNAS two-column template), and the sources are `references.bib` and `figures/`. Status: **outline v0 (2026-10-16), no results yet.** Every bracketed `[X]` is a number the pipeline must produce, and every "Expected" line is a hypothesis to check, not a finding.

## Before writing: relationship to the JQD:DM submission

The JQD:DM Special Workflow Issue paper (`docs/loi-draft.md`, full manuscript due 2027-01-15) and this PNAS article draw on the same data. Both journals expect a manuscript that is not under consideration elsewhere, and both ask authors to disclose related work. Pick one of these routes before drafting past the outline.

| Option | What the PNAS paper is | Risk |
| --- | --- | --- |
| **A. Distinct contributions (recommended)** | JQD:DM publishes the descriptive panel: the frame, the measures, and edition-by-edition description. PNAS makes one broader argument (the attention–authorship gap and its translation-dependence), adds analyses JQD does not contain (translation provenance, editor concentration, cross-edition editor flows), cites the JQD paper, and is submitted after it. | Editors may still see heavy overlap. Disclose the JQD manuscript in the PNAS cover letter, and keep the PNAS figures non-overlapping. |
| B. PNAS instead of JQD:DM | Withdraw from the special issue (the LOI is due 2026-10-25) and write only this paper. | Loses the fast special-issue timeline. |
| C. JQD:DM only | Shelve this outline. | — |

Check PNAS's editorial policies on prior publication and related manuscripts on the author-center site before deciding. That page blocks automated fetches, so its current wording has not been checked for this outline.

## Format constraints (from the PNAS template's own guidance, 2026-10-16)

- **Article type:** Research Report, Direct Submission. A standard 6-page article is about 4,000 words, 50 references and 4 medium-size display items. The maximum is 12 pages. (A Brief Report is 3 pages, about 1,600 words and 15 references, and has no significance statement.)
- **Abstract:** 250 words or fewer, one paragraph, written for a general reader.
- **Significance statement:** 50–120 words, at a level an undergraduate-educated scientist outside the field can follow.
- **Keywords:** 3–5.
- **Front matter:** classification, author contributions, competing-interests declaration, and corresponding author. The corresponding author's ORCID is entered in PNAScentral, not in the manuscript.
- **Main text:** no "Introduction" heading. Suggested order: Results, Discussion, Materials and Methods. References are numbered in order of citation, and every reference cited in the main text belongs in the main file.
- **Figures:** final size 8.7 cm (one column), 11.4 cm or 17.8 cm wide. Lettering 6–12 pt. RGB. PDF or EPS preferred.
- **SI Appendix:** a single PDF, with figures and tables numbered S1, S2, …. If detailed methods go in the SI, the main-text Methods still have to carry the logic.
- **Data availability:** data, code and protocols in a public repository at publication. Datasets, original or reused, must be cited in the references.

**Classification (proposed):** Social Sciences: Social Sciences, dual-classified with Physical Sciences: Computer Sciences. Confirm against PNAScentral's current list.

**Keywords (proposed):** Wikipedia | generative AI | knowledge commons | multilingual | peer production

## Title options

1. Attention outpaces authorship: how the world's encyclopedia documented generative AI
2. Reading about AI in twenty languages, written mostly in one
3. The knowledge commons that trains AI, writing about AI

## Core claim (to be tested)

After November 2022, readers' attention to AI topics on Wikipedia grew across all 20 most-read language editions, but the volunteer labor that writes those articles grew far less evenly. Authorship concentrated in English Wikipedia and in a small core of editors, and coverage in many other editions arrived late and largely by translation from English. The result is a widening gap between where the public reads about a consequential technology and where knowledge about it is produced. That gap matters for global access to reliable information about AI, and also for AI itself, because Wikipedia is a primary training and grounding corpus for large language models.

The paper is descriptive and comparative. November 2022 is a period boundary, and the paper makes no causal claim about ChatGPT. PNAS does not forbid causal claims, but this design cannot support them, and the text should say so once, plainly, in the Discussion.

## Significance statement (draft, target ≤ 120 words)

> Wikipedia is where much of the world reads about new technologies, and it is also a main source of the text that AI systems learn from. We measured how 20 of Wikipedia's largest language communities wrote and read about artificial intelligence from 2020 to 2026. Reading about AI rose in every language, but writing about it did not keep pace: [most] new and revised AI articles were written in English by a small group of editors, and other languages often received translated copies months later. The gap between who reads and who writes about AI shows how unevenly reliable knowledge about a consequential technology is produced, and it identifies where the shared knowledge base that AI depends on is thinnest.

(About 115 words. Rewrite once results exist. Bracketed words are claims the data must support.)

## Abstract (draft skeleton, target ≤ 250 words)

1. **Context (2 sentences).** Wikipedia's role as a reference source and as AI training data; AI's arrival as a mass-audience topic after November 2022.
2. **Gap (1 sentence).** Studies of Wikipedia after ChatGPT have looked at Wikipedia's overall traffic and editing, mostly in English. None measures how its language communities documented AI itself.
3. **Data and design (2 sentences).** 1,211 topics that English Wikipedia's WikiProject Artificial Intelligence considers in scope, followed across 20 language editions (5,928 articles), November 2020 to September 2026, using the complete public revision histories and human pageviews.
4. **Findings (3–4 sentences, all to be filled).**
   - Attention rose [X]-fold, ranging from [X] to [X] across editions.
   - Edits and editors rose [X]-fold, concentrated in [English, N editions].
   - The top [1%] of editors made [X]% of edits.
   - [X]% of non-English articles created after November 2022 began as translations from English, with a median lag of [X] months.
5. **Implication (1–2 sentences).** An attention–authorship gap in the knowledge commons, and what it means for access and for AI training data.

## Introduction (≈700 words, no heading)

1. **Hook.** Wikipedia is among the most visited reference sources on the web and a primary training and grounding corpus for large language models. Generative AI's public arrival made AI itself a topic that hundreds of millions of people looked up.
2. **What is known.**
   - Wikipedia language editions cover different topics and cover shared topics differently (Hecht & Gergle; Callahan & Herring 2011; Roy et al. 2021).
   - Breaking-news topics draw concentrated, bursty collaboration (Keegan et al.).
   - Wikipedia's value is bound up with search and other platforms (McMahon et al.; Vincent et al.).
   - Recent work asks whether generative AI erodes Wikipedia's readership and contributors (Reeves et al.; Lyu et al.; Wagner & Jiang 2025), and how much new content is machine-written (Brooks et al.).
3. **The gap.** Prior work studies Wikipedia in general after ChatGPT, mostly English Wikipedia. Nobody has measured how the encyclopedia's language communities documented AI itself, or compared who reads that coverage with who writes it.
4. **This paper.** A fixed topic set followed across 20 editions makes production and consumption comparable across languages. Close with three questions:
   - Q1: how coverage spread;
   - Q2: whether attention and authorship grew together;
   - Q3: how concentrated and how translation-dependent the authorship was.

## Results (≈1,800 words, four subsections, one display item each)

### 1. A shared topic set, unevenly covered (Fig. 1)

- **Already measured:** the frame (1,211 topics, 5,928 articles); 39% of topics exist only in English; the median topic appears in 2 editions; 49 appear in all 20.
- **To compute:** coverage trajectories, i.e. cumulative articles by edition, before and after November 2022; topics created after November 2022 ("entrants") versus incumbents.
- **Fig. 1 (17.8 cm):**
  - (A) topic × edition coverage matrix, topics sorted by number of editions and editions by coverage;
  - (B) cumulative articles per edition over time, with November 2022 marked;
  - (C) share of each edition's AI articles that are entrants.
- **Expected:** coverage grows in every edition, but entrants are concentrated in English, and the lag from English creation to other editions is months.

### 2. Attention rose everywhere (Fig. 2)

- **Measure:** monthly human pageviews to frame articles; the frame's share of each edition's total human pageviews (`view_share`).
- **Fig. 2 (11.4 cm):**
  - (A) indexed monthly views by edition (small multiples or ridgeline);
  - (B) post- versus pre-period ratio of `view_share` per edition, with bootstrap 95% CIs.
- **Expected:** the share of attention rises in all editions, with the largest relative increases outside English.
- **Caveat to show:** Wikimedia's reclassification of automated traffic; restrict to `agent=user` and show sensitivity in the SI.

### 3. Authorship concentrated (Fig. 3)

- **Measures:** edits, distinct editors, new editors per article-month; concentration of edits across editors (Gini, top-1% share); anonymous, temporary and bot shares.
- **New relative to JQD:DM:** editors active in several editions (via pseudonymized global accounts) and their share of non-English AI edits. (Needs CentralAuth-level linking. Check feasibility, and check against the governance item in `ROADMAP.md`.)
- **Fig. 3 (8.7 cm):**
  - (A) editors per article-month, pre versus post, by edition;
  - (B) concentration curves of edits.
- **Expected:** editing grows less than attention; a small core does most of the work; cross-edition editors carry a large share of non-English edits.
- **Measurement break:** temporary accounts replaced IP editing in 2025. Report by edition and avoid reading the anonymous series across the break.

### 4. The attention–authorship gap and translation dependence (Fig. 4)

- **Headline estimand:** for each edition, Δlog(attention) − Δlog(authorship) between periods, with an article-cluster bootstrap CI.
- **Translation:** share of post-period non-English creations tagged `contenttranslation`, the source language when it is recoverable, and the lag from the English article's creation.
- **Fig. 4 (11.4 cm):**
  - (A) edition-level scatter of Δattention against Δauthorship, with a 45° line, CIs and point size by readership;
  - (B) translation share and median lag by edition.
- **Robustness (SI):** the core-importance subset (183 topics, 2,142 articles); swapping the 20th edition; pooling with editions weighted equally versus by readership.

## Discussion (≈700 words)

1. **Restate.** Attention to AI on Wikipedia spread across languages faster than authorship did.
2. **Why it matters for access.** Readers in many languages meet thinner, later, translated coverage of a technology that affects them, and that affects how the public understands AI policy, risk and use.
3. **Why it matters for AI.** Wikipedia is upstream of the models. Gaps in non-English AI coverage are gaps in the multilingual text those models learn about themselves from. State this as an implication, not a measured effect.
4. **What this design cannot say.**
   - No causal attribution to ChatGPT or to any other event.
   - The English-defined frame misses topics covered only outside English. An exploratory crawl found 17% of topics in other editions' AI categories have no English article.
   - Survivorship.
   - Pageview classification.
5. **What would help.** Translation tooling, cross-edition editor recruitment, and attention-weighted priorities for missing articles (connect to Wikimedia's own work on knowledge gaps, e.g. Wulczyn et al.).

## Materials and Methods (≈800 words in the main text; details in the SI)

- **Frame.**
  - WikiProject Artificial Intelligence assessment snapshot (WP1, 2026-10-09): 1,246 main-namespace pages, 1,211 Wikidata items.
  - Mapping: exact-title matching and sitelinks through the Wikidata Query Service, with fallbacks for redirects and for scholarly-graph items.
  - Relevance audit: 200 random topics, precision reported with a 95% CI.
  - Core-importance subset.
- **Editions.** Top 20 by human pageviews in October 2022.
- **Data.**
  - `mediawiki_history` dumps (snapshot 2026-09) for revisions, editors, reverts and Content Translation tags.
  - Wikimedia REST pageviews, daily, `agent=user`.
  - Both datasets cited in the references, as PNAS requires.
- **Measures.** As in `DATA-DICTIONARY.md` (`article_month`).
- **Estimation.**
  - Pre (Nov 2020–Oct 2022) versus post (Nov 2022–Sep 2026) comparisons on the log scale.
  - Article-cluster bootstrap CIs.
  - Pooled estimates two ways: editions weighted equally and by readership.
  - Segmented trends as a descriptive check, not identification.
- **Ethics and privacy.**
  - Public trace data; editor identifiers HMAC-pseudonymized at ingest; only aggregates released.
  - **Must confirm:** the university IRB's determination (exempt, or not human-subjects research), and how to state it. PNAS asks for IRB identification when research involves human participants.
- **Use of AI tools.** Disclose AI-assisted drafting and coding as PNAS's current editorial policy requires (check the policy text).

## SI Appendix (plan)

- **S1** Frame construction and relevance audit.
- **S2** Language ranking and cutoff sensitivity.
- **S3** Measurement breaks: automated-traffic reclassification and temporary accounts.
- **S4** Per-edition versions of Figs. 1–4.
- **S5** Core-importance robustness.
- **S6** Content Translation detection.
- **S7** Data dictionary for the released panels.

## Data, code and materials availability

- Released aggregate panels (`article_month`, edition-month) and code, deposited with a DOI (the Dataverse kit is a `ROADMAP.md` L5 item), with the frame snapshot and WP1 source-of-record.
- Raw inputs are public Wikimedia dumps and APIs, cited with access dates.
- No editor-level data released (see `ROADMAP.md`, blocking governance item).

## Word and display budget (6-page target)

| Part | Words |
| --- | --- |
| Introduction | 700 |
| Results (4 × 450) | 1,800 |
| Discussion | 700 |
| Materials and Methods | 800 |
| **Total main text** | **≈4,000** |
| Display items | 4 figures (no main-text tables) |
| References | ≤ 50 |

## Open questions for the PI

1. Route A, B or C above?
2. Is cross-edition editor linking (global accounts) in scope, given the editor-level governance item that is still blocking?
3. Should the PNAS analysis plan be preregistered (e.g. on OSF) before the panel is built? That would strengthen the descriptive estimands against forking-paths concerns.
4. Coauthors? (PNAS asks for author contributions, and the JQD:DM issue limits authors to one submission each.)
5. Which PNAS editor or member to suggest, and whom to exclude, in the cover letter?

## Reference notes

`references.bib` holds the citations named above. Entries marked `UNVERIFIED` come from memory and must be checked against the published versions before use. Entries without that mark were confirmed in a scholarly index (Wiley Scholar Gateway, 2026-10-16).
