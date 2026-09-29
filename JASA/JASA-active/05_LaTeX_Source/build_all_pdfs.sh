#!/usr/bin/env bash
set -euo pipefail

SOURCE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGE_ROOT="$(cd "${SOURCE_ROOT}/.." && pwd)"
BUILD_ROOT="$(mktemp -d /tmp/salcdi-submission-pdfs.XXXXXX)"

cleanup() {
  find "${BUILD_ROOT}" -type f -delete 2>/dev/null || true
  find "${BUILD_ROOT}" -depth -type d -empty -delete 2>/dev/null || true
}
trap cleanup EXIT

for command_name in latexmk pdfinfo grep; do
  command -v "${command_name}" >/dev/null 2>&1 || {
    echo "Required command is unavailable: ${command_name}" >&2
    exit 1
  }
done

rsync -a "${SOURCE_ROOT}/Manuscript_and_Supplement/" \
  "${BUILD_ROOT}/Manuscript_and_Supplement/"
mkdir -p "${BUILD_ROOT}/Cover_Letter" "${BUILD_ROOT}/ACC"
cp -p "${SOURCE_ROOT}/Cover_Letter/Cover_Letter.tex" \
  "${BUILD_ROOT}/Cover_Letter/Cover_Letter.tex"
cp -p "${SOURCE_ROOT}/ACC/ACC_form.tex" \
  "${BUILD_ROOT}/ACC/ACC_form.tex"

(
  cd "${BUILD_ROOT}/Manuscript_and_Supplement/paper"
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    manuscript_unblinded.tex >/dev/null
  latexmk -pdf -interaction=nonstopmode -halt-on-error \
    manuscript_blind.tex >/dev/null
)
(
  cd "${BUILD_ROOT}/Manuscript_and_Supplement/supplement"
  latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex >/dev/null
)
(
  cd "${BUILD_ROOT}/Cover_Letter"
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    Cover_Letter.tex >/dev/null
)
(
  cd "${BUILD_ROOT}/ACC"
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    ACC_form.tex >/dev/null
)

log_files=(
  "${BUILD_ROOT}/Manuscript_and_Supplement/paper/manuscript_unblinded.log"
  "${BUILD_ROOT}/Manuscript_and_Supplement/paper/manuscript_blind.log"
  "${BUILD_ROOT}/Manuscript_and_Supplement/supplement/supplement.log"
  "${BUILD_ROOT}/Cover_Letter/Cover_Letter.log"
  "${BUILD_ROOT}/ACC/ACC_form.log"
)
if grep -En \
  'undefined references|Citation.*undefined|Reference.*undefined|multiply defined|Overfull \\hbox' \
  "${log_files[@]}"; then
  echo "LaTeX log audit failed." >&2
  exit 1
fi

mkdir -p "${PACKAGE_ROOT}/01_Manuscripts" \
  "${PACKAGE_ROOT}/02_Cover_Letter" \
  "${PACKAGE_ROOT}/03_Supplementary_Materials"
cp -p "${BUILD_ROOT}/Manuscript_and_Supplement/paper/manuscript_unblinded.pdf" \
  "${PACKAGE_ROOT}/01_Manuscripts/Manuscript_with_author_details.pdf"
cp -p "${BUILD_ROOT}/Manuscript_and_Supplement/paper/manuscript_blind.pdf" \
  "${PACKAGE_ROOT}/01_Manuscripts/Manuscript_anonymous.pdf"
cp -p "${BUILD_ROOT}/Manuscript_and_Supplement/supplement/supplement.pdf" \
  "${PACKAGE_ROOT}/03_Supplementary_Materials/Supplementary_Material.pdf"
cp -p "${BUILD_ROOT}/Cover_Letter/Cover_Letter.pdf" \
  "${PACKAGE_ROOT}/02_Cover_Letter/Cover_Letter.pdf"
cp -p "${BUILD_ROOT}/ACC/ACC_form.pdf" \
  "${PACKAGE_ROOT}/03_Supplementary_Materials/ACC_form.pdf"

for pdf_path in \
  "${PACKAGE_ROOT}/01_Manuscripts/Manuscript_with_author_details.pdf" \
  "${PACKAGE_ROOT}/01_Manuscripts/Manuscript_anonymous.pdf" \
  "${PACKAGE_ROOT}/02_Cover_Letter/Cover_Letter.pdf" \
  "${PACKAGE_ROOT}/03_Supplementary_Materials/Supplementary_Material.pdf" \
  "${PACKAGE_ROOT}/03_Supplementary_Materials/ACC_form.pdf"
do
  [[ -s "${pdf_path}" ]] || {
    echo "Missing rebuilt PDF: ${pdf_path}" >&2
    exit 1
  }
done

echo "Rebuilt five submission PDFs in ${PACKAGE_ROOT}"
