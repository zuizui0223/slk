# Zenodo deposit handoff — SLK Am Nat V1

## Purpose

Prepare the archive-deposit step required by *The American Naturalist* without conflating it with reviewer access.

## Current payload status — REBUILD REQUIRED

The previously frozen reviewer/archive ZIP was created before the manuscript was reframed around persistent multifunctionality. Its historical checksum remains in the stale receipt for provenance, but that ZIP is **not current for submission and must not be uploaded to Zenodo**.

Current required sequence:

```text
biology-refocused source
-> build anonymous reviewer bundle
-> regenerate deterministic distribution ZIP
-> run bundled tests + anonymity scan + checksum manifest
-> register new source commit / size / SHA256
-> only then create or update the Zenodo draft
```

The metadata template has already been updated to the new manuscript title and keywords, but its payload checksum is intentionally blank until the new ZIP is frozen.

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

No upload payload is currently frozen. Do not use the pre-refocus ZIP or its checksum.

After regeneration, record the new file, size, SHA256, file count, bundled test result, and identity scan in `submission/AMNAT_REVIEWER_ZIP_RECEIPT_V1.json`, then copy those values into the Zenodo metadata and handoff.

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
ARCHIVE_PAYLOAD_READY       false
PACKAGE_REBUILD_REQUIRED    true
ZENODO_METADATA_TEMPLATE    ready_without_payload_checksum
ZENODO_DRAFT_CREATED        false
ZENODO_FILE_UPLOADED        false
ZENODO_DOI_RESERVED         false
ZENODO_RECORD_PUBLISHED     false
```

The next internal action is package regeneration and verification. Authenticated Zenodo actions remain author-controlled.
