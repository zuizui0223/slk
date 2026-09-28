# SLK external submission action packet V1

## Current internal state

```text
SCIENTIFIC_PACKAGE         READY
FULL_CI                    PASS
ANONYMOUS_REVIEW_MANUSCRIPT READY
REVIEWER_CODE_THEORY_BUNDLE READY
FULL_PAGE_QA               PASS_34_34
INTERNAL_BLOCKERS          NONE
```

## Route decision 1 — reviewer data/code access

Choose exactly one reviewer-access route for initial submission.

### Route A — private/anonymized repository link

1. Upload the exact curated reviewer bundle from the current main build to a repository that supports private/anonymized reviewer access.
2. Confirm the link does not expose author names, repository history or identity-bearing URLs.
3. Insert the private reviewer URL into the review-access statement.
4. Enter the data location in Editorial Manager.

### Route B — Editorial Manager ZIP

The upload-ready package is already frozen and verified:

```text
file                    SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
SHA256                  ee30f9a3f0982ef0a6d84b6900aa296c70135d0e6ff210f8bf0410267abdd08b
size                    58,096 bytes
files                   23
bundled tests           13 passed / 0 failed
cache/bytecode files    0
anonymity scan          PASS
checksum manifest       PASS
receipt                 submission/AMNAT_REVIEWER_ZIP_RECEIPT_V1.json
```

1. Upload this exact ZIP directly to Editorial Manager as the reviewer-access data/code package.
2. Do not create or insert an identity-bearing public URL merely to satisfy a link field.
3. In Editorial Manager, identify the uploaded package as the reviewer-access location if the form permits.
4. **Also complete the archive deposit at initial submission**; the ZIP route replaces only the reviewer-access link, not the archive-deposit requirement.

## Route decision 2 — archive deposit and publication DOI

A provider-neutral verified payload is ready, and a Zenodo handoff is registered:

```text
payload                   SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
SHA256                    ee30f9a3f0982ef0a6d84b6900aa296c70135d0e6ff210f8bf0410267abdd08b
Zenodo handoff             submission/ZENODO_DEPOSIT_HANDOFF_V1.md
metadata template          submission/ZENODO_DEPOSIT_METADATA_TEMPLATE_V1.json
```

The archive deposit is required at initial submission but may remain private/non-public for peer review. The recommended default for this code/theory package is a Zenodo **draft** using the verified ZIP. Reviewer access can remain the separate Editorial Manager ZIP route.

For publication, finalize the archive in a curated permanent repository and obtain a DOI.

```text
ARCHIVE_PROVIDER           = ZENODO_RECOMMENDED / AUTHOR CONFIRMATION
ARCHIVE_PAYLOAD_READY      = true
ARCHIVE_METADATA_TEMPLATE  = ready
ARCHIVE_DEPOSIT_CREATED    = false
PERMANENT_ARCHIVE_DOI      = [PENDING]
PUBLICATION_READY          = false until DOI/archive gate closes
```

## Editor / reviewer candidate research

A current, unranked candidate shortlist is available at:

```text
submission/AMNAT_EDITOR_REVIEWER_CANDIDATES_V1.md
```

It contains 3 current Am Nat associate-editor candidates and 5 outside reviewer candidates selected from current public research profiles. **Do not copy them into Editorial Manager until the authors complete the journal conflict checks**, especially recent collaboration and same-institution screening.

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

A convenience ZIP containing the validated upload files is prepared locally:

```text
file       SLK_AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT.zip
SHA256     3a0cc0fef7843fef7086602b63f4be5de7f243667d42bfb9fb3d731407217cd0
size       1,607,305 bytes
files      8
receipt    submission/AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT_RECEIPT_V1.json
```

It contains the anonymous manuscript DOCX/PDF, anonymous title-page DOCX/PDF, the verified reviewer data/code ZIP, the build QA receipt, an internal checksum manifest, and a short portal-upload README.

The convenience ZIP itself is not a journal submission format: unzip it locally, then upload the appropriate constituent files separately in Editorial Manager.

## Current readiness receipt

The current unfilled portal template has been evaluated and frozen at:

```text
submission/AMNAT_PORTAL_READINESS_CURRENT_V1.json
status = BLOCKED
machine assets = READY
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
