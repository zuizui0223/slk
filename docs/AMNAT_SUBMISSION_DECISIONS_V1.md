# SLK Am Nat submission decisions V1

## Purpose

Freeze the remaining scope decisions after theory ownership, journal-prose conversion, prior-art coverage, formula consistency, and current journal-format checks have been closed.

## Decision 1 — keep one explicit population-process exemplar

```text
ADD_SECOND_POPULATION_PROCESS_BEFORE_SUBMISSION = false
```

The fixation/occupancy results remain tied to the registered exponential Moran / connected symmetric rare-mutation process. Their role is not to claim universal population genetics. Their role is to demonstrate that transporting the same architecture-value object into a declared stochastic population process can create new separations and can also force an exact invariant.

Adding a second process before submission would broaden the paper without repairing the main reviewer risk, which is conceptual importance of the integrated transport rather than lack of another process example. Generality is therefore claimed through the upstream `Phi=R-K` architecture-value layer; the later fixation/occupancy formulas remain explicitly process specific.

Revisit only if review specifically demands process robustness.

## Decision 2 — do not manufacture a Pedicularis worked result

```text
ADD_PARTIAL_PEDICULARIS_WORKED_RESULT_TO_MAIN_TEXT = false
```

The Pedicularis G1-G5 programme is prospectively registered but has no completed biological G1-G5 receipt. It must therefore not be used as a worked empirical result merely to make the theory look more validated.

Figure 3 already provides the empirical measurement ladder. Pedicularis remains the first prospective application and can be cited as future execution/protocol material if needed, but the submission manuscript should keep the explicit statement that no single biological system has completed the full ladder.

A real partial worked example can be added only after an actual identified receipt exists and its claim ceiling is clear.

## Decision 3 — retain The American Naturalist as primary target

```text
PRIMARY_TARGET = The American Naturalist
ECOLOGY_LETTERS_REASSESSMENT = requires_real_same_system_G1_G5_receipt
```

The current paper is strongest as a conceptual/theoretical integration paper: an architecture-specific estimand transport, constructive split witnesses, one exact process-level invariant, and an empirical measurement ladder. That profile fits an Am Nat theory contribution better than a broad empirical-synthesis claim.

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
WITNESS_ARITHMETIC                       PASS
FIGURE_1_GENERALITY                      REPAIRED
CLAIM_PROVENANCE_OWNERSHIP               REPAIRED
AMNAT_TITLE_WORDS                         9 PASS
AMNAT_ABSTRACT_WORDS                    172 PASS
AMNAT_TEXT_WORDS_EXCL_LITERATURE       2941 PASS
AMNAT_FIGURES                             3 PASS
CI_TESTS                                163 PASS
```

## Remaining mechanical submission tasks

The current journal instructions still require a double-spaced review PDF with line and page numbers and a reviewer-accessible data/code package. Because double-anonymous review is required, the current identity-bearing GitHub URL should not be placed directly in the anonymous manuscript. See `docs/AMNAT_SUBMISSION_CHECKLIST_V1.md`.

## Remaining scientific-editorial risk

The remaining reviewer question is:

> Does the integrated transport generate enough biological insight to be more than a careful synthesis of known criteria?

The submission answer must center on three deductions:

1. the same upstream architecture comparison can change verdict as it is transported through later estimands;
2. the framework identifies exactly where a verdict must be re-tested and gives constructive witness regimes for those failures;
3. separation is not universal: the registered process forces reciprocal fixation ordering and weak-mutation occupancy ordering to re-align, showing that the framework predicts both splits and invariants.

## Submission state

```text
TARGET                 = THE_AMERICAN_NATURALIST
ARTICLE_TYPE           = MAJOR_ARTICLE
MANUSCRIPT             = SLK_MANUSCRIPT_AMNAT_V3.md
THEORY                  = READY
JOURNAL_PROSE           = READY_FOR_FINAL_TYPESETTING
PRIOR_ART_CORE          = READY
FORMULA_CONSISTENCY     = PASS
FORMAT_LIMITS           = PASS
EMPIRICAL_CLAIM_CEILING = THEORY_ONLY / NO_END_TO_END_G1_G9
MAIN_OPEN_RISK          = CONCEPTUAL_IMPORTANCE_FRAMING
```
