# SLK quantitative claim ledger V1

## Purpose

This ledger separates quantities that come from biological data or literature audit from quantities that are constructive theory, conditional model predictions, or not yet estimated in nature. It does not add a scientific claim to the canonical manuscript.

## Claim classes

- `EMPIRICAL` — estimated from a biological dataset on a declared measurement scale.
- `LITERATURE-AUDIT` — a count or classification of screened sources/systems; not an effect-size estimate.
- `THEORETICAL-WITNESS` — a constructive parameter regime used to prove a non-implication or boundary result; not an empirical estimate.
- `MODEL-PREDICTION` — a theorem or quantitative consequence conditional on an explicitly declared evolutionary process/model.
- `NOT-ESTIMATED` — a biologically meaningful quantity for which the present paper does not report a field or cross-system estimate.

## Registered quantitative objects

| Object | Class | Frozen quantitative statement | Interpretation ceiling |
|---|---|---|---|
| conflict -> payoff separation | `THEORETICAL-WITNESS` | `L=1, R=1/2, K=1` gives `Phi=-1/2` | proves `L>0 !=> Phi>0` in the declared architecture comparison; not an empirical estimate |
| payoff -> accessibility separation | `THEORETICAL-WITNESS` | `s0=1/2, Delta=2, k=3/2`, with `k_local=1<k<2=k_global` | proves global value need not imply local reachability |
| accessible payoff -> invasion separation | `THEORETICAL-WITNESS` | `Phi=0.2, eta=0.5`, giving `Delta(0)=-0.3<0` | proves accessible positive architecture value need not imply rare invasion |
| invasion -> reciprocal fixation separation | `THEORETICAL-WITNESS` | `Phi=-0.2, eta=-1`, giving `Delta(0)=0.8>0` but `rho_D/rho_S<1` | proves rare invasion need not imply reciprocal fixation superiority |
| absolute fixation advantage -> occupancy separation | `THEORETICAL-WITNESS` | `Phi=-0.1, eta=-0.5`, with `3Phi>eta` yet `Pi_D<Pi_S` | proves absolute fixation advantage over neutrality need not imply greater weak-mutation occupancy |
| fixation-occupancy invariant | `MODEL-PREDICTION` | under connected symmetric rare mutation and the registered exponential Moran process, `rho(j|i)>rho(i|j)` iff `Pi_j>Pi_i` | reciprocal fixation ordering and stationary monomorphic occupancy ordering coincide only under the registered process assumptions |
| empirical end-to-end hierarchy | `EMPIRICAL` | No single biological system is claimed to have completed the full measurement ladder end to end. | the paper supplies an empirical measurement programme, not a completed cross-level calibration |
| prior-art/evidence placement | `LITERATURE-AUDIT` | the manuscript uses a compact prior-art set to place modularity, specialization, accessibility, finite-population fixation, and weak-mutation theory | citation coverage is not natural prevalence or an empirical architecture-effect estimate |

## Quantities explicitly not estimated

```text
NATURAL_PREVALENCE = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_L = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_R = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_K = NOT_ESTIMATED
FIELD_DISTRIBUTION_OF_PHI = NOT_ESTIMATED
FIELD_ACCESSIBILITY_FREQUENCY = NOT_ESTIMATED
FIELD_INVASION_FREQUENCY = NOT_ESTIMATED
FIELD_FIXATION_FREQUENCY = NOT_ESTIMATED
FIELD_OCCUPANCY_FREQUENCY = NOT_ESTIMATED
```

The witness values above are deliberately constructive. They demonstrate logical separations inside declared model classes and are **not an empirical estimate** of how large `L`, `Phi`, `eta`, fixation advantage, or occupancy differences are in nature.

## Promotion rule

A numerical value may be described as empirical only after the corresponding biological quantity has been measured on the required scale. In particular, empirical promotion requires, in order: identified shared-axis conflict; an estimated or bounded `L`; common-scale `R` and `K`; local release/mutation information; rare-frequency performance; a finite-population process; and a mutation graph/kernel where occupancy is claimed.
