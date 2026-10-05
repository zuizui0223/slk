# SLK external submission action packet V1

## Current internal state

```text
SCIENTIFIC_MANUSCRIPT          READY
FULL_CI                       PASS
ANONYMOUS_REVIEW_BUILD        PASS
REVIEWER_DISTRIBUTION_ZIP     READY_CURRENT
EDITORIAL_MANAGER_UPLOAD_KIT  READY_CURRENT
ZENODO_PAYLOAD                READY_CURRENT
RENDERED_LAYOUT_QA            PASS_28_28
KEY_FIGURES_FULL_SIZE_QA      PASS
INTERNAL_BLOCKERS             NONE
```

Current frozen artifacts:

```text
reviewer ZIP
  file    SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
  size    59,927 bytes
  SHA256  b0589f1d1b3fb1191d46bd42c375e2bb4e55f0d625fec26a605c12292e17ee8e

Editorial Manager convenience kit
  file    SLK_AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT.zip
  size    1,527,268 bytes
  SHA256  3b8bb9f80c35c998de2eb2a08a039acdbf4188f35d24e6c0adff2caeb678de1c

source commit  5f6443189c13df6c83a8c7f78bac2c8223e632f2
workflow run   37211106188
artifact       11306233624
```

The current review manuscript is 28 pages. All pages were inspected for layout at overview scale, with Figures 1-3 and their surrounding pages inspected at full size. No clipping, overlap, broken glyphs, or identity-bearing text was found.

## Reviewer access and archive route

Editorial Manager ZIP remains the reviewer-access route, and the same verified anonymous reviewer ZIP is the current Zenodo draft payload. The Zenodo draft itself still requires an authenticated author action.

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

Status: `READY_CURRENT`.

Use the current deterministic kit SHA256 `3b8bb9f80c35c998de2eb2a08a039acdbf4188f35d24e6c0adff2caeb678de1c`. The outer convenience ZIP should be unpacked locally; upload its constituent files separately in Editorial Manager.

## Current readiness receipt

The current unfilled portal template has been evaluated and frozen at:

```text
submission/AMNAT_PORTAL_READINESS_CURRENT_V1.json
status = BLOCKED
machine assets = CURRENT
internal blockers = NONE
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
