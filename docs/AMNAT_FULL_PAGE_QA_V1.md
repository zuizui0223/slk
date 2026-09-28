# SLK Am Nat full-page review QA V1

## Canonical build audited

```text
canonical manuscript      manuscript/SLK_MANUSCRIPT_AMNAT_V4.md
main source commit        b4285a244ebdb8f7adab0f2e9eb42a8d8dc92fe4
workflow run              36441156403
workflow artifact         10978421671
artifact ZIP SHA256       723d2fc72409d35f97a1ef6befbd6005b30cc0cddd51291ff88ee6e9cbd7a8d6
main review PDF pages     35
anonymous title pages      1
embedded figures           3
identity scan              PASS
claim verification         PASS
```

This build contains the Bowers et al. (2005) trade-off/invasion prior-art expansion.

## Page-by-page visual review

All 35 rendered manuscript pages were inspected. No page showed clipped text, overlapping text, broken table cells, missing figure content, black replacement boxes, or content outside the printable page area.

Targeted high-information pages were checked at full-page resolution:

- page 5 — Figure 1 and caption;
- page 9 — Figure 2 and caption;
- pages 13-15 — critical-surface and constructive-witness tables;
- pages 25-27 — UTA1.10 gate-localization table across page breaks;
- pages 27-28 — UTA1.11 interval-box uncertainty paragraph and conservative outer-set caveat;
- page 29 — Figure 3 and caption;
- pages 33-35 — Discussion, novelty/scope boundary, and complete ten-reference Literature Cited.

Table headers repeat correctly across page breaks. UTA1.10 and UTA1.11 remain readable without clipping or overlap.

## Render parity

The current main PDF was render-compared page by page against the already inspected Bowers prior-art pull-request artifact.

```text
pages compared            35
changed pages              0
maximum changed pixels     0
```

The PDF byte streams may differ because they were separately generated, but their rendered pages are pixel-identical.

## Extracted-text audit

The rendered PDF was extracted with layout preservation and checked for:

- replacement-glyph artifacts;
- TODO / TBD / FIXME markers;
- unresolved template placeholders;
- merge-conflict markers;
- identity-bearing repository or author strings;
- missing numbered section headings;
- missing registered core references.

Results:

```text
replacement / placeholder findings  0
identity-string findings             0
sections 1-12                        PRESENT
Novelty boundary                     PRESENT
Scope boundary                       PRESENT
Literature Cited                     PRESENT
registered core references           10/10 PRESENT
```

The Literature Cited renders in alphabetical order from Bowers et al. through Weinreich et al.

## Reviewer distribution package

The canonical reviewer distribution ZIP is built deterministically from only the sixteen files listed in the bundle checksum manifest plus the manifest itself.

```text
files                     17
cache / bytecode files     0
bundled tests             13/13 PASS
manifest checks           PASS
identity scan             PASS
receipt tolerance check   PASS
```

## Status

```text
FULL_PAGE_BY_PAGE_REVIEW_QA = PASS
```

This closes the internal rendered-manuscript proofread/QA item. It does not replace author approval, author metadata, AI-use disclosure, authenticated archive deposition, or submission-portal actions.
