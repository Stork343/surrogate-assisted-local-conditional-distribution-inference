# Anonymous Reproducibility Package

**Archive identifier:** `SALCDI-SC4-BLIND-2026-08-23`
**Canonical implementation:** `salcdi-canonical-p0d-v2`
**Band result schema:** `salcdi-band-repro-v1`

This package supports double-anonymized review of *Surrogate-Assisted Local Conditional Distribution Inference with Scarce Reference Outcomes*. It is generated from an explicit allowlist and is separate from the internal authoring and submission artifact.

## Contents

- blind main-manuscript PDF;
- blind Supplement PDF;
- reusable statistical functions;
- simulation data-generating, estimation, and summarization code;
- application-analysis code and public-data retrieval documentation;
- AI-evaluator configuration, prompts, synthetic dossiers, expert outcomes,
  automated-score tables, and analysis code without credentials;
- canonical result registry, claim map, machine-readable tables, and validation scripts;
- package metadata and tests;
- session information and a SHA-256 manifest.

## Rebuild the manuscript artifacts

From the package root, one command rebuilds all six main figures, the fixed-mask
Supplement diagnostic, three main tables, and Supplement Tables S5--S6 from the
included frozen machine-readable evidence:

```sh
bash reproducibility/rebuild_submission_artifacts.sh
```

This is a presentation-only rebuild. It does not rerun the Monte Carlo
experiments or estimators. The Python figure dependencies are pinned in
`reproducibility/requirements-figures.txt`; the application figures use the R
packages recorded in the project lockfile.

Large Monte Carlo result objects and raw API response caches are not duplicated
in this anonymous archive. The author-generated synthetic dossiers, expert
outcomes, automated-score tables, and machine-readable evidence underlying the
manuscript tables and figures are included. The separately retained full
submission archive contains the complete intermediate result store.

## Primary validation

From the package root, run the implementation, design-correspondence, and
claim-to-evidence checks with:

```sh
Rscript reproducibility/run_correspondence_gate.R .
Rscript reproduce.R 4 all
```

The first command runs the package tests and the 15-condition correspondence
gate. The second prints the ordered recomputation plan without executing it.
The included registry records 242 validated source objects. Revalidating those
objects with `validate_frozen_results.R` requires either a completed full
recomputation or the separately retained intermediate result store.

## Anonymity control

The build pipeline rejects author names, institutions, email addresses, repository-owner identifiers, private local paths, and identifying PDF metadata. The package does not include unblinded manuscript source, author metadata, funding statements, cover letters, internal status documents, repository history, or legacy manuscript directories.

## Data access

The EPA and VitalDB applications use publicly accessible source data obtained
through documented scripts or official repositories. The synthetic dossiers,
expert outcomes, and automated scores used in the AI-assisted review study are
included in this package. No API credential is included.
