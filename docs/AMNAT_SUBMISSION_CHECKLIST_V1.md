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
ABSTRACT_WORDS                    184
TEXT_WORDS_EXCL_LITERATURE_CITED 5418
FIGURES                             3
```

## Current journal-limit checks

The current The American Naturalist author instructions specify that Major Articles should usually be no more than 7,500 words excluding Literature Cited, with no more than six figures and/or tables; abstracts are limited to 200 words. The title page should include article type, four to six keywords, text word count, and a list of manuscript elements. Initial submissions require double spacing, line numbers, page numbers, author/date citations, and double-anonymous review formatting.

Status:

```text
MAJOR_ARTICLE_TEXT_LIMIT        PASS
ABSTRACT_200_WORD_LIMIT         PASS
FIGURE_TABLE_LIMIT              PASS   (3 figures + 3 in-text tables = 6 items)
TITLE_LENGTH_PREFERENCE         PASS   (7 words; concise)
KEYWORDS_1_TO_6                 PASS   (6)
ANONYMOUS_TITLE_PAGE            PASS
AUTHORS_REMOVED_FROM_MANUSCRIPT PASS
```

## Submission package state

### 1. Anonymous review manuscript — BUILD PASS, MANUAL QA REOPENED

The biology-refocused manuscript, title page, and all three figures build successfully through the anonymous-review workflow. The workflow verifies manuscript limits, generates the DOCX/PDF, embeds all three figures, checks line/page numbering, and scans rendered files for identity-bearing text.

Because the title, prose, figures, references, and pagination changed after the previous 35-page proofread, that earlier page-by-page QA is **historical evidence only**. It does not certify the refocused render.

Status: `AUTOMATED BUILD PASS — NEW RENDER REQUIRES FINAL HUMAN PAGE-BY-PAGE QA`.

### 2. Anonymous reviewer code/theory package — SOURCE BUILD PASS, FROZEN ZIP STALE

The current workflow successfully builds the curated anonymous reviewer bundle from the refocused source. However, the previously frozen distribution ZIP and its SHA256 were generated from an earlier manuscript state.

The historical ZIP receipt is retained for provenance but now has:

```text
status                 STALE_AFTER_MANUSCRIPT_REFOCUS_REBUILD_REQUIRED
current_for_submission false
```

Do **not** upload the old `SLK_AMNAT_REVIEWER_DATA_CODE_BUNDLE_FINAL.zip`, do not deposit it to Zenodo, and do not reuse its SHA256 in Editorial Manager.

Required internal action:

```text
regenerate deterministic reviewer ZIP from refocused source
-> rerun bundled tests / anonymity scan / internal checksum manifest
-> register new ZIP SHA256 + size + source commit
-> rebuild Editorial Manager upload kit
-> rerun final rendered-page QA
```

Status: `BLOCKED UNTIL REFOCUSED PACKAGE IS REBUILT AND VERIFIED`.

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

Initial review does not require exact production reference style as long as author/year citations and an alphabetical Literature Cited are present. The biology-refocused V4 has 13 main-text references; every Literature Cited entry is cited in the manuscript and the list is alphabetical. Broader technical prior art remains documented in the repository but is no longer carried into the streamlined main bibliography when the corresponding derivation has moved out of the journal-facing prose.

Status: `PASS FOR INITIAL REVIEW`.

## Current blocker

The scientific manuscript and automated review-package build pass, but the **submission package is intentionally fail-closed after the biology refocus**. The frozen reviewer ZIP, Zenodo payload checksum, Editorial Manager convenience kit, and previous manual page-by-page QA all belong to the pre-refocus version.

Current internal actions:

```text
REFOCUSED_REVIEWER_ZIP_REBUILD          REQUIRED
NEW_ZIP_CHECKSUM_RECEIPT                REQUIRED
EDITORIAL_MANAGER_UPLOAD_KIT_REBUILD    REQUIRED
REFOCUSED_RENDER_PAGE_BY_PAGE_QA        REQUIRED
```

After those are closed, the remaining author-controlled items are metadata, acknowledgments/contributions, AI-disclosure approval, archive creation, portal upload, and all-author approval.
