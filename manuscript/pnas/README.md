# PNAS research article

A PNAS Direct Submission research article built on this repository's pipeline. Start with `OUTLINE.md`. It covers the argument, section plan, word budget, figure plan, and the open decision about how this paper relates to the JQD:DM submission.

| File | What it is |
| --- | --- |
| `OUTLINE.md` | The working outline: claim, significance and abstract drafts, section plan, figures, SI plan, open questions. |
| `main.tex` | The manuscript skeleton in the PNAS two-column template, with stub text and figure placeholders. |
| `references.bib` | Bibliography. Entries marked `UNVERIFIED` must be checked before citing. |
| `figures/` | Final figures, exported from the pipeline's `results/figures/` at PNAS sizes (8.7, 11.4, or 17.8 cm wide). |
| `pnas-new.cls`, `pnasresearcharticle.sty`, `pnas-new.bst`, `jabbrv.sty`, `jabbrv-ltwa-*.ldf` | The PNAS LaTeX template files, vendored unchanged from the PNAS Overleaf template the PI supplied (2026-10-16). Do not edit them. |

Build with pdfLaTeX and BibTeX, e.g. `latexmk -pdf main.tex` from this folder. The class loads `lmodern`, `helvet`, `lettrine`, `mdframed`, `tikz`, `natbib`, and `authblk`, so a full TeX Live install is the easiest route. Overleaf works too: upload this folder, or start from the PNAS template there and copy in `main.tex` and `references.bib`.

PNAS's author guidance referenced in `OUTLINE.md` comes from the template itself. The author-center pages (https://www.pnas.org/author-center/submitting-your-manuscript) are the authority, so re-check them before submission.
