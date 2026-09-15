# SLK — The American Naturalist submission checklist V1

## Current submission surface

```text
MANUSCRIPT = manuscript/SLK_MANUSCRIPT_AMNAT_V3.md
TITLE_PAGE = manuscript/AMNAT_TITLE_PAGE_V1.md
ARTICLE_TYPE = Major Article
```

Automated count from `scripts/check_amnat_manuscript.py`:

```text
TITLE_WORDS                         9
ABSTRACT_WORDS                    172
TEXT_WORDS_EXCL_LITERATURE_CITED 2941
FIGURES                             3
```

## Current journal-limit checks

The current The American Naturalist author instructions specify that Major Articles should usually be no more than 7,500 words excluding Literature Cited, with no more than six figures and/or tables; abstracts are limited to 200 words. The title page should include article type, four to six keywords, text word count, and a list of manuscript elements. Initial submissions require double spacing, line numbers, page numbers, author/date citations, and double-anonymous review formatting.

Status:

```text
MAJOR_ARTICLE_TEXT_LIMIT        PASS
ABSTRACT_200_WORD_LIMIT         PASS
FIGURE_TABLE_LIMIT              PASS   (3 figures + 1 in-text table = 4 items)
TITLE_LENGTH_PREFERENCE         PASS   (9 words; journal suggests ~8–10)
KEYWORDS_1_TO_6                 PASS   (6)
ANONYMOUS_TITLE_PAGE            PASS
AUTHORS_REMOVED_FROM_MANUSCRIPT PASS
```

## Submission package state

### 1. Anonymous review manuscript — PASS

The CI-built review manuscript is generated directly from the canonical V3 source and has been rendered and visually inspected page by page.

```text
MAIN_REVIEW_PDF_PAGES     18
ANONYMOUS_TITLE_PDF_PAGES  1
DOUBLE_SPACED              true
LINE_NUMBERS               true
PAGE_NUMBERS               true
EMBEDDED_FIGURES           3
VISUAL_QA                   PASS — all 19 rendered pages inspected
```

The final formatting QA repaired the two renderer-visible defects found during review: inherited blue heading color and footer line-number duplication. Figure 3's closing validation note was also shortened until it rendered fully inside its SVG canvas.

Status: `PASS — reader-facing review files generated and visually verified`.

### 2. Anonymous reviewer code/theory package — PASS INTERNALLY

The review bundle is curated rather than being a repository dump. It contains:

- the exact anonymous manuscript and title-page sources;
- `theory/SLK_CORE_THEORY_V1.md`;
- `theory/NON_EQUIVALENCE_THEOREM_V1.md`;
- the three submitted SVG figure sources;
- `code/verify_amnat_claims.py`;
- a precomputed `CLAIM_VERIFICATION_RECEIPT.json`;
- `ANONYMITY_AUDIT.txt`;
- `SHA256SUMS.txt`.

The verifier recomputes all five registered witness regimes and the fixation–occupancy invariant. The invariant grid contains 112 comparisons with maximum absolute error 0.0. The bundle identity scan passes and excludes repository history, remote URLs, and author metadata.

The identity-bearing GitHub repository URL must still not be inserted into the anonymous manuscript. At submission, upload this bundle directly through the journal system or place the exact bundle in an anonymous reviewer-accessible deposit.

Status: `PASS INTERNALLY — external portal/deposit upload remains a submission action`.

### 3. Author metadata outside the anonymous manuscript

Author names, affiliations, emails, ORCIDs, acknowledgments, and author-contribution statements should remain outside the anonymous review manuscript and be entered in the journal submission fields/comments as instructed.

Status: `READY FOR USER-SUPPLIED AUTHOR METADATA`.

### 4. AI-use transparency

Prepare the journal-appropriate disclosure during the submission/acceptance workflow rather than adding identifying material to the anonymous scientific text.

Status: `DISCLOSURE REQUIRED BEFORE SUBMISSION`.

### 5. Reference-format final polish

Initial review does not require exact production reference style as long as author/year citations and an alphabetical Literature Cited are present. V3 has the registered eight-paper core prior-art set in alphabetical order. Production-style punctuation can be normalized later if requested.

Status: `PASS FOR INITIAL REVIEW`.

## Current blocker

No internal scientific-package or mechanical-format blocker remains. The repository now produces a double-spaced, line-numbered, page-numbered anonymous review manuscript and a curated anonymous reviewer code/theory bundle with executable claim verification.

Remaining actions are external/human controlled:

```text
AUTHOR_METADATA        REQUIRED
AI_USE_DISCLOSURE      REQUIRED
ALL_AUTHOR_APPROVAL    REQUIRED
PORTAL_FILE_UPLOAD     REQUIRED
ANONYMOUS_BUNDLE_UPLOAD_OR_DEPOSIT REQUIRED
```

Scientific reviewer risk remains conceptual importance of the integrated estimand transport, not format compliance.
