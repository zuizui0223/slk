# SLK manuscript section-to-claim map V1

This document maps the flagship manuscript directly onto the canonical theorem-claim ledger.

## Section map

| Manuscript section | Claim IDs | Claim class | Primary role | Must not overclaim |
|---|---|---|---|---|
| Abstract | C1-C9, INV1 | mixed | summarize separations plus invariant | do not imply end-to-end empirical validation or universal non-equivalence |
| 1. Introduction | C1-C9, INV1 overview | synthesis + prior-art boundary | motivate estimand transport, separations and re-alignment | do not claim first theory of modularity, specialization, games or weak mutation |
| 2. Identifying the conflict budget | C1 | empirical handoff | define valid entry receipt `L` | multifunctionality alone does not identify `L` |
| 3. Persistent compromise and architecture crossing | C2, C4 | definition/classification | define `R`, operational `K`, `Phi=R-K`, and middle world | no historical persistence claim; no undefined omnibus `K` |
| 4. Differentiation recovers only released conflict | C3-C5 | general definition + quadratic corollary + model result | use `Phi=R-K` generally; derive `R=sL` only in quadratic bridge | do not promote `R=sL` to arbitrary landscapes; `Phi>0` does not mean differentiation evolves |
| 5. Global value can exceed local accessibility | C6 | theorem/model result | separate global optimality from reachable steps | requires declared mutation neighborhood |
| 6. Population feedback splits architecture boundary | C7 | theorem/model result | separate intrinsic payoff from rare invasion | requires declared pair game / feedback |
| 7. Fixation is another estimand | C8 | process-specific theorem | distinguish rare invasion, reciprocal fixation ordering, absolute fixation advantage | Moran-specific unless generalized |
| 8. Weak-mutation occupancy and fixation-occupancy invariant | C9, INV1 | process-specific theorem + invariant | separate occupancy from accessibility/absolute fixation while proving reciprocal-fixation alignment | requires symmetric rare mutation + registered fixation kernel |
| 9. Split-and-invariant theorem with explicit witnesses | NE1-NE5, INV1 | theorem synthesis | provide constructive witness regimes and exact re-alignment | do not claim every adjacent stage differs |
| 10. Empirical programme | G1-G9 | empirical gates | give sequential validation design | no completed biological chain claimed |
| 11. Discussion | C1-C9, INV1 | synthesis + novelty boundary | state what SLK integrates and what prior theory already owns | preserve all claim ceilings |

## Reader-facing theorem order

```text
C1  valid conflict receipt L
 ↓
C2  persistent compromise class
 ↓
C4  general architecture margin Phi=R-K
 ↙
C3  quadratic bridge R=sL (model-specific corollary)
 ↓
C5  global architecture value
 ↓
C6  local accessibility split
 ↓
C7  invasion split
 ↓
C8  fixation criteria split
 ↓
C9  weak-mutation occupancy
 ↘
INV1 reciprocal fixation ordering <=> occupancy ordering
```

The formal constructive witnesses are registered in `theory/NON_EQUIVALENCE_THEOREM_V1.md`. The operational definition of `K` is registered in `docs/K_OPERATIONAL_DEFINITION_V1.md`; prior-art claim boundaries are registered in `docs/PRIOR_ART_BOUNDARY_V1.md`.

## Manuscript rule

Every future substantive claim added to `manuscript/SLK_MANUSCRIPT_V0.md` must do one of three things:

1. map to an existing C/G/INV identifier;
2. be explicitly labelled as interpretation/synthesis;
3. receive a new identifier in `docs/THEOREM_CLAIM_LEDGER_V1.md` before being promoted as a primary result.

Any use of `R=sL` must explicitly state the quadratic partial-release assumptions or cite the registered corollary. Any empirical use of `K` must satisfy the operational receipt.

This prevents manuscript prose from outrunning the registered theory.