# SLK Core Theory V1

## 1. Shared-coordinate conflict

Let multiple functions be constrained to a shared phenotypic coordinate. Let `L >= 0` denote the fitness-scale compromise load identified for that shared architecture.

`L=0` means that no shared-axis conflict has been identified on the registered common fitness scale. `L>0` means that the shared coordinate imposes a positive compromise cost.

## 2. Recoverable conflict loss and architecture payoff

Let `s in [0,1]` denote the fraction of the shared compromise load recoverable by an accessible differentiated architecture, and let `K >= 0` denote the additional architecture cost on the same fitness scale.

Define

```text
R = sL
Phi = R-K = sL-K.
```

Then

```text
L > 0, Phi < 0  persistent compromise world
Phi = 0         architecture critical surface
Phi > 0         differentiated architecture globally favored.
```

This classification concerns optimized architecture value. It does not yet imply evolutionary accessibility or population establishment.

## 3. Global value does not imply local accessibility

Let a local release coordinate be `d`, with recovery function `R(d)` and linear marginal architecture price `k`. Define

```text
k_local  = R'(0)
k_global = R(dmax)/dmax.
```

When recovery is convex,

```text
k_local <= k_global.
```

Therefore a nonempty interval can exist:

```text
k_local < k < k_global.
```

Inside this interval, infinitesimal or small-step release is selected against even though complete release has positive global payoff. Hence

```text
Phi > 0
```

does not imply local evolutionary reachability.

For the registered two-function quadratic barrier,

```text
W_k = s0(1-s0)Delta^2,
```

which is maximal at `s0=1/2`.

## 4. Architecture payoff and frequency-dependent population payoff

For a pair of architectures with intrinsic gap `Phi`, let symmetric frequency-dependent feedback be summarized by `eta`. The canonical selection difference can be written

```text
Delta(p) = Phi + eta(2p-1).
```

The rare-invasion boundaries split from the static architecture boundary:

```text
Phi = +eta
Phi = -eta.
```

Thus `Phi=0` is an architecture-value crossing, whereas rare invasion can switch at distinct population-dependent thresholds.

## 5. Deterministic phase distinction

For strict inequalities,

```text
Phi < -|eta|             first architecture dominance
Phi >  |eta|             second architecture dominance
|Phi| < |eta|, eta < 0   stable coexistence
|Phi| < |eta|, eta > 0   coordination bistability.
```

Therefore positive architecture value alone does not determine the population phase.

## 6. Finite-population fixation

Under the registered exponential Moran process for a canonical symmetric architecture pair,

```text
rho_D / rho_S = exp[beta(N-2)Phi].
```

This establishes a fixation-ordering result that is distinct from rare invasion.

Under weak selection, absolute mutant advantage relative to neutrality follows a different criterion and must not be collapsed into reciprocal fixation ordering.

## 7. Weak-mutation occupancy

For connected symmetric rare mutation among a finite set of architectures with symmetric game matrix `A`, define self-play score

```text
u_i = A_ii/2.
```

The monomorphic stationary law is

```text
Pi_i proportional to exp[beta(N-2)u_i].
```

For zero-diagonal architecture feedback, `u_i` reduces to intrinsic architecture value. Off-diagonal interaction can still alter invasion, coexistence, transition rates, and metastability without changing these stationary monomorphic weights.

## 8. SLK hierarchy

The flagship theorem architecture is therefore not one threshold but a sequence:

```text
L
-> Phi=sL-K
-> local accessibility
-> invasion
-> fixation
-> occupancy.
```

The central non-equivalence statement is

```text
conflict exists
!= differentiation pays
!= differentiation is reachable
!= differentiation invades
!= differentiation fixes more often
!= differentiation dominates long-run occupancy.
```

## Claim boundary

This document migrates only the cross-repository mathematical spine. It does not claim universality beyond the declared model classes. Contextual-optimum identification, middle-world geometry, ecological mechanism identification, continuous branching, modular topology, and spatial/temporal transport remain owned by the sister repositories unless explicitly re-derived here.