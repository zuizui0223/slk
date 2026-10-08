# The American Naturalist portal handoff — SLK

This file is the submission-layer contract for the journal-facing manuscript. It does not change the scientific claims.

## Frozen submission target

```text
JOURNAL = The American Naturalist
ARTICLE_TYPE = Major Article
MANUSCRIPT = manuscript/SLK_MANUSCRIPT_AMNAT_V4.md
ANONYMOUS_TITLE_PAGE = manuscript/AMNAT_TITLE_PAGE_V1.md
COVER_LETTER = NOT_EXPECTED
```

The journal evaluates initial submissions under double-anonymous review. Author names, affiliations and email addresses belong in Editorial Manager, not in the manuscript or reviewer package. Acknowledgments and the author-contribution statement belong in the Editorial Manager Author Comments field at initial submission.

## Portal fields that require human input

### Author metadata

- author list and order;
- affiliations;
- email address for every author;
- corresponding author;
- ORCID(s), where supplied;
- all-author approval of the exact submitted version.

### Suggested reviewers

The journal encourages reviewer suggestions. Do not infer names from citations or repository history. For every suggested reviewer, confirm no conflict of interest, including no collaboration with any author during the previous 48 months and no employment at the same institution.

| Name | Institution | Email | Expertise | Conflict check |
|---|---|---|---|---|
|  |  |  |  |  |

### Associate-editor suggestion

- Suggested associate editor: [AUTHOR-CONTROLLED]
- Reason for fit: [AUTHOR-CONTROLLED]

### Additional-information fields

- Preprint status: [YES/NO + repository if applicable]
- Agreement with journal data-sharing policy: [AUTHOR CONFIRMATION]
- Reviewer-access route: [PRIVATE/ANONYMIZED REPOSITORY LINK OR EDITORIAL MANAGER ZIP]
- Initial archive deposit: [REQUIRED AT SUBMISSION; MAY REMAIN PRIVATE FOR REVIEW]
- Permanent archive/DOI plan: [REQUIRED FOR PUBLICATION]

## Data/code access and archiving — two separate gates

The American Naturalist requires the data/code needed to recreate results to be available to reviewers and editors at first submission. Its current submission instructions explicitly allow either:

```text
A  reviewer-accessible private/anonymized repository link
OR
B  a ZIP file uploaded directly to Editorial Manager
```

The reviewer-access route is therefore **not** restricted to an anonymous external URL.

Separately, the journal's archiving policy requires the data/code package to be deposited in a public data archive at initial submission, although the deposit may remain non-public/private-for-review during peer review. For publication, the repository must be curated, permanent and freely accessible, and the dataset/code archive must have a DOI. If code is hosted on GitHub, the journal specifically recommends depositing the final necessary code on Zenodo to obtain a permanent DOI.

For SLK, the reviewer package should be the exact curated anonymous review bundle, not the identity-bearing GitHub repository. Whether supplied through a private repository link or Editorial Manager ZIP, it must preserve:

```text
repository_history_included = false
repository_remote_url_included = false
author_metadata_included = false
```

### Route A — private/anonymized repository

Insert a reviewer-access statement using the private/anonymized URL, for example:

> The code and theory materials needed to reproduce the registered witness regimes, ecological threshold-displacement predictions, arbitrary-shape endpoint invasion, finite-frequency endpoint certification, frequency-response diagnostics, and fixation–occupancy verification are available to reviewers at [ANONYMOUS_REVIEW_ARCHIVE_URL].

### Route B — Editorial Manager ZIP

Upload the exact curated reviewer bundle as the reviewer-accessible ZIP in Editorial Manager. Do not invent or insert a public identity-bearing URL merely to create a link. This route changes only reviewer access: create the required archive deposit separately at initial submission, then finalize its DOI/public state for publication.

The identity-bearing GitHub repository URL must not be inserted into the double-anonymous review manuscript.

## Author Comments field

Do not upload a conventional cover letter unless the journal office specifically requests one. Put only necessary submission information into Author Comments.

### Acknowledgments

[AUTHOR-CONTROLLED TEXT]

### Author contributions

[AUTHOR-CONTROLLED TEXT]

### Optional editorial note

Use only if needed. The journal states that cover letters are not expected and that some editors do not consider promotional fit statements.

## Generative-AI transparency gate

The journal permits generative AI for readability, drafting, and code troubleshooting with human oversight. It further requires AI use that generated scientific content such as analysis or figures to be described transparently in the Methods to support repeatability.

For SLK, generative AI was used beyond language polishing: it assisted scientific drafting, mathematical/theoretical development, code generation/troubleshooting, and repository/reproducibility work. The submission should therefore carry an explicit author-approved disclosure rather than treating disclosure as optional.

Conservative starting text, to be edited and approved by the authors for factual accuracy:

> Generative AI tools were used during development of this work to assist with scientific drafting and editing, mathematical and theoretical exploration, and code generation and troubleshooting. All claims, derivations, numerical checks, code, figures, references, and final prose remain the responsibility of the authors and were subject to author review and validation.

The exact placement should follow the journal's current instruction that scientific-content-generating AI use be described transparently in the Methods. Do not mark this gate complete until the authors approve the wording and confirm that it accurately describes the actual workflow.

## Upload set

- anonymous review manuscript PDF/DOCX generated from the canonical source;
- anonymous title page;
- reviewer-access data/code package: `SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip`, current SHA256 `b0589f1d1b3fb1191d46bd42c375e2bb4e55f0d625fec26a605c12292e17ee8e`;
- initial private/non-public archive deposit in a curated repository;
- permanent archive DOI/publication plan;
- any journal-required source files;
- author metadata in Editorial Manager only.

## Final gate

```text
SCIENTIFIC_MANUSCRIPT = READY
AUTOMATED_REVIEW_BUILD = PASS
DOUBLE_ANONYMITY_SOURCE_CHECK = PASS
RENDERED_LAYOUT_QA = PASS_28_28
COVER_LETTER = NOT_REQUIRED
REVIEWER_DATA_CODE_ACCESS = EDITORIAL_MANAGER_ZIP_READY
EDITORIAL_MANAGER_UPLOAD_KIT = READY_CURRENT
ZENODO_ARCHIVE_PAYLOAD = READY_CURRENT
AUTHOR_METADATA = REQUIRED_EXTERNAL_ACTION
ACKNOWLEDGMENTS_AND_CONTRIBUTIONS = REQUIRED_EXTERNAL_ACTION
AI_DISCLOSURE = REQUIRED_AUTHOR_APPROVAL
INITIAL_ARCHIVE_DEPOSIT = REQUIRED_EXTERNAL_ACTION
ALL_AUTHOR_APPROVAL = REQUIRED_EXTERNAL_ACTION
PORTAL_UPLOAD = REQUIRED_EXTERNAL_ACTION
```

The reviewer ZIP and upload kit are current. The portal readiness validator remains fail-closed until the human-controlled fields and upload steps are completed.
