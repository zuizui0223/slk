# SLK non-equivalence theorem V1

## Purpose

The flagship hierarchy contains several distinct evolutionary statements, but not every adjacent pair is non-equivalent under every registered process. This document records explicit witness regimes for the genuine separations and the fixation-occupancy invariant that closes one apparent gap.

The witnesses are now embedded in the single registered family in `theory/UNIFIED_THRESHOLD_ATLAS_V1.md`, so the flagship no longer relies on disconnected toy examples.

## Definitions

Use the general SLK architecture margin

```text
Phi = R-K.
```

Under the registered quadratic partial-release bridge only,

```text
R=sL,
Phi=sL-K.
```

For the registered canonical two-architecture population game,

```text
Delta(p)=Phi+eta(2p-1).
```

For the declared self-excluding exponential Moran process,

```text
rho_D/rho_S = exp[beta(N-2)Phi].
```

Under weak selection, absolute fixation advantage of a single D mutant over neutrality obeys the registered first-order criterion

```text
rho_D > 1/N  iff  3Phi > eta.
```

Under connected symmetric rare mutation among a finite symmetric architecture game,

```text
Pi_i proportional to exp[beta(N-2)u_i],
u_i=A_ii/2.
```

## Common constructive family

Use throughout

```text
d in [0,1],
R(d)=d+d^2,
K(d)=k d.
```

Then

```text
k_local=R'(0)=1,
k_global=R(1)=2,
Phi=R(1)-K(1)=2-k.
```

When an upstream conflict budget is required, set `L=2`, so `R(1)=L`.

This one family supplies NE1-NE5.

## Theorem NE1 — conflict does not imply profitable differentiation

Choose

```text
L=2,
k=2.2.
```

Then

```text
R(1)=2,
K(1)=2.2,
Phi=-0.2.
```

Thus

```text
L>0
```

does not imply

```text
Phi>0.
```

The mathematical point is a non-implication; the biological point is that a real conflict budget can be cheaper to tolerate than to recover with the declared differentiated architecture.

## Theorem NE2 — profitable differentiation does not imply small-step selective accessibility

For convex recovery define

```text
k_local=R'(0),
k_global=R(dmax)/dmax.
```

Convexity with `R(0)=0` gives

```text
k_local<=k_global.
```

Whenever

```text
k_local<k<k_global,
```

the endpoint has positive net value while sufficiently small release steps are selectively downhill.

In the common family choose

```text
k=1.5.
```

Then

```text
Phi=0.5>0,
Phi'(0)=1-1.5=-0.5<0.
```

Hence global architecture advantage need not imply accessibility through sufficiently small selectively uphill release steps.

This does not prove absolute historical unreachability by drift, large mutations, recombination, or other paths.

## Theorem NE3 — small-step accessibility and positive intrinsic architecture value do not imply rare invasion

Use the same architecture family and choose

```text
k=0.8,
eta=1.5.
```

Then

```text
Phi=1.2>0
```

and the release direction is locally uphill because

```text
Phi'(0)=1-0.8=0.2>0.
```

But when D is rare,

```text
Delta(0)=Phi-eta=1.2-1.5=-0.3<0.
```

Thus the same explicit architecture model is both locally accessible and globally favorable before population feedback, yet D cannot invade S from rarity after the registered frequency-dependent interaction is introduced.

## Theorem NE4 — rare invasion does not imply reciprocal fixation superiority

Use the same architecture family and choose

```text
k=2.2,
eta=-1.
```

Then

```text
Phi=-0.2
```

but

```text
Delta(0)=Phi-eta=0.8>0,
```

so D invades when rare.

For `beta>0` and `N>2`,

```text
rho_D/rho_S
=exp[beta(N-2)Phi]
<1.
```

Thus D can invade S from rarity while a D mutant fixes less often in S than an S mutant fixes in D.

## Theorem NE5 — absolute fixation advantage does not imply greater symmetric weak-mutation occupancy

Use the same architecture family and choose

```text
k=2.1,
eta=-0.5.
```

Then

```text
Phi=-0.1
```

and, under the registered weak-selection criterion,

```text
3Phi=-0.3>eta=-0.5.
```

Therefore a single D mutant has

```text
rho_D>1/N
```

to first order in the weak-selection expansion.

However `Phi<0`, so for the corresponding symmetric pair

```text
u_D-u_S=Phi<0
```

and under connected symmetric rare mutation

```text
Pi_D<Pi_S.
```

Thus absolute mutant advantage over neutrality and long-run monomorphic occupancy answer different questions.

## Theorem INV1 — reciprocal fixation ordering and symmetric weak-mutation occupancy ordering coincide

For any allowed pair `i,j` in the registered finite symmetric architecture game with symmetric rare mutation,

```text
rho(j|i)/rho(i|j)
=exp[beta(N-2)(u_j-u_i)]
```

and

```text
Pi_j/Pi_i
=exp[beta(N-2)(u_j-u_i)].
```

Therefore

```text
rho(j|i)>rho(i|j)
iff
Pi_j>Pi_i.
```

So reciprocal fixation ordering is not another independent split from occupancy under this declared process. It is an invariant bridge between pairwise substitution bias and stationary monomorphic weight.

This equivalence breaks if the assumptions used for the Gibbs law are changed, for example under non-reversible mutation bias, non-rare mutation, non-symmetric games, or when polymorphic states cannot be collapsed to a monomorphic substitution chain.

## Flagship synthesis

The non-equivalence results are now a corollary of a common threshold atlas rather than a list of unrelated examples:

```text
small-step release surface       k=k_local
global endpoint-value surface    k=k_global  <=> Phi=0
rare-D-invasion surface          Phi=eta
reverse-invasion surface         Phi=-eta
reciprocal-fixation surface      Phi=0
absolute-fixation surface        3Phi=eta    [weak selection]
rare-mutation occupancy surface  Phi=0
```

The correct SLK structure is therefore a hierarchy with both separations and one registered re-alignment:

```text
conflict L>0
   !=> Phi>0
          !=> small-step accessibility
                 !=> rare invasion
                        !=> reciprocal fixation superiority

absolute fixation advantage over neutrality
   !=> greater weak-mutation occupancy

but, under symmetric rare mutation + exponential Moran:
reciprocal fixation ordering
    <=> stationary monomorphic occupancy ordering.
```

See `theory/UNIFIED_THRESHOLD_ATLAS_V1.md` for the master critical-surface theorem and its proof.
