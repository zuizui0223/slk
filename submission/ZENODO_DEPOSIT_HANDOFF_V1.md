# Zenodo deposit handoff — SLK Am Nat V1

## Purpose

Prepare the archive-deposit step required by *The American Naturalist* without conflating it with reviewer access.

## Current payload status — READY

The biology-refocused package has been rebuilt deterministically and verified.

```text
file      SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
size      59,927 bytes
SHA256    b0589f1d1b3fb1191d46bd42c375e2bb4e55f0d625fec26a605c12292e17ee8e
files     17
identity  PASS
source    5f6443189c13df6c83a8c7f78bac2c8223e632f2
```

This is the current payload for both reviewer-code access and a Zenodo draft. Do not substitute an older pre-refocus ZIP.

## Why draft first

Zenodo records begin as drafts. A draft can be saved and edited before publication. Publishing the record registers the DOI; a DOI may also be reserved before publication if desired.

For SLK:

```text
initial submission:
    create Zenodo draft
    upload verified ZIP
    enter author-controlled metadata
    save draft
    do not publish merely to provide reviewer access

review:
    give reviewers the Editorial Manager ZIP
    keep Zenodo draft editable

before publication:
    confirm final archive contents
    confirm creators / affiliations / license
    add related article metadata when available
    reserve/finalize DOI as appropriate
    publish permanent archive
```

## Upload payload

Use exactly the current deterministic reviewer/archive ZIP:

```text
file      SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
size      59,927 bytes
SHA256    b0589f1d1b3fb1191d46bd42c375e2bb4e55f0d625fec26a605c12292e17ee8e
files     17
identity  PASS
```

The exact package receipt is `submission/AMNAT_REVIEWER_ZIP_RECEIPT_V1.json`.

## Metadata template

Use:

```text
submission/ZENODO_DEPOSIT_METADATA_TEMPLATE_V1.json
```

Fields that must be supplied or approved by the authors:

- creator names and order;
- affiliations;
- ORCID identifiers where desired;
- license;
- publication date when the record is published;
- related article DOI after one exists;
- final decision on DOI reservation timing.

Do not invent these values from repository metadata.

## Recommended record type

```text
Resource type = Software
```

The archived object is chiefly executable theory/code and supporting reproducibility material. If the authors prefer another Zenodo resource type, change it before publication and keep the deposited file unchanged unless there is a scientific reason to regenerate the package.

## DOI

Zenodo registers a DOI when a draft is published. If the DOI must be known before publication, use Zenodo's DOI reservation function while the upload remains a draft.

Deleting a draft after reserving a DOI loses that reservation.

## Final archive verification

Immediately before publishing the Zenodo record:

1. download or inspect the draft file;
2. confirm its SHA256 equals the registered value above, unless a deliberately regenerated final package has been substituted;
3. if substituted, rerun the same test/anonymity/checksum workflow and register the new receipt in SLK;
4. confirm metadata and license with all authors;
5. publish the record and record the resulting DOI in the submission handoff.

## Current state

```text
ARCHIVE_PAYLOAD_READY       true
PACKAGE_REBUILD_REQUIRED    false
ZENODO_METADATA_TEMPLATE    ready
ZENODO_DRAFT_CREATED        false
ZENODO_FILE_UPLOADED        false
ZENODO_DOI_RESERVED         false
ZENODO_RECORD_PUBLISHED     false
```

The remaining Zenodo actions require an authenticated author account and author-controlled metadata.
