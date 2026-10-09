# AI on Wikipedia

A descriptive, cross-language analysis of how the production (article creation, revision, coauthorship) and consumption (pageviews) of AI-related Wikipedia articles changed across the 20 most-read Wikipedia language editions before and after November 2022.

A CUPIDS Lab data project. Maturity level: **L2 (Reproduce)**. Toolchain: **Python (conda + Snakemake)**. Sensitivity: **public (conditional — becomes sensitive-human if editor-level identifiers are retained or shared; see `ROADMAP.md`)**. Openness: **open-on-publication**.

## What & why

Wikipedia is both an information infrastructure that generative AI systems are trained on and a public that documents, argues about, and reads about AI. The public release of ChatGPT on 30 November 2022 is a convenient temporal marker for the period in which AI became a mass-audience topic. This project *describes* — it does not estimate causal effects of — how Wikipedia's coverage of AI changed across language communities: which AI topics exist in which languages, who writes and revises them, how concentrated that work is, and how much attention readers pay to them, comparing a pre-period (Nov 2020 – Oct 2022) to a post-period (Nov 2022 – Sep 2026).

The immediate deliverable is a manuscript for the *Journal of Quantitative Description: Digital Media* Special Workflow Issue (LOI due 2026-10-25; manuscript due 2027-01-15). Beneficiaries are researchers of online knowledge production and AI's information ecosystem, Wikimedia communities documenting AI, and the Wikimedia Foundation. The design partner is the PI; the roadmap records roles to add if coauthors join. Success is a re-runnable pipeline whose outputs every number in the manuscript can be traced back to. See `docs/design-memo.md` for the full research design and `docs/loi-draft.md` for the LOI skeleton.

## Repository layout

This repo follows the CUPIDS Lab data-project conventions. Key locations: `data/raw` holds original, **immutable** source data (never edited in place — bulk or re-downloadable inputs such as `mediawiki_history` dumps are git-ignored, while the small curated WikiProject AI snapshot `data/raw/wp1_artificial_intelligence_2026-10-09.tsv` is the tracked source-of-record via a `.gitignore` carve-out); `data/interim` and `data/processed` hold derived data that can always be regenerated from raw; `DATA-DICTIONARY.md` documents the schema. See `ROADMAP.md` for what is planned but not yet built.

```
├── Snakefile, config.yaml          # pipeline-as-code + all parameters (languages, window, frame)
├── src/ai_on_wikipedia/            # one module per pipeline stage
├── data/{raw,interim,processed,external}/
├── exploratory/                    # notebooks only live here
├── results/{figures,tables}/       # generated; regenerate with snakemake
├── docs/design-memo.md             # research design + brainstorm
├── docs/loi-draft.md               # JQD:DM Letter of Inquiry skeleton
└── manuscript/                     # JQD:DM LaTeX template (XeLaTeX)
```

## Getting started

```bash
git clone https://github.com/brianckeegan/ai-on-wikipedia
cd ai-on-wikipedia
```

Set up the environment and run the pipeline:

```bash
conda env create -f environment.yml
conda activate ai-on-wikipedia
pip install -e .      # install the project so pipeline modules import
cp .env.example .env  # then set EDITOR_ID_SALT to a long random string (never commit .env)
snakemake -n          # dry-run: preview the steps (run from the repo root)
snakemake --cores 4   # run the pipeline
```

The pipeline calls public Wikimedia APIs and downloads public dumps. Set a descriptive `user_agent` with contact information in `config.yaml` before running, and keep request rates polite: the APIs rate-limit aggressively from shared IPs.

## Data access

Processed, non-sensitive data is shared in open formats. See `DATA-DICTIONARY.md` for the schema. Only **aggregated** outputs (article-month and wiki-month tables) are intended for release; editor identifiers are salted-hashed at ingest and never written to `data/processed/` (see `ROADMAP.md`, blocking item).

## Documentation

- `DATA-DICTIONARY.md` — variables, grain, provenance, units, missingness, known issues.
- `decision-log.md` — why key choices were made.
- `CHANGELOG.md` — what changed and when.
- `docs/design-memo.md` — research question, sampling frame, measures, threats, literature pointers.
- `docs/loi-draft.md` — the four LOI questions with draft answers.

## Citation

If you use this project, please cite it. Brian C. Keegan et al., *AI on Wikipedia*, CUPIDS Lab, 2026. Machine-readable metadata is in `CITATION.cff` and `codemeta.json`.

## License

Code is released under MIT. See `LICENSE`. Wikipedia text and metadata are © their contributors under CC BY-SA 4.0; derived aggregate data inherit those terms where applicable.

## Contact

Brian C. Keegan · accounts@brianckeegan.com · CUPIDS Lab.
