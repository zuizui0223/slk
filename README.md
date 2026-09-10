# SLK — From Shared Conflict to Evolutionary Architecture

SLK is the integrated flagship theory programme connecting four previously separate repositories:

- [`sch`](https://github.com/zuizui0223/sch): identifies whether a shared-coordinate functional conflict exists and estimates its compromise load `L`.
- [`balance`](https://github.com/zuizui0223/balance): classifies the persistent-compromise region `L > 0, Phi < 0`.
- [`bita`](https://github.com/zuizui0223/bita): defines recoverable conflict loss and the architecture margin `Phi = sL - K`.
- [`payoff`](https://github.com/zuizui0223/payoff): transports architecture payoff into accessibility, invasion, fixation, and long-run occupancy.

The integrated spine is:

```text
SCH      identifies L
BALANCE classifies L > 0, Phi < 0
BITA    defines/tests Phi = sL - K and Phi > 0
PAYOFF  maps Phi into evolutionary outcomes
```

## Central question

> When multiple biological functions are forced to share one phenotypic coordinate, when is differentiation worth its architectural cost, and when does that global advantage actually become an evolutionary outcome?

## Core hierarchy

```text
shared functional conflict
        |
        v
conflict load L
        |
        +-- L = 0: no identified shared-axis conflict
        |
        v
recoverable loss R = sL
        |
        v
architecture margin Phi = sL - K
        |
        +-- L > 0, Phi < 0: persistent compromise / BALANCE
        +-- Phi = 0: architecture critical surface
        +-- Phi > 0: differentiation globally favored / BITA
        |
        v
local accessibility
        |
        +-- globally favored but locally inaccessible
        |
        v
population transport
        |
        +-- rare invasion
        +-- fixation
        +-- weak-mutation occupancy
```

The key conceptual claim is that these levels are distinct estimands:

```text
conflict exists
!= differentiation pays
!= differentiation is locally reachable
!= differentiation can invade
!= differentiation fixes more often
!= differentiation dominates long-run occupancy.
```

## What SLK owns

SLK owns only the cross-repository theory needed for the integrated hierarchy:

1. identification and interpretation of the conflict budget `L`;
2. the persistent-compromise classification `L > 0, Phi < 0`;
3. the architecture payoff bridge `R=sL`, `Phi=sL-K`;
4. the distinction between global architecture value and local evolutionary accessibility;
5. the minimal transport from architecture payoff to invasion, fixation, and occupancy.

The flagship never uses `Phi>0` as shorthand for "differentiation evolves". Every later stage has its own gate.

## What SLK deliberately does not absorb

The sister repositories remain active and now develop their residual independent contributions:

- **SCH:** causal identification of contextual versus pure-function optima; multifunctionality-versus-conflict inference; empirical crossed-design programme.
- **BALANCE:** middle-world geometry, direct worldline identification, reserve/depth/topology, and persistence/hysteresis methods.
- **BITA:** ecological mechanism identification after differentiation; interaction-versus-mechanism inference; partial-identification workflow.
- **PAYOFF:** continuous architecture, evolutionary branching, edgewise modularization/topology, and spatial/temporal spectral dynamics.

Those topics may be cited by SLK but are not required for the flagship proof spine.

## Canonical reader path

1. `manuscript/SLK_MANUSCRIPT_V0.md` — first integrated manuscript draft.
2. `theory/SLK_CORE_THEORY_V1.md` — minimal mathematical spine.
3. `docs/THEOREM_CLAIM_LEDGER_V1.md` — theorem/corollary/empirical-handoff status for every flagship claim.
4. `docs/OWNERSHIP_AND_HANDOFF.md` — claim ownership and anti-duplication boundary.
5. `docs/PAPER_ROADMAP.md` — flagship and residual-paper programme.
6. `PROVENANCE.md` — source repositories and migration provenance.

## Current status

```text
INTEGRATED_SPINE_DEFINED
FLAGSHIP_MANUSCRIPT_STARTED
CORE_THEORY_MIGRATED_CONCEPTUALLY
THEOREM_CLAIM_LEDGER_REGISTERED
SOURCE_REPOSITORIES_HAVE_RESIDUAL_MANUSCRIPT_V0S
EMPIRICAL_CLAIM_CEILING_UNCHANGED
```

SLK does not turn theoretical quantities into empirical measurements by declaration. Any empirical use of `L`, `s`, `K`, `Phi`, accessibility, invasion, fixation, or occupancy must retain the identification requirements and uncertainty of the source analysis.