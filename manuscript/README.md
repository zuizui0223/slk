# SLK manuscript surfaces

Two manuscript surfaces are retained deliberately.

## Journal-facing manuscript

`SLK_MANUSCRIPT_AMNAT_V4.md`

This is the current submission-oriented manuscript. Relative to V3 it promotes the split logic into a unified critical-surface theorem, places all five separation witnesses inside one convex recovery family, makes cross-level preservation of the endpoint contrast explicit, and tightens the accessibility claim to sufficiently small selectively uphill release steps. The process assumptions and empirical claim ceiling are unchanged. The title is 9 words and the abstract is 177 words by the registered checker.

`AMNAT_TITLE_PAGE_V1.md` contains the anonymous title-page metadata and CI-derived counts.

`SLK_MANUSCRIPT_AMNAT_V3.md` is retained as the pre-atlas split-and-witness checkpoint; `SLK_MANUSCRIPT_AMNAT_V2.md` is retained as the prior-art-complete checkpoint; `SLK_MANUSCRIPT_AMNAT_V1.md` is retained as the first label-free journal-prose checkpoint. None should be treated as the current submission surface.

`LITERATURE_CITED_AMNAT_V1.md` is the bibliography ledger used to audit the eight-paper registered prior-art set.

## Audit manuscript

`SLK_MANUSCRIPT_V0.md`

Use this file for theorem/claim traceability. It retains explicit claim IDs, empirical gate IDs, ceiling labels, and links to the internal theorem and provenance ledgers.

## Synchronization rule

The journal-facing manuscript must not introduce a stronger scientific claim than the audit manuscript. Any substantive theorem, estimand, process assumption, witness regime, empirical ceiling, or novelty-boundary change must first be reflected in the internal claim ledger and then propagated to both surfaces.

Purely editorial journal changes, citation expansion, and journal-specific prose may be made only to the journal-facing file, provided they do not strengthen the claim ceiling.

The current automated submission check is `scripts/check_amnat_manuscript.py`; it runs in CI before the test suite.
