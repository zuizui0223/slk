# From functional conflict to evolutionary architecture: when does differentiation pay, and when does payoff become evolution?

## Abstract

Traits commonly contribute to multiple biological functions, but multifunctionality alone does not establish a trade-off, and a trade-off alone does not imply that differentiated architecture should evolve. We develop a unified framework that separates whether a shared-coordinate functional conflict exists, how much fitness is lost to compromise, how much of that loss can be recovered by an alternative architecture, whether recovery exceeds architecture-specific cost, whether the globally favorable architecture is locally reachable, and whether it can invade, fix, or dominate long-run occupancy. A shared-coordinate conflict is summarized by a compromise load `L`. Let `R` denote the optimized fitness loss recovered by a differentiated architecture before its additional architecture-specific debit `K`; the general architecture margin is `Phi=R-K`. In a registered quadratic partial-release bridge, `R=sL`, so `Phi=sL-K` follows as a model-specific corollary rather than a universal identity. The region `L>0, Phi<0` defines persistent compromise despite real conflict; `Phi>0` identifies global advantage of the declared differentiated comparison. We then derive explicit witness regimes showing that conflict need not imply profitable differentiation, profitable differentiation need not imply local accessibility, accessible positive intrinsic value need not imply rare invasion, and rare invasion need not imply reciprocal fixation superiority. Under weak selection, absolute mutant advantage over neutrality can also disagree with long-run monomorphic occupancy. However, under the registered symmetric rare-mutation exponential Moran process, reciprocal fixation ordering and stationary monomorphic occupancy ordering coincide exactly through the same self-play score difference. The resulting framework is therefore a hierarchy of evolutionary criteria containing both sharp separations and a process-level invariant, together with an empirical gate structure that prevents stronger claims from being inferred from weaker measurements.

**Claim map:** C1-C9 plus invariant INV1. Formal witnesses are registered in `theory/NON_EQUIVALENCE_THEOREM_V1.md`.

## 1. Introduction

A trait can perform several functions without those functions opposing one another. Even when opposing selection is real, the existence of compromise does not tell us whether adding phenotypic dimensions is worth the cost of maintaining a more complex architecture. And even when differentiation has higher optimized fitness, evolution may fail to reach it through available mutations or may reject it at the population level.

These questions have deep prior literatures. The modularity and evolvability literature has long emphasized that reducing pleiotropic interference among functions can improve adaptive potential (Wagner & Altenberg 1996). General theory of functional specialization has already identified conditions under which division of labor among modules is favored, including positional effects, accelerating performance functions, and synergistic interactions (Rueffler, Hermisson & Wagner 2012). Evolutionary-game and finite-population theory has separately distinguished invasion, fixation, and weak-mutation long-run behavior (Taylor et al. 2004; Fudenberg et al. 2006). SLK therefore does **not** claim a first theory of modularity, specialization, evolutionary games, fixation, or rare-mutation stationary dynamics.

The contribution here is the architecture-specific handoff between these literatures. We start from an empirically identified shared-coordinate conflict budget rather than assuming that multifunctionality implies conflict; separate recoverable architecture value from architecture-specific cost; then transport that value through local accessibility, frequency-dependent invasion, finite-population fixation, and weak-mutation occupancy. This construction lets us ask where successive criteria genuinely separate, where they re-align under an exact invariant, and what additional measurements are required before moving from one biological claim to the next.

Our central hierarchy is

```text
shared-coordinate conflict
-> compromise load L
-> recoverable loss R
-> architecture margin Phi=R-K
-> local accessibility
-> rare invasion
-> fixation
-> weak-mutation occupancy.
```

For the quadratic partial-release bridge only,

```text
R=sL,
Phi=sL-K.
```

The main theorem is therefore a structured split-and-invariant result rather than a slogan that every adjacent step differs (Fig. 1). The downward arrows in Fig. 1 are handoffs between estimands, not logical implications.

![Figure 1. SLK hierarchy showing genuine splits and the fixation-occupancy invariant.](../figures/FIG1_LOGIC_DIAGRAM.svg)

**Figure 1. From functional conflict to evolutionary outcome.** SLK separates inferential levels that are often collapsed. Positive `Phi` is not an evolutionary verdict: local mutational accessibility can fail even when complete differentiation has positive payoff; frequency-dependent feedback can shift rare-invasion boundaries away from the intrinsic architecture crossing; and finite-population fixation is governed by a process-specific rule. Dashed side boxes show explicit witness conditions for genuine non-implications. Under the registered reversible weak-mutation exponential-Moran model, reciprocal fixation ordering and long-run monomorphic occupancy ordering re-align because both depend on the same self-play score difference. Full caption and design specification are in `figures/FIG1_CAPTION_AND_SPEC.md`.

## 2. Identifying the conflict budget

**Claim C1 - EMPIRICAL HANDOFF.**

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the compromise load on a common fitness scale. `L=0` is the no-identified-conflict boundary; `L>0` means that forcing the functions onto one coordinate produces a positive fitness loss relative to the relevant function-specific benchmark.

The empirical interpretation of `L` requires causal care. Context-specific optima measured under selective environments are not automatically pure-function optima. In practice, the conflict budget should therefore be exported only from designs that identify opposing causal geometry or from explicitly bounded state-specific contrasts. The integrated theory starts from a valid `L` receipt; it does not redefine how that receipt is obtained.

**Ceiling:** SLK does not prove that a biological system has `L>0`; that conclusion must be imported from an identified SCH-style analysis.

## 3. Persistent compromise and the architecture crossing

**Claims C2 and C4 - DEFINITION / CLASSIFICATION plus architecture bridge.**

Let `R>=0` be the optimized shared-coordinate compromise loss recovered by the declared differentiated architecture **before** charging any additional debit specific to possessing, maintaining, regulating, or expressing that architecture. Let `K>=0` be that additional architecture-specific debit, measured on the same fitness scale and over the same comparison horizon. Define

```text
Phi=R-K.
```

Three regions follow:

```text
L=0                no identified shared-axis conflict
L>0, Phi<0         persistent compromise
Phi=0              architecture critical surface
Phi>0              differentiation globally favored.
```

The middle region is biologically important. Conflict is real, but it is still cheaper to tolerate compromise than to pay for additional architecture. Thus persistence of an integrated trait is not evidence that the functions are aligned; it can instead indicate that the declared differentiated alternative fails a cost-benefit test.

`K` is not a free biological label. Any empirical estimate must declare the shared and differentiated comparison states, fitness scale, time horizon, included cost channels, excluded channels, possible overlap with `R`, and uncertainty or bound. A cost already expressed through reduced recovered performance cannot be charged again in `K`. The operational receipt is specified in `docs/K_OPERATIONAL_DEFINITION_V1.md`.

**Ceiling:** `L>0, Phi<0` classifies a declared comparison; it does not by itself establish historical persistence, realized structural absence of differentiation, or a particular developmental mechanism.

## 4. Differentiation recovers only the conflict it actually releases

**Claims C3-C5 - GENERAL DEFINITION plus QUADRATIC COROLLARY and MODEL RESULT.**

The general framework does not require recovery to be a fixed fraction of `L`. It requires only an architecture comparison yielding a recoverable amount `R`, after which

```text
Phi=R-K.
```

A differentiated architecture is globally favored under the declared optimized comparison exactly when

```text
Phi>0 iff K<R.
```

The parameter `s` enters in the registered quadratic partial-release bridge. There, `s in [0,1]` is both the realized separation fraction and the recovered fraction of the one-axis compromise load, giving

```text
R=sL,
Phi=sL-K.
```

This is **Claim C3**, a quadratic corollary rather than an arbitrary-landscape identity. It provides a transparent worked bridge between measured conflict magnitude and partial release, but the flagship logic uses `Phi=R-K` as its general architecture-value coordinate.

Under the registered nested architecture comparison, **Claim C5** states that `Phi>0` means the differentiated architecture has higher globally optimized payoff than the declared shared comparison. Structural elaboration with weak functional decoupling can remain below the crossing even when full theoretical decoupling would be beneficial.

Figure 2 separates this architecture-value classification from later realization criteria. Panel A lives on the `L-Phi` plane. Panels B and C deliberately introduce additional coordinates, because local accessibility depends on release-path geometry and rare invasion depends on population feedback. Those later boundaries therefore cannot be drawn as universal extra lines in the same `L-Phi` plane.

![Figure 2. Architecture-value phase map with accessibility and invasion insets.](../figures/FIG2_PHASE_MAP.svg)

**Figure 2. Architecture-value classification and evolutionary realization require different coordinates.** The `L-Phi` plane classifies persistent compromise versus globally favorable differentiation. Accessibility and invasion require additional coordinates and are therefore shown as separate conditional insets rather than universal boundaries in the same phase plane. Full caption and specification are in `figures/FIG2_CAPTION_AND_SPEC.md`.

**Ceiling:** `Phi>0` is a global-value statement only. It is not shorthand for local reachability, invasion, fixation, occupancy, or historical evolution.

## 5. Global value can exceed local accessibility

**Claim C6 - THEOREM / MODEL RESULT.**

The architecture crossing is not yet an evolutionary transition. Let `d` measure release from the current integrated state, with recovery function `R(d)` and linear marginal architecture price `k`. Define

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

**Claim C7 - THEOREM / MODEL RESULT.**

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

**Claim C8 - THEOREM / PROCESS-SPECIFIC MODEL RESULT.**

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

## 8. Weak-mutation occupancy and a fixation-occupancy invariant

**Claim C9 - PROCESS-SPECIFIC STATIONARY RESULT; invariant INV1.**

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

This result sits inside a well-developed literature on finite-population evolutionary games and weak-mutation substitution processes; the SLK contribution is the exact placement of the invariant inside the architecture-value transport, not the invention of weak-mutation Markov-chain theory.

**Ceiling:** the invariant requires a finite symmetric game, connected symmetric rare mutation, and the registered exponential Moran fixation process.

## 9. Split-and-invariant theorem with explicit witnesses

### Theorem NE - evolutionary criteria separate at specific transitions

There exist admissible parameter regimes in which each of the following implications fails:

```text
L>0                         !=> Phi>0
Phi>0                       !=> local accessibility
accessible + Phi>0          !=> rare invasion
rare invasion               !=> reciprocal fixation superiority
absolute fixation advantage !=> greater weak-mutation occupancy.
```

Explicit witnesses are:

| Separation | Witness | Result |
|---|---|---|
| conflict -> payoff | `L=1, R=1/2, K=1` | `L>0` but `Phi=-1/2` |
| payoff -> accessibility | `s0=1/2, Delta=2, k=3/2` | `k_local=1<k<2=k_global` |
| accessible payoff -> invasion | `Phi=0.2, eta=0.5` | `Delta(0)=-0.3<0` |
| invasion -> reciprocal fixation | `Phi=-0.2, eta=-1` | `Delta(0)=0.8>0` but `rho_D/rho_S<1` |
| absolute fixation advantage -> occupancy | `Phi=-0.1, eta=-0.5` | `3Phi>eta`, yet `Pi_D<Pi_S` |

The final pair contains an important qualification: reciprocal fixation ordering itself does **not** diverge from stationary monomorphic occupancy ordering under connected symmetric rare mutation and the registered exponential Moran process. Both are controlled by the same self-play score difference.

So the flagship conclusion is not that every adjacent evolutionary statement is different. It is that the hierarchy contains four sharp separations plus one fixation-criterion split, followed by a process-level invariant that re-aligns reciprocal fixation and occupancy.

Full derivation and witnesses are registered in `theory/NON_EQUIVALENCE_THEOREM_V1.md`.

## 10. Empirical programme

**Empirical gates G1-G9; not a claim of completed end-to-end validation.**

SLK is deliberately cumulative. Each gate adds a new estimand and raises the ceiling of the biological claim; failure at a later gate does not erase what earlier gates established (Fig. 3).

![Figure 3. Empirical measurement ladder for SLK.](../figures/FIG3_EMPIRICAL_LADDER.svg)

**Figure 3. Sequential empirical validation of the SLK hierarchy.** G1 identifies a real shared-coordinate conflict; G2 estimates or bounds `L`; G3 quantifies recoverable architecture benefit `R` (and, where the quadratic bridge is justified, the partial-release fraction `s`); G4 defines architecture cost `K` on the same fitness scale; and G5 evaluates `Phi=R-K`. These first five gates are sufficient only for architecture-value classification. G6 introduces the local mutation/release neighborhood needed for accessibility claims. G7 measures rare-frequency performance and population feedback needed for invasion claims. G8 specifies the stochastic finite-population process needed for fixation claims, and G9 specifies the mutation graph/kernel needed for stationary occupancy. Full caption and gate table are in `figures/FIG3_CAPTION_AND_SPEC.md`.

The gate-specific claim ceilings are:

```text
G1 passed       -> a real shared-axis conflict is identified
G2 passed       -> conflict magnitude L is estimated or bounded
G3-G4 passed    -> recoverable benefit R and architecture cost K are separately quantified
G5 passed       -> persistent compromise or global differentiated advantage is classified
G6 passed       -> local reachability/trapping is identified under a declared path geometry
G7 passed       -> rare-invasion phase is identified under a declared population mapping
G8 passed       -> fixation statements are justified under an explicit finite-population process
G9 passed       -> weak-mutation monomorphic occupancy is justified under an explicit mutation graph/kernel.
```

This ordering prevents a common empirical shortcut: endpoint superiority at G5 cannot substitute for G6-G9. Likewise, a rare-invasion assay at G7 cannot by itself determine fixation or occupancy. Under the registered symmetric rare-mutation exponential-Moran model, reciprocal fixation ordering and occupancy ordering coincide, but that agreement is a theorem conditional on the process assumptions rather than permission to skip process specification.

**Current empirical ceiling:** no single biological system is claimed here to have passed G1-G9 end to end.

## 11. Discussion

The central contribution is not a new synonym for trade-off or modularity. Nor is it the generic statement that benefits must exceed costs. Existing work already explains why interference among functions can favor modularity or specialization, and existing population theory already separates invasion, fixation, and long-run stochastic behavior. The contribution is the explicit architecture-specific **estimand transport** that begins with a causally identified shared-coordinate conflict and preserves the extra assumptions needed at every later stage.

At the organismal scale, `L` asks whether integration is costly. At the architecture scale, `R` asks how much of that compromise an alternative architecture can recover, while `Phi=R-K` asks whether that recovery pays for the architecture-specific debit. At the mutational scale, accessibility asks whether the better architecture can be reached. At the population scale, invasion and fixation ask distinct establishment questions. At the long-run evolutionary scale, occupancy asks how often monomorphic states are expected under the registered mutation-selection process.

The framework therefore contributes three linked objects. First, it supplies a common handoff coordinate system without pretending that all quantities live on the same phase plane. Second, the constructive witnesses identify where apparently adjacent criteria genuinely diverge, while INV1 identifies a nontrivial condition under which reciprocal fixation and occupancy re-align. Third, G1-G9 translates the theory into a sequential empirical claim ladder, so that a study can stop at the strongest level its measurements actually justify.

This framing also sharpens what would falsify or limit the framework. If a biological system lacks an identified `L`, the architecture argument never starts. If `R` and `K` cannot be placed on a common fitness scale, `Phi` is not empirically evaluable. If mutation neighborhoods, population feedback, or stochastic process assumptions are unspecified, later evolutionary claims remain open even when endpoint architecture value is known. The hierarchy is therefore cumulative rather than all-or-nothing.

The three figures mirror the three levels of the contribution. Figure 1 gives the logic of split and invariant; Figure 2 gives the coordinate geometry of architecture value versus realization; Figure 3 gives the empirical ladder required to move from one claim level to the next. Together they make the framework mathematically explicit and experimentally falsifiable without claiming an end-to-end empirical demonstration that has not yet been performed.

### Claim-status summary

```text
C1      empirical handoff
C2      definition / classification
C3      quadratic corollary R=sL
C4      general architecture margin Phi=R-K
C5      global-value model result
C6      accessibility theorem / model result
C7      invasion theorem / model result
C8      process-specific fixation result
C9      process-specific occupancy result
INV1    reciprocal fixation <=> occupancy ordering under registered assumptions
G1-G9   empirical application gates
```

### Novelty boundary

SLK does not claim:

- the first theory of modularity or evolvability;
- the first theory of functional specialization or division of labor;
- the first distinction between invasion and fixation in finite populations;
- the first weak-mutation stationary distribution;
- universality of `R=sL` outside the declared quadratic bridge.

SLK does claim the integrated architecture-specific hierarchy from identified conflict to evolutionary realization, constructive split witnesses within the declared models, the placement of INV1 inside that hierarchy, and a gate-by-gate empirical claim ceiling.

### Scope boundary

The present paper deliberately excludes continuous-architecture branching, edgewise modular topology, spatial spectral invasion, temporal Floquet dynamics, detailed contextual-optimum identification, middle-world depth metrics, and ecological route identification after differentiation. Those are independent extensions developed in the sister repositories and are not required for the flagship argument.

## References cited in the novelty boundary

- Fudenberg, D., Nowak, M. A., Taylor, C. & Imhof, L. A. 2006. Evolutionary game dynamics in finite populations with strong selection and weak mutation. *Theoretical Population Biology* 70:352-363.
- Rueffler, C., Hermisson, J. & Wagner, G. P. 2012. Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109:E326-E335.
- Taylor, C., Fudenberg, D., Sasaki, A. & Nowak, M. A. 2004. Evolutionary game dynamics in finite populations. *Bulletin of Mathematical Biology* 66:1621-1644.
- Wagner, G. P. & Altenberg, L. 1996. Complex adaptations and the evolution of evolvability. *Evolution* 50:967-976.
