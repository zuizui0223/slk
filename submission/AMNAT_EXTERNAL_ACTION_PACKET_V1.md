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
4. **Also complete the archive deposit at initial submission**; the ZIP route replaces only the reviewer-access link, not the archive-deposit requirement.

## Route decision 2 — archive deposit and publication DOI

Prepare a curated repository deposit containing only final necessary data/code/theory materials plus a comprehensive README. The archive deposit is required at initial submission but may remain private/non-public for peer review.

For publication, finalize the archive in a curated permanent repository and obtain a DOI. For code maintained on GitHub, the journal recommends a permanent DOI deposit such as Zenodo.

```text
ARCHIVE_PROVIDER           = [AUTHOR CHOICE]
ARCHIVE_DEPOSIT_CREATED    = false
REVIEW_PRIVATE_ACCESS      = [PENDING]
PERMANENT_ARCHIVE_DOI      = [PENDING]
PUBLICATION_READY          = false until DOI/archive gate closes
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
