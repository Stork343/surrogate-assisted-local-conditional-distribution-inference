# JRSSB V5

Surrogate-assisted local conditional distribution inference with certified simultaneous gains

This directory publishes the V5 editorial submission materials. The scientific baseline is the author's frozen V3 study; it does not include the separate later information-boundary development. The source files and vector figures reproduce the V5 package delivered on 29 September 2026.

## Files

- [Main manuscript](01_Manuscript/manuscript.pdf): expected 29 pages, including references, six figures and three tables.
- [Supplement](02_Supplementary_Material/supplement.pdf): expected 53 pages, including Figure S1.
- [Cover letter](03_Cover_Letter/cover_letter.pdf).
- [Complete editable LaTeX sources](04_LaTeX_Source/).
- [Separate vector figures](05_Separate_Figures/).
- [Combined manuscript and supplement](downloads/manuscript_and_supplement.pdf).
- [LaTeX source ZIP](downloads/LaTeX_Source.zip).
- [Editorial submission ZIP](downloads/JRSSB_V5_editorial_submission.zip).

The PDF and ZIP links are populated by the `Publish JRSSB V5 PDFs` workflow. Its report records page counts and file checksums. Source Git hashes are checked before building; no statistical analyses are rerun. Existing JASA, V3 checkpoint and writing_v4 directories are unchanged.

## Computational archive

`Frozen_V3_reproduction.zip` from the delivered complete submission package has NOT been uploaded by this publication step. It remains in the author's downloaded V5 package. The earlier public computation checkpoint is historical and is not a replacement for that frozen archive. The editorial ZIP therefore contains manuscript materials only, not the complete computational reproduction package. The statements in the scientific manuscript and cover letter are preserved verbatim from V5.

## Rebuild

Run `bash build_all.sh` inside `04_LaTeX_Source` with pdfLaTeX and BibTeX. The GitHub workflow compiles a temporary copy and writes PDFs to the publication folders without changing the frozen sources, numbers, statements, references or figure captions.
