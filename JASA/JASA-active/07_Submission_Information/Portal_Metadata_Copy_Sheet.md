# JASA Portal Metadata Copy Sheet

Use this sheet to populate the live submission portal. The corresponding
author should compare each field with the portal's current wording before
release.

## Journal and section

- **Journal:** Journal of the American Statistical Association
- **Section:** Theory and Methods
- **Article type:** Original research article / method article, using the
  closest label offered by the portal

## Title

**Surrogate-Assisted Local Conditional Distribution Inference with Scarce
Reference Outcomes**

## Suggested short title

**Surrogate-Assisted Local Distribution Inference**

## Abstract (184 words)

Reference outcomes are costly, while cheaper surrogates are available for most
units. We study the conditional distribution of a reference outcome at a
chosen covariate value under selective verification, where few verified
observations may lie nearby. A surrogate-free X-based estimator remains valid
but can be noisy; surrogate outcome regression improves precision but can
increase error when its local correction is inaccurate. We retain this
surrogate-free estimator as an anchor and select one correction weight across
the CDF by an observable local variance criterion. Sample splitting separates
regression fitting and weight selection from final CDF evaluation. We
establish path-oracle equivalence, a uniform Gaussian limit, and multiplier
validity when the verification fraction may decrease. The bands cover a
kernel-localized CDF; point-target CDF and quantile inference additionally
require localization-bias control. Simulations show that the criterion
distinguishes helpful from harmful full borrowing: the adaptive weight
approaches zero under local reversal and retains gains under alignment,
although Full can be more efficient under strong alignment. Two real-data
applications and a controlled review benchmark show that the precision gain
varies with the strength and direction of the local surrogate relation.

## Keywords

two-phase sampling; missing at random; negative transfer; selective
verification; semiparametric efficiency; multiplier bootstrap

## Authors

1. **Jian Hou** — College of Systems Engineering, National University of
   Defense Technology, Changsha, Hunan 410073, China; ORCID
   0000-0002-9248-6874; houjian1997@nudt.edu.cn.
2. **Tan Meng** — Center for Applied Statistics, School of Statistics, Renmin
   University of China, Beijing 100872, China; ORCID
   0009-0001-1812-1834; mengtan33@ruc.edu.cn.
3. **Maozai Tian** — Center for Applied Statistics, School of Statistics,
   Renmin University of China, Beijing 100872, China; ORCID
   0000-0002-0515-4477; mztian@ruc.edu.cn; corresponding author.

## Funding

This work was partially supported by the Beijing Natural Science Foundation,
project “Theory, Methodology and Applications of Functional Hierarchical
Quantile Regression Modeling” (No. 1242005); the Fundamental Research Funds
for the Central Universities and the Research Funds of Renmin University of
China, project “Robust Statistical Inference for Complex Data” (No. 25XNN015);
and the Ministry of Education Humanities and Social Sciences Research General
Project, project “Research on Spatial-temporal Quantile Regression Modeling:
Theoretical Methods and Applications” (No. 25YJA910005).

## Conflict of interest

The authors declare that there are no conflicts of interest.

## Prior dissemination and concurrent submission

The manuscript is original and is not under consideration by another journal.
Neither the manuscript nor substantially overlapping material has previously
been published, posted as a preprint or working paper, presented at a
conference or seminar, included in a thesis or dissertation, deposited in a
public manuscript repository, or circulated in another form.

## Generative AI Use Statement

DeepSeek models `deepseek-v4-pro` and `deepseek-v4-flash` were used as
automated surrogate evaluators in the controlled synthetic AI-assisted review
benchmark. They scored the synthetic dossiers under a common rubric before the
expert-review samples were drawn; expert-panel outcomes defined the reference
estimand. OpenAI Codex (GPT-5) was used during manuscript preparation to assist
with code debugging, selective editorial revision, language refinement, and
checks of wording, consistency, citations, and typography. The authors
reviewed and verified the research design, statistical analyses, all code
changes, and all revised text. All authors approved these uses and the present
disclosure and accept responsibility for the article.

## Author contributions

Jian Hou conceived the study, developed the main content of the manuscript,
and wrote the software. Maozai Tian checked the theoretical arguments and
verified the accuracy of the manuscript. Tan Meng identified, obtained,
checked, and curated the application data and wrote the code for the empirical
analyses.

The corresponding author must enter the CRediT labels only after Tan Meng
confirms the final allocation in `CREDIT_STATEMENT_DRAFT.md`.

## Data and code availability

The EPA air-sensor and VitalDB data are publicly available from the sources
cited in Section 5. Code and derived numerical data sufficient to reproduce
every table and figure accompany the submission. The complete computational
materials retain the synthetic dossiers, expert-panel outcomes, automated
scores, and intermediate simulation results and are available to the editors
during review.

## Reviewer fields

No suggested or opposed reviewers have been supplied. The corresponding
author should complete these fields under the portal's current conflict rules.
