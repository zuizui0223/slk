# From functional conflict to evolutionary architecture: when does differentiation pay, and when does payoff become evolution?

## Abstract

Traits commonly contribute to multiple biological functions, but multifunctionality alone does not establish a trade-off, and a trade-off alone does not imply that differentiated architecture should evolve. We develop a unified framework that separates six questions that are often collapsed: whether a shared-coordinate functional conflict exists, how much fitness is lost to compromise, how much of that loss can be recovered by differentiation, whether the recovered loss exceeds architectural cost, whether the globally favorable architecture is locally reachable, and whether it can invade, fix, or dominate long-run occupancy. A shared-coordinate conflict is summarized by a compromise load `L`. If a differentiated architecture recovers fraction `s` of that load at added cost `K`, its intrinsic architecture margin is `Phi=sL-K`. The region `L>0, Phi<0` defines persistent compromise despite real conflict; `Phi>0` identifies global advantage of differentiation. We then show why that crossing is not an evolutionary verdict. Convex recovery can generate an accessibility gap in which complete differentiation is beneficial while all sufficiently small release steps are selected against. Frequency-dependent ecological feedback splits the static crossing into distinct rare-invasion boundaries, while finite-population fixation and weak-mutation occupancy obey still different criteria. The resulting hierarchy—`L -> Phi -> accessibility -> invasion -> fixation -> occupancy`—provides a common language for connecting experimentally identified functional conflict to the evolution of trait architecture without treating global optimality, local evolvability, and population establishment as equivalent.

## 1. Introduction

A trait can perform several functions without those functions opposing one another. Even when opposing selection is real, the existence of compromise does not tell us whether adding phenotypic dimensions is worth the cost of maintaining a more complex architecture. And even when differentiation has higher optimized fitness, evolution may fail to reach it through available mutations or may reject it at the population level.

These distinctions are usually studied in separate literatures: multifunctional trait conflict, modularity and division of labour, adaptive landscapes, evolutionary games, fixation, and mutation-selection dynamics. The separation is useful methodologically but obscures a simple causal sequence. A biological system must first contain recoverable conflict before differentiation can have a benefit. That benefit must exceed architecture cost before differentiation is globally worthwhile. A globally worthwhile architecture must still be accessible from the current state, and an accessible mutant must still invade, establish, and persist.

Here we integrate these steps in one hierarchy. The framework does not claim that every multifunctional trait should differentiate. Its purpose is the opposite: to state precisely which additional conditions are required at each transition and to show where apparently similar statements diverge.

Our central hierarchy is

```text
shared-coordinate conflict
-> compromise load L
-> recoverable loss R=sL
-> architecture margin Phi=sL-K
-> local accessibility
-> rare invasion
-> fixation
-> weak-mutation occupancy.
```

The main result is a non-equivalence theorem in conceptual form: each arrow introduces a new estimand, so success at one level does not guarantee success at the next.

## 2. Identifying the conflict budget

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the compromise load on a common fitness scale. `L=0` is the no-identified-conflict boundary; `L>0` means that forcing the functions onto one coordinate produces a positive fitness loss relative to the relevant function-specific benchmark.

The empirical interpretation of `L` requires causal care. Context-specific optima measured under selective environments are not automatically pure-function optima. In practice, the conflict budget should therefore be exported only from designs that identify opposing causal geometry or from explicitly bounded state-specific contrasts. The integrated theory starts from a valid `L` receipt; it does not redefine how that receipt is obtained.

## 3. Persistent compromise and the architecture crossing

Let `s in [0,1]` be the fraction of the shared compromise load recoverable by a differentiated architecture and let `K>=0` be its additional cost on the same fitness scale. Define

```text
R=sL
Phi=sL-K.
```

Three regions follow:

```text
L=0                no identified shared-axis conflict
L>0, Phi<0         persistent compromise
Phi=0              architecture critical surface
Phi>0              differentiation globally favored.
```

The middle region is biologically important. Conflict is real, but it is still cheaper to tolerate compromise than to pay for additional architecture. Thus the persistence of an integrated trait is not evidence that the functions are aligned; it can instead indicate that differentiation fails a cost-benefit test.

## 4. Differentiation recovers only the conflict it actually releases

The parameter `s` separates complete architectural freedom from realized partial differentiation. Additional trait dimensions do not imply complete functional independence. In the quadratic bridge, the realized separation fraction is also the recovered fraction of the one-axis compromise load, giving `R=sL`.

This makes the architecture threshold operationally transparent:

```text
Phi>0 iff K<sL.
```

The architecture therefore gains only from the portion of compromise that is actually released. Structural elaboration with weak functional decoupling can remain below the crossing even when full theoretical decoupling would be beneficial.

## 5. Global value can exceed local accessibility

The architecture crossing is not yet an evolutionary transition. Let `d` measure release from the current integrated state, with recovery function `R(d)` and linear marginal price `k`. Define

```text
k_local=R'(0)
k_global=R(dmax)/dmax.
```

For convex recovery, `k_local<=k_global`. Hence the interval

```text
k_local<k<k_global
```

can be nonempty. Inside it, all sufficiently small releases are selected against even though complete release has positive net payoff.

This produces a globally favorable but locally inaccessible architecture. In the registered two-function quadratic case, the barrier width is

```text
W_k=s0(1-s0)Delta^2,
```

maximized at intermediate residual integration, `s0=1/2`.

The result separates two questions that are often conflated: whether a differentiated architecture would be better if present, and whether evolution can reach it by locally available changes.

## 6. Population feedback splits the architecture boundary

Suppose two architectures differ intrinsically by `Phi` but also experience symmetric frequency-dependent ecological feedback summarized by `eta`. Their canonical selection difference is

```text
Delta(p)=Phi+eta(2p-1).
```

The static architecture boundary `Phi=0` then splits into two rare-invasion boundaries,

```text
Phi=+eta
Phi=-eta.
```

The population phase is therefore not determined by architecture value alone. Depending on `eta`, the system can show dominance, stable coexistence, or coordination bistability.

## 7. Fixation is another estimand

In finite populations, invasion when rare and fixation ordering need not coincide. Under the registered exponential Moran process for the canonical symmetric pair,

```text
rho_D/rho_S=exp[beta(N-2)Phi].
```

Thus reciprocal fixation ordering has a particularly simple dependence on intrinsic architecture value, while absolute mutant advantage relative to neutrality can obey a different criterion. Population size and stochasticity therefore add a distinct layer rather than merely adding noise around deterministic invasion.

## 8. Long-run occupancy need not equal accessibility

Under connected symmetric rare mutation among architectures, the monomorphic stationary law can be written in terms of self-play scores `u_i=A_ii/2`:

```text
Pi_i proportional to exp[beta(N-2)u_i].
```

For zero-diagonal interaction feedback this reduces to intrinsic architecture value. Off-diagonal ecological interactions can still alter invasion, coexistence, substitution rates, and metastability while cancelling from these long-run monomorphic weights.

A globally favored architecture can therefore have high stationary weight yet remain difficult to reach from a particular starting topology. Long-run abundance and evolutionary accessibility answer different questions.

## 9. A hierarchy of non-equivalent evolutionary statements

The integrated framework can be summarized as

```text
conflict exists
!= differentiation pays
!= differentiation is reachable
!= differentiation invades
!= differentiation fixes more often
!= differentiation dominates long-run occupancy.
```

Each inequality is constructive: the model contains explicit parameter regions in which the statement on the left is true and the statement on the right is false.

This hierarchy clarifies why apparently contradictory empirical patterns can coexist. Persistent multifunctional compromise can occur under real conflict; globally superior differentiated architectures can remain evolutionarily trapped; invasion and fixation can disagree; and long-run occupancy can favor architectures that are difficult to access from a specific ancestral state.

## 10. Empirical programme

The framework suggests a sequential rather than all-at-once empirical strategy.

First, identify a shared-coordinate conflict and estimate a fitness-scale compromise budget `L`. Second, quantify how much of that budget an experimentally accessible differentiated architecture recovers and estimate its added cost `K`. Third, test local release steps rather than inferring accessibility from endpoint comparisons. Fourth, estimate frequency-dependent performance where population feedback is plausible. Finally, distinguish invasion assays, fixation proxies, and long-run occupancy rather than treating them as interchangeable evidence.

The framework is therefore designed to turn a broad question—why multifunctional traits remain integrated or become differentiated—into a sequence of falsifiable measurements.

## 11. Discussion

The central contribution is not a new synonym for trade-off or modularity. It is a bridge between causal functional conflict and evolutionary architecture that preserves the distinctions introduced by each biological scale.

At the organismal scale, `L` asks whether integration is costly. At the architecture scale, `Phi=sL-K` asks whether differentiation is worth that cost. At the mutational scale, accessibility asks whether the better architecture can be reached. At the population scale, invasion and fixation ask whether it can establish. At the long-run evolutionary scale, occupancy asks how often it is expected to be observed under recurrent mutation and selection.

Treating these as one question creates false paradoxes. Separating them yields a phase-structured theory of trait architecture.

### Scope boundary

The present paper deliberately excludes continuous-architecture branching, edgewise modular topology, spatial spectral invasion, temporal Floquet dynamics, detailed contextual-optimum identification, middle-world depth metrics, and ecological route identification after differentiation. Those are independent extensions developed in the sister repositories and are not required for the flagship argument.