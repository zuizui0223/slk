# Why multifunctional structures persist under conflicting selection

## Abstract

Multifunctional structures often face conflicting selection, yet many remain integrated rather than evolving division of labor. Why? We distinguish three biological explanations that can produce the same observed persistence. First, differentiation may fail to recover enough fitness to repay the cost of maintaining additional structure or regulation. Second, a differentiated endpoint may be fitter but unreachable through sufficiently small selectively favorable changes. Third, a favorable and reachable differentiated type may fail to establish when rare because its ecological performance is frequency dependent. These alternatives imply that conflict magnitude alone cannot rank systems by their propensity to differentiate, and that persistent multifunctionality is not evidence for weak conflict or for any single evolutionary constraint. Along one environmental gradient, the limiting reason for persistence can also change before the phenotype does. We formalize the distinction using a common fitness comparison, show how profitability, reachability, and establishment can cross at different conditions, and translate the theory into measurements that discriminate among the three explanations. The goal is a biological account of why functional conflict is sometimes resolved by division of labor and sometimes retained as multifunctional compromise.

## 1. Introduction

In the subalpine herb *Pedicularis rex*, tubular flowers are subtended by cup-like bracts that hold rainwater. The water protects developing fruits from seed predators, but pollinators favor greater corolla exsertion above the protective bracts. Across 14 populations, greater exsertion was associated with greater pollen receipt and also with greater seed predation: the same floral axis is pulled in opposite directions by mutualists and antagonists (Sun, Armbruster, and Huang 2016). Experimentally draining the bracts increased seed predation, confirming that the water-filled structure contributes to defense (Sun and Huang 2015). This is a concrete multifunctional compromise. The interesting evolutionary question is not simply whether conflict exists, but why conflict of this kind sometimes produces separate functional structures and sometimes remains embedded in one architecture.

Biology contains many versions of this problem. In heterantherous flowers, distinct anther types can divide pollen-feeding and pollen-transfer functions, although alternative functions such as staggered pollen presentation show that morphological differentiation alone does not prove division of labor (Vallejo-Marín et al. 2009; Kay et al. 2020). At the molecular level, gene duplication can allow descendant copies to escape an adaptive conflict that constrained a multifunctional ancestral protein (Des Marais and Rausher 2008). In sexually antagonistic traits, sex-biased or sex-specific regulation can decouple phenotypes that were previously constrained by a shared genome (Ingleby, Flis, and Morrow 2015). Across these systems, differentiation is one possible evolutionary resolution of conflicting functional demands.

The basic conditions favoring specialization are already well developed. General theory shows that division of labor is favored by positional effects, accelerating performance functions, and synergistic interactions among modules, while developmental constraints and maintenance of differentiated pathways can still limit its evolution (Rueffler, Hermisson, and Wagner 2012). Models of pleiotropy likewise show that multifunctionality or specialization depends on the shape of functional trade-offs and on how component performance maps to fitness; complete subfunctionalization is expected only under restricted conditions (Guillaume and Otto 2012). We therefore do not claim that functional conflict automatically produces specialization, or that specialization is favored whenever a verbal trade-off is present. Nor do we claim a first connection between trade-off geometry and invasion: adaptive-dynamics and trade-off–invasion theory already distinguish a phenotype's performance from its ability to invade an ecological background (Dieckmann and Law 1996; Bowers et al. 2005). Egas, Dieckmann, and Sabelis (2004) further showed that an evolutionarily stable specialist–generalist state can nevertheless be unreachable through gradual evolution. Separating endpoint value from reachability is therefore also prior art.

We instead organize these results around a narrower and partly inverse biological problem: **what does it mean when a multifunctional structure remains integrated despite documented conflict?** Existing models primarily ask which conditions favor specialization. We ask how to diagnose the reason for non-specialization once the same persistent multifunctional phenotype has already been observed, and whether that limiting reason can change across environments before morphology changes. The same observation can arise for at least three different reasons. A split may simply not pay: the fitness recovered by separating functions may be smaller than the additional structural, developmental, regulatory, or maintenance cost of doing so. A split may pay at the endpoint but be difficult to reach: small changes away from the integrated state can initially reduce fitness even when a more differentiated endpoint would be superior. Or a differentiated type may be reachable and intrinsically favorable yet fail to spread from rarity because pollinators, competitors, enemies, or other ecological partners change its fitness when it is uncommon. These are different biological explanations, not different names for the same constraint.

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

**Figure 1. Three reasons why multifunctionality can persist despite conflict.** After a functional conflict has been established, division of labor can fail at three biologically different stages: the differentiated architecture may not repay its own cost (`Phi<0`); a fitter differentiated endpoint may be locally inaccessible (`Phi>0, g_0<0`); or a favorable and initially reachable differentiated type may fail to establish when rare (`Phi>0, g_0>0, Delta_R<0`). These routes converge on the same observed phenotype—persistent multifunctionality—but imply different next measurements. *Pedicularis rex* illustrates a system in which conflict is documented while the cause of persistence remains open.

## 2. Is the functional conflict real?

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the compromise load on a common fitness scale. `L=0` is the no-identified-conflict boundary; `L>0` means that forcing the functions onto one coordinate produces a positive fitness loss relative to the relevant function-specific benchmark.

The empirical interpretation of `L` requires causal care. Context-specific optima measured under selective environments are not automatically pure-function optima. In practice, the conflict budget should therefore be exported only from designs that identify opposing causal geometry or from explicitly bounded state-specific contrasts. The analysis starts from an empirically supported estimate or bound for `L`; it does not redefine how that evidence is obtained. Thus the present framework does not prove that a biological system has `L>0`; that conclusion must be imported from an identified analysis of shared-coordinate conflict.

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

The parameter `s` enters in the quadratic partial-release model used here. There, `s in [0,1]` is both the realized separation fraction and the recovered fraction of the one-axis compromise load, giving

```text
R=sL,
Phi=sL-K.
```

This is a quadratic corollary rather than an arbitrary-landscape identity. It provides a transparent worked bridge between measured conflict magnitude and partial release, but the general architecture-value coordinate remains `Phi=R-K`.

Under the nested architecture comparison used here, `Phi>0` means the differentiated architecture has higher globally optimized payoff than the declared shared comparison. Structural elaboration with weak functional decoupling can remain below the crossing even when full theoretical decoupling would be beneficial.

Figure 2 separates this architecture-value classification from later realization criteria. Panel A lives on the `L-Phi` plane. Panels B and C deliberately introduce additional coordinates, because local accessibility depends on release-path geometry and rare invasion depends on population feedback. Those later boundaries therefore cannot be drawn as universal extra lines in the same `L-Phi` plane.

![](../figures/FIG2_PHASE_MAP.svg)

**Figure 2. Division of labor can become profitable, reachable, and able to establish under different conditions.** The `L-Phi` plane first separates persistent compromise from positive net architecture value. Convex recovery can then leave a range in which the differentiated endpoint is fitter but small changes remain downhill, and frequency-dependent ecology can delay rare establishment beyond both crossings. Along an environmental gradient that lowers marginal architecture cost, sufficiently strong positive feedback gives `E_V<E_A<E_I`: populations can remain visibly multifunctional while the limiting reason for persistence changes from negative value, to local inaccessibility, to rare-establishment failure.

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

This produces an endpoint architecture that is globally favorable but cannot be approached by sufficiently small selectively uphill release steps along the declared path. It does not rule out crossing by drift, large mutations, recombination, or another developmental route. In the two-function quadratic example, the barrier width is

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

The population phase is therefore not determined by architecture value alone. Depending on `eta`, the system can show dominance, stable coexistence, or coordination bistability. This split is conditional on the symmetric pair mapping used here and on an identified or explicitly specified population-feedback term.

## 7. Why can multifunctionality persist? Three distinct explanations

Once conflict has been established, continued integration does not identify its cause. The same observed multifunctional structure is compatible with three biologically different states.

| Observed quantities | Biological interpretation | What to measure next |
|---|---|---|
| `L>0, Phi<0` | **Division of labor does not pay.** Conflict is real, but the differentiated architecture fails the net cost-benefit test. | Separate recoverable benefit `R` from architecture cost `K`; compare alternative differentiated designs. |
| `Phi>0, g_0<0` | **Division of labor would pay but is locally difficult to reach.** The endpoint is better, yet sufficiently small release from the integrated state is initially selected against. | Measure fitness along alternative developmental or mutational paths and at larger step sizes. |
| `Phi>0, g_0>0, Delta_R<0` | **A favorable differentiated type cannot establish when rare.** Value and initial reachability pass, but ecology reverses the verdict at low frequency. | Measure rare-frequency performance and the ecological interaction responsible for `Delta_R-Phi`. |

Here `g_0=R'(0)-k` is the local fitness gradient away from the integrated architecture, and `Delta_R` is the selection difference experienced by a rare differentiated type. A fourth state, `Phi>0, g_0>0, Delta_R>0`, excludes these three early explanations in the measured context but does not prove that differentiation must fix or persist historically.

This is the main biological use of the theory. Persistent integration is not a diagnosis of weak conflict, developmental constraint, or ecological exclusion by itself. Those explanations become distinguishable only after the corresponding quantities are measured.

## 8. Formal model for the three explanations

Let release from the shared architecture be `d in [0,dmax]`, with differentiable convex recovery `R(d)`, `R(0)=0`, and linear path cost `K(d)=kd`. Define

```text
k_local  = R'(0)
k_global = R(dmax)/dmax
Phi      = R(dmax)-k dmax.
```

The endpoint differentiated architecture is favorable when `Phi>0`, equivalently `k<k_global`. Sufficiently small release from the integrated architecture is selectively uphill when `k<k_local`. Convexity gives

```text
k_local <= k_global.
```

Whenever the inequality is strict, the interval

```text
k_local < k < k_global
```

is nonempty. In that interval, the differentiated endpoint is fitter although every sufficiently small release step is initially downhill. This is the reachability explanation above.

For ecological establishment, use the canonical frequency-dependent comparison

```text
Delta(p)=Phi+eta(2p-1),
```

where `p` is the frequency of the differentiated type. Rare differentiated types invade when

```text
Delta(0)=Phi-eta>0,
```

and resist reverse invasion when

```text
Delta(1)=Phi+eta>0.
```

Thus the architecture-value boundary `Phi=0` and the establishment boundaries `Phi=+/-eta` need not coincide.

The three relevant decision surfaces are therefore

| Biological question | Criterion favoring differentiation | Boundary |
|---|---|---|
| does differentiation pay? | `Phi>0` | `Phi=0` |
| are small release steps uphill? | `k<k_local` | `k=k_local` |
| can a rare differentiated type establish? | `Phi>eta` | `Phi=eta` |

A single convex recovery family is enough to show that the answers can separate:

```text
d in [0,1]
R(d)=d+d^2
K(d)=kd
k_local=1
k_global=2
Phi=2-k.
```

With `L=2` when an upstream conflict quantity is needed:

| Separation | Parameters | Result |
|---|---|---|
| conflict does not imply positive value | `k=2.2` | `L>0`, but `Phi=-0.2` |
| positive value does not imply small-step reachability | `k=1.5` | `Phi=0.5>0`, but `g_0=-0.5` |
| positive value plus initial reachability does not imply rare establishment | `k=0.8, eta=1.5` | `Phi=1.2>0`, `g_0=0.2>0`, but `Delta(0)=-0.3` |

The point is not the difficulty of these inequalities. It is that the same persistent phenotype can be generated by failure at three different biological stages, each requiring a different measurement to distinguish it.

## 9. Biological predictions

The threshold atlas changes the biological interpretation of several common comparative patterns.

### The reason for persistence can change before the phenotype does

Consider an environmental coordinate `E` that progressively lowers the marginal cost of architectural release,

```text
k(E)=k0-c(E-E0),
c>0.
```

With convex recovery, the environment at which differentiation first becomes profitable (`E_V`) necessarily precedes the environment at which sufficiently small release steps become uphill (`E_A`):

```text
E_A-E_V
=
(k_global-k_local)/c
>
0.
```

For the canonical frequency-dependent comparison, rare establishment occurs at

```text
E_I-E_V
=
eta/(c dmax).
```

If coordination-like feedback is strong enough that

```text
eta
>
dmax(k_global-k_local),
```

then

```text
E_V < E_A < E_I.
```

A transect of still-integrated populations can then cross three different limiting regimes without showing any morphological transition:

```text
E < E_V
    differentiation does not pay

E_V < E < E_A
    differentiation pays but is locally difficult to reach

E_A < E < E_I
    differentiation pays and is initially reachable,
    but a rare differentiated type cannot establish.
```

This is stronger than saying that environment changes the amount of selection for specialization. It predicts **turnover in the reason why the same multifunctional phenotype persists**. The empirical test is to measure `Phi`, the local release gradient `g_0`, and rare-frequency performance across populations that remain morphologically integrated.

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

Thus the same parameters predict not only which transition occurs first but also the width of the coordination or coexistence zone along the ecological gradient. These affine displacement formulas are direct solutions of the crossing equations; we use them as testable ecological mappings, not as standalone mathematical novelty.

If `eta>0`, coordination-like ecological feedback creates an interval in which differentiation already pays but cannot establish from rarity. If `eta<0`, negative-frequency feedback allows the differentiated type to invade before its intrinsic endpoint margin becomes positive; in the deterministic game considered here this leads toward coexistence rather than proving intrinsic endpoint superiority.

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

The population mapping is directly estimable without observing fixation. At a fixed ecological context,

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

The minimal canonical pair is the nested case `h0=kappa=0`. The three-point coefficient recovery is ordinary quadratic interpolation; its role here is to diagnose whether the canonical mapping is adequate rather than to claim a new interpolation result.

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

regardless of how nonlinear the interior frequency response may be. Dependence on the rare-mutant endpoint is part of the standard definition of invasion fitness; the useful step here is keeping the independently measured architecture contrast `Phi` explicit while the ecological endpoint offset is added.

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

## 10. How to distinguish the alternatives empirically

The empirical programme is deliberately cumulative. Each measurement step supports a stronger biological conclusion, and failure at a later step does not erase what earlier measurements established (Fig. 3).

![](../figures/FIG3_EMPIRICAL_LADDER.svg)

**Figure 3. How to distinguish the causes of persistent multifunctionality.** The empirical sequence first establishes real functional conflict and places it on a common fitness scale. It then asks whether division of labor pays (`Phi=R-K`), whether a fitter differentiated state is locally reachable, and whether it can establish when rare. A negative result at these three stages diagnoses the three explanations in Figure 1. Fixation and long-run occupancy are optional downstream extensions rather than mandatory endpoints of the core biological test.

The corresponding measurement ladder is:

```text
documented functional conflict  -> opposing functional selection is established
estimated or bounded L          -> conflict magnitude is placed on a common fitness scale
estimated R and K               -> test whether division of labor pays
local release gradient g0       -> test whether a fitter differentiated state is reachable
rare-frequency performance      -> test whether that state can establish when rare
```

This ordering prevents a common empirical shortcut: stronger conflict does not imply that division of labor pays, endpoint superiority does not imply reachability, and reachability does not imply establishment. A study can stop once the biological cause of persistence has been identified. Fixation and long-run occupancy require additional process assumptions only when the biological question extends beyond establishment.

No biological system is claimed here to have completed this full sequence end to end.

### Running example: what is already known in *Pedicularis rex*?

Existing experiments and field comparisons establish opposing selection on floral exsertion and support a protective function of water-filled bracts. In the terminology used here, that is evidence that the **conflict is real**, but it is not yet an estimate of the full conflict load `L` on a common fitness scale, and it says nothing by itself about `R`, `K`, reachability, or rare establishment. The next biological experiment is therefore not "measure more conflict." It is to decouple presentation and protection experimentally and ask how much reproductive fitness can be recovered when the two functions are allowed to approach their separate optima. A distinct architecture treatment, with its own developmental or material burden measured rather than assumed, is then needed to decide whether division of labor would actually pay.

## 11. Downstream population-process extensions

The three explanations above concern whether division of labor is favorable, reachable, and able to establish. Stronger claims about fixation or long-run occupancy require an explicit population process.

For the canonical pair under the self-excluding exponential Moran process,

```text
rho_D/rho_S = exp[beta(N-2)Phi].
```

Reciprocal fixation ordering therefore switches at `Phi=0`, whereas absolute fixation advantage over neutrality follows `3Phi>eta` only in the weak-selection approximation. Under connected symmetric rare mutation, the monomorphic stationary occupancy ratio is

```text
Pi_D/Pi_S = exp[beta(N-2)Phi].
```

so reciprocal fixation ordering and symmetric rare-mutation occupancy re-align exactly at the same `Phi=0` surface. This is useful as a process-level consistency result, but it is not a fourth explanation for why a multifunctional architecture initially persists. A biological application need not estimate fixation or occupancy unless its question extends beyond establishment.

## 12. Discussion

The biological problem addressed here is why a structure can remain multifunctional even when its functions are demonstrably in conflict. *Pedicularis rex* makes that problem tangible: greater floral exposure improves pollen receipt but also exposes reproductive tissues to seed predators, while water-filled bracts provide protection. The existence of this conflict does not tell us whether the flower "should" evolve separate structures for presentation and defense. To answer that question one must know what differentiation would recover, what it would cost, whether a favorable differentiated state is reachable, and whether it could establish in the ecological context in which it first appears.

This view turns persistent multifunctionality from a single outcome into three alternative explanations. In the first, integration persists because it is still the better architecture after the costs of separation are paid. In the second, division of labor would be better if present, but the route from the current structure initially runs downhill in fitness. In the third, a differentiated form is both favorable and reachable but cannot spread from rarity because its ecological interactions are frequency dependent. These alternatives matter because they imply different evolutionary histories, different responses to environmental change, and different experiments.

The first alternative connects directly to existing theories of specialization. Rueffler, Hermisson, and Wagner (2012) showed that performance curvature, positional effects, and synergy determine when division of labor is favored; Guillaume and Otto (2012) showed similarly that the evolution of pleiotropy versus specialization depends on functional trade-offs and trait–fitness mappings. The molecular "escape from adaptive conflict" literature provides empirical examples in which duplication releases a multifunctional protein from antagonistic pleiotropy (Des Marais and Rausher 2008), while heteranthery provides a floral example in which distinct organs can perform different pollen functions (Vallejo-Marín et al. 2009). Our contribution is not to replace these theories. It is to make persistent multifunctionality itself the object to be explained and to separate failure of **value**, failure of **reachability**, and failure of **establishment** as empirically distinguishable causes.

That distinction also clarifies what comparative data can and cannot show. A stronger measured conflict need not predict a greater incidence of division of labor, because the same conflict can differ in recoverability and in the cost of the alternative architecture. The relevant comparative test is therefore not simply "more conflict -> more specialization." It is whether specialization becomes more likely after controlling for the fraction of conflict that can actually be released and for the costs of maintaining separate functional modules. Reversals are possible: a system with stronger conflict can remain integrated while a system with weaker conflict differentiates if the latter can recover more of its conflict at lower cost.

Ecological context adds a second prediction, and a sharper one follows when value, reachability, and establishment are placed on the same gradient. The environment in which division of labor first becomes profitable need not be the environment in which a rare differentiated type can spread. Under convex recovery, the local-reachability crossing can lie between those two points. A set of populations can therefore remain visibly multifunctional while the limiting explanation changes from negative net value, to local inaccessibility, to rare-establishment failure. The phenotype can stay the same while the evolutionary reason for its persistence turns over. Frequency-dependent interactions can move the establishment boundary in either direction. In a floral system, for example, a new presentation architecture could have high intrinsic performance but receive poor service when rare if pollinators learn, assort, or respond to reward frequency; alternatively, negative-frequency dependence could allow a differentiated form to establish before it is intrinsically superior. This is why the profitability and establishment questions should be measured separately rather than collapsed into a single "selection for specialization" estimate.

The *P. rex* literature already establishes the first empirical prerequisite: opposing selection acts on floral exsertion, and the defensive role of water-filled bracts has experimental support (Sun and Huang 2015; Sun, Armbruster, and Huang 2016). It does **not** yet establish why this conflict remains integrated. Doing so would require a design that independently manipulates floral presentation and defensive protection, places their consequences on a common reproductive-fitness scale, and then asks how much fitness an experimentally decoupled arrangement recovers relative to the cost of producing or maintaining that arrangement. Only after a favorable differentiated comparison is demonstrated does it become meaningful to test mutational or developmental reachability and rare-frequency establishment. In this sense, *P. rex* is a motivating biological system, not an empirical result of the present paper.

The finite-population fixation and weak-mutation occupancy results are retained because they show that even after establishment, stronger evolutionary statements require additional process assumptions. They are not the headline biological claim. A shorter empirical application can stop after value, reachability, or rare establishment, depending on the question and available measurements. This keeps the theory subordinate to the biological problem rather than turning every downstream estimand into a required step.

### Position relative to existing theory

The paper therefore sits between three established literatures. The specialization and pleiotropy literature asks when differentiated modules outperform multifunctional ones. The accessibility and adaptive-dynamics literature asks whether a favorable phenotype can be reached and invade. Empirical conflict-resolution literatures—gene duplication, sexual dimorphism, and floral division of labor among them—document particular ways in which shared functions can become decoupled. We connect these literatures around one unresolved observation: **continued multifunctionality under documented conflict**. The new object is the diagnosis of that persistence, not any one algebraic inequality used to formalize it.

This positioning also sets a clear empirical standard. Morphological differentiation alone does not demonstrate functional division of labor, as alternative explanations for heteranthery illustrate (Kay et al. 2020). Conversely, absence of morphological differentiation does not demonstrate weak conflict. A convincing test must measure the conflicting functions, the performance recovered by decoupling them, the cost of the alternative architecture, and—only when relevant—the evolutionary and ecological barriers between the observed and differentiated states.

### Scope boundary

The present paper addresses the persistence or emergence of differentiated architecture from a multifunctional comparison. It does not attempt a general theory of every form of modularity, continuous branching, sexual conflict, gene duplication, social division of labor, or floral diversification. Those literatures supply biological instances and mechanisms; the present analysis asks the narrower question of why a documented functional conflict can end either in division of labor or in persistent multifunctionality.

## Literature Cited

Bowers, R. G., A. Hoyle, A. White, and M. Boots. 2005. The geometric theory of adaptive evolution: trade-off and invasion plots. *Journal of Theoretical Biology* 233:363–377.

Des Marais, D. L., and M. D. Rausher. 2008. Escape from adaptive conflict after duplication in an anthocyanin pathway gene. *Nature* 454:762–765.

Guillaume, F., and S. P. Otto. 2012. Gene functional trade-offs and the evolution of pleiotropy. *Genetics* 192:1389–1409.

Kay, K. M., T. Jogesh, D. Tataru, and S. Akiba. 2020. Darwin's vexing contrivance: a new hypothesis for why some flowers have two kinds of anther. *Proceedings of the Royal Society B* 287:20202593.

Ingleby, F. C., I. Flis, and E. H. Morrow. 2015. Sex-biased gene expression and sexual conflict throughout development. *Cold Spring Harbor Perspectives in Biology* 7:a017632.

Sun, S.-G., W. S. Armbruster, and S.-Q. Huang. 2016. Geographic consistency and variation in conflicting selection generated by pollinators and seed predators. *Annals of Botany* 118:227–237.

Sun, S.-G., and S.-Q. Huang. 2015. Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019.

Vallejo-Marín, M., J. S. Manson, J. D. Thomson, and S. C. H. Barrett. 2009. Division of labour within flowers: heteranthery, a floral strategy to reconcile contrasting pollen fates. *Journal of Evolutionary Biology* 22:828–839.

Dieckmann, U., and R. Law. 1996. The dynamical theory of coevolution: a derivation from stochastic ecological processes. *Journal of Mathematical Biology* 34:579–612.

Egas, M., U. Dieckmann, and M. W. Sabelis. 2004. Evolution restricts the coexistence of specialists and generalists: the role of trade-off structure. *The American Naturalist* 163:518–531.

Espinosa-Soto, C., and A. Wagner. 2010. Specialization can drive the evolution of modularity. *PLoS Computational Biology* 6:e1000719.

Fudenberg, D., M. A. Nowak, C. Taylor, and L. A. Imhof. 2006. Evolutionary game dynamics in finite populations with strong selection and weak mutation. *Theoretical Population Biology* 70:352–363.

Kashtan, N., and U. Alon. 2005. Spontaneous evolution of modularity and network motifs. *Proceedings of the National Academy of Sciences USA* 102:13773–13778.

Richardson, L. F., and J. A. Gaunt. 1927. The deferred approach to the limit. *Philosophical Transactions of the Royal Society of London, Series A* 226:299–361.

Rueffler, C., J. Hermisson, and G. P. Wagner. 2012. Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109:E326–E335.

Taylor, C., D. Fudenberg, A. Sasaki, and M. A. Nowak. 2004. Evolutionary game dynamics in finite populations. *Bulletin of Mathematical Biology* 66:1621–1644.

Wagner, G. P., and L. Altenberg. 1996. Perspective: complex adaptations and the evolution of evolvability. *Evolution* 50:967–976.

Weinreich, D. M., N. F. Delaney, M. A. DePristo, and D. L. Hartl. 2006. Darwinian evolution can follow only very few mutational paths to fitter proteins. *Science* 312:111–114.
