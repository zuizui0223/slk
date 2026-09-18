# SLK Core Theory V1

## 1. Shared-coordinate conflict

Let multiple functions be constrained to a shared phenotypic coordinate. Let `L >= 0` denote the fitness-scale compromise load identified for that shared architecture.

`L=0` means that no shared-axis conflict has been identified on the registered common fitness scale. `L>0` means that the shared coordinate imposes a positive compromise cost.

## 2. Recoverable conflict loss and architecture payoff

Let `R >= 0` denote the optimized amount of shared-coordinate compromise loss recovered by the declared differentiated architecture before charging its additional architecture-specific debit `K >= 0`, with both quantities expressed on the same fitness scale and comparison horizon.

Define the general architecture margin

```text
Phi = R-K.
```

Under the registered quadratic partial-release bridge only, let `s in [0,1]` denote the recoverable fraction of the shared compromise load. Then

```text
R = sL
Phi = sL-K.
```

The classification is

```text
L > 0, Phi < 0  persistent compromise world
Phi = 0         architecture critical surface
Phi > 0         differentiated architecture globally favored.
```

This classification concerns optimized architecture value. It does not yet imply evolutionary accessibility or population establishment. `R=sL` is not a universal identity for arbitrary landscapes.

## 3. Global value does not imply small-step accessibility

Let a local release coordinate be `d`, with recovery function `R(d)` and linear marginal architecture price `k`. Define

```text
k_local  = R'(0)
k_global = R(dmax)/dmax.
```

When recovery is convex and `R(0)=0`,

```text
k_local <= k_global.
```

If the inequality is strict, the interval

```text
k_local < k < k_global
```

is nonempty. Inside this interval,

```text
Phi'(0)<0
```

for release from the current architecture, while the endpoint margin satisfies

```text
Phi(dmax)>0.
```

Thus complete release can be globally favorable even though sufficiently small release steps are selectively downhill.

This is a local selective-accessibility statement under the declared release path, not a claim that drift, large mutations, recombination, or other developmental paths can never cross the barrier.

For the registered two-function quadratic barrier,

```text
W_k = s0(1-s0)Delta^2,
```

which is maximal at `s0=1/2`.

## 4. Architecture payoff and frequency-dependent population payoff

For a pair of endpoint architectures with intrinsic gap `Phi`, let symmetric frequency-dependent feedback be summarized by `eta`. The registered canonical selection difference is

```text
Delta(p) = Phi + eta(2p-1).
```

The rare-invasion surfaces are

```text
Phi = +eta
Phi = -eta.
```

Thus `Phi=0` is an architecture-value crossing, whereas invasion can switch at distinct population-dependent thresholds.

## 5. Deterministic phase distinction

For strict inequalities,

```text
Phi < -|eta|             first architecture dominance
Phi >  |eta|             second architecture dominance
|Phi| < |eta|, eta < 0   mutual invasibility / stable coexistence
|Phi| < |eta|, eta > 0   mutual non-invasibility / coordination bistability.
```

Therefore positive architecture value alone does not determine the population phase.

## 6. Finite-population fixation

Under the registered self-excluding exponential Moran process for a canonical symmetric architecture pair,

```text
rho_D / rho_S = exp[beta(N-2)Phi].
```

For `beta>0` and `N>2`,

```text
rho_D>rho_S
iff
Phi>0.
```

This reciprocal fixation ordering is distinct from rare invasion.

Under weak selection, absolute mutant advantage relative to neutrality follows the separate registered criterion

```text
rho_D>1/N
iff
3Phi>eta,
```

to first order in the weak-selection expansion.

## 7. Weak-mutation occupancy

For connected symmetric rare mutation among a finite set of architectures with symmetric game matrix `A`, define self-play score

```text
u_i = A_ii/2.
```

The monomorphic stationary law is

```text
Pi_i proportional to exp[beta(N-2)u_i].
```

For the registered canonical pair, `u_D-u_S=Phi`, so

```text
Pi_D>Pi_S
iff
Phi>0.
```

Off-diagonal interaction can still alter invasion, coexistence, transition rates, and metastability without changing these symmetric rare-mutation monomorphic weights.

## 8. Unified critical-surface theorem

For the registered composite model in `theory/UNIFIED_THRESHOLD_ATLAS_V1.md`, the same endpoint comparison encounters the following surfaces:

```text
small-step selective release       k = k_local
global endpoint value              k = k_global  <=> Phi = 0
rare D invasion                    Phi = eta
resistance to rare S invasion      Phi = -eta
reciprocal fixation ordering       Phi = 0
absolute fixation vs neutrality    3Phi = eta    [weak selection]
rare-mutation occupancy ordering   Phi = 0
```

This is the mathematical spine of SLK. Different evolutionary questions are not merely named differently; they are cut by different surfaces once new biological or population-level mechanisms enter.

At the same time, three later criteria re-align under the registered process:

```text
global endpoint D>S
iff
reciprocal fixation favors D
iff
symmetric rare-mutation occupancy favors D
iff
Phi>0.
```

This equality is conditional on the canonical equal-diagonal-feedback mapping, the declared exponential Moran process, and symmetric rare mutation. It is not a universal law outside those assumptions.

## 9. One-family constructive separation

The witness family

```text
d in [0,1]
R(d)=d+d^2
K(d)=k d
```

has

```text
k_local=1
k_global=2
Phi=2-k.
```

By varying only `k` and `eta`, it realizes all flagship non-implications:

```text
k=2.2                 -> L>0 can coexist with Phi<0
k=1.5                 -> Phi>0 but small release is downhill
k=0.8, eta=1.5        -> small release uphill + Phi>0, but no rare invasion
k=2.2, eta=-1         -> rare invasion, but reciprocal fixation favors S
k=2.1, eta=-0.5       -> absolute fixation advantage, but occupancy favors S
```

The proof details and claim boundaries are registered in `theory/UNIFIED_THRESHOLD_ATLAS_V1.md` and `theory/NON_EQUIVALENCE_THEOREM_V1.md`.

## 10. SLK hierarchy

The flagship theorem architecture is

```text
L
-> R
-> Phi=R-K
-> local accessibility
-> invasion
-> fixation
-> occupancy.
```

Under the registered quadratic bridge, the middle two steps reduce to `R=sL` and `Phi=sL-K`.

The strongest compact statement is not that all stages are generically different. It is:

```text
new mechanisms introduce new critical surfaces,
some adjacent criteria separate,
and the registered fixation-occupancy process forces one exact re-alignment.
```

## Claim boundary

This document migrates only the cross-repository mathematical spine. It does not claim universality beyond the declared model classes. Contextual-optimum identification, middle-world geometry, ecological mechanism identification, continuous branching, modular topology, and spatial/temporal transport remain owned by the sister repositories unless explicitly re-derived here.
