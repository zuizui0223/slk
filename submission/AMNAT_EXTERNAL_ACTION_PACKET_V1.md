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

1. Upload the exact curated reviewer bundle directly to Editorial Manager as the reviewer-access data/code package.
2. Do not create or insert an identity-bearing public URL merely to satisfy a link field.
3. In Editorial Manager, identify the uploaded package as the reviewer-access location if the form permits.
4. Keep the permanent DOI archive as a separate publication requirement.

## Route decision 2 — permanent archive

Prepare a curated permanent repository deposit containing only final necessary data/code/theory materials plus a comprehensive README.

For code maintained on GitHub, the journal recommends a permanent DOI deposit such as Zenodo.

```text
PERMANENT_ARCHIVE_PROVIDER  = [AUTHOR CHOICE]
PERMANENT_ARCHIVE_DOI       = [PENDING]
PUBLICATION_READY           = false until DOI/archive gate closes
```

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

## Final portal order

```text
1  choose reviewer-access route
2  prepare reviewer access package/link
3  approve AI disclosure
4  enter author metadata
5  enter acknowledgments + contributions in Author Comments
6  answer preprint/data-sharing fields
7  enter reviewer/AE suggestions if desired
8  upload anonymous manuscript + title page + reviewer data/code package
9  verify Editorial Manager-generated review PDF
10 obtain all-author approval and submit
```
