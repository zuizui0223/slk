# The American Naturalist policy audit — 2026-09-28

This receipt records the submission-policy interpretation used by the SLK portal handoff. It does not change any scientific claim.

## Official source checked

The American Naturalist — Instructions for Authors, checked 2026-09-28.

## Double-anonymous review

For article submissions, author names, affiliations and email addresses belong in Editorial Manager rather than in the review manuscript. Acknowledgments and the Author Contribution Statement belong in the Editorial Manager Comments field during initial double-anonymous review.

The current SLK anonymous manuscript/reviewer bundle already enforces the identity-removal requirements.

## Reviewer access to data/code

The submission instructions state that reviewers and editors must be able to access the data/code package at first submission and explicitly give two routes:

```text
A  private/anonymized repository link
OR
B  ZIP file uploaded directly to Editorial Manager
```

Therefore an external anonymous URL is not the only valid reviewer-access route.

## Permanent archiving

The journal separately requires data/code archiving. Its instructions state that complete deposition in a public data archive is required at the time of initial submission, although the deposit may remain private/non-public for peer review. The permanent DOI is a publication-stage requirement and must be in place before production/publication.

For GitHub-hosted code, the journal recommends depositing the final necessary code on Zenodo to obtain a permanent DOI.

Thus the SLK submission workflow should distinguish:

```text
reviewer access route
!=
archive-deposit requirement
!=
final DOI/publication state
```

A direct Editorial Manager ZIP can satisfy reviewer access, but it does not remove the initial-submission archive-deposit requirement. The DOI can be finalized later for publication.

## Generative AI

The journal allows generative AI for readability, drafting and code troubleshooting under human oversight. It requires transparent description when AI is used to generate scientific content such as analysis or figures.

For SLK, AI use was broader than language polishing and included scientific drafting/theoretical exploration and code generation/troubleshooting. The submission therefore requires an author-approved disclosure that accurately describes the actual workflow.

## Submission consequence

```text
REVIEWER_ACCESS_ROUTE          = PRIVATE_LINK_OR_EM_ZIP
ARCHIVE_DEPOSIT                 = REQUIRED_AT_INITIAL_SUBMISSION
PERMANENT_ARCHIVE_DOI          = REQUIRED_FOR_PUBLICATION
AI_DISCLOSURE                  = REQUIRED_AUTHOR_APPROVAL
COVER_LETTER                   = NOT_EXPECTED
DOUBLE_ANONYMOUS_REVIEW        = REQUIRED
```

This policy receipt should be rechecked if the journal changes its Instructions for Authors before actual portal submission.
