# Manuscript

`main.tex` is the JQD:DM article template (downloaded 2026-10-09 from https://journalqd.org/libraryFiles/downloadPublic/53, line endings normalized to LF). Do not change the preamble above the `DO NOT MAKE CHANGES ABOVE THIS LINE` marker except to fill the header short title and author names when the journal asks for them. Review is double-blind, so leave author fields as placeholders in the review copy.

Build with XeLaTeX, because the template loads `fontspec` with Times New Roman and Arial: `latexmk -xelatex main.tex`. Add `figure1.png` (or remove the sample figure) before building. Bibliography entries go in `ref.bib` (natbib, apalike).

Every number, table, and figure in the manuscript should come from a pipeline output under `results/`. The Special Workflow Issue's LLM check tests consistency between text, tables, and figures.
