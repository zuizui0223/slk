# SLK external submission action packet V1

## Current internal state

```text
SCIENTIFIC_MANUSCRIPT          READY
FULL_CI                       PASS
ANONYMOUS_REVIEW_BUILD        PASS
REVIEWER_DISTRIBUTION_ZIP     STALE_REBUILD_REQUIRED
EDITORIAL_MANAGER_UPLOAD_KIT  STALE_REBUILD_REQUIRED
ZENODO_PAYLOAD                STALE_REBUILD_REQUIRED
FINAL_PAGE_BY_PAGE_QA         REOPENED_AFTER_REFOCUS
INTERNAL_BLOCKERS             PACKAGE_REBUILD_AND_FINAL_VISUAL_QA
```

The manuscript was substantially reframed after the previous fixed submission ZIP was created. The old ZIP, its SHA256, the old convenience upload kit, and the old 35-page manual QA must not be treated as current.

## Internal actions before any external submission step

1. regenerate the deterministic anonymous reviewer ZIP from the biology-refocused source;
2. verify bundled tests, anonymity scan, and internal checksum manifest;
3. register the new source commit, ZIP SHA256, size, and file count;
4. rebuild the Editorial Manager convenience kit;
5. perform final page-by-page QA on the newly rendered manuscript;
6. only then proceed to Editorial Manager or Zenodo.

## Reviewer access and archive route

Editorial Manager ZIP remains the intended reviewer-access route, and Zenodo remains the intended archive provider. **Neither payload is currently frozen.** Do not upload the historical pre-refocus package.

## Author-controlled metadata

```text
AUTHOR_LIST_AND_ORDER        [REQUIRED]
AFFILIATIONS                  [REQUIRED]
EMAIL_EACH_AUTHOR             [REQUIRED]
CORRESPONDING_AUTHOR          [REQUIRED]
ORCID                         [OPTIONAL / WHERE SUPPLIED]
ACKNOWLEDGMENTS               [REQUIRED IF APPLICABLE]
AUTHOR_CONTRIBUTIONS          [REQUIRED]
PREPRINT_STATUS               [REQUIRED PORTAL RESPONSE]
DATA_SHARING_AGREEMENT        [REQUIRED PORTAL RESPONSE]
SUGGESTED_REVIEWERS           [AUTHOR CONTROLLED]
ASSOCIATE_EDITOR              [AUTHOR CONTROLLED]
ALL_AUTHOR_APPROVAL           [REQUIRED]
```

## AI disclosure — author approval gate

Candidate wording:

> Generative AI tools were used during development of this work to assist with scientific drafting and editing, mathematical and theoretical exploration, and code generation and troubleshooting. All claims, derivations, numerical checks, code, figures, references, and final prose remain the responsibility of the authors and were subject to author review and validation.

Before submission the authors must edit this sentence if needed so it exactly matches the actual workflow and approve its placement in the manuscript.

## Local Editorial Manager upload kit

Status: `REBUILD_REQUIRED_AFTER_MANUSCRIPT_REFOCUS`.

The historical kit receipt is retained for provenance but has `current_for_submission=false`. A replacement kit must be built only after the new reviewer ZIP is frozen.

## Current readiness receipt

The current unfilled portal template has been evaluated and frozen at:

```text
submission/AMNAT_PORTAL_READINESS_CURRENT_V1.json
status = BLOCKED
reviewer ZIP / upload kit / archive payload = REBUILD_REQUIRED
internal blocker = REBUILD_SUBMISSION_ARTIFACTS_AND_FINAL_VISUAL_QA
human/external missing fields = 13
```

The missing fields are author list, acknowledgments status, author contributions, AI-disclosure approval, preprint status, data-sharing agreement, reviewer-ZIP upload, initial archive deposit/reference, manuscript/title-page upload, Editorial Manager generated-PDF verification, and all-author approval.

No additional repository implementation is required to clear these fields.

## Minimal machine gate

Fill only:

```text
submission/AMNAT_PORTAL_INPUT_TEMPLATE_V1.json
```

Then run:

```bash
python scripts/check_amnat_portal_readiness.py submission/AMNAT_PORTAL_INPUT_TEMPLATE_V1.json
```

The template is intentionally fail-closed. It returns `READY_TO_SUBMIT` only after author metadata, AI-disclosure approval, reviewer ZIP upload, initial archive deposit, portal-file upload checks, data-sharing confirmation, and all-author approval are complete.

For the later publication archive gate:

```bash
python scripts/check_amnat_portal_readiness.py \
  submission/AMNAT_PORTAL_INPUT_TEMPLATE_V1.json \
  --phase publication
```

The publication phase additionally requires the permanent archive DOI and public-release readiness.

This validator is the final machine gate only; it does not create accounts, upload to Zenodo/Editorial Manager, choose reviewers, or approve author-controlled text.

## Final portal order

```text
1  choose archive provider and create initial private/non-public deposit
2  choose reviewer-access route (private link or EM ZIP)
3  prepare reviewer access package/link
4  approve AI disclosure
5  enter author metadata
6  enter acknowledgments + contributions in Author Comments
7  answer preprint/data-sharing fields
8  enter reviewer/AE suggestions if desired
9  upload anonymous manuscript + title page + reviewer data/code package
10 verify Editorial Manager-generated review PDF
11 obtain all-author approval and submit
12 before publication, finalize permanent DOI archive
```
