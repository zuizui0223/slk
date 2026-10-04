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
```

The refocused manuscript is now a biological theory paper about why documented conflict can remain multifunctional. Its central contribution is the inverse diagnosis of three causes—failure of net value, local reachability, or rare establishment—rather than the threshold atlas as an object in itself. That framing remains appropriate for *The American Naturalist*.

The submission framing must continue to emphasize biological theory and falsifiable measurement consequences, not software governance or repository architecture.

## Closed scientific items

```text
BIOLOGICAL_QUESTION_REFOCUS              PASS
THREE_CAUSE_PERSISTENCE_DIAGNOSIS        PASS
PEDICULARIS_RUNNING_EXAMPLE_BOUNDARY     PASS
PRIOR_ART_REPOSITIONING                  PASS
GENERAL_MARGIN Phi=R-K                   PASS
LOCAL_ACCESSIBILITY_SEPARATION            PASS
RARE_ESTABLISHMENT_SEPARATION             PASS
ECOLOGICAL_THRESHOLD_DISPLACEMENT         PASS
CONFLICT_DIFFERENTIATION_DISCORDANCE      PASS
DOWNSTREAM_FIXATION_OCCUPANCY_SCOPE       PASS
AMNAT_TITLE_WORDS                          7 PASS
AMNAT_ABSTRACT_WORDS                     168 PASS
AMNAT_TEXT_WORDS_EXCL_LITERATURE        5760 PASS
AMNAT_FIGURES                              3 PASS
AMNAT_TABLES                               3 PASS
AMNAT_FIGURE_TABLE_TOTAL                   6 PASS
FULL_CI                                   PASS
REFOCUSED_REVIEW_PACKAGE_BUILD            PASS
```

The mathematical theory files retain the fuller witness family and process results. Their presence no longer determines the manuscript's subject.

## Remaining submission actions

The biology-refocused source passes CI and the anonymous package build. The old frozen reviewer ZIP and upload kit do not.

```text
REVIEWER_BUNDLE_ACCESS_ROUTE          REBUILD_REQUIRED_AFTER_REFOCUS
EDITORIAL_MANAGER_UPLOAD_KIT          REBUILD_REQUIRED_AFTER_REFOCUS
INITIAL_ARCHIVE_PAYLOAD               REBUILD_REQUIRED_AFTER_REFOCUS
FINAL_RENDERED_PAGE_QA                REQUIRED_AFTER_REBUILD
AUTHOR_METADATA                       REQUIRED
AI_USE_DISCLOSURE                     REQUIRED_AUTHOR_APPROVAL
ALL_AUTHOR_APPROVAL                   REQUIRED
INITIAL_ARCHIVE_DEPOSIT               REQUIRED
PORTAL_UPLOAD                         REQUIRED
PERMANENT_ARCHIVE_DOI                 REQUIRED_FOR_PUBLICATION
```

The portal validator now refuses a reviewer package whose receipt is not both `EDITORIAL_MANAGER_ZIP_READY` and `current_for_submission=true`.

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
SCIENTIFIC_FRAMING      = BIOLOGY_FIRST_THREE_CAUSE_DIAGNOSIS
THEORY                  = READY
FORMAT_LIMITS           = PASS
FULL_CI                 = PASS
ANONYMOUS_PACKAGE_BUILD = PASS
FROZEN_REVIEWER_ZIP     = STALE_REBUILD_REQUIRED
EM_UPLOAD_KIT           = STALE_REBUILD_REQUIRED
ZENODO_PAYLOAD          = STALE_REBUILD_REQUIRED
FINAL_MANUAL_RENDER_QA  = REOPENED
INTERNAL_BLOCKERS       = REBUILD_AND_VERIFY_SUBMISSION_ARTIFACTS
```
