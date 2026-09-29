#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
if command -v bibtex >/dev/null 2>&1; then BIBTEX=bibtex
elif command -v bibtex.original >/dev/null 2>&1; then BIBTEX=bibtex.original
else echo "BibTeX is required." >&2; exit 1; fi
cd paper
for target in manuscript supplement; do
  pdflatex -interaction=nonstopmode -halt-on-error "$target.tex"
  "$BIBTEX" "$target"
  pdflatex -interaction=nonstopmode -halt-on-error "$target.tex"
  pdflatex -interaction=nonstopmode -halt-on-error "$target.tex"
done
cd ../submission
pdflatex -interaction=nonstopmode -halt-on-error cover_letter.tex
pdflatex -interaction=nonstopmode -halt-on-error cover_letter.tex
