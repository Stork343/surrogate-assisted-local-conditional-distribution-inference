# JASA Initial Submission Package

**Manuscript:** *Surrogate-Assisted Local Conditional Distribution Inference
with Scarce Reference Outcomes*

**Target:** *Journal of the American Statistical Association*, Theory and
Methods

**Prepared:** 25 August 2026

This package is organized for the corresponding author to check and upload.
The live submission portal controls the final category labels if they differ
from those below.

## 1. Files for the submission portal

| Package file | Suggested portal designation | Reviewer-visible |
|---|---|:---:|
| `01_Manuscripts/Manuscript_with_author_details.pdf` | Manuscript - with author details / not for review | No |
| `01_Manuscripts/Manuscript_anonymous.pdf` | Manuscript - anonymous / main document | Yes |
| `02_Cover_Letter/Cover_Letter.pdf` | Cover Letter | No |
| `03_Supplementary_Materials/Supplementary_Material.pdf` | Supplemental Material | Yes |
| `03_Supplementary_Materials/ACC_form.pdf` | Supplemental Material / ACC | Yes |
| `04_Data_and_Code/Data_and_Code_Anonymous.zip` | Data and Code / Supplemental Material | Yes |
| `06_Figures_and_Tables/Figures/` | Figure files, if requested separately | Yes |
| `06_Figures_and_Tables/Tables/` | Table files, if requested separately | Yes |

Do not assign the manuscript with author details, the cover letter, or the
files under `07_Submission_Information/` to a reviewer-visible category.

## 2. Data and code

`Data_and_Code_Anonymous.zip` is the self-contained anonymous computational
supplement. It contains the estimator and simulation code, analysis scripts,
tests, machine-readable results, synthetic dossiers, expert outcomes,
automated-score tables, and instructions for obtaining the public EPA and
VitalDB source data. Raw API response caches, credentials, author identities,
and the large internal result store are not included.

From the uncompressed data-and-code package, the principal check is:

```sh
bash reproducibility/rebuild_submission_artifacts.sh
Rscript reproducibility/run_correspondence_gate.R .
```

## 3. LaTeX sources

`05_LaTeX_Source/` contains the source for all five PDF deliverables:

- blind and unblinded manuscripts;
- Supplement;
- cover letter;
- ACC form.

To rebuild them from a clean temporary directory:

```sh
cd 05_LaTeX_Source
bash build_all_pdfs.sh
```

The build script places the rebuilt PDFs back into folders 1--3. The authoring
sources `Cover_Letter.md` and `ACC_form.Rmd` are also retained alongside their
standalone LaTeX files.

## 4. Corresponding-author checks before submission

1. Confirm title, author order, affiliations, emails, ORCIDs, funding, and
   conflicts against `07_Submission_Information/Portal_Metadata_Copy_Sheet.md`.
2. Obtain Tan Meng's direct approval of the final manuscripts, Supplement,
   and CRediT allocation.
3. Confirm whether “Writing - review and editing” accurately applies to Tan
   Meng before entering CRediT roles.
4. Complete the suggested/opposed reviewer fields under the portal's current
   conflict rules.
5. Inspect the portal-generated reviewer PDF page by page and verify that the
   anonymous manuscript and reviewer-visible supplements contain no author
   identity.

## 5. Package integrity

`FILE_INVENTORY.csv` records the byte size, checksum, suggested designation,
and reviewer visibility of every file. The accompanying `.zip.sha256` file
checks the complete package transferred to the corresponding author.
