# SLK non-equivalence theorem V1

## Purpose

The flagship hierarchy contains several distinct evolutionary statements, but not every adjacent pair is non-equivalent under every registered process. This document gives explicit witness regimes for the genuine separations and records the fixation–occupancy invariant that closes one apparent gap.

## Definitions

Use the SLK architecture margin

```text
Phi = sL-K.
```

For a canonical two-architecture population game,

```text
Delta(p)=Phi+eta(2p-1).
```

For the declared self-excluding exponential Moran process,

```text
rho_D/rho_S = exp[beta(N-2)Phi].
```

Under weak selection, absolute fixation advantage of a single D mutant over neutrality obeys

```text
rho_D > 1/N  iff  3Phi > eta.
```

Under connected symmetric rare mutation among a finite symmetric architecture game,

```text
Pi_i proportional to exp[beta(N-2)u_i],
u_i=A_ii/2.
```

## Theorem NE1 — conflict does not imply profitable differentiation

There exist parameters with

```text
L>0
```

but

```text
Phi<0.
```

Witness:

```text
L=1
s=1/2
K=1
Phi=-1/2.
```

Thus real shared-axis conflict can coexist with persistent compromise.

## Theorem NE2 — profitable differentiation does not imply local accessibility

For convex recovery, define

```text
k_local=R'(0)
k_global=R(dmax)/dmax.
```

Whenever

```text
k_local<k<k_global,
```

complete release has positive net payoff while sufficiently small release is selected against.

Quadratic witness:

```text
s0=1/2
Delta=2
k_local=s0^2 Delta^2=1
k_global=s0 Delta^2=2
k=3/2.
```

Hence global architecture advantage need not be reachable by local release mutations.

## Theorem NE3 — local accessibility and positive intrinsic architecture value do not imply rare invasion

Take a locally accessible architecture with no release barrier and choose

```text
Phi=0.2
eta=0.5.
```

Then D has positive intrinsic architecture value, but when rare

```text
Delta(0)=Phi-eta=-0.3<0.
```

So D cannot invade S from rarity. This is the coordination region.

## Theorem NE4 — rare invasion does not imply reciprocal fixation superiority

Choose

```text
Phi=-0.2
eta=-1.
```

Then

```text
Delta(0)=Phi-eta=0.8>0,
```

so D invades when rare. But for beta>0 and N>2,

```text
rho_D/rho_S=exp[beta(N-2)Phi]<1.
```

Thus D can invade S when rare while a D mutant fixes less often in S than an S mutant fixes in D.

## Theorem NE5 — absolute fixation advantage does not imply greater symmetric weak-mutation occupancy

Choose

```text
Phi=-0.1
eta=-0.5.
```

Under weak selection,

```text
3Phi=-0.3>eta=-0.5,
```

so a single D mutant has

```text
rho_D>1/N.
```

However `Phi<0`, so for the corresponding symmetric pair

```text
u_D-u_S=Phi<0,
```

and therefore under connected symmetric rare mutation

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

The correct SLK structure is therefore not a chain of universal pairwise non-equivalences. It is a branching hierarchy with both separations and one registered invariant:

```text
conflict L>0
   !=> Phi>0
          !=> local accessibility
                 !=> rare invasion
                        !=> reciprocal fixation superiority

absolute fixation advantage over neutrality
   !=> greater weak-mutation occupancy

but, under symmetric rare mutation + exponential Moran:
reciprocal fixation ordering
    <=> stationary monomorphic occupancy ordering.
```

The conceptual contribution is stronger when these distinctions are stated exactly: evolutionary criteria split where different biological mechanisms enter, and can re-align when a process-level invariant forces them to.