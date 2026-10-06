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
TITLE_WORDS                         7
ABSTRACT_WORDS                    167
TEXT_WORDS_EXCL_LITERATURE_CITED 7093
FIGURES                             3
TABLES                              0
```

## Current journal-limit checks

The current The American Naturalist author instructions specify that Major Articles should usually be no more than 7,500 words excluding Literature Cited, with no more than six figures and/or tables; abstracts are limited to 200 words. The title page should include article type, four to six keywords, text word count, and a list of manuscript elements. Initial submissions require double spacing, line numbers, page numbers, author/date citations, and double-anonymous review formatting.

Status:

```text
MAJOR_ARTICLE_TEXT_LIMIT        PASS
ABSTRACT_200_WORD_LIMIT         PASS
FIGURE_TABLE_LIMIT              PASS   (3 figures + 0 tables = 3 items)
TITLE_LENGTH_PREFERENCE         PASS   (7 words; concise)
KEYWORDS_1_TO_6                 PASS   (6)
ANONYMOUS_TITLE_PAGE            PASS
AUTHORS_REMOVED_FROM_MANUSCRIPT PASS
```

## Submission package state

### 1. Anonymous review manuscript — SOURCE READY, PACKAGE REBUILD PENDING

The current ecology-first manuscript, title page, and all three figures build successfully through the anonymous-review workflow. The current PDF is 28 pages, double spaced, line numbered, page numbered, and passes the rendered identity scan.

All 28 rendered pages were inspected at overview scale, and the three figure pages were inspected at full size. No clipping, overlap, broken glyphs, or figure-title truncation was found.

Status: `PREVIOUS 28-PAGE LAYOUT QA PASS — REBUILD REQUIRED AFTER LATEST ECOLOGICAL PREDICTION EDIT`.

### 2. Anonymous reviewer code/theory package — REBUILD PENDING

The current deterministic reviewer ZIP is frozen and verified:

```text
file      SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip
size      59,927 bytes
SHA256    b0589f1d1b3fb1191d46bd42c375e2bb4e55f0d625fec26a605c12292e17ee8e
files     17
identity  PASS
```

The current Editorial Manager convenience kit is also frozen:

```text
file      SLK_AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT.zip
size      1,527,268 bytes
SHA256    3b8bb9f80c35c998de2eb2a08a039acdbf4188f35d24e6c0adff2caeb678de1c
files     8
```

Status: `FAIL-CLOSED UNTIL THE LATEST SOURCE IS REBUILT AND NEW CHECKSUMS ARE REGISTERED`.

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

Status: `AI DISCLOSURE REQUIRED — AUTHOR APPROVAL OF EXACT WORDING BEFORE SUBMISSION`.

### 6. Reviewer / editor / additional-information fields

The live submission flow asks for reviewer suggestions and additional information including preprint status, data location/data-sharing compliance, and a potentially suitable associate editor. Reviewer identities must not be inferred from citations or repository history. The journal flags recent collaboration (previous 48 months) and same-institution employment as conflicts.

Status: `AUTHOR-CONTROLLED PORTAL FIELDS`.

### 7. Reference-format final polish

Initial review does not require exact production reference style as long as author/year citations and an alphabetical Literature Cited are present. The biology-refocused V4 uses a literature-based natural-history synthesis spanning floral division of labor, temporal pollen presentation, geographic mosaics of mutualist–antagonist selection, frequency dependence, organismal integration, and cichlid jaw decoupling. Technical process results that no longer support the biological main line remain in the supporting theory rather than the journal-facing narrative.

Status: `PASS FOR INITIAL REVIEW`.

## Current blocker

The scientific source is ready, but the deterministic reviewer package must be rebuilt after the latest manuscript and figure edits. Remaining steps are author-controlled or authenticated external actions:

```text
AUTHOR_METADATA                       REQUIRED
ACKNOWLEDGMENTS / CONTRIBUTIONS       REQUIRED
AI_USE_DISCLOSURE                     REQUIRED_AUTHOR_APPROVAL
PREPRINT / DATA_SHARING FIELDS        REQUIRED
REVIEWER_ZIP_UPLOAD                   REQUIRED
INITIAL_ZENODO_DRAFT                  REQUIRED
MANUSCRIPT / TITLE PAGE UPLOAD        REQUIRED
EDITORIAL_MANAGER PDF VERIFICATION    REQUIRED
ALL_AUTHOR_APPROVAL                   REQUIRED
```
