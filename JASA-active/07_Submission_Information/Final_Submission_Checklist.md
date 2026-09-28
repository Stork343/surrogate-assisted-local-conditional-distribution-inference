# Corresponding-Author Review Checklist

**Manuscript:** *Surrogate-Assisted Local Conditional Distribution Inference
with Scarce Reference Outcomes*

**Target:** *Journal of the American Statistical Association*, Theory and
Methods

**Prepared:** 25 August 2026

The files in the accompanying review folder are ready for the corresponding
author's submission check. Do not upload the full internal computational
archive or the unblinded manuscript to a reviewer-visible category.

## 1. Author and declaration check

- [ ] Confirm title, author order, affiliations, emails, and ORCIDs against
  `AUTHOR_METADATA_FORM.md`.
- [ ] Confirm the funding and conflict-of-interest statements in the
  unblinded manuscript.
- [ ] Obtain and record Tan Meng's approval of the final manuscripts,
  Supplement, and CRediT roles.
- [ ] Confirm the CRediT statement in `CREDIT_STATEMENT_DRAFT.md` and decide
  whether “Writing – review and editing” accurately applies to Tan Meng.
- [ ] Confirm the prior-dissemination and concurrent-submission statement.
- [ ] Confirm that the Generative AI Use Statement accurately names the tools
  and uses; it does not mention the manuscript-editing skill.

## 2. Scientific-file check

- [ ] Read the blind manuscript as the reviewer will see it.
- [ ] Compare the unblinded manuscript with the blind manuscript; author,
  funding, and contribution information should be the only substantive
  differences.
- [ ] Check that every main-text reference to a Supplement theorem, table, or
  figure resolves correctly.
- [ ] Confirm that the Supplement contains the complete proofs for the main
  theoretical results and the stated technical extensions.
- [ ] Compare all six main figures and all three main tables with the values
  described in the manuscript.
- [ ] Check the cover letter for scientific emphasis and the statement of
  originality.

## 3. Reproducibility check

- [ ] Review `ACC_form.pdf` and confirm every checked box and software/runtime
  statement.
- [ ] Uncompress the anonymous computational package and start with
  `reproducibility/ANONYMOUS_REVIEW_README.md`.
- [ ] Run `bash reproducibility/rebuild_submission_artifacts.sh` inside that
  package and compare the rebuilt figures and tables with the submission PDFs.
- [ ] Confirm that the anonymous package contains no author names,
  affiliations, private paths, or credentials.
- [ ] Retain the full internal computational archive for an editor or
  reproducibility reviewer; do not expose it to anonymous referees.

## 4. Suggested portal file designations

| File | Suggested designation | Reviewer-visible |
|---|---|:---:|
| Blind manuscript PDF | Manuscript – anonymous / main document | Yes |
| Unblinded manuscript PDF | Manuscript with author details / not for review | No |
| Supplement PDF | Supplemental material for review | Yes |
| ACC PDF | Supplemental material | Yes |
| Anonymous computational package | Supplemental material / data and code | Yes |
| Cover letter PDF | Cover letter | Normally no |
| Standalone figure files | Figure files, if requested separately | Yes |
| Full internal computational archive | Retain for editor/AER request | No |

The live portal's labels control if they differ from the table above.

## 5. Final portal proof

- [ ] Copy the title, abstract, keywords, author metadata, funding, conflicts,
  and declarations from the prepared records rather than retyping from memory.
- [ ] Inspect the portal-generated reviewer PDF page by page.
- [ ] Verify that the reviewer proof contains no author identity, funding,
  acknowledgments, CRediT statement, private repository location, or local
  filesystem path.
- [ ] Verify that every uploaded Supplement, figure, and table is present and
  in the intended order.
- [ ] Save the portal confirmation and final uploaded-file list with the
  project records.
