# SLK Am Nat submission decisions V1

## Purpose

Freeze the remaining scope decisions after theory ownership, journal-prose conversion, prior-art coverage, formula consistency, review-file generation, anonymous reviewer packaging, and visual QA have been closed.

## Decision 1 — keep fixation and occupancy out of the biological main line

```text
FIXATION_OCCUPANCY_ROLE = SUPPORTING_THEORY_ONLY
```

The paper now ends its biological explanation at rare establishment. Finite-population fixation and weak-mutation occupancy remain mathematically valid downstream results, but they are not additional causes of persistent multifunctionality and should not compete with the ecology in the main narrative.

Revisit only if review specifically asks for downstream population-process consequences.

## Decision 2 — do not manufacture a Pedicularis worked result

```text
ADD_PARTIAL_PEDICULARIS_WORKED_RESULT_TO_MAIN_TEXT = false
```

The Pedicularis G1-G5 programme is prospectively registered but has no completed biological G1-G5 receipt. It must therefore not be used as a worked empirical result merely to make the theory look more validated.

Pedicularis is now used as a literature-based natural system: opposing pollinator and seed-predator selection, geographic variation in antagonism, and predator-driven density dependence establish the ecological problem without manufacturing a new empirical SLK result.

A real partial worked example can be added only after an actual identified receipt exists and its claim ceiling is clear.

## Decision 3 — retain The American Naturalist as primary target

```text
PRIMARY_TARGET = The American Naturalist
```

The refocused manuscript is now an evolutionary-ecology paper about why comparable functional conflicts have different resolutions in nature. Its central contribution is the three-state account of persistent integration—adaptive integration, historical/developmental trapping, and ecological stabilization—and the prediction that those selective states can turn over across environments before morphology changes. That framing remains appropriate for *The American Naturalist*.

## Closed scientific items

```text
BIOLOGICAL_QUESTION_REFOCUS              PASS
HIDDEN_BOTTLENECK_TURNOVER_THEORY       PASS
PEDICULARIS_RUNNING_EXAMPLE_BOUNDARY     PASS
PRIOR_ART_REPOSITIONING                  PASS
GENERAL_MARGIN Phi=R-K                   PASS
LOCAL_ACCESSIBILITY_SEPARATION            PASS
RARE_ESTABLISHMENT_SEPARATION             PASS
ECOLOGICAL_THRESHOLD_DISPLACEMENT         PASS
CONFLICT_DIFFERENTIATION_DISCORDANCE      PASS
DOWNSTREAM_FIXATION_OCCUPANCY_SCOPE       PASS
AMNAT_TITLE_WORDS                          7 PASS
AMNAT_ABSTRACT_WORDS                     187 PASS
AMNAT_TEXT_WORDS_EXCL_LITERATURE        7063 PASS
AMNAT_FIGURES                              3 PASS
AMNAT_TABLES                               0 PASS
AMNAT_FIGURE_TABLE_TOTAL                   3 PASS
FULL_CI                                   REBUILD_PENDING_LATEST_SOURCE
REFOCUSED_REVIEW_PACKAGE_BUILD            REBUILD_PENDING_LATEST_SOURCE
```

The mathematical theory files retain the fuller witness family and process results. Their presence no longer determines the manuscript's subject.

## Remaining submission actions

The ecology-first source passes CI, the anonymous package build, deterministic packaging, and rendered-layout QA. The remaining actions are external or author controlled.

```text
REVIEWER_BUNDLE_ACCESS_ROUTE          REBUILD_PENDING_LATEST_SOURCE
EDITORIAL_MANAGER_UPLOAD_KIT          REBUILD_PENDING_LATEST_SOURCE
INITIAL_ARCHIVE_PAYLOAD               REBUILD_PENDING_LATEST_SOURCE
RENDERED_LAYOUT_QA                    REBUILD_PENDING_LATEST_SOURCE
AUTHOR_METADATA                       REQUIRED
AI_USE_DISCLOSURE                     REQUIRED_AUTHOR_APPROVAL
ALL_AUTHOR_APPROVAL                   REQUIRED
INITIAL_ARCHIVE_DEPOSIT               REQUIRED
PORTAL_UPLOAD                         REQUIRED
PERMANENT_ARCHIVE_DOI                 REQUIRED_FOR_PUBLICATION
```

The portal validator now refuses a reviewer package whose receipt is not both `EDITORIAL_MANAGER_ZIP_READY` and `current_for_submission=true`.

## Remaining scientific-editorial risk

The remaining reviewer question is biological:

> Does the hidden turnover of evolutionary bottlenecks behind one unchanged phenotype explain something beyond established specialization theory, known hysteresis, and the general fact that ecology shapes integration?

The submission answer is now four concrete predictions:

1. **One unchanged phenotype can hide turnover in the limiting evolutionary process.** Across environments, persistence can shift from architecture economics, to path limitation, to ecological establishment before morphology changes.
2. **Phenotypic stasis can hide declining evolutionary resistance.** Before morphology changes, the minimum favorable structural release and/or the critical local frequency required for a divided architecture to spread can shrink toward zero.
3. **Conflict strength does not rank organization.** Stronger functional conflict can remain integrated when little conflict is recoverable or division of labor is costly.
4. **Different bottlenecks predict different natural histories.** Path limitation predicts environmental lag and architecture legacy; positive frequency dependence predicts priority-dependent alternative patches; negative frequency dependence predicts mixed zones; weak feedback permits more direct replacement.

Hysteresis, bistability, coexistence, valley crossing, and frequency dependence are prior art. The residual contribution is their ordered placement within one multifunctional-to-divided architecture problem and the resulting prediction that the selective meaning and fragility of an unchanged integrated phenotype can turn over before visible reorganization.

## Submission state

```text
TARGET                  = THE_AMERICAN_NATURALIST
ARTICLE_TYPE            = MAJOR_ARTICLE
MANUSCRIPT              = SLK_MANUSCRIPT_AMNAT_V4.md
SCIENTIFIC_FRAMING      = ECOLOGICAL_RESOLUTIONS_THREE_STATE_THEORY
THEORY                  = READY
FORMAT_LIMITS           = PASS
FULL_CI                 = PASS
ANONYMOUS_PACKAGE_BUILD = PASS
FROZEN_REVIEWER_ZIP     = STALE_AFTER_LATEST_SOURCE_EDIT
EM_UPLOAD_KIT           = STALE_AFTER_LATEST_SOURCE_EDIT
ZENODO_PAYLOAD          = STALE_AFTER_LATEST_SOURCE_EDIT
RENDERED_LAYOUT_QA      = REBUILD_PENDING
INTERNAL_BLOCKERS       = REBUILD_LATEST_SOURCE_PACKAGE
```
