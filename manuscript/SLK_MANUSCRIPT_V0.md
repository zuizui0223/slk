# From functional conflict to evolutionary architecture: when does differentiation pay, and when does payoff become evolution?

## Abstract

Traits commonly contribute to multiple biological functions, but multifunctionality alone does not establish a trade-off, and a trade-off alone does not imply that differentiated architecture should evolve. We develop a unified framework that separates whether a shared-coordinate functional conflict exists, how much fitness is lost to compromise, how much of that loss can be recovered by differentiation, whether recovery exceeds architectural cost, whether the globally favorable architecture is locally reachable, and whether it can invade, fix, or dominate long-run occupancy. A shared-coordinate conflict is summarized by a compromise load `L`. If a differentiated architecture recovers fraction `s` of that load at added cost `K`, its intrinsic architecture margin is `Phi=sL-K`. The region `L>0, Phi<0` defines persistent compromise despite real conflict; `Phi>0` identifies global advantage of differentiation. We then derive explicit witness regimes showing that conflict need not imply profitable differentiation, profitable differentiation need not imply local accessibility, local accessibility plus positive intrinsic value need not imply rare invasion, and rare invasion need not imply reciprocal fixation superiority. Under weak selection, absolute mutant advantage over neutrality can also disagree with long-run monomorphic occupancy. However, under the registered symmetric rare-mutation exponential Moran process, reciprocal fixation ordering and stationary monomorphic occupancy ordering coincide exactly through the same self-play score difference. The resulting framework is therefore not a chain of universal non-equivalences but a hierarchy of evolutionary criteria containing both sharp separations and a process-level invariant.

**Claim map:** C1–C9 plus invariant INV1. Formal witnesses are registered in `theory/NON_EQUIVALENCE_THEOREM_V1.md`.

## 1. Introduction

A trait can perform several functions without those functions opposing one another. Even when opposing selection is real, the existence of compromise does not tell us whether adding phenotypic dimensions is worth the cost of maintaining a more complex architecture. And even when differentiation has higher optimized fitness, evolution may fail to reach it through available mutations or may reject it at the population level.

These distinctions are usually studied in separate literatures: multifunctional trait conflict, modularity and division of labour, adaptive landscapes, evolutionary games, fixation, and mutation-selection dynamics. The separation is useful methodologically but obscures a simple causal sequence. A biological system must first contain recoverable conflict before differentiation can have a benefit. That benefit must exceed architecture cost before differentiation is globally worthwhile. A globally worthwhile architecture must still be accessible from the current state, and an accessible mutant must still invade and establish. Some later criteria remain distinct, while others can re-align under specific process assumptions.

Here we integrate these steps in one hierarchy. The framework does not claim that every multifunctional trait should differentiate. Its purpose is the opposite: to state precisely which additional conditions are required at each transition, construct parameter regions where apparently similar statements diverge, and identify where a process-level invariant forces two criteria to agree.

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

The main theorem is therefore a structured non-equivalence result rather than a slogan that every adjacent step differs (Fig. 1). The downward arrows in Fig. 1 are handoffs between estimands, not logical implications.

![Figure 1. SLK hierarchy showing genuine splits and the fixation–occupancy invariant.](../figures/FIG1_LOGIC_DIAGRAM.svg)

**Figure 1. From functional conflict to evolutionary outcome.** SLK separates six inferential levels that are often collapsed. Positive `Phi` is not an evolutionary verdict: local mutational accessibility can fail even when complete differentiation has positive payoff; frequency-dependent feedback can shift rare-invasion boundaries away from the intrinsic architecture crossing; and finite-population fixation is governed by a process-specific rule. Dashed side boxes show explicit witness conditions for genuine non-implications. Under the registered reversible weak-mutation exponential-Moran model, reciprocal fixation ordering and long-run monomorphic occupancy ordering re-align because both depend on the same self-play score difference. Full caption and design specification are in `figures/FIG1_CAPTION_AND_SPEC.md`.

## 2. Identifying the conflict budget

**Claim C1 — EMPIRICAL HANDOFF.**

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the compromise load on a common fitness scale. `L=0` is the no-identified-conflict boundary; `L>0` means that forcing the functions onto one coordinate produces a positive fitness loss relative to the relevant function-specific benchmark.

The empirical interpretation of `L` requires causal care. Context-specific optima measured under selective environments are not automatically pure-function optima. In practice, the conflict budget should therefore be exported only from designs that identify opposing causal geometry or from explicitly bounded state-specific contrasts. The integrated theory starts from a valid `L` receipt; it does not redefine how that receipt is obtained.

**Ceiling:** SLK does not prove that a biological system has `L>0`; that conclusion must be imported from an identified SCH-style analysis.

## 3. Persistent compromise and the architecture crossing

**Claims C2 and C4 — DEFINITION / CLASSIFICATION plus model bridge.**

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

**Ceiling:** `L>0, Phi<0` classifies a declared comparison; it does not by itself establish historical persistence, realized structural absence of differentiation, or a particular developmental mechanism.

## 4. Differentiation recovers only the conflict it actually releases

**Claims C3–C5 — COROLLARY plus MODEL RESULT.**

The parameter `s` separates complete architectural freedom from realized partial differentiation. Additional trait dimensions do not imply complete functional independence. In the quadratic bridge, the realized separation fraction is also the recovered fraction of the one-axis compromise load, giving

```text
R=sL.
```

This is **Claim C3**, a quadratic corollary rather than an arbitrary-landscape identity.

The architecture margin is

```text
Phi=R-K,
```

and under the quadratic bridge

```text
Phi=sL-K.
```

This is **Claim C4**.

The architecture threshold is therefore

```text
Phi>0 iff K<sL.
```

Under the registered nested architecture comparison, **Claim C5** states that `Phi>0` means the differentiated architecture has higher globally optimized payoff than the declared shared comparison.

The architecture therefore gains only from the portion of compromise that is actually released. Structural elaboration with weak functional decoupling can remain below the crossing even when full theoretical decoupling would be beneficial.

Figure 2 separates this architecture-value classification from the later realization criteria. Panel A lives entirely on the `L–Phi` plane. Panels B and C deliberately introduce additional coordinates, because local accessibility depends on release-path geometry and rare invasion depends on population feedback. Those later boundaries therefore cannot be drawn as universal extra lines in the same `L–Phi` plane.

![Figure 2. Architecture-value phase map with accessibility and invasion insets.](../figures/FIG2_PHASE_MAP.svg)

**Figure 2. Architecture-value classification and evolutionary realization require different coordinates.** The `L–Phi` plane classifies persistent compromise versus globally favorable differentiation. Accessibility and invasion require additional coordinates and are therefore shown as separate conditional insets rather than universal boundaries in the same phase plane. Full caption and specification are in `figures/FIG2_CAPTION_AND_SPEC.md`.

**Ceiling:** `Phi>0` is a global-value statement only. It is not shorthand for local reachability, invasion, fixation, occupancy, or historical evolution.

## 5. Global value can exceed local accessibility

**Claim C6 — THEOREM / MODEL RESULT.**

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

**Ceiling:** accessibility is conditional on the declared mutation/release neighborhood and path geometry.

## 6. Population feedback splits the architecture boundary

**Claim C7 — THEOREM / MODEL RESULT.**

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

**Ceiling:** the split requires the registered symmetric pair mapping and an identified or declared population-feedback term.

## 7. Fixation is another estimand

**Claim C8 — THEOREM / PROCESS-SPECIFIC MODEL RESULT.**

In finite populations, invasion when rare and fixation ordering need not coincide. Under the registered exponential Moran process for the canonical symmetric pair,

```text
rho_D/rho_S=exp[beta(N-2)Phi].
```

Thus reciprocal fixation ordering depends on intrinsic architecture value, whereas rare invasion depends on both `Phi` and `eta`. Under weak selection, absolute mutant advantage relative to neutrality follows another criterion,

```text
rho_D>1/N iff 3Phi>eta.
```

The distinction between reciprocal fixation ordering and absolute fixation advantage matters for the final transport step.

**Ceiling:** these fixation results are specific to the declared Moran mapping.

## 8. Weak-mutation occupancy and a fixation–occupancy invariant

**Claim C9 — PROCESS-SPECIFIC STATIONARY RESULT; invariant INV1.**

Under connected symmetric rare mutation among architectures, the monomorphic stationary law can be written in terms of self-play scores `u_i=A_ii/2`:

```text
Pi_i proportional to exp[beta(N-2)u_i].
```

For any allowed pair `i,j`, the same self-play difference determines the reciprocal fixation ratio:

```text
rho(j|i)/rho(i|j)
=exp[beta(N-2)(u_j-u_i)],
```

so

```text
rho(j|i)>rho(i|j)
iff
Pi_j>Pi_i.
```

Thus reciprocal fixation ordering and symmetric weak-mutation monomorphic occupancy ordering are not independent under this registered process; they coincide exactly. By contrast, absolute fixation advantage over neutrality can disagree with occupancy ordering because it depends on `eta` as well as `Phi` under weak selection.

**Ceiling:** the invariant requires a finite symmetric game, connected symmetric rare mutation, and the registered exponential Moran fixation process.

## 9. Non-equivalence theorem with explicit witnesses

### Theorem NE — evolutionary criteria separate at specific transitions

There exist admissible parameter regimes in which each of the following implications fails:

```text
L>0                   !=> Phi>0
Phi>0                 !=> local accessibility
accessible + Phi>0    !=> rare invasion
rare invasion         !=> reciprocal fixation superiority
absolute fixation advantage !=> greater weak-mutation occupancy.
```

Explicit witnesses are:

| Separation | Witness | Result |
|---|---|---|
| conflict -> payoff | `L=1, s=1/2, K=1` | `L>0` but `Phi=-1/2` |
| payoff -> accessibility | `s0=1/2, Delta=2, k=3/2` | `k_local=1<k<2=k_global` |
| accessible payoff -> invasion | `Phi=0.2, eta=0.5` | `Delta(0)=-0.3<0` |
| invasion -> reciprocal fixation | `Phi=-0.2, eta=-1` | `Delta(0)=0.8>0` but `rho_D/rho_S<1` |
| absolute fixation advantage -> occupancy | `Phi=-0.1, eta=-0.5` | `3Phi>eta`, yet `Pi_D<Pi_S` |

The final pair contains an important qualification: reciprocal fixation ordering itself does **not** diverge from stationary monomorphic occupancy ordering under connected symmetric rare mutation and the registered exponential Moran process. Both are controlled by the same self-play score difference.

So the flagship conclusion is not that every adjacent evolutionary statement is different. It is that the hierarchy contains **four sharp separations plus one fixation-criterion split, followed by a process-level invariant that re-aligns reciprocal fixation and occupancy**.

Full derivation and witnesses are registered in `theory/NON_EQUIVALENCE_THEOREM_V1.md`.

## 10. Empirical programme

**Empirical gates G1–G9; not a claim of completed end-to-end validation.**

The framework suggests a sequential rather than all-at-once empirical strategy.

First, identify a shared-coordinate conflict and estimate a fitness-scale compromise budget `L` (`G1–G2`). Second, quantify how much of that budget an experimentally accessible differentiated architecture recovers and estimate its added cost `K` (`G3–G5`). Third, test local release steps rather than inferring accessibility from endpoint comparisons (`G6`). Fourth, estimate frequency-dependent performance where population feedback is plausible (`G7`). Finally, distinguish rare invasion, reciprocal fixation ordering, absolute fixation advantage, and long-run occupancy by explicitly specifying the relevant process and mutation connectivity (`G8–G9`).

**Current empirical ceiling:** no single biological system is claimed here to have passed G1–G9 end to end.

## 11. Discussion

The central contribution is not a new synonym for trade-off or modularity. It is a bridge between causal functional conflict and evolutionary architecture that preserves the distinctions introduced by each biological scale.

At the organismal scale, `L` asks whether integration is costly. At the architecture scale, `Phi=sL-K` asks whether differentiation is worth that cost. At the mutational scale, accessibility asks whether the better architecture can be reached. At the population scale, invasion and fixation ask whether it can establish. At the long-run evolutionary scale, occupancy asks how often monomorphic states are expected under the registered mutation-selection process.

Treating all of these as one question creates false paradoxes. Treating all of them as automatically different is also too crude. The exact structure is more informative: some criteria genuinely separate because a new mechanism enters, whereas reciprocal fixation and symmetric rare-mutation occupancy re-align under an exact invariant.

### Claim-status summary

```text
C1      empirical handoff
C2      definition / classification
C3      quadratic corollary
C4      definition + quadratic bridge
C5      global-value model result
C6      accessibility theorem / model result
C7      invasion theorem / model result
C8      process-specific fixation result
C9      process-specific occupancy result
INV1    reciprocal fixation <=> occupancy ordering under registered assumptions
G1-G9   empirical application gates
```

### Scope boundary

The present paper deliberately excludes continuous-architecture branching, edgewise modular topology, spatial spectral invasion, temporal Floquet dynamics, detailed contextual-optimum identification, middle-world depth metrics, and ecological route identification after differentiation. Those are independent extensions developed in the sister repositories and are not required for the flagship argument.