# Why multifunctional structures persist under conflicting selection

## Abstract

Biological structures often perform several functions whose optima conflict. One possible response is division of labor: duplicated genes can specialize, sexes can evolve different expression programs, and floral organs can differentiate into distinct functional types. Yet many systems remain multifunctional despite clear opposing selection. Why? We distinguish three biological explanations that produce the same observed persistence. First, a differentiated architecture may fail to recover enough of the conflict to repay the cost of maintaining additional structure or regulation. Second, a differentiated endpoint may have higher fitness but be unreachable through sufficiently small selectively favorable changes. Third, a reachable differentiated type may still fail to establish when rare because its ecological performance depends on frequency. These alternatives imply that conflict magnitude alone cannot rank systems by their propensity to differentiate, and that persistent multifunctionality is not evidence for weak conflict or for any single evolutionary constraint. We formalize the distinction using a common fitness comparison, derive environmental predictions for when profitability and establishment diverge, and translate the theory into measurements that discriminate among the three explanations. The aim is not a new theory of trade-offs or specialization, but a biological account of why functional conflict is sometimes resolved by division of labor and sometimes retained as multifunctional compromise.

## 1. Introduction

In the subalpine herb *Pedicularis rex*, flowers sit above cup-like bracts that collect rainwater. The water protects developing fruits from seed predators, but pollinators favor greater corolla exsertion above the protective bracts. Across 14 populations, greater exsertion was associated with greater pollen receipt and also with greater seed predation: the same floral axis is pulled in opposite directions by mutualists and antagonists (Sun, Armbruster, and Huang 2016). Experimentally draining the bracts increased seed predation, confirming that the water-filled structure contributes to defense (Sun and Huang 2015). This is a concrete multifunctional compromise. The interesting evolutionary question is not simply whether conflict exists, but why conflict of this kind sometimes produces separate functional structures and sometimes remains embedded in one architecture.

Biology contains many versions of this problem. In heterantherous flowers, distinct anther types can divide pollen-feeding and pollen-transfer functions, although alternative functions such as staggered pollen presentation show that morphological differentiation alone does not prove division of labor (Vallejo-Marín et al. 2009; Kay et al. 2020). At the molecular level, gene duplication can allow descendant copies to escape an adaptive conflict that constrained a multifunctional ancestral protein (Des Marais and Rausher 2008). In sexually antagonistic traits, sex-biased or sex-specific regulation can decouple phenotypes that were previously constrained by a shared genome. Across these systems, differentiation is one possible evolutionary resolution of conflicting functional demands.

The basic conditions favoring specialization are already well developed. General theory shows that division of labor depends on performance curvature, positional effects, and synergistic interactions among modules (Rueffler, Hermisson, and Wagner 2012). Models of pleiotropy likewise show that multifunctionality or specialization depends on the shape of functional trade-offs and on how component performance maps to fitness; complete subfunctionalization is expected only under restricted conditions (Guillaume and Otto 2012). We therefore do not claim that functional conflict automatically produces specialization, or that specialization is favored whenever a verbal trade-off is present. Nor do we claim a first connection between trade-off geometry and invasion: adaptive-dynamics and trade-off–invasion theory already distinguish a phenotype's performance from its ability to invade an ecological background (Dieckmann and Law 1996; Bowers et al. 2005).

We instead organize these results around a narrower biological problem: **what does it mean when a multifunctional structure remains integrated despite documented conflict?** The same observation can arise for at least three different reasons. A split may simply not pay: the fitness recovered by separating functions may be smaller than the additional structural, developmental, regulatory, or maintenance cost of doing so. A split may pay at the endpoint but be difficult to reach: small changes away from the integrated state can initially reduce fitness even when a more differentiated endpoint would be superior. Or a differentiated type may be reachable and intrinsically favorable yet fail to spread from rarity because pollinators, competitors, enemies, or other ecological partners change its fitness when it is uncommon. These are different biological explanations, not different names for the same constraint.

This distinction changes how conflict should be interpreted comparatively. Stronger opposing selection need not imply a greater tendency toward division of labor, because systems can differ in how much of the conflict differentiation actually releases and in the cost of the alternative architecture. Likewise, the ecological position where differentiation becomes profitable need not coincide with the position where a rare differentiated type can establish. Persistent multifunctionality is therefore an outcome that must be diagnosed, rather than a direct measure of conflict strength or evolutionary constraint.

The core biological sequence in this paper is

```text
functional conflict
-> fitness that division of labor could recover
-> cost of the differentiated architecture
-> net value of differentiation
-> evolutionary reachability
-> establishment when rare.
```

We denote the conflict load by `L`, the recoverable component by `R`, the architecture-specific cost by `K`, and the net value of differentiation by `Phi=R-K`. The first three steps answer whether division of labor would be worth having; the next two ask whether a favorable differentiated state can actually evolve and establish. Finite-population fixation and long-run occupancy are retained later as process-specific downstream extensions, but they are not the biological premise of the paper.

The resulting theory is used for two purposes. First, it identifies the measurements needed to distinguish the three explanations for persistent multifunctionality. Second, it generates comparative and environmental predictions: conflict magnitude can be decoupled from differentiation when recoverability or architecture cost varies, and frequency-dependent ecology can displace establishment from the environment where differentiation first becomes profitable. Figure 1 summarizes the formal thresholds supporting these biological alternatives; the equations are tools for separating explanations, not the subject of the paper.

![](../figures/FIG1_LOGIC_DIAGRAM.svg)

**Figure 1. One architecture comparison crosses different evolutionary thresholds.** The same comparison is transported from identified conflict through endpoint value, small-step selective accessibility, invasion, fixation, and occupancy. Exact critical surfaces are shown beside each stage: `Phi=0` for endpoint value, `k=k_local` for sufficiently small release, `Phi=±eta` for reciprocal invasion boundaries, `Phi=0` for reciprocal fixation ordering, `3Phi=eta` for absolute fixation advantage under weak selection, and `Phi=0` for symmetric rare-mutation occupancy. The repeated `Phi=0` surface marks the exact re-alignment of endpoint value, reciprocal fixation ordering, and occupancy under the registered process. The left panel shows that all five non-implications can be realized in one convex recovery family.

## 2. Is the functional conflict real?

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the compromise load on a common fitness scale. `L=0` is the no-identified-conflict boundary; `L>0` means that forcing the functions onto one coordinate produces a positive fitness loss relative to the relevant function-specific benchmark.

The empirical interpretation of `L` requires causal care. Context-specific optima measured under selective environments are not automatically pure-function optima. In practice, the conflict budget should therefore be exported only from designs that identify opposing causal geometry or from explicitly bounded state-specific contrasts. The integrated theory starts from a valid `L` receipt; it does not redefine how that receipt is obtained. Thus the present framework does not prove that a biological system has `L>0`; that conclusion must be imported from an identified analysis of shared-coordinate conflict.

## 3. Would division of labor pay?

Let `R>=0` be the optimized shared-coordinate compromise loss recovered by the declared differentiated architecture before charging any additional debit specific to possessing, maintaining, regulating, or expressing that architecture. Let `K>=0` be that additional architecture-specific debit, measured on the same fitness scale and over the same comparison horizon. Define

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

`K` is not a free biological label. Any empirical estimate must declare the shared and differentiated comparison states, fitness scale, time horizon, included cost channels, excluded channels, possible overlap with `R`, and uncertainty or bounds. A cost already expressed through reduced recovered performance cannot be charged again in `K`. Accordingly, `L>0, Phi<0` classifies a declared comparison; it does not by itself establish historical persistence, realized structural absence of differentiation, or a particular developmental mechanism.

## 4. How much of the conflict can differentiation actually release?

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

This is a quadratic corollary rather than an arbitrary-landscape identity. It provides a transparent worked bridge between measured conflict magnitude and partial release, but the general architecture-value coordinate remains `Phi=R-K`.

Under the registered nested architecture comparison, `Phi>0` means the differentiated architecture has higher globally optimized payoff than the declared shared comparison. Structural elaboration with weak functional decoupling can remain below the crossing even when full theoretical decoupling would be beneficial.

Figure 2 separates this architecture-value classification from later realization criteria. Panel A lives on the `L-Phi` plane. Panels B and C deliberately introduce additional coordinates, because local accessibility depends on release-path geometry and rare invasion depends on population feedback. Those later boundaries therefore cannot be drawn as universal extra lines in the same `L-Phi` plane.

![](../figures/FIG2_PHASE_MAP.svg)

**Figure 2. Architecture value and evolutionary realization occupy different coordinates and can cross at different ecological thresholds.** The `L-Phi` plane classifies persistent compromise versus globally favorable differentiation. Small-step accessibility introduces release-path geometry, and frequency-dependent invasion introduces `eta`. Along an ecological gradient with `Phi(E)=a(E-E_V)`, the rare-invasion crossing occurs at `E_I=E_V+eta/a`: positive `eta` delays establishment beyond the value crossing, whereas negative `eta` permits rare invasion before intrinsic endpoint value becomes positive. Thus the position of realized differentiation can shift even when the underlying architecture comparison is unchanged.

`Phi>0` is therefore a global-value statement only. It is not shorthand for local reachability, invasion, fixation, occupancy, or historical evolution.

## 5. Can a fitter differentiated architecture be reached?

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

This produces an endpoint architecture that is globally favorable but cannot be approached by sufficiently small selectively uphill release steps along the declared path. It does not rule out crossing by drift, large mutations, recombination, or another developmental route. In the registered two-function quadratic case, the barrier width is

```text
W_k=s0(1-s0)Delta^2,
```

maximized at intermediate residual integration, `s0=1/2`.

Accessibility is therefore conditional on the declared mutation or release neighborhood and its path geometry. Endpoint architecture value alone does not identify local reachability.

## 6. Can a differentiated type establish when rare?

Suppose two architectures differ intrinsically by `Phi` but also experience symmetric frequency-dependent ecological feedback summarized by `eta`. Their canonical selection difference is

```text
Delta(p)=Phi+eta(2p-1).
```

The static architecture boundary `Phi=0` then splits into two rare-invasion boundaries,

```text
Phi=+eta
Phi=-eta.
```

The population phase is therefore not determined by architecture value alone. Depending on `eta`, the system can show dominance, stable coexistence, or coordination bistability. This split is conditional on the registered symmetric pair mapping and an identified or declared population-feedback term.

## 7. What happens after establishment depends on the population process

In finite populations, invasion when rare and fixation ordering need not coincide. Under the registered exponential Moran process for the canonical symmetric pair,

```text
rho_D/rho_S=exp[beta(N-2)Phi].
```

Thus reciprocal fixation ordering depends on intrinsic architecture value, whereas rare invasion depends on both `Phi` and `eta`. Under weak selection, absolute mutant advantage relative to neutrality follows another criterion,

```text
rho_D>1/N iff 3Phi>eta.
```

The distinction between reciprocal fixation ordering and absolute fixation advantage matters for the final transport step. These fixation results are specific to the declared Moran mapping.

## 8. Long-run persistence is a further population-process question

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

This result sits inside a well-developed literature on finite-population evolutionary games and weak-mutation substitution processes; the contribution here is the exact placement of the invariant inside the architecture-value transport, not the invention of weak-mutation Markov-chain theory. The invariant requires a finite symmetric game, connected symmetric rare mutation, and the registered exponential Moran fixation process.

## 9. Formal model: separating the biological explanations

The preceding stages can be embedded in one registered composite model rather than treated as separate counterexamples. Let release from the shared architecture be `d in [0,dmax]`, let recovery `R(d)` be differentiable and convex with `R(0)=0`, and let path cost be linear, `K(d)=kd`. Define

```text
k_local  = R'(0)
k_global = R(dmax)/dmax
Phi      = R(dmax)-k dmax.
```

For the same endpoint pair, use the registered canonical population game

```text
Delta(p)=Phi+eta(2p-1),
```

the self-excluding exponential Moran process, and connected symmetric rare mutation.

The cross-level mapping is exact for the declared comparison. The architecture path generates the endpoint gap `Phi=W_D-W_S`; the canonical pair has self-play difference `A_DD/2-A_SS/2=Phi`; and the registered reciprocal-fixation and symmetric rare-mutation occupancy ratios both use that same self-play difference. Frequency dependence enters through `eta` and moves invasion boundaries without redefining the endpoint contrast. Thus the later stages transport one `Phi`, rather than substituting unrelated payoff quantities.

Under these assumptions the critical surfaces are

| Evolutionary question | Criterion for D | Critical surface |
|---|---|---|
| sufficiently small release is selectively uphill | `k<k_local` | `k=k_local` |
| differentiated endpoint has positive global value | `Phi>0`, equivalently `k<k_global` | `Phi=0` |
| D invades S from rarity | `Phi>eta` | `Phi=eta` |
| D resists rare S invasion | `Phi>-eta` | `Phi=-eta` |
| reciprocal fixation ordering favors D | `Phi>0` | `Phi=0` |
| absolute fixation exceeds neutrality, weak selection | `3Phi>eta` | `3Phi=eta` |
| symmetric rare-mutation occupancy favors D | `Phi>0` | `Phi=0` |

The proof is direct but informative. Net value along the construction path is `R(d)-kd`, so the derivative at the shared state changes sign at `k=k_local`; endpoint value changes sign at `k=k_global`. Rare invasion and resistance to reverse invasion are the endpoint signs `Delta(0)=Phi-eta` and `Delta(1)=Phi+eta`. Reciprocal fixation satisfies

```text
rho_D/rho_S=exp[beta(N-2)Phi],
```

while symmetric rare-mutation occupancy satisfies the identical pairwise ratio

```text
Pi_D/Pi_S=exp[beta(N-2)Phi].
```

Thus the same architecture comparison is cut by genuinely different surfaces when release geometry and frequency dependence enter, but reciprocal fixation and monomorphic occupancy re-align exactly at `Phi=0` under the registered process.

Convexity adds a structural result. Because `R(0)=0`,

```text
k_local<=k_global.
```

Whenever the inequality is strict, the interval

```text
k_local<k<k_global
```

contains architectures whose differentiated endpoint has positive global value even though sufficiently small release steps are selectively downhill.

All flagship non-implications can then be realized inside one convex recovery family,

```text
d in [0,1],
R(d)=d+d^2,
K(d)=kd,
```

for which

```text
k_local=1,
k_global=2,
Phi=2-k.
```

Setting `L=2` when an upstream conflict budget is needed gives the following constructive witnesses:

| Separation | Parameters | Result |
|---|---|---|
| conflict -> payoff | `L=2, k=2.2` | `L>0` but `Phi=-0.2` |
| payoff -> small-step accessibility | `k=1.5` | `Phi=0.5>0`, but `Phi'(0)=-0.5` |
| accessible payoff -> invasion | `k=0.8, eta=1.5` | `Phi=1.2>0`, `Phi'(0)=0.2>0`, but `Delta(0)=-0.3` |
| invasion -> reciprocal fixation | `k=2.2, eta=-1` | `Delta(0)=0.8>0`, but `rho_D/rho_S<1` |
| absolute fixation advantage -> occupancy | `k=2.1, eta=-0.5` | `3Phi=-0.3>eta`, but `Pi_D<Pi_S` |

The value of the theorem is therefore not that each inequality is mathematically difficult. It is that one declared architecture comparison encounters different exact decision surfaces as the biological question changes. The framework identifies where a verdict must be re-tested rather than carried forward by verbal implication.

The final pair remains an important qualification: reciprocal fixation ordering itself does not diverge from stationary monomorphic occupancy ordering under connected symmetric rare mutation and the registered exponential Moran process. Both are controlled by the same self-play score difference.

## 10. Biological predictions

The threshold atlas changes the biological interpretation of several common comparative patterns.

### Conflict and differentiation need not covary monotonically

Under the quadratic bridge,

```text
Phi=sL-K.
```

Thus a larger conflict load does not necessarily predict stronger differentiation across populations or taxa. A high-conflict system can remain integrated when little of the conflict is recoverable by the candidate architecture or when architecture-specific cost is high. Conversely, a system with more modest conflict can cross the differentiation threshold if recovery is efficient and architecture cost is low. The relevant comparative target is therefore not conflict magnitude alone but the triplet `(L,R,K)`, or `(L,s,K)` where the quadratic bridge is justified.

This gives a specific interpretation to persistent integration: an integrated phenotype in the presence of measured opposing functional selection is not evidence that the conflict is weak. It can instead locate the system below the architecture-value surface.

### Ecological feedback can delay or advance establishment without changing endpoint value

Let an environmental coordinate `E` change the intrinsic architecture margin approximately linearly,

```text
Phi(E)=a(E-E_V),
a>0,
```

while the local frequency-feedback term is `eta`. The endpoint architecture becomes globally favorable at

```text
E=E_V,
```

whereas a rare differentiated type can invade at

```text
E_I=E_V+eta/a.
```

The displacement is therefore

```text
E_I-E_V=eta/a,
```

and the environmental distance between the two reciprocal invasion boundaries is

```text
|E_I-E_R|=2|eta|/a.
```

Thus the same parameters predict not only which transition occurs first but also the width of the coordination or coexistence zone along the ecological gradient. These affine displacement formulas are direct solutions of the registered crossing equations; we use them as testable ecological mappings, not as standalone mathematical novelty.

If `eta>0`, coordination-like ecological feedback creates an interval in which differentiation already pays but cannot establish from rarity. If `eta<0`, negative-frequency feedback allows the differentiated type to invade before its intrinsic endpoint margin becomes positive; in the registered deterministic game this leads toward coexistence rather than proving intrinsic endpoint superiority.

This yields a directly testable comparative prediction: the ecological position of the invasion transition should be displaced from the architecture-value transition by the strength of frequency feedback relative to the environmental slope of architecture value. Environmental or community change can therefore alter realized differentiation even when the underlying functional conflict is unchanged.

The prediction also extends when ecological feedback itself changes along the same gradient. If

```text
eta(E)=eta_0+b(E-E_V),
```

then the affine model gives

```text
E_I-E_V=eta_0/(a-b),
E_R-E_V=-eta_0/(a+b).
```

Thus the **slope** of ecological feedback matters as well as its magnitude. Coordination-like feedback that strengthens in the same direction as architecture value (`0<b<a`) pushes establishment farther from the value crossing than the constant-`eta` prediction. As `b` approaches `a`, the rare-invasion threshold is driven far away; if `b>=a` with `eta_0>0`, increasing `E` in the affine model never overcomes the coordination barrier even though intrinsic endpoint value continues to increase. For smooth non-affine systems the local approximation is `E_I-E_V approximately eta(E_V)/[Phi'(E_V)-eta'(E_V)]`. Ecology can therefore alter not only which threshold is crossed first but whether an invasion crossing occurs in the focal environmental direction at all.

### A two-frequency experiment separates architecture value from ecological feedback

The registered population mapping is directly estimable without observing fixation. At a fixed ecological context,

```text
Delta(p)=Phi+eta(2p-1).
```

Measure the relative performance of D versus S at two frequencies symmetric around one half, `p_-=1/2-q` and `p_+=1/2+q`. Then

```text
Phi=[Delta(p_+)+Delta(p_-)]/2
eta=[Delta(p_+)-Delta(p_-)]/(4q).
```

Thus the same experiment separates the intrinsic endpoint-centered architecture coordinate from frequency-dependent ecological feedback. The two-frequency identities are the direct solution of the declared linear map; their role is experimental decomposition, not a new algebraic identification theorem. Repeating this design across environments reconstructs `Phi(E)` and `eta(E)`, allowing independent estimation of the value crossing `E_V`, the invasion crossing `E_I`, and their local slopes. A failure of the linear-in-frequency fit is informative rather than fatal: it rejects the minimal canonical population mapping and indicates that a richer interaction model is required.

### A third frequency treatment tests and repairs the canonical mapping

The two-frequency decomposition above assumes that population feedback is linear in frequency. That assumption is testable. Retain the independently measured architecture margin `Phi` from G5 and add a balanced-frequency treatment `p_0=1/2`. Approximate the population selection difference by

```text
Delta(p)
=
Phi+h0+eta x+kappa x^2,
x=2p-1.
```

With `p_-=1/2-q`, `p_0=1/2`, and `p_+=1/2+q`,

```text
h0=Delta(p_0)-Phi,

eta=[Delta(p_+)-Delta(p_-)]/(4q),

kappa=
[Delta(p_+)+Delta(p_-)-2Delta(p_0)]/(8q^2).
```

The minimal canonical pair is the nested case `h0=kappa=0`. The three-point coefficient recovery is ordinary quadratic interpolation; its SLK role is to diagnose whether the canonical mapping is adequate rather than to claim a new interpolation result.

When curvature is retained, rare invasion and resistance to reverse invasion become

```text
Phi>eta-kappa-h0
```

and

```text
Phi>-eta-kappa-h0.
```

Along `Phi(E)=a(E-E_V)` with locally constant `h0`, `eta`, and `kappa`,

```text
E_I-E_V=(eta-kappa-h0)/a,
E_R-E_V=-(eta+kappa+h0)/a.
```

Hence `eta` controls the spacing between reciprocal invasion thresholds, while `h0+kappa` shifts the center of the entire invasion window relative to the independently measured architecture-value crossing. Nonlinearity therefore does not merely invalidate the minimal model; to quadratic order it has a distinct ecological signature.

This diagnostic extension applies to invasion inference only. The canonical Moran fixation and weak-mutation occupancy invariant is not automatically inherited once `h0` or `kappa` is nonzero.

### Invasion prediction itself does not require a linear or quadratic frequency curve

The internal shape of frequency dependence is useful for mechanism diagnosis, but it is not required to define invasion. Write the population selection difference generally as

```text
Delta(p,E)=Phi(E)+H(p,E),
```

where `H` contains any additional ecological frequency-dependent contribution. Define the endpoint ecological offsets

```text
h_R(E)=lim_{p->0} H(p,E),
h_D(E)=lim_{p->1} H(p,E).
```

Then rare D invasion and resistance to rare S invasion are exactly

```text
Phi(E)+h_R(E)>0
```

and

```text
Phi(E)+h_D(E)>0.
```

Thus the generalized invasion surfaces are simply

```text
Phi=-h_R,
Phi=-h_D,
```

regardless of how nonlinear the interior frequency response may be. Dependence on the rare-mutant endpoint is part of the standard definition of invasion fitness; the useful SLK step is keeping the independently measured architecture contrast `Phi` explicit while the ecological endpoint offset is added.

Along `Phi(E)=a(E-E_V)` with locally constant endpoint offsets,

```text
E_I-E_V=-h_R/a,
E_R-E_V=-h_D/a.
```

Therefore

```text
E_I-E_R=(h_D-h_R)/a
```

and

```text
(E_I+E_R)/2-E_V=-(h_R+h_D)/(2a).
```

The canonical and quadratic models are nested descriptions of these endpoint offsets: the former has `h_R=-eta`, `h_D=eta`; the latter has `h_R=h0-eta+kappa`, `h_D=h0+eta+kappa`.

This means higher-order frequency dependence changes how ecological mechanisms are decomposed, but it does not invalidate deterministic endpoint invasion inference if the endpoint selection limits can be estimated. Fixation and occupancy remain separate and are not rescued by this endpoint argument.

### Finite-frequency assays can certify the endpoint signs

Endpoint invasion does not require experimentally attaining exactly `p=0` or `p=1`. Suppose near the rare-D endpoint that

```text
|Delta(p)-Delta_R| <= M_R p.
```

A measurement at `p=epsilon` then implies

```text
Delta_R
in
[
Delta(epsilon)-M_R epsilon,
Delta(epsilon)+M_R epsilon
].
```

If the lower bound is positive, rare D invasion is certified; if the upper bound is negative, failure of rare D invasion is certified. An interval containing zero is unresolved, not evidence of no invasion.

A stronger second-order certificate uses two rare frequencies. If `|Delta''(p)|<=C_R` on `[0,2epsilon]`, define

```text
Delta_R_hat
=
2Delta(epsilon)-Delta(2epsilon).
```

Then

```text
|Delta_R_hat-Delta_R|
<=
C_R epsilon^2.
```

The same construction applies near `p=1` using `1-epsilon` and `1-2epsilon`. Thus finite-frequency experiments can reduce deterministic endpoint approximation error from order `epsilon` to order `epsilon^2` when a curvature bound is available. This two-scale cancellation is Richardson-type extrapolation (Richardson and Gaunt 1927); the contribution here is its use as a prospective rare-frequency sign certificate with explicit biological and sampling uncertainty, not the extrapolation algebra itself.

Sampling uncertainty can be folded into the same certificate. If `Delta(epsilon)` and `Delta(2epsilon)` have intervals `[L_1,U_1]` and `[L_2,U_2]`, then

```text
Delta_R
in
[
2L_1-U_2-C_R epsilon^2,
2U_1-L_2+C_R epsilon^2
].
```

Only an interval entirely above or below zero licenses an invasion or non-invasion verdict; overlap with zero remains unresolved.

Along an environmental value gradient `Phi(E)=a(E-E_V)`, a fitness-scale endpoint error bound `B` translates directly into environmental threshold uncertainty

```text
|E_I_hat-E_I| <= B/a.
```

For the two-point certificate, `B=C_R epsilon^2`. This turns endpoint invasion from an ideal limit into a prospective sampling-resolution problem.

### Persistent integration is non-identifying, but the sign sequence is diagnostic

A single observed state—continued integration—does not identify why differentiation is absent. Once upstream quantities are measured, however, the transport sequence can localize the first layer at which the verdict changes. Let `g_0=R'(0)-k` denote the net small-release gradient along the declared path and `Delta_R=lim_{p->0}Delta(p)` the rare-D selection difference.

| Measured sign pattern | Localized layer | What the pattern licenses | Next measurement / excluded inference |
|---|---|---|---|
| `L>0, Phi<0` | architecture value | conflict is real, but the declared D is not net favorable | separate `R` from `K`; do not infer weak conflict or historical persistence |
| `Phi>0, g_0<0` | local release | the endpoint is better, but sufficiently small release is downhill on the declared path | test alternative paths and step sizes; do not infer global inaccessibility |
| `Phi>0, g_0>0, Delta_R<0` | rare invasion | value and the initial release direction pass, but rare D does not establish | estimate `h_R=Delta_R-Phi` and frequency response; causal mechanism remains unidentified |
| `Phi>0, g_0>0, Delta_R>0` | early-gate exclusion | the first three registered failure modes are excluded in the measured context | test full-path geometry and fixation/demography/history; do not infer realized differentiation must occur |
| `Phi<0, Delta_R>0` | ecological rescue at rarity | D has a rare-frequency advantage despite negative intrinsic endpoint value | measure `Delta_D`; do not infer intrinsic endpoint superiority |
| `Delta_R>0`, `rho_D/rho_S<1` | reciprocal fixation | deterministic rare entry does not imply fixation ordering in the declared finite process | validate population size, selection mapping, and fixation kernel; no process-independent conclusion |
| reciprocal fixation and occupancy orderings disagree under the registered symmetric rare-mutation process | process consistency | at least one registered stochastic-process assumption is inadequate | audit the mutation model and fixation kernel; this is not a new biological gate |

Boundary values are not pooled with neighboring failures. `Phi=0` is the architecture-value boundary; `g_0=0` leaves the local-release verdict unresolved at first order and requires higher-order path geometry; `Delta_R=0` is the rare-invasion boundary. With sampling uncertainty, an interval overlapping any of these zero surfaces remains unresolved rather than being assigned to either adjacent regime.

Conversely, `Phi>0`, `g_0>0`, and `Delta_R>0` only exclude these three early failure modes in the measured context. They do not prove that the full path is barrier-free or that differentiation must fix, persist, or be historically realized.

With uncertainty, the diagnostic is set-valued rather than forced into one row. Closed intervals for `Phi`, `g_0`, and `Delta_R` define a Cartesian uncertainty box and retain every gate state whose sequential sign conditions intersect that box. An interval crossing zero therefore preserves the relevant boundary state and any downstream branch that positive values still permit. If valid box bounds are tightened by set inclusion, the compatible-state set can only stay the same or shrink. Better-resolved measurements therefore have an explicit diagnostic payoff: they eliminate explanations rather than manufacturing a sharper label from an unresolved sign. When the intervals are only marginal bounds, this is a conservative outer state set because covariance or other joint constraints may rule out some retained sign combinations. Exact joint compatibility would require a joint feasible region. This is uncertainty propagation through the gate logic, not a new partial-identification method.

The ecological contribution of SLK is therefore not a universal prediction that conflict produces modularity. It is **gate localization under a fixed architecture comparison**. The same macroscopic persistence can correspond to different sign patterns, and each pattern directs the next measurement. Mechanism attribution remains a separate causal problem.

## 11. How to distinguish the alternatives empirically

The empirical programme is deliberately cumulative. Each measurement level adds a new estimand and raises the ceiling of the biological claim; failure at a later level does not erase what earlier measurements established (Fig. 3).

![](../figures/FIG3_EMPIRICAL_LADDER.svg)

**Figure 3. Sequential empirical validation of the SLK hierarchy.** A first stage identifies a real shared-coordinate conflict and estimates or bounds `L`. The next stages quantify recoverable architecture benefit `R` and architecture cost `K` on a common fitness scale, allowing evaluation of `Phi=R-K`. These measurements are sufficient only for architecture-value classification. Stronger claims require additional information: a local mutation or release neighborhood for accessibility, rare-frequency performance and population feedback for invasion, an explicit stochastic finite-population process for fixation, and a mutation graph or kernel for stationary occupancy.

The corresponding measurement ladder is:

```text
identified conflict             -> a real shared-axis conflict is established
estimated or bounded L          -> conflict magnitude is quantified
estimated R and K               -> recoverable benefit and architecture cost are separated
evaluated Phi=R-K               -> persistent compromise or global differentiated advantage is classified
local release neighborhood      -> local reachability/trapping can be evaluated
rare-frequency performance      -> rare-invasion phase can be evaluated
finite-population process       -> fixation statements become justified
mutation graph/kernel           -> weak-mutation monomorphic occupancy becomes justified.
```

This ordering prevents a common empirical shortcut: endpoint superiority cannot substitute for local accessibility or later population-process measurements. Likewise, a rare-invasion assay cannot by itself determine fixation or occupancy. Under the registered symmetric rare-mutation exponential-Moran model, reciprocal fixation ordering and occupancy ordering coincide, but that agreement is a theorem conditional on the process assumptions rather than permission to skip process specification.

No single biological system is claimed here to have completed the full measurement ladder end to end.

## 12. Discussion

The central contribution is not a new synonym for trade-off or modularity. Nor is it the generic statement that benefits must exceed costs. Existing work already explains why interference among functions can favor modularity or specialization, and geometric adaptive-evolution theory has already placed trade-off curves and resident-mutant invasion boundaries in a common representation (Bowers et al. 2005). Existing population theory likewise separates invasion, fixation, and long-run stochastic behavior. The contribution is the explicit architecture-specific estimand transport that begins with a causally identified shared-coordinate conflict and preserves the extra assumptions needed at every later stage.

At the organismal scale, `L` asks whether integration is costly. At the architecture scale, `R` asks how much of that compromise an alternative architecture can recover, while `Phi=R-K` asks whether that recovery pays for the architecture-specific debit. At the mutational scale, small-step accessibility asks whether sufficiently small release changes along the declared path are selectively uphill. At the population scale, invasion and fixation ask distinct establishment questions. At the long-run evolutionary scale, occupancy asks how often monomorphic states are expected under the registered mutation-selection process.

The registered composite model is nested rather than a sequence of unrelated payoff substitutions. The architecture path defines the endpoint contrast `Phi`; the canonical game is parameterized so that its self-play score difference is the same `Phi`; and the registered fixation and occupancy ratios inherit that same difference. What changes downstream is therefore the additional mechanism and coordinate required for the next question, not the identity of the endpoint architecture comparison.

The framework therefore contributes four linked objects. First, it supplies a common handoff coordinate system without pretending that all quantities live on the same phase plane. Second, the unified critical-surface atlas identifies where added mechanisms change the decision boundary while preserving the same endpoint contrast across the registered population mapping; the fixation-occupancy invariant records one condition under which later criteria re-align. Third, the transport resolves an important observational ambiguity: persistent integration is compatible with negative architecture value, a local release barrier, or a rare-establishment barrier. The discordance table localizes these alternatives by their measured sign sequence and directs the next discriminating measurement without claiming mechanism identification. Fourth, the empirical measurement ladder translates the theory into a sequential claim structure, so that a study can stop at the strongest level its measurements actually justify.

This framing also sharpens what would falsify or limit the framework. If a biological system lacks an identified `L`, the architecture argument never starts. If `R` and `K` cannot be placed on a common fitness scale, `Phi` is not empirically evaluable. If mutation neighborhoods, population feedback, or stochastic process assumptions are unspecified, later evolutionary claims remain open even when endpoint architecture value is known. The hierarchy is therefore cumulative rather than all-or-nothing.

The three figures mirror the three levels of the contribution. Figure 1 gives the critical-surface transport, the one-family witness system, and the exact re-alignment; Figure 2 gives the coordinate geometry of architecture value versus realization; Figure 3 gives the empirical ladder required to move from one claim level to the next. Together they make the framework mathematically explicit and experimentally falsifiable without claiming an end-to-end empirical demonstration that has not yet been performed.

### Novelty boundary

We do not claim a first theory of modularity or evolvability, a first theory of functional specialization or division of labor, a first theory that fitter endpoints can be locally inaccessible, a first common geometry connecting trade-offs to invasion boundaries, a first distinction between invasion and fixation in finite populations, or a first weak-mutation stationary distribution. We also do not claim mathematical novelty for `R=sL` under the quadratic bridge, affine threshold-shift algebra, two- or three-frequency coefficient recovery, endpoint invasion defined at rarity, Richardson-type extrapolation, or the fixation-occupancy ordering result under the registered symmetric rare-mutation process. These transparent pieces are deliberately retained because they make the handoffs testable. Our contribution is the integrated architecture-specific transport from an identified conflict receipt through a common endpoint contrast to accessibility and population realization, the one-family atlas showing where added mechanisms alter the decision boundary, and the gate-by-gate empirical claim ceiling that prevents familiar component results from being overinterpreted.

### Scope boundary

The present paper deliberately excludes continuous-architecture branching, edgewise modular topology, spatial spectral invasion, temporal Floquet dynamics, detailed contextual-optimum identification, middle-world depth metrics, and ecological route identification after differentiation. Those are independent extensions developed in sister repositories and are not required for the flagship argument.

## Literature Cited

Bowers, R. G., A. Hoyle, A. White, and M. Boots. 2005. The geometric theory of adaptive evolution: trade-off and invasion plots. *Journal of Theoretical Biology* 233:363–377.

Des Marais, D. L., and M. D. Rausher. 2008. Escape from adaptive conflict after duplication in an anthocyanin pathway gene. *Nature* 454:762–765.

Guillaume, F., and S. P. Otto. 2012. Gene functional trade-offs and the evolution of pleiotropy. *Genetics* 192:1389–1409.

Kay, K. M., T. Jogesh, D. Tataru, and S. Akiba. 2020. Darwin's vexing contrivance: a new hypothesis for why some flowers have two kinds of anther. *Proceedings of the Royal Society B* 287:20202593.

Sun, S.-G., W. S. Armbruster, and S.-Q. Huang. 2016. Geographic consistency and variation in conflicting selection generated by pollinators and seed predators. *Annals of Botany* 118:227–237.

Sun, S.-G., and S.-Q. Huang. 2015. Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019.

Vallejo-Marín, M., J. S. Manson, J. D. Thomson, and S. C. H. Barrett. 2009. Division of labour within flowers: heteranthery, a floral strategy to reconcile contrasting pollen fates. *Journal of Evolutionary Biology* 22:828–839.

Dieckmann, U., and R. Law. 1996. The dynamical theory of coevolution: a derivation from stochastic ecological processes. *Journal of Mathematical Biology* 34:579–612.

Espinosa-Soto, C., and A. Wagner. 2010. Specialization can drive the evolution of modularity. *PLoS Computational Biology* 6:e1000719.

Fudenberg, D., M. A. Nowak, C. Taylor, and L. A. Imhof. 2006. Evolutionary game dynamics in finite populations with strong selection and weak mutation. *Theoretical Population Biology* 70:352–363.

Kashtan, N., and U. Alon. 2005. Spontaneous evolution of modularity and network motifs. *Proceedings of the National Academy of Sciences USA* 102:13773–13778.

Richardson, L. F., and J. A. Gaunt. 1927. The deferred approach to the limit. *Philosophical Transactions of the Royal Society of London, Series A* 226:299–361.

Rueffler, C., J. Hermisson, and G. P. Wagner. 2012. Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109:E326–E335.

Taylor, C., D. Fudenberg, A. Sasaki, and M. A. Nowak. 2004. Evolutionary game dynamics in finite populations. *Bulletin of Mathematical Biology* 66:1621–1644.

Wagner, G. P., and L. Altenberg. 1996. Perspective: complex adaptations and the evolution of evolvability. *Evolution* 50:967–976.

Weinreich, D. M., N. F. Delaney, M. A. DePristo, and D. L. Hartl. 2006. Darwinian evolution can follow only very few mutational paths to fitter proteins. *Science* 312:111–114.
