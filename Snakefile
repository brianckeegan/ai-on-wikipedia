# Pipeline-as-code for AI on Wikipedia.
# Pipelines, not cleaned snapshots, are the shared artifact: when the sources are
# re-released (new dump snapshot, new WP1 snapshot), re-running this re-applies every
# transformation. Preview with `snakemake -n`.
#
# Stages: rank_languages -> frame -> audit_sample
#         -> mediawiki_history -> revisions (per wiki) -> pageviews (per wiki)
#         -> panel -> describe

configfile: "config.yaml"

WIKIS = config["languages"]["wikis"]
PKG = "ai_on_wikipedia"


rule all:
    input:
        "results/tables/language_ranking.csv",
        "results/tables/relevance_audit_sample.csv",
        "data/processed/article_month.parquet",
        "results/tables/summary_by_wiki_period.csv",


# Rank candidate wikis by user pageviews in the reference month. The analysis list
# in config.yaml is pinned by hand after reviewing this table.
rule rank_languages:
    output:
        "results/tables/language_ranking.csv",
    shell:
        "python -m {PKG}.languages {output}"


# Build the frame: WikiProject AI articles (WP1 snapshot) mapped to Wikidata items and
# their sitelinks in every analysis wiki.
rule frame:
    input:
        config["frame"]["wp1_snapshot"],
    output:
        "data/processed/frame.parquet",
    shell:
        "python -m {PKG}.frame {input} {output}"


# Random sample of frame items for hand-coding topical relevance.
rule audit_sample:
    input:
        "data/processed/frame.parquet",
    output:
        "results/tables/relevance_audit_sample.csv",
    shell:
        "python -m {PKG}.audit {input} {output}"


# Download the mediawiki_history dump files for one wiki (bulk, git-ignored).
rule mediawiki_history:
    output:
        directory("data/raw/mediawiki_history/{wiki}"),
    shell:
        "python -m {PKG}.dumps {wildcards.wiki} {output}"


# Filter the dump to frame pages; hash editor identifiers at ingest.
rule revisions:
    input:
        frame="data/processed/frame.parquet",
        dump="data/raw/mediawiki_history/{wiki}",
    output:
        "data/interim/revisions/{wiki}.parquet",
    shell:
        "python -m {PKG}.revisions {wildcards.wiki} {input.frame} {input.dump} {output}"


# Daily user pageviews for every frame article in one wiki, plus the wiki-wide total
# (used as the denominator for attention shares).
rule pageviews:
    input:
        "data/processed/frame.parquet",
    output:
        "data/interim/pageviews/{wiki}.parquet",
    shell:
        "python -m {PKG}.pageviews {wildcards.wiki} {input} {output}"


# Article-month panel: production + consumption measures, aggregate only.
rule panel:
    input:
        frame="data/processed/frame.parquet",
        revisions=expand("data/interim/revisions/{wiki}.parquet", wiki=WIKIS),
        pageviews=expand("data/interim/pageviews/{wiki}.parquet", wiki=WIKIS),
    output:
        "data/processed/article_month.parquet",
    shell:
        "python -m {PKG}.panel {input.frame} {output} "
        "--revisions {input.revisions} --pageviews {input.pageviews}"


# Descriptive tables for the manuscript (pre vs. post, by wiki and frame bound).
rule describe:
    input:
        "data/processed/article_month.parquet",
    output:
        "results/tables/summary_by_wiki_period.csv",
    shell:
        "python -m {PKG}.describe {input} {output}"
