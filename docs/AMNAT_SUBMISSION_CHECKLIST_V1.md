# SLK — The American Naturalist submission checklist V1

## Current submission surface

```text
MANUSCRIPT = manuscript/SLK_MANUSCRIPT_AMNAT_V4.md
TITLE_PAGE = manuscript/AMNAT_TITLE_PAGE_V1.md
ARTICLE_TYPE = Major Article
PORTAL_HANDOFF = submission/AMNAT_PORTAL_HANDOFF_V1.md
```

Automated count from `scripts/check_amnat_manuscript.py`:

```text
TITLE_WORDS                         9
ABSTRACT_WORDS                    191
TEXT_WORDS_EXCL_LITERATURE_CITED 5833
FIGURES                             3
```

## Current journal-limit checks

The current The American Naturalist author instructions specify that Major Articles should usually be no more than 7,500 words excluding Literature Cited, with no more than six figures and/or tables; abstracts are limited to 200 words. The title page should include article type, four to six keywords, text word count, and a list of manuscript elements. Initial submissions require double spacing, line numbers, page numbers, author/date citations, and double-anonymous review formatting.

Status:

```text
MAJOR_ARTICLE_TEXT_LIMIT        PASS
ABSTRACT_200_WORD_LIMIT         PASS
FIGURE_TABLE_LIMIT              PASS   (3 figures + 3 in-text tables = 6 items)
TITLE_LENGTH_PREFERENCE         PASS   (9 words; journal suggests ~8–10)
KEYWORDS_1_TO_6                 PASS   (6)
ANONYMOUS_TITLE_PAGE            PASS
AUTHORS_REMOVED_FROM_MANUSCRIPT PASS
```

## Submission package state

### 1. Anonymous review manuscript — REBUILD PENDING AFTER UTA1.10

The CI-built review manuscript is generated directly from the canonical V4 source. The last completed package predates the UTA1.10 diagnostic-table revision. A fresh build is required before the generated-file status can be promoted back to PASS.

```text
CURRENT_SOURCE_TEXT_WORDS   5833
CURRENT_SOURCE_TABLES        3
CURRENT_SOURCE_FIGURES       3
REVIEW_PDF_REBUILD           PENDING
ANONYMOUS_TITLE_REBUILD      PENDING
STRUCTURE_ANONYMITY_RECHECK  PENDING
UTA1_10_RECEIPT_RECHECK      PENDING
FULL_PAGE_BY_PAGE_PROOFREAD  OPEN
```

The previously generated review PDF was inspected before the UTA1.10 revision. Because the source now contains a third table and revised abstract/discussion, the current generated package must be rebuilt and rechecked before portal upload.

Status: `REBUILD PENDING — DO NOT USE THE PRE-UTA1.10 REVIEW PACKAGE`.

### 2. Anonymous reviewer code/theory package — REBUILD PENDING, DEPOSIT STILL REQUIRED

The review bundle is curated rather than being a repository dump. It contains:

- the exact anonymous manuscript and title-page sources;
- `theory/SLK_CORE_THEORY_V1.md`;
- `theory/UNIFIED_THRESHOLD_ATLAS_V1.md`;
- `theory/NON_EQUIVALENCE_THEOREM_V1.md`;
- the three submitted SVG figure sources;
- `code/verify_amnat_claims.py`;
- a precomputed `CLAIM_VERIFICATION_RECEIPT.json`;
- `ANONYMITY_AUDIT.txt`;
- `SHA256SUMS.txt`.

The verifier recomputes the common convex recovery family, all five registered witness regimes, the critical surfaces, and the fixation–occupancy invariant. The invariant grid contains 112 comparisons with maximum absolute error 0.0. The bundle identity scan passes and excludes repository history, remote URLs, and author metadata.

Current journal instructions require data/code needed to recreate results to be deposited in a public data repository and made reviewer-accessible at first submission. The deposit can remain non-public during review, but a reviewer-accessible link must be included in the manuscript. Therefore direct portal upload of the bundle alone is not treated as sufficient unless the journal office explicitly confirms otherwise.

The identity-bearing GitHub repository URL must not be inserted into the anonymous manuscript. Deposit the exact curated anonymous bundle in a repository that supports anonymous/reviewer access and insert that link in the anonymous manuscript.

Status: `REBUILD CURRENT UTA1.10 BUNDLE, THEN ANONYMOUS_REVIEW_ARCHIVE_URL remains an external submission blocker`.

### 3. Author metadata outside the anonymous manuscript

Author names, affiliations, emails, ORCIDs, acknowledgments, and author-contribution statements should remain outside the anonymous review manuscript. Names/affiliations/emails belong in Editorial Manager; acknowledgments and author contributions belong in the Author Comments field for initial double-anonymous review.

Status: `READY FOR USER-SUPPLIED AUTHOR METADATA`.

### 4. Cover letter / Author Comments — JOURNAL-SPECIFIC ROUTE LOCKED

The current journal instructions state that cover letters are not expected and may be removed. If a message is necessary, it should be entered in the Author Comments field. Do not spend submission effort on a conventional promotional cover letter.

Author Comments must carry the acknowledgments and author-contribution statement because these are removed from the anonymous manuscript.

Status: `PORTAL ROUTE DEFINED — HUMAN TEXT REQUIRED`.

### 5. AI-use transparency

Current instructions permit generative AI for readability, drafting and code troubleshooting under human oversight. Use that generates scientific content, analysis, figures, or other repeatability-relevant material must be described transparently in the manuscript. The exact disclosure must match actual use and be approved by the authors.

A non-authoritative starting template is registered in `submission/AMNAT_PORTAL_HANDOFF_V1.md`.

Status: `AUTHOR-APPROVED DISCLOSURE REQUIRED BEFORE SUBMISSION`.

### 6. Reviewer / editor / additional-information fields

The live submission flow asks for reviewer suggestions and additional information including preprint status, data location/data-sharing compliance, and a potentially suitable associate editor. Reviewer identities must not be inferred from citations or repository history. The journal flags recent collaboration (previous 48 months) and same-institution employment as conflicts.

Status: `AUTHOR-CONTROLLED PORTAL FIELDS`.

### 7. Reference-format final polish

Initial review does not require exact production reference style as long as author/year citations and an alphabetical Literature Cited are present. V4 has the registered nine-paper core prior-art set, including the Richardson-extrapolation antecedent, in alphabetical order. Production-style punctuation can be normalized later if requested.

Status: `PASS FOR INITIAL REVIEW`.

## Current blocker

The scientific source is within the journal limits, but the generated anonymous manuscript and reviewer bundle must be rebuilt from the current UTA1.10 source before the package can be considered mechanically closed.

Remaining actions are external/human controlled:

```text
AUTHOR_METADATA                       REQUIRED
ANONYMOUS_REVIEW_ARCHIVE_URL          REQUIRED
ACKNOWLEDGMENTS_IN_AUTHOR_COMMENTS     REQUIRED
AUTHOR_CONTRIBUTIONS_IN_COMMENTS       REQUIRED
AI_USE_DISCLOSURE                      REQUIRED_IF_APPLICABLE_TO_CONTENT
SUGGESTED_REVIEWER_FIELDS              AUTHOR_CONTROLLED
ASSOCIATE_EDITOR_SUGGESTION            AUTHOR_CONTROLLED
PREPRINT_AND_DATA_SHARING_FIELDS       REQUIRED_PORTAL_RESPONSES
ALL_AUTHOR_APPROVAL                    REQUIRED
PORTAL_FILE_UPLOAD                     REQUIRED
```

Scientific reviewer risk is now whether UTA1.10 gate localization—distinguishing negative value, local-release, and rare-establishment explanations for the same persistent phenotype—provides enough biological leverage beyond the deliberately non-novel component algebra, not format compliance.
