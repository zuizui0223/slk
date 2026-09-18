# SLK Am Nat submission decisions V1

## Purpose

Freeze the remaining scope decisions after theory ownership, journal-prose conversion, prior-art coverage, formula consistency, review-file generation, anonymous reviewer packaging, and visual QA have been closed.

## Decision 1 — keep one explicit population-process exemplar

```text
ADD_SECOND_POPULATION_PROCESS_BEFORE_SUBMISSION = false
```

The fixation/occupancy results remain tied to the registered exponential Moran / connected symmetric rare-mutation process. Their role is not to claim universal population genetics. Their role is to demonstrate that transporting the same architecture-value object into a declared stochastic population process can create new separations and can also force an exact invariant.

Adding a second process before submission would broaden the paper without repairing the main reviewer risk, which is now the empirical generality of the ecological threshold predictions rather than lack of another process example. Generality is therefore claimed through the upstream `Phi=R-K` architecture-value layer; the later fixation/occupancy formulas remain explicitly process specific.

Revisit only if review specifically demands process robustness.

## Decision 2 — do not manufacture a Pedicularis worked result

```text
ADD_PARTIAL_PEDICULARIS_WORKED_RESULT_TO_MAIN_TEXT = false
```

The Pedicularis G1-G5 programme is prospectively registered but has no completed biological G1-G5 receipt. It must therefore not be used as a worked empirical result merely to make the theory look more validated.

Figure 3 provides the empirical measurement ladder. Pedicularis remains the first prospective application, but the submission manuscript keeps the explicit statement that no single biological system has completed the full ladder.

A real partial worked example can be added only after an actual identified receipt exists and its claim ceiling is clear.

## Decision 3 — retain The American Naturalist as primary target

```text
PRIMARY_TARGET = The American Naturalist
ECOLOGY_LETTERS_REASSESSMENT = requires_real_same_system_G1_G5_receipt
```

The current paper is strongest as a conceptual/theoretical ecology paper: an architecture-specific estimand transport, a unified critical-surface theorem, ecological threshold-displacement and conflict–differentiation discordance predictions, one-family constructive split witnesses, one exact process-level invariant, and an empirical measurement ladder. That profile fits an Am Nat theory contribution better than a broad empirical-synthesis claim.

The submission framing must emphasize biological theory and falsifiable measurement consequences, not software governance, repository integration, or bookkeeping.

## Closed pre-submission items

```text
THEORY_OWNERSHIP                         CLOSED
GENERAL_MARGIN Phi=R-K                  CLOSED
QUADRATIC_BRIDGE_SCOPE R=sL             CLOSED
JOURNAL_PROSE_CONVERSION                 CLOSED
REGISTERED_PRIOR_ART_COVERAGE            8/8 PASS
CORE_LITERATURE_CITED                    CLOSED
THEOREM_FORMULA_CONSISTENCY              PASS_AFTER_REPAIR
UNIFIED_THRESHOLD_ATLAS                  PASS
CROSS_LEVEL_PHI_COMPATIBILITY            PASS
ECOLOGICAL_THRESHOLD_DISPLACEMENT        PASS
ECOLOGICAL_FEEDBACK_GRADIENT             PASS
TWO_FREQUENCY_PHI_ETA_IDENTIFICATION      PASS
THREE_FREQUENCY_CURVATURE_DIAGNOSTIC     PASS
GENERALIZED_INVASION_SURFACES            PASS
ARBITRARY_SHAPE_ENDPOINT_INVASION        PASS
CONFLICT_DIFFERENTIATION_DISCORDANCE     PASS
FIGURE_2_ECOLOGICAL_PANEL                PASS
FIGURE_1_THRESHOLD_ATLAS                 PASS
WITNESS_ARITHMETIC                       PASS
FIGURE_1_GENERALITY                      REPAIRED
CLAIM_PROVENANCE_OWNERSHIP               REPAIRED
AMNAT_TITLE_WORDS                         9 PASS
AMNAT_ABSTRACT_WORDS                    189 PASS
AMNAT_TEXT_WORDS_EXCL_LITERATURE       4438 PASS
AMNAT_FIGURES                             3 PASS
AMNAT_TABLES                              2 PASS
AMNAT_FIGURE_TABLE_TOTAL                  5 PASS
FULL_CI_PY311_PY312                      PASS
REVIEW_MANUSCRIPT_PDF                    28 PAGES PASS
ANONYMOUS_TITLE_PAGE_PDF                  1 PAGE PASS
DOUBLE_SPACING_LINE_PAGE_NUMBERS         PASS
ANONYMOUS_REVIEWER_BUNDLE                PASS
IDENTITY_SCAN                             PASS
CLAIM_VERIFIER_NE1_NE5                    PASS
FIXATION_OCCUPANCY_INVARIANT_GRID        112/112 PASS
FIGURE_1_MANUAL_QA                       PASS
FIGURE_3_MANUAL_QA                       PASS
FINAL_FULL_PAGE_PROOFREAD                 OPEN
```

## Remaining submission actions

There is no remaining internal theory or reviewer-package construction task required before upload. The generated files pass structural and anonymity checks; a final human page-by-page proofread remains before portal upload. The identity-bearing GitHub URL must not be placed in the anonymous manuscript; the generated reviewer bundle should instead be uploaded directly through the journal system or through an anonymous reviewer-accessible deposit.

Remaining actions are controlled outside the scientific package:

```text
AUTHOR_METADATA                       REQUIRED
AI_USE_DISCLOSURE                     REQUIRED
ALL_AUTHOR_APPROVAL                   REQUIRED
PORTAL_UPLOAD                         REQUIRED
ANONYMOUS_BUNDLE_UPLOAD_OR_DEPOSIT    REQUIRED
```

## Remaining scientific-editorial risk

The remaining reviewer question is:

> Can rare-D and resident-D endpoint selection limits be estimated with acceptable extrapolation error on a scale compatible with independently measured `Phi`?

The submission answer must center on four deductions:

1. the same upstream architecture comparison can change verdict as it is transported through later estimands;
2. along an ecological gradient, value and invasion are displaced by `eta/a`, predicting both transition order and the width `2|eta|/a` of the coordination/coexistence zone in the registered affine slice;
3. conflict magnitude alone cannot rank differentiation when recoverability or architecture cost varies, so conflict–architecture discordance is expected rather than anomalous;
4. separation is not universal: the registered process forces reciprocal fixation ordering and weak-mutation occupancy ordering to re-align, showing that the framework predicts both splits and invariants.

## Submission state

```text
TARGET                  = THE_AMERICAN_NATURALIST
ARTICLE_TYPE            = MAJOR_ARTICLE
MANUSCRIPT              = SLK_MANUSCRIPT_AMNAT_V4.md
THEORY                  = READY
JOURNAL_PROSE           = READY
PRIOR_ART_CORE          = READY
FORMULA_CONSISTENCY     = PASS
FORMAT_LIMITS           = PASS
ANONYMOUS_REVIEW_FILES  = READY
REVIEWER_CODE_PACKAGE   = READY
EMPIRICAL_CLAIM_CEILING = THEORY_ONLY / NO_END_TO_END_G1_G9
INTERNAL_BLOCKERS       = NONE
EXTERNAL_ACTIONS        = METADATA + DISCLOSURE + APPROVAL + UPLOAD
MAIN_OPEN_RISK          = ENDPOINT_LIMIT_ESTIMATION
```
