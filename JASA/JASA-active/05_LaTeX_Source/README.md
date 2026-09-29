# LaTeX Sources for the Submission PDFs

This directory contains source for every PDF in the submission package.

## Contents

- `Manuscript_and_Supplement/paper/`: blind and unblinded manuscript drivers,
  shared section files, bibliography files, tables, and figures.
- `Manuscript_and_Supplement/supplement/`: Supplement driver and section files.
- `Cover_Letter/Cover_Letter.tex`: standalone LaTeX cover letter.
- `Cover_Letter/Cover_Letter.md`: authoring source for the cover letter.
- `ACC/ACC_form.tex`: standalone LaTeX source for the completed ACC.
- `ACC/ACC_form.Rmd`: completed official JASA R Markdown form.
- `build_all_pdfs.sh`: clean rebuild of all five PDFs.

## Build

Requirements are TeX Live 2024 or later, `latexmk`, XeLaTeX, BibTeX, R with
`rmarkdown`, and Pandoc. From this directory:

```sh
bash build_all_pdfs.sh
```

The build runs in a temporary directory, so auxiliary files do not enter the
submission package. The unblinded manuscript source and cover-letter source
contain author identity and must not be uploaded to a reviewer-visible
category.
