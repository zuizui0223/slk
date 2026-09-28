# SLK Am Nat full-page review QA V1

## Canonical build audited

```text
canonical manuscript      manuscript/SLK_MANUSCRIPT_AMNAT_V4.md
main source commit        d1b7e3a163d01e203093a33b0600873991e874bd
workflow run              36368293728
workflow artifact         10948535664
artifact ZIP SHA256       0d6ec7ad88930dd97830110d278273ccb5ed117061e9dce63b265be355189df0
main review PDF pages     34
anonymous title pages      1
embedded figures           3
identity scan              PASS
claim verification         PASS
```

The workflow artifact was generated after UTA1.11 merged to main.

## Page-by-page visual review

All 34 rendered manuscript pages were inspected. No page showed clipped text, overlapping text, broken table cells, missing figure content, black replacement boxes, or content outside the printable page area.

Targeted high-information pages were checked at full-page resolution:

- page 5 — Figure 1 and caption;
- page 9 — Figure 2 and caption;
- pages 13-15 — critical-surface and constructive-witness tables;
- pages 25-27 — UTA1.10 gate-localization table across page breaks;
- pages 27-28 — UTA1.11 interval-box uncertainty paragraph, including the conservative outer-set caveat;
- page 29 — Figure 3 and caption;
- pages 33-34 — novelty/scope boundary and complete Literature Cited.

Table headers repeat correctly across page breaks. UTA1.10 and UTA1.11 remain readable without clipping or overlap.

## Render parity

The current main PDF was render-compared page by page at 120 dpi against the already inspected UTA1.11 pull-request artifact.

```text
pages compared            34
changed pages              0
maximum changed pixels     0
```

The two PDF byte streams differ because they were separately generated, but their rendered pages are pixel-identical. Their `CLAIM_VERIFICATION_RECEIPT.json` files are byte-identical.

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
registered core references            9/9 PRESENT
```

The Literature Cited renders in alphabetical order from Dieckmann & Law through Weinreich et al.

## Status

```text
FULL_PAGE_BY_PAGE_REVIEW_QA = PASS
```

This closes the internal rendered-manuscript proofread/QA item. It does not replace author approval, author metadata, AI-use disclosure where applicable, reviewer-accessible archive deposition, or submission-portal actions.
