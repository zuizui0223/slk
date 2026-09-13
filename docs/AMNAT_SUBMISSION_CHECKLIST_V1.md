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
MAJOR_ARTICLE_TEXT_LIMIT       PASS
ABSTRACT_200_WORD_LIMIT        PASS
FIGURE_TABLE_LIMIT             PASS   (3 figures + 1 in-text table = 4 items)
TITLE_LENGTH_PREFERENCE        PASS   (9 words; journal suggests ~8–10)
KEYWORDS_1_TO_6                PASS   (6)
ANONYMOUS_TITLE_PAGE           PASS
AUTHORS_REMOVED_FROM_MANUSCRIPT PASS
```

## Still required before actual upload

### 1. Build the submission PDF

The final review PDF must be double spaced and include line numbers and page numbers. The Markdown source itself does not satisfy this presentation requirement.

Status: `OPEN — final PDF/typesetting step`.

### 2. Anonymous reviewer-accessible data/code link

The journal requires data and analysis code used by the manuscript to be available to editors/reviewers at submission. Double-anonymous review also means external URLs, README files, code files, and data should not reveal author identity.

The current GitHub repository URL contains the owner's account identity and should therefore **not** be inserted directly into the anonymous review manuscript. Prepare an anonymized reviewer-accessible deposit or upload the review package directly through the submission system.

Status: `OPEN — anonymous review deposit/link required`.

### 3. Author metadata outside the anonymous manuscript

Author names, affiliations, emails, ORCIDs, acknowledgments, and author-contribution statements should remain outside the anonymous review manuscript and be entered in the journal submission fields/comments as instructed.

Status: `READY FOR USER-SUPPLIED AUTHOR METADATA`.

### 4. AI-use transparency

The journal's current policy permits generative AI for drafting/readability and code assistance with human oversight, but requires transparent use and places full responsibility for accuracy on the authors. Prepare the journal-appropriate disclosure during submission/acceptance workflow rather than adding identifying material to the anonymous scientific text.

Status: `DISCLOSURE REQUIRED BEFORE SUBMISSION`.

### 5. Reference-format final polish

Initial review does not require exact production reference style as long as author/year citations and an alphabetical Literature Cited are present. V3 has the registered eight-paper core prior-art set in alphabetical order. Production-style punctuation can be normalized in the final typeset build.

Status: `PASS FOR INITIAL REVIEW`.

## Current blocker

No manuscript-length or figure-count problem remains. The remaining mechanical submission tasks are the anonymized data/code review package and generation of the double-spaced, line-numbered, page-numbered PDF. Scientific reviewer risk remains conceptual importance, not format compliance.
