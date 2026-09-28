# SLK Am Nat submission decisions V1

## Purpose

Freeze the remaining scope decisions after theory ownership, journal-prose conversion, prior-art coverage, formula consistency, review-file generation, anonymous reviewer packaging, and visual QA have been closed.

## Decision 1 — keep one explicit population-process exemplar

```text
ADD_SECOND_POPULATION_PROCESS_BEFORE_SUBMISSION = false
```

The fixation/occupancy results remain tied to the registered exponential Moran / connected symmetric rare-mutation process. Their role is not to claim universal population genetics. Their role is to demonstrate that transporting the same architecture-value object into a declared stochastic population process can create new separations and can also force an exact invariant.

Adding a second process before submission would broaden the paper without repairing the main reviewer risk, which is whether UTA1.10-UTA1.11 gate localization and conservative uncertainty propagation provide enough biological leverage beyond familiar component theories. Generality is therefore claimed through the upstream `Phi=R-K` architecture-value layer; the later fixation/occupancy formulas remain explicitly process specific.

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

The current paper is strongest as a conceptual/theoretical ecology paper: an architecture-specific estimand transport, a unified critical-surface atlas, ecological threshold-displacement and conflict–differentiation discordance predictions, one-family constructive split witnesses, a process-level consistency invariant, and an empirical measurement ladder. That profile fits an Am Nat theory contribution better than a broad empirical-synthesis claim.

The submission framing must emphasize biological theory and falsifiable measurement consequences, not software governance, repository integration, or bookkeeping.

## Closed pre-submission items

```text
THEORY_OWNERSHIP                         CLOSED
GENERAL_MARGIN Phi=R-K                  CLOSED
QUADRATIC_BRIDGE_SCOPE R=sL             CLOSED
JOURNAL_PROSE_CONVERSION                 CLOSED
REGISTERED_PRIOR_ART_COVERAGE           10/10 PASS
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
FINITE_FREQUENCY_ENDPOINT_BOUNDS         PASS
SAMPLING_PLUS_APPROXIMATION_INTERVAL     PASS
CONFLICT_DIFFERENTIATION_DISCORDANCE     PASS
GATE_LOCALIZATION_DIAGNOSTIC_UTA1_10      PASS
INTERVAL_COMPATIBLE_STATE_SET_UTA1_11      PASS
FIGURE_2_ECOLOGICAL_PANEL                PASS
FIGURE_1_THRESHOLD_ATLAS                 PASS
WITNESS_ARITHMETIC                       PASS
FIGURE_1_GENERALITY                      REPAIRED
CLAIM_PROVENANCE_OWNERSHIP               REPAIRED
AMNAT_TITLE_WORDS                         9 PASS
AMNAT_ABSTRACT_WORDS                    191 PASS
AMNAT_TEXT_WORDS_EXCL_LITERATURE       6098 PASS
AMNAT_FIGURES                             3 PASS
AMNAT_TABLES                              3 PASS
AMNAT_FIGURE_TABLE_TOTAL                  6 PASS
FULL_CI_PY311_PY312                      RECHECK_PENDING_PRIOR_ART
REVIEW_MANUSCRIPT_PDF                    REBUILD_PENDING_PRIOR_ART
ANONYMOUS_TITLE_PAGE_PDF                  1 PAGE PASS
DOUBLE_SPACING_LINE_PAGE_NUMBERS         PASS
ANONYMOUS_REVIEWER_BUNDLE                REBUILD_PENDING_PRIOR_ART
IDENTITY_SCAN                             RECHECK_PENDING_PRIOR_ART
CLAIM_VERIFIER_NE1_NE5_UTA1_11            PASS
FIXATION_OCCUPANCY_INVARIANT_GRID        PROCESS_DERIVED PASS
MORAN_PROCESS_CANONICAL_GRID              PASS
CANONICAL_MAPPING_GUARD                   PASS
NUMERICAL_TOLERANCE_POLICY                PASS
FIGURE_1_MANUAL_QA                       PASS
FIGURE_3_MANUAL_QA                       PASS
ANON_REVIEW_MORAN_TEST                  13/13 PASS
INV1_PROCESS_COMPARISONS                336 PASS
CANONICAL_MAPPING_GUARD                 PASS
UTA1_10_DIAGNOSTIC_TABLE_MANUAL_QA       PASS_PAGES_25_27_EXCLUSION_STATE
UTA1_11_INTERVAL_BOX_MANUAL_QA            PASS_PAGES_27_28_OUTER_SET_CAVEAT
FINAL_FULL_PAGE_PROOFREAD                 RECHECK_PENDING_PRIOR_ART
```

## Remaining submission actions

The current UTA1.10-UTA1.11 source plus submission tooling passes Python 3.11/3.12 CI (571/571), review-package build, rendered identity scan, executable claim verification, targeted QA of the diagnostic table and interval-box caveat, and full rendered page-by-page QA (34/34). The identity-bearing GitHub URL must not be placed in the anonymous manuscript; the generated reviewer bundle should instead be uploaded directly through the journal system or through an anonymous reviewer-accessible deposit.

Remaining actions are controlled outside the scientific package:

```text
AUTHOR_METADATA                       REQUIRED
AI_USE_DISCLOSURE                     REQUIRED_AUTHOR_APPROVAL
ALL_AUTHOR_APPROVAL                   REQUIRED
PORTAL_INPUT_VALIDATOR                READY
EDITORIAL_MANAGER_UPLOAD_KIT          READY
REVIEWER_BUNDLE_ACCESS_ROUTE          EDITORIAL_MANAGER_ZIP_READY
INITIAL_ARCHIVE_DEPOSIT               PAYLOAD_READY_AUTHENTICATED_DEPOSIT_PENDING
PORTAL_UPLOAD                         REQUIRED
PERMANENT_ARCHIVE_DOI                 METADATA_TEMPLATE_READY_DOI_PENDING
```

## Remaining scientific-editorial risk

The remaining reviewer question is:

> Does carrying one identified architecture comparison across familiar component theories generate enough biological leverage to justify the synthesis, once the component algebra is explicitly not claimed as new?

The submission answer must center on four deductions:

1. persistent integration is observationally non-identifying: `Phi<0`, a downhill local release gradient, and failure of rare establishment can produce the same macroscopic absence of differentiation;
2. because the upstream architecture comparison is held fixed, strict signs localize the first changed layer, while interval uncertainty yields the full compatible-state set; nested valid bounds can only remove candidates and therefore quantify what added precision resolves;
3. environmental threshold displacement and conflict–architecture discordance provide comparative settings in which these gate changes can be tested rather than inferred from phenotype alone;
4. separation is not universal: the registered process supplies a fixation–occupancy consistency surface, so an observed disagreement also has a diagnostic interpretation.

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
ANONYMOUS_REVIEW_FILES  = REBUILD_PENDING_PRIOR_ART
REVIEWER_CODE_PACKAGE   = REBUILD_PENDING_PRIOR_ART
EMPIRICAL_CLAIM_CEILING = THEORY_ONLY / NO_END_TO_END_G1_G9
INTERNAL_BLOCKERS       = CURRENT_REVIEW_PACKAGE_REBUILD
EXTERNAL_ACTIONS        = AUTHOR_INPUT + AUTHENTICATED_ZENODO_DRAFT + EDITORIAL_MANAGER_UPLOAD + APPROVAL + PUBLICATION_DOI
MAIN_OPEN_RISK          = UTA1_10_11_DIAGNOSTIC_BIOLOGICAL_PAYOFF
```
