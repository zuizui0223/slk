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
- Reviewer-accessible data/code archive URL: [REQUIRED BEFORE SUBMISSION]

## Data/code archive gate — required at first submission

The American Naturalist requires the data and/or code needed to recreate the results to be deposited in a public data repository and made accessible to reviewers and editors at first submission. The deposit may remain non-public during review, but the manuscript must contain a reviewer-accessible link.

For SLK the deposited object should be the exact curated anonymous review bundle, not the identity-bearing GitHub repository. The deposit must preserve the existing anonymity audit:

```text
repository_history_included = false
repository_remote_url_included = false
author_metadata_included = false
```

Before upload, replace the token below with the reviewer-accessible repository URL and insert the resulting sentence into the anonymous manuscript in a short Data and code availability section:

> The code and theory materials needed to reproduce the registered witness regimes, ecological threshold-displacement predictions, frequency-response diagnostics, and fixation–occupancy verification are available to reviewers at [ANONYMOUS_REVIEW_ARCHIVE_URL].

Do not insert the public identity-bearing repository URL into the double-anonymous manuscript.

## Author Comments field

Do not upload a conventional cover letter unless the journal office specifically requests one. Put only necessary submission information into Author Comments.

### Acknowledgments

[AUTHOR-CONTROLLED TEXT]

### Author contributions

[AUTHOR-CONTROLLED TEXT]

### Optional editorial note

Use only if needed. The journal states that cover letters are not expected and that some editors do not consider promotional fit statements.

## Generative-AI transparency gate

The journal permits generative AI for readability, drafting and code troubleshooting with human oversight, but use that generated scientific content must be described transparently in the manuscript where needed for repeatability. Before submission, the authors must approve an exact disclosure matching the actual use.

Suggested starting text, to be edited for factual accuracy:

> Generative AI tools were used during manuscript development to assist with drafting, editing, and code troubleshooting. All mathematical arguments, numerical checks, code, figures, references, and final prose were reviewed and validated by the authors, who take full responsibility for the submitted content.

Do not mark this gate complete until the wording accurately reflects actual use and is placed in the journal-appropriate location.

## Upload set

- anonymous review manuscript PDF/DOCX generated from the canonical source;
- anonymous title page;
- exact anonymous reviewer data/code deposit link in the manuscript;
- any journal-required source files;
- author metadata in Editorial Manager only.

## Final gate

```text
SCIENTIFIC_PACKAGE = READY
DOUBLE_ANONYMITY = READY
COVER_LETTER = NOT_REQUIRED
ANONYMOUS_DATA_CODE_DEPOSIT = REQUIRED_EXTERNAL_ACTION
AUTHOR_METADATA = REQUIRED_EXTERNAL_ACTION
ACKNOWLEDGMENTS_AND_CONTRIBUTIONS = REQUIRED_EXTERNAL_ACTION
REVIEWER_AND_AE_FIELDS = AUTHOR_CONTROLLED
AI_DISCLOSURE = AUTHOR_APPROVAL_REQUIRED
ALL_AUTHOR_APPROVAL = REQUIRED_EXTERNAL_ACTION
PORTAL_UPLOAD = REQUIRED_EXTERNAL_ACTION
```
