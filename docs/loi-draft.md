# LOI — JQD:DM Special Workflow Issue

Due **2026-10-25** through "Submit a Letter of Inquiry" (journalqd.org/about/submissions; log in or register first). The journal sets no length or file format; this version is plain text that can be pasted into the form. A 150-word abstract comes first, followed by direct answers to the four required questions, in order. The journal says an abstract is not a substitute for those answers, so the abstract supplements them and does not replace them. Frame sizes come from the pipeline's frame stage, run on 2026-10-09 (`snakemake data/processed/frame.parquet`). Status: **v1 draft with numbers, for the PI to edit.**

**Working title:** Writing and Reading About AI: Production and Consumption of AI-Related Wikipedia Articles Across 20 Language Editions, 2020–2026

---

**Abstract**

Generative AI became a mass-audience topic after November 2022, and Wikipedia is a main place where the public documents and reads about it. We describe how Wikipedia's coverage of artificial intelligence changed across the 20 most-read language editions from November 2020 to September 2026. Our frame is the articles English Wikipedia's WikiProject Artificial Intelligence considers in scope: 1,211 topics with 5,928 articles across the 20 editions. Because every edition is measured on the same topics, the editions serve as comparisons for one another. Using public revision histories and pageview data, we describe coverage, revision activity, coauthorship, and readership before and after November 2022, and whether reading about AI kept pace with writing about it in each language. We treat November 2022 as a period boundary, not a cause, and report estimates with uncertainty. The result documents how unevenly reference knowledge about a consequential technology is produced and consumed across languages.

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

We report each measure by edition and by period, with bootstrap confidence intervals over articles. Because every edition is measured on the same set of topics, the editions serve as comparison cases for one another: the differences between language communities are as central to the description as the differences between periods.

**3. How is the sample constructed?**

There is no authoritative list of "AI articles," so we use the judgment of the editors who maintain the topic. English Wikipedia's WikiProject Artificial Intelligence tags the articles its participants consider within scope and rates their quality and importance. A snapshot of its assessment list, taken 9 October 2026, contains 1,246 main-namespace pages. These resolve to 1,211 distinct Wikidata items; 28 pages have no item. Through Wikidata's cross-language links, these items have 5,928 articles across the 20 editions, from 1,211 in English to 115 in Swedish. Coverage is uneven: 39% of the topics have an article only in English, the median topic appears in two editions, and 49 appear in all 20.

Holding the topic set fixed is what makes the editions comparable. Each edition is described on the same list of topics, so differences in coverage, editing, and readership between editions cannot come from different definitions of "AI." This cross-edition comparison takes the place of a comparison with non-AI articles. We also report edition-wide totals of pageviews and edits as denominators, so that each edition's AI activity is read against its own overall trend.

The cost of this design is that the topic set is defined by English Wikipedia. Topics covered only in other editions fall outside it. As a check on how much is missed, we crawled each edition's own artificial intelligence category and its immediate subcategories: about one in six of the topics filed there has no English article. We state this as a scope condition rather than correcting for it.

*Relevance audit.* WikiProject tags are not perfectly precise; the list includes a few pages that are only loosely related to AI. We hand-code a simple random sample of 200 topics for whether each is substantively about AI and report the frame's precision with a 95% interval. We also check that our main results hold when the frame is restricted to the 183 topics the WikiProject rates as being of top, high, or mid importance (2,154 articles across the 20 editions).

*Editions.* We include the 20 editions with the most human pageviews in October 2022, the last month before the split: English, Japanese, Spanish, Russian, French, German, Italian, Chinese, Portuguese, Arabic, Persian, Polish, Turkish, Dutch, Indonesian, Ukrainian, Swedish, Czech, Vietnamese, and Korean. Ranking by readership rather than article count excludes editions whose size comes mostly from automatically generated articles. The ranking is tight near the cutoff (the 19th through 22nd editions are within 12% of one another), so we will show that results do not depend on which edition takes the last slot.

*Data.* Revision histories come from Wikimedia's public `mediawiki_history` dumps (snapshot 2026-09). Pageviews come from the Wikimedia pageviews API, restricted to traffic classified as human. Editor identifiers are pseudonymized with a keyed hash before analysis, and only aggregates will be released.

*Weighting.* The frame is a census of the WikiProject's topics, not a probability sample, so we do not apply sampling weights within it. Two weighting choices remain, and we state both. Article-level summaries weight every article equally. Summaries of what readers encounter weight articles by pageviews. Pooled cross-edition figures are reported twice: weighting editions equally (each language community as one unit) and weighting by readership. We expect the two to differ sharply, because English accounts for most AI pageviews.

*Known limitations.* The frame is observed in 2026, so articles deleted before then are absent, and articles created after November 2022 exist only in the later period by construction. We therefore report incumbent and newly created articles separately. Pageviews are recorded under an article's current title, so we add views logged under earlier titles. Two measurement changes fall inside the window, and we flag them where they affect the series: Wikimedia's reclassification of automated traffic, and the replacement of IP editing by temporary accounts in 2025.

**4. How does it pertain to digital media?**

Wikipedia is one of the most heavily used reference sources on the web. It is a frequent destination from search engines, and it is a primary source of training and grounding data for large language models. In the period we study, artificial intelligence became both a subject that Wikipedia's language communities had to document and a technology that changes how readers reach Wikipedia. Our questions concern this platform directly: who writes about AI on it, in which languages, how that work is organized, and how much readers in each language community consult it. The answers describe how unevenly collaboratively produced reference knowledge about a consequential technology was distributed across the world's largest online encyclopedia, and where public attention outpaced the volunteer labor that maintains it.
