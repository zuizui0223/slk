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
| unified witness family | `MODEL-PREDICTION` | `R(d)=d+d^2`, `K(d)=kd`, `d in [0,1]` gives `k_local=1`, `k_global=2`, `Phi=2-k` | one declared convex recovery family generates all registered separation witnesses; not an empirical fit |
| conflict -> payoff separation | `THEORETICAL-WITNESS` | `L=2, k=2.2` gives `R(1)=2`, `K(1)=2.2`, `Phi=-0.2` | proves `L>0 !=> Phi>0` inside the common family; not an empirical estimate |
| payoff -> small-step accessibility separation | `THEORETICAL-WITNESS` | `k=1.5` gives `Phi=0.5>0` but `Phi'(0)=-0.5<0` | proves global endpoint value need not imply sufficiently small selectively uphill release |
| accessible payoff -> invasion separation | `THEORETICAL-WITNESS` | `k=0.8, eta=1.5` gives `Phi=1.2`, `Phi'(0)=0.2`, `Delta(0)=-0.3` | proves small-step accessible positive endpoint value need not imply rare invasion |
| invasion -> reciprocal fixation separation | `THEORETICAL-WITNESS` | `k=2.2, eta=-1` gives `Phi=-0.2`, `Delta(0)=0.8>0` but `rho_D/rho_S<1` | proves rare invasion need not imply reciprocal fixation superiority |
| absolute fixation advantage -> occupancy separation | `THEORETICAL-WITNESS` | `k=2.1, eta=-0.5` gives `Phi=-0.1`, `3Phi=-0.3>eta` yet `Pi_D<Pi_S` | proves absolute fixation advantage over neutrality need not imply greater weak-mutation occupancy |
| critical-surface atlas | `MODEL-PREDICTION` | small-step release: `k=k_local`; endpoint value/fixation/occupancy: `Phi=0`; rare invasion: `Phi=eta`; reverse invasion: `Phi=-eta`; absolute fixation under weak selection: `3Phi=eta` | exact thresholds are conditional on the registered path, game, Moran, and mutation assumptions |
| ecological threshold displacement | `MODEL-PREDICTION` | for constant feedback, `E_I=E_V+eta/a`; with `eta(E)=eta_0+b(E-E_V)`, `E_I-E_V=eta_0/(a-b)` and `E_R-E_V=-eta_0/(a+b)` | exact for registered affine slices; smooth systems use local slope approximations |
| two-frequency Phi/eta identification | `MODEL-PREDICTION` | for `p_-=1/2-q` and `p_+=1/2+q`, `Phi=[Delta_++Delta_-]/2` and `eta=[Delta_+-Delta_-]/(4q)` | exact under the registered linear-in-frequency canonical pair; curvature rejects the minimal mapping |
| three-frequency curvature diagnostic | `MODEL-PREDICTION` | with independent `Phi`, `h0=Delta_0-Phi`, `eta=(Delta_+-Delta_-)/(4q)`, `kappa=(Delta_++Delta_--2Delta_0)/(8q^2)`; invasion surfaces become `Phi=eta-kappa-h0` and `Phi=-eta-kappa-h0` | quadratic diagnostic for invasion only; canonical fixation/occupancy formulas do not automatically extend |
| arbitrary-shape endpoint invasion | `MODEL-PREDICTION` | for `Delta=Phi+H(p)`, rare D invasion is `Phi+h_R>0` and reverse resistance is `Phi+h_D>0`, with `h_R=lim_{p->0}H`, `h_D=lim_{p->1}H` | exact deterministic endpoint criterion; does not imply canonical fixation or occupancy results |
| finite-frequency endpoint certificate | `MODEL-PREDICTION` | one-point bound: `Delta_R in [Delta(eps)-M eps, Delta(eps)+M eps]`; two-point bound: `Delta_R_hat=2Delta(eps)-Delta(2eps)`, error `<=C eps^2`; sampling intervals widen these bounds | deterministic certificate conditional on local smoothness bounds; overlap with zero is unresolved |
| conflict–differentiation discordance | `MODEL-PREDICTION` | under `Phi=sL-K`, `L_A>L_B` does not imply `Phi_A>Phi_B` when `s` or `K` differs | comparative prediction only after valid common-scale conflict, recoverability and cost definitions |
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
