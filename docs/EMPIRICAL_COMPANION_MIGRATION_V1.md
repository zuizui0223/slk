# Empirical companion migration contract — Pedicularis anchor

## Decision

The Pedicularis programme is an empirical execution package, not part of the SLK flagship theory surface. Migration should therefore be package-level rather than deleting individual outreach utilities opportunistically.

The pre-pruning recovery point is:

```text
archive/pedicularis-operations-2026-09-27
source commit: 0f632f7cfce12f04cb2106c24753ca976f30d677
```


The exact 160-file migration inventory is frozen machine-readably in:

```text
data/EMPIRICAL_COMPANION_MIGRATION_MANIFEST_V1.json
```

That manifest is the canonical checklist for companion copy completeness and later SLK pruning. It records destination fields as null and `slk_deletion_authorized=false` until a destination repository, destination commit, and verified companion CI are recorded.

## Why WAVE1 outreach cannot be pruned alone

At the frozen source commit, the WAVE1 permission/outreach subgraph contains:

```text
data      5 files
docs      4 files
scripts  11 files
tests    10 files
total    30 files / 258,366 bytes
```

Those files are not isolated. The canonical Pedicularis execution-state object references the response adjudicator, send/response receipt tooling, outreach manager, message renderer, follow-up planner and related templates. Context-recovery documentation also points into the permission-routing layer.

Therefore deleting only the correspondence machinery would leave a syntactically present but semantically stale execution state.

## Migration unit

The safe migration unit is the candidate-specific Pedicularis execution package:

- `data/PEDICULARIS_*`;
- `docs/PEDICULARIS_*`;
- Pedicularis-specific scripts under `scripts/`;
- Pedicularis-specific tests and fixtures under `tests/`.

At the frozen source commit, Pedicularis-named tracked files account for 160 files and approximately 1.46 MB. Generic SLK theory, manuscript, figures, theorem/process validation, estimand definitions, and the G1-G9 measurement ladder remain in the flagship.

## Promotion exception

A Pedicularis artifact stays or returns to the SLK flagship only if it changes at least one of:

1. an SLK estimand definition or identification requirement;
2. a registered model assumption or mathematical result;
3. a generic G1-G9 empirical gate;
4. the manuscript claim ceiling;
5. a real biological result that is discussed in the flagship manuscript.

Administrative auditability, permission correspondence, field logistics, and candidate-specific power/layout machinery do not satisfy this exception by themselves.

## Non-destructive migration sequence

```text
1  freeze source snapshot                                  DONE
2  provision a Pedicularis empirical companion            REQUIRED
3  copy the complete execution package to that companion  REQUIRED
4  verify companion paths/tests and record destination SHA REQUIRED
5  prune duplicated candidate-specific files from SLK     ONLY AFTER 2-4
6  retain a short empirical-anchor pointer in SLK          REQUIRED
```

No file deletion from the flagship is authorized before the destination repository and destination commit are recorded. Git history plus the archive branch provide independent recovery paths, but the companion copy should exist before main is pruned.

Destination verification is machine-gated by:

```text
data/EMPIRICAL_COMPANION_DESTINATION_RECEIPT_TEMPLATE_V1.json
scripts/check_empirical_companion_destination.py
tests/test_empirical_companion_destination.py
```

The validator returns `READY_TO_PRUNE_SLK` only when:

```text
destination repository is identified
destination commit is a full Git SHA
destination CI is verified
copied file inventory matches all 160 frozen paths exactly
verification reference is present.
```

A missing file, extra file, duplicate file, unverified CI state, or incomplete destination receipt keeps SLK deletion unauthorized.

## Immediate development rule

Until migration is complete, no new permission/outreach/readiness infrastructure should be merged into the flagship. PR #84 remains a draft migration source rather than a flagship merge candidate.
