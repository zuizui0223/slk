# From functional conflict to evolutionary architecture: thresholds for differentiation

## Abstract

Multifunctional traits can experience genuine conflict without favoring differentiated architecture, and globally favorable differentiation need not become an evolutionary outcome. We develop an architecture-specific transport framework carrying one identified conflict comparison through architecture value, small-step release, invasion, fixation, and occupancy. Conflict is summarized by `L`; a differentiated comparison recovers `R` and incurs `K`, so `Phi=R-K`. In one composite model, critical surfaces separate small-step accessibility at `k=k_local`, endpoint value at `Phi=0`, rare invasion at `Phi=eta`, reverse invasion at `Phi=-eta`, and weak-selection absolute fixation at `3Phi=eta`; reciprocal fixation and symmetric rare-mutation occupancy re-align at `Phi=0` under the registered Moran process. This geometry yields an ecological prediction: along `Phi(E)=a(E-E_V)`, the rare-invasion threshold shifts from the architecture-value threshold by `eta/a`, so frequency-dependent ecology can delay or advance establishment without changing the endpoint comparison. It also predicts that conflict magnitude alone cannot rank differentiation when recoverability or architecture cost varies. Even under arbitrary nonlinear frequency dependence, deterministic invasion depends only on the ecological offsets at the rare-D and resident-D endpoints. A cumulative measurement ladder states the evidence needed for each claim.

## 1. Introduction

A trait can perform several functions without those functions opposing one another. Even when opposing selection is real, the existence of compromise does not tell us whether adding phenotypic dimensions is worth the cost of maintaining a more complex architecture. And even when differentiation has higher optimized fitness, evolution may fail to reach it through available mutations or may reject it at the population level.

These questions have deep prior literatures, and most individual arrows in our framework already have important antecedents. The modularity and evolvability literature established that genotype–phenotype organization can alter evolvability and that reduced interference among functions can favor modular organization (Wagner and Altenberg 1996). Modular organization can also emerge under modularly varying goals (Kashtan and Alon 2005), while specialization itself can promote modularity by reducing interference among gene activities (Espinosa-Soto and Wagner 2010). General theory of functional specialization and division of labor has already identified conditions under which specialization is favored, including performance curvature, positional effects, and synergistic interactions (Rueffler, Hermisson, and Wagner 2012). We therefore do not claim the ideas that conflict can favor modular organization, that specialization can pay when benefits exceed costs, or that modularity can improve evolvability.

A separate literature establishes that endpoint value does not determine evolutionary realization. Adaptive-dynamics theory formalizes evolution through rare local mutations and invasion fitness in an ecological background (Dieckmann and Law 1996), while empirical fitness landscapes show that only a restricted subset of mutational paths to a fitter endpoint may be selectively accessible (Weinreich et al. 2006). Finite-population evolutionary-game theory further distinguishes invasion and fixation criteria (Taylor et al. 2004), and strong-selection/weak-mutation theory gives a substitution process with long-run stochastic state occupancy (Fudenberg et al. 2006). We therefore do not claim local mutational accessibility, invasion–fixation distinctions, or weak-mutation stationary dynamics as new concepts.

The contribution here is instead the architecture-specific handoff across these literatures. We start from an empirically identified shared-coordinate conflict budget rather than assuming that multifunctionality implies conflict; separate recoverable architecture value from architecture-specific cost; then transport that value through local accessibility, frequency-dependent invasion, finite-population fixation, and weak-mutation occupancy. The same upstream architecture comparison is therefore forced through a sequence of distinct estimands, making it possible to identify where its verdict must be re-tested, where adjacent criteria genuinely separate, and where two later criteria re-align under an exact process-level invariant. The empirical counterpart is a measurement ladder that states what additional information is required before each stronger biological interpretation is licensed.

This transport yields ecological predictions that are not contained in the endpoint cost-benefit comparison alone. Two populations can have the same intrinsic architecture margin but differ in whether differentiation establishes because their frequency-dependent ecological feedback differs. Conversely, two populations can experience different conflict loads yet show the opposite ranking of differentiation because recoverability and architecture cost differ. Along an environmental gradient, the environment where differentiation first becomes globally profitable need not be the environment where a rare differentiated type can invade. SLK therefore predicts systematic discordance between functional conflict, architecture value, and realized differentiation rather than treating such discordance as noise or failed adaptation.

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

The main result is therefore a critical-surface transport theorem rather than a claim that every adjacent stage differs. The same endpoint architecture comparison is carried through local release geometry, frequency-dependent competition, finite-population fixation, and rare-mutation occupancy. New mechanisms split the critical surfaces, whereas the registered fixation-occupancy process forces an exact re-alignment at `Phi=0`. Figure 1 summarizes those surfaces directly; its arrows are handoffs between estimands, not logical implications.

![](../figures/FIG1_LOGIC_DIAGRAM.svg)

**Figure 1. One architecture comparison crosses different evolutionary thresholds.** The same comparison is transported from identified conflict through endpoint value, small-step selective accessibility, invasion, fixation, and occupancy. Exact critical surfaces are shown beside each stage: `Phi=0` for endpoint value, `k=k_local` for sufficiently small release, `Phi=±eta` for reciprocal invasion boundaries, `Phi=0` for reciprocal fixation ordering, `3Phi=eta` for absolute fixation advantage under weak selection, and `Phi=0` for symmetric rare-mutation occupancy. The repeated `Phi=0` surface marks the exact re-alignment of endpoint value, reciprocal fixation ordering, and occupancy under the registered process. The left panel shows that all five non-implications can be realized in one convex recovery family.

## 2. Identifying the conflict budget

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the compromise load on a common fitness scale. `L=0` is the no-identified-conflict boundary; `L>0` means that forcing the functions onto one coordinate produces a positive fitness loss relative to the relevant function-specific benchmark.

The empirical interpretation of `L` requires causal care. Context-specific optima measured under selective environments are not automatically pure-function optima. In practice, the conflict budget should therefore be exported only from designs that identify opposing causal geometry or from explicitly bounded state-specific contrasts. The integrated theory starts from a valid `L` receipt; it does not redefine how that receipt is obtained. Thus the present framework does not prove that a biological system has `L>0`; that conclusion must be imported from an identified analysis of shared-coordinate conflict.

## 3. Persistent compromise and the architecture crossing

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

## 4. Differentiation recovers only the conflict it actually releases

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

## 5. Global value can exceed local accessibility

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

The population phase is therefore not determined by architecture value alone. Depending on `eta`, the system can show dominance, stable coexistence, or coordination bistability. This split is conditional on the registered symmetric pair mapping and an identified or declared population-feedback term.

## 7. Fixation is another estimand

In finite populations, invasion when rare and fixation ordering need not coincide. Under the registered exponential Moran process for the canonical symmetric pair,

```text
rho_D/rho_S=exp[beta(N-2)Phi].
```

Thus reciprocal fixation ordering depends on intrinsic architecture value, whereas rare invasion depends on both `Phi` and `eta`. Under weak selection, absolute mutant advantage relative to neutrality follows another criterion,

```text
rho_D>1/N iff 3Phi>eta.
```

The distinction between reciprocal fixation ordering and absolute fixation advantage matters for the final transport step. These fixation results are specific to the declared Moran mapping.

## 8. Weak-mutation occupancy and a fixation-occupancy invariant

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

## 9. Unified critical-surface theorem and constructive witnesses

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

## 10. Ecological deductions from threshold ordering

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

Thus the same parameters predict not only which transition occurs first but also the width of the coordination or coexistence zone along the ecological gradient.

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

Thus the same experiment separates the intrinsic endpoint-centered architecture coordinate from frequency-dependent ecological feedback. Repeating this design across environments reconstructs `Phi(E)` and `eta(E)`, allowing independent estimation of the value crossing `E_V`, the invasion crossing `E_I`, and their local slopes. A failure of the linear-in-frequency fit is informative rather than fatal: it rejects the minimal canonical population mapping and indicates that a richer interaction model is required.

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

The minimal canonical pair is the nested case `h0=kappa=0`. Thus a third frequency treatment diagnoses whether the canonical mapping is adequate rather than assuming it.

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

regardless of how nonlinear the interior frequency response may be.

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

The same construction applies near `p=1` using `1-epsilon` and `1-2epsilon`. Thus finite-frequency experiments can reduce deterministic endpoint approximation error from order `epsilon` to order `epsilon^2` when a curvature bound is available.

Along an environmental value gradient `Phi(E)=a(E-E_V)`, a fitness-scale endpoint error bound `B` translates directly into environmental threshold uncertainty

```text
|E_I_hat-E_I| <= B/a.
```

For the two-point certificate, `B=C_R epsilon^2`. This turns endpoint invasion from an ideal limit into a prospective sampling-resolution problem.

### Discordance becomes diagnostic

Observed mismatches between conflict, value, and realized architecture identify which gate needs to be measured next rather than falsifying the whole framework.

- Strong identified conflict with `Phi<0`: persistent compromise remains favored; measure `R` and `K`.
- `Phi>0` with a downhill small-release gradient: a small-step construction barrier separates the current state from the better endpoint; measure `k_local` and path geometry.
- `Phi>0` but D fails when rare: coordination-like ecological feedback blocks establishment; estimate `eta`.
- `Phi<0` but D invades when rare: negative-frequency feedback rescues rare entry; test coexistence rather than claiming endpoint superiority.
- Reciprocal fixation and occupancy orderings disagree under the registered process: process assumptions are violated; audit mutation symmetry/rarity, game symmetry, and the fixation kernel.

The ecological contribution of SLK is therefore not a universal prediction that conflict produces modularity. It is a prediction of **where discordance should occur, which ecological mechanism creates it, and which additional measurement resolves it**.

## 11. Empirical measurement programme

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

The central contribution is not a new synonym for trade-off or modularity. Nor is it the generic statement that benefits must exceed costs. Existing work already explains why interference among functions can favor modularity or specialization, and existing population theory already separates invasion, fixation, and long-run stochastic behavior. The contribution is the explicit architecture-specific estimand transport that begins with a causally identified shared-coordinate conflict and preserves the extra assumptions needed at every later stage.

At the organismal scale, `L` asks whether integration is costly. At the architecture scale, `R` asks how much of that compromise an alternative architecture can recover, while `Phi=R-K` asks whether that recovery pays for the architecture-specific debit. At the mutational scale, small-step accessibility asks whether sufficiently small release changes along the declared path are selectively uphill. At the population scale, invasion and fixation ask distinct establishment questions. At the long-run evolutionary scale, occupancy asks how often monomorphic states are expected under the registered mutation-selection process.

The registered composite model is nested rather than a sequence of unrelated payoff substitutions. The architecture path defines the endpoint contrast `Phi`; the canonical game is parameterized so that its self-play score difference is the same `Phi`; and the registered fixation and occupancy ratios inherit that same difference. What changes downstream is therefore the additional mechanism and coordinate required for the next question, not the identity of the endpoint architecture comparison.

The framework therefore contributes four linked objects. First, it supplies a common handoff coordinate system without pretending that all quantities live on the same phase plane. Second, the unified critical-surface theorem identifies exactly where apparently adjacent criteria diverge while preserving the same endpoint contrast across the registered population mapping; the fixation-occupancy invariant then identifies the condition under which reciprocal fixation and occupancy re-align. Third, the ecological threshold-displacement result predicts when community or environmental feedback should make realized differentiation lag behind or precede intrinsic architecture value, and the discordance table turns mismatches into diagnostic evidence. Fourth, the empirical measurement ladder translates the theory into a sequential claim structure, so that a study can stop at the strongest level its measurements actually justify.

This framing also sharpens what would falsify or limit the framework. If a biological system lacks an identified `L`, the architecture argument never starts. If `R` and `K` cannot be placed on a common fitness scale, `Phi` is not empirically evaluable. If mutation neighborhoods, population feedback, or stochastic process assumptions are unspecified, later evolutionary claims remain open even when endpoint architecture value is known. The hierarchy is therefore cumulative rather than all-or-nothing.

The three figures mirror the three levels of the contribution. Figure 1 gives the critical-surface transport, the one-family witness system, and the exact re-alignment; Figure 2 gives the coordinate geometry of architecture value versus realization; Figure 3 gives the empirical ladder required to move from one claim level to the next. Together they make the framework mathematically explicit and experimentally falsifiable without claiming an end-to-end empirical demonstration that has not yet been performed.

### Novelty boundary

We do not claim a first theory of modularity or evolvability, a first theory of functional specialization or division of labor, a first theory that fitter endpoints can be locally inaccessible, a first distinction between invasion and fixation in finite populations, or a first weak-mutation stationary distribution. We also do not claim universality of `R=sL` outside the declared quadratic bridge. We claim the integrated architecture-specific hierarchy from identified conflict to evolutionary realization, a unified critical-surface theorem that places value, small-step accessibility, invasion, fixation, and occupancy in one compatible registered model, one-family constructive separation witnesses, an ecological threshold-displacement prediction linking environment and frequency feedback, the exact fixation-occupancy re-alignment within that hierarchy, and a gate-by-gate empirical claim ceiling.

### Scope boundary

The present paper deliberately excludes continuous-architecture branching, edgewise modular topology, spatial spectral invasion, temporal Floquet dynamics, detailed contextual-optimum identification, middle-world depth metrics, and ecological route identification after differentiation. Those are independent extensions developed in sister repositories and are not required for the flagship argument.

## Literature Cited

Dieckmann, U., and R. Law. 1996. The dynamical theory of coevolution: a derivation from stochastic ecological processes. *Journal of Mathematical Biology* 34:579–612.

Espinosa-Soto, C., and A. Wagner. 2010. Specialization can drive the evolution of modularity. *PLoS Computational Biology* 6:e1000719.

Fudenberg, D., M. A. Nowak, C. Taylor, and L. A. Imhof. 2006. Evolutionary game dynamics in finite populations with strong selection and weak mutation. *Theoretical Population Biology* 70:352–363.

Kashtan, N., and U. Alon. 2005. Spontaneous evolution of modularity and network motifs. *Proceedings of the National Academy of Sciences USA* 102:13773–13778.

Rueffler, C., J. Hermisson, and G. P. Wagner. 2012. Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109:E326–E335.

Taylor, C., D. Fudenberg, A. Sasaki, and M. A. Nowak. 2004. Evolutionary game dynamics in finite populations. *Bulletin of Mathematical Biology* 66:1621–1644.

Wagner, G. P., and L. Altenberg. 1996. Perspective: complex adaptations and the evolution of evolvability. *Evolution* 50:967–976.

Weinreich, D. M., N. F. Delaney, M. A. DePristo, and D. L. Hartl. 2006. Darwinian evolution can follow only very few mutational paths to fitter proteins. *Science* 312:111–114.
