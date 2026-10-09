# LOI — JQD:DM Special Workflow Issue

Due **2026-10-25** through "Submit a Letter of Inquiry" (journalqd.org/about/submissions; log in or register first). The journal sets no length or file format, so this version aims for roughly 900 words of plain text that can be pasted into the form. It answers the four required questions directly and in order. Numbers marked `[TBD]` come from the pipeline (`ROADMAP.md`). Status: **v1 draft for the PI to edit.**

**Working title:** Writing and Reading About AI: Production and Consumption of AI-Related Wikipedia Articles Across 20 Language Editions, 2020–2026

---

**1. What is your research question, in one sentence?**

How did the production (article creation, revision, and coauthorship) and consumption (pageviews) of Wikipedia articles about artificial intelligence change across the 20 most-read Wikipedia language editions after November 2022, relative to each edition's own prior trajectory and its edition-wide activity?

**2. What is being described?**

We describe monthly activity on AI-related Wikipedia articles from November 2020 through September 2026 in 20 language editions. We split this window at November 2022, the month ChatGPT was released to the public, into a 24-month earlier period and a 47-month later period. The split is a descriptive marker: we make no claim that the release, or any other event, caused the differences we report.

The unit of observation is a topic (a Wikidata item) in a language edition in a month. For each unit we describe five things:

- **Coverage.** Whether an article on the topic exists in the edition, when it was created, and whether it predates or postdates November 2022.
- **Revision.** The volume of edits, the bytes added and removed, and the share of edits that are later reverted.
- **Coauthorship.** How many distinct editors contribute, how many are new to the article, how concentrated the work is among them, and what share comes from unregistered, temporary, and automated accounts.
- **Consumption.** Pageviews from human readers, and the share of each edition's total traffic that AI articles receive.
- **Alignment of production and consumption.** For each edition, whether growth in reading about AI kept pace with growth in writing about it.

We report each measure by edition and by period, with bootstrap confidence intervals over articles. We also report the differences between editions, which we expect to be at least as informative as the differences between periods.

**3. How is the sample constructed?**

There is no authoritative list of "AI articles," so we construct two frames that bracket the population and report every result for both.

*Narrow frame.* English Wikipedia's WikiProject Artificial Intelligence tags articles its participants judge to be within scope. A snapshot of its assessment list, taken 9 October 2026, contains 1,246 main-namespace pages, which resolve to [TBD] distinct Wikidata items. Through Wikidata's cross-language links, these items have [TBD] articles across the 20 editions, ranging from [TBD] in English to [TBD] in [TBD]. This frame is curated and precise, but it is anchored in English: it can only find topics that English Wikipedia covers.

*Broad frame.* Each edition maintains its own category for artificial intelligence (all linked to one Wikidata item). We collect every article within two levels of each edition's category and take the union across editions. This yields [TBD] distinct items, [TBD]% of which have no English article. This frame captures coverage that originates outside English but includes more off-topic pages, because category hierarchies drift.

*Relevance audit.* We draw a stratified random sample of 600 items (200 found only in the narrow frame, 200 only in the broad frame, and 200 in both) and hand-code each for whether it is substantively about AI. We report the precision of each stratum with its uncertainty. Findings that hold in both frames are robust to how "AI-related" is defined. Where the frames diverge, the divergence is itself a description of how language communities organize knowledge about AI.

*Editions.* We include the 20 editions with the most human pageviews in October 2022, the last month before the split: English, Japanese, Spanish, Russian, French, German, Italian, Chinese, Portuguese, Arabic, Persian, Polish, Turkish, Dutch, Indonesian, Ukrainian, Swedish, Czech, Vietnamese, and Korean. Ranking by readership rather than article count excludes editions whose size comes mostly from automatically generated articles. Readership drops off steeply: the 19th through 22nd editions are within 12% of one another, so we will show that results do not hinge on the last slot.

*Data.* Revision histories come from Wikimedia's public `mediawiki_history` dumps (snapshot 2026-09). Pageviews come from the Wikimedia pageviews API, restricted to traffic classified as human. Editor identifiers are pseudonymized with a keyed hash before analysis, and only aggregates will be released.

*Weighting.* Each frame is a census, not a probability sample, so we do not apply sampling weights within it. Two weighting choices remain, and we state both. Article-level summaries weight every article equally. Summaries of what readers encounter weight articles by pageviews. Pooled cross-edition figures are reported twice: weighting editions equally (each language community as one unit) and weighting by readership. We expect the two to differ sharply, because English accounts for most AI pageviews.

*Known limitations.* Both frames are observed in 2026, so articles deleted before then are absent, and articles created after November 2022 exist only in the later period by construction. We therefore report incumbent and newly created articles separately. Pageviews are recorded under an article's current title, so we add views logged under earlier titles. Two measurement changes fall inside the window, and we flag them where they affect the series: Wikimedia's reclassification of automated traffic, and the replacement of IP editing by temporary accounts in 2025.

**4. How does it pertain to digital media?**

Wikipedia is one of the most heavily used reference sources on the web. It is a frequent destination from search engines, and it is a primary source of training and grounding data for large language models. In the period we study, artificial intelligence became both a subject that Wikipedia's language communities had to document and a technology that changes how readers reach Wikipedia. Our questions concern this platform directly: who writes about AI on it, in which languages, how that work is organized, and how much readers in each language community consult it. The answers describe how unevenly collaboratively produced reference knowledge about a consequential technology was distributed across the world's largest online encyclopedia, and where public attention outpaced the volunteer labor that maintains it.
