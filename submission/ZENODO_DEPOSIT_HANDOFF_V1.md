# Zenodo deposit handoff — SLK Am Nat V1

## Purpose

Prepare the archive-deposit step required by The American Naturalist without conflating it with reviewer access.

The reviewer-access route is already ready as an Editorial Manager ZIP:

```text
SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
SHA256 ee30f9a3f0982ef0a6d84b6900aa296c70135d0e6ff210f8bf0410267abdd08b
```

The same verified, cache-free deterministic ZIP is suitable as the file payload for a Zenodo draft. Zenodo recommends ZIP packaging for deposits with many files, and a software record can contain a single compressed source/reproducibility package.

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

Use exactly:

```text
file      SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
size      58,096 bytes
SHA256    ee30f9a3f0982ef0a6d84b6900aa296c70135d0e6ff210f8bf0410267abdd08b
files     17
tests     13 passed / 0 failed
identity  PASS
```

The exact package receipt is:

```text
submission/AMNAT_REVIEWER_ZIP_RECEIPT_V1.json
```

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
ZENODO_METADATA_TEMPLATE    ready
ZENODO_DRAFT_CREATED        false
ZENODO_FILE_UPLOADED        false
ZENODO_DOI_RESERVED         false
ZENODO_RECORD_PUBLISHED     false
```

The remaining actions require an authenticated Zenodo account and author-controlled metadata.
