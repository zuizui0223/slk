# SLK repository scope boundary

## Purpose

SLK is the flagship theory repository. Its tracked surface should make the architecture-value transport easy to inspect, test, and review:

```text
identified conflict L
-> recoverable benefit R
-> architecture cost K
-> Phi = R - K
-> accessibility
-> invasion
-> fixation
-> occupancy
```

A biological execution programme can motivate and test this hierarchy without becoming the repository's dominant software surface.

## Keep canonical in SLK

The following remain first-class SLK material:

1. the journal-facing and audit manuscripts;
2. the registered theory, proofs, witnesses, and numerical/process validation;
3. figures and manuscript-facing checks;
4. generic estimand definitions and claim ceilings, including the G1-G9 measurement ladder;
5. the operational definition of `K` and other definitions required to interpret the manuscript;
6. prior-art, claim-provenance, and cross-repository ownership ledgers;
7. a concise statement that `Pedicularis rex` is the first prospective same-system empirical anchor and that no real G1-G5 receipt has yet closed.

## Treat as companion empirical/operations material

Candidate-specific execution machinery should live in a Pedicularis companion repository rather than grow the flagship surface. This includes, unless a file directly changes a manuscript estimand or claim ceiling:

- permission/contact routing;
- inquiry-message generation;
- send, response, and follow-up receipts;
- correspondence provenance and administrative readiness audits;
- access and scouting logistics;
- candidate-specific recovery packets;
- field-operation ledgers and handoff state machines;
- candidate-specific sample-size, calibration, and execution machinery;
- tests whose only purpose is to validate the above administrative or field-workflow state.

These materials can remain temporarily in SLK while migration is prepared. Historical commits remain valid provenance.

A non-destructive recovery snapshot is frozen at:

```text
archive/pedicularis-operations-2026-09-27
source commit: 0f632f7cfce12f04cb2106c24753ca976f30d677
```

This branch preserves the pre-pruning operational tree independently of later flagship cleanup.

## Promotion rule

A Pedicularis change belongs in the SLK flagship only if at least one of the following is true:

1. it changes the definition or identification of an SLK estimand;
2. it changes a theorem, corollary, or registered model assumption;
3. it changes the generic empirical measurement ladder;
4. it changes the manuscript's scientific claim ceiling;
5. it provides a real biological result that must be represented in the flagship manuscript.

Administrative completeness alone is not a promotion criterion.

## Boundary-freeze inventory

At the boundary-freeze snapshot on SLK main, the Pedicularis-specific operational surface contains:

```text
160 files total

docs/    30
data/    39
scripts/ 50
tests/   41
```

The inventory is defined mechanically by the same path families used by the scope guard. This count is a migration baseline, not a publication metric. After the boundary is merged, the expected direction in SLK is monotonically downward as files are copied to the empirical companion and deleted from the flagship.

A future increase in this count is a scope regression.

The non-destructive package-level migration sequence is frozen in:

```text
docs/EMPIRICAL_COMPANION_MIGRATION_V1.md
```

## Executable scope guard

The boundary is enforced in pull-request CI by:

```text
scripts/check_repository_scope_boundary.py
tests/test_repository_scope_boundary.py
.github/workflows/test.yml
```

The guard treats the current Pedicularis operational surface as **frozen in place**. Matching is case-insensitive and applies to nested paths under `docs/`, `data/`, `scripts/`, and `tests/` whenever the path contains `pedicularis`. The examples below cover the current naming convention:

```text
docs/PEDICULARIS_*
data/PEDICULARIS_*
scripts/*pedicularis*.py
tests/test_pedicularis_*.py
```

the flagship repository allows:

```text
DELETE
```

during migration, but blocks:

```text
ADD
MODIFY
COPY
RENAME.
```

This is intentionally asymmetric. Existing files may remain temporarily for provenance and may be removed as the companion migration proceeds, but the flagship cannot accumulate new candidate-specific operational machinery.

Generic manuscript, theory, claim-ledger, prior-art, ownership, and repository-boundary files remain editable.

## Current boundary decision

The WAVE1 outreach-readiness work in PR #84 is retained as a draft migration source and is not part of the flagship merge path. Existing permission-integrity machinery is sufficient for provenance while the empirical companion is separated.

No destructive migration is required to enforce this boundary: first stop further flagship growth, then copy/move the empirical execution surface with history-preserving references, and only then prune duplicate files from SLK.
