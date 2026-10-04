# Why multifunctional structures persist under conflicting selection

## Abstract

Functional conflict can be resolved in several ways. Functions may remain integrated within one structure, become partitioned among specialized modules, or be separated in time or ecological context. Why does nature use different resolutions to similar conflicts? We distinguish three reasons why a multifunctional architecture can persist even when division of labor is conceivable: differentiation may not repay its structural or regulatory cost; a fitter differentiated state may be separated from the current state by selectively unfavorable intermediates; or ecological interactions may prevent a favorable differentiated type from spreading when rare. These alternatives imply that conflict strength alone cannot predict biological organization. They also predict that environmental change can alter the reason for persistence before morphology changes, because architecture value, evolutionary accessibility, and ecological establishment need not shift together. Natural systems already show the broader pattern: the pollen-consumption conflict is resolved by functional heteranthery in some flowers but by temporal pollen dosing in others, pollinator identity shifts pollen-presentation strategies, and ecological context can partially recouple anatomically decoupled feeding structures. Functional conflict therefore creates an evolutionary problem, but ecology and architecture jointly determine its resolution.

## 1. Introduction

In the subalpine herb *Pedicularis rex*, tubular flowers are subtended by cup-like bracts that hold rainwater. The water protects developing fruits from seed predators, but pollinators favor greater corolla exsertion above the protective bracts. Across 14 populations, greater exsertion was associated with greater pollen receipt and also with greater seed predation: the same floral axis is pulled in opposite directions by mutualists and antagonists (Sun, Armbruster, and Huang 2016). Experimentally draining the bracts increased seed predation, confirming that the water-filled structure contributes to defense (Sun and Huang 2015). This is a concrete multifunctional compromise. The interesting evolutionary question is not simply whether conflict exists, but why conflict of this kind sometimes produces separate functional structures and sometimes remains embedded in one architecture.

Biology contains many versions of this problem. In heterantherous flowers, distinct anther types can divide pollen-feeding and pollen-transfer functions, although alternative functions such as staggered pollen presentation show that morphological differentiation alone does not prove division of labor (Vallejo-Marín et al. 2009; Kay et al. 2020). At the molecular level, gene duplication can allow descendant copies to escape an adaptive conflict that constrained a multifunctional ancestral protein (Des Marais and Rausher 2008). In sexually antagonistic traits, sex-biased or sex-specific regulation can decouple phenotypes that were previously constrained by a shared genome (Ingleby, Flis, and Morrow 2015). Across these systems, differentiation is one possible evolutionary resolution of conflicting functional demands.

The basic conditions favoring specialization are already well developed. General theory shows that division of labor is favored by positional effects, accelerating performance functions, and synergistic interactions among modules, while developmental constraints and maintenance of differentiated pathways can still limit its evolution (Rueffler, Hermisson, and Wagner 2012). Models of pleiotropy likewise show that multifunctionality or specialization depends on the shape of functional trade-offs and on how component performance maps to fitness; complete subfunctionalization is expected only under restricted conditions (Guillaume and Otto 2012). We therefore do not claim that functional conflict automatically produces specialization, or that specialization is favored whenever a verbal trade-off is present. Nor do we claim a first connection between trade-off geometry and invasion: adaptive-dynamics and trade-off–invasion theory already distinguish a phenotype's performance from its ability to invade an ecological background (Dieckmann and Law 1996; Bowers et al. 2005). Egas, Dieckmann, and Sabelis (2004) further showed that an evolutionarily stable specialist–generalist state can nevertheless be unreachable through gradual evolution. Separating endpoint value from reachability is therefore also prior art.

We instead organize these results around a biological problem that is visible across natural systems: **why does the same kind of functional conflict produce different evolutionary resolutions?** Existing theory already identifies conditions favoring specialization and cases in which a stable specialized outcome is not gradually attainable. Natural history adds a further complication: structural division of labor is only one possible resolution. The same underlying conflict can also be reduced by temporal regulation, by retaining an integrated architecture, or by combining partial structural differentiation with continued ecological integration. We focus on why an integrated architecture can remain one of these viable outcomes. It may remain because separation simply does not pay after structural, developmental, regulatory, or maintenance costs are included; because a fitter differentiated state lies beyond selectively unfavorable intermediates; or because ecological interactions prevent a favorable differentiated type from spreading when rare.

This distinction changes how conflict should be interpreted comparatively. Stronger opposing selection need not imply a greater tendency toward division of labor, because systems can differ in how much of the conflict differentiation actually releases and in the cost of the alternative architecture. Likewise, the ecological position where differentiation becomes profitable need not coincide with the position where a rare differentiated type can establish. Persistent multifunctionality is therefore an evolutionary outcome in its own right, not merely unfinished specialization and not a direct measure of conflict strength.

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

The resulting theory generates two broad ecological predictions. First, conflict magnitude can be decoupled from differentiation when recoverability or architecture cost varies. Second, ecological context can shift the transition from integration to division of labor because the environment where differentiation becomes profitable need not be the environment where it becomes reachable or can establish. Figure 1 summarizes these alternative evolutionary states; the equations are tools for explaining biological organization rather than the subject of the paper.

![](../figures/FIG1_LOGIC_DIAGRAM.svg)

**Figure 1. Three reasons why multifunctionality can persist despite conflict.** After a functional conflict has been established, division of labor can fail at three biologically different stages: the differentiated architecture may not repay its own cost (`Phi<0`); a fitter differentiated endpoint may be locally inaccessible (`Phi>0, g_0<0`); or a favorable and initially reachable differentiated type may fail to establish when rare (`Phi>0, g_0>0, Delta_R<0`). These routes converge on the same observed phenotype—persistent multifunctionality—but imply different evolutionary responses to changes in architecture and ecology. *Pedicularis rex* illustrates a system in which conflict is documented while its evolutionary resolution remains integrated.

## 2. Functional conflict creates the problem, not its resolution

Consider two or more fitness-relevant functions constrained to one phenotypic coordinate. Let `L>=0` denote the fitness loss created by forcing those functions onto a shared compromise. `L>0` therefore means that the same architecture cannot simultaneously occupy the function-specific optima.

That conflict does not specify what evolution should do next. A lineage can retain the compromise, divide functions among structures, regulate the shared structure differently across time or context, or combine these responses. The pollen dilemma illustrates this immediately: pollen can be lost to pollinators as food yet is also required for male reproduction, but natural plants respond through several distinct floral strategies rather than one universal architecture.

In the theory below, `L` is therefore the magnitude of the problem that differentiation might release. It is not itself a pressure toward any particular solution. This distinction is essential because two systems with equally strong conflict can occupy different architectures, whereas two systems with different conflict strengths can converge on the same organization.

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

## 7. Three evolutionary states behind persistent multifunctionality

Continued integration does not imply one evolutionary condition. The same multifunctional phenotype can occupy three biologically different states.

| Evolutionary state | Formal condition | Biological meaning | Expected response to ecological or architectural change |
|---|---|---|---|
| **adaptive integration** | `L>0, Phi<0` | conflict is real, but an integrated architecture still has higher net value than the declared divided alternative | stronger recoverability or lower architecture cost can make division of labor favorable |
| **historical or developmental trapping** | `Phi>0, g_0<0` | a differentiated endpoint is fitter, but sufficiently small changes away from integration are initially selected against | a new developmental route, recombination, large-effect change, or altered path cost can release the system |
| **ecological stabilization of integration** | `Phi>0, g_0>0, Delta_R<0` | differentiation is favorable and initially reachable, but a rare differentiated type performs poorly in its ecological background | changing competitors, mutualists, enemies, or frequency-dependent interactions can permit establishment |

Here `g_0=R'(0)-k` is the local fitness gradient away from the integrated architecture, and `Delta_R` is the selection difference experienced by a rare differentiated type. A fourth state, `Phi>0, g_0>0, Delta_R>0`, removes these three early barriers but still does not guarantee fixation or historical realization.

The biological distinction is therefore not merely between "specialized" and "unspecialized." An integrated structure can be the favored architecture, a locally trapped architecture, or an architecture maintained by its ecological context. The same morphology can consequently have different evolutionary meanings in different populations or environments.

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

The point is not the difficulty of these inequalities. It is that the same persistent phenotype can be generated by three different evolutionary states, and those states respond differently when architecture or ecology changes.

## 9. Biological predictions

These distinctions change the biological interpretation of several common comparative patterns.

### The reason for persistence can change before the phenotype does

Consider an environmental coordinate `E` that progressively lowers the marginal cost of architectural release,

```text
k(E)=k0-c(E-E0),
c>0.
```

This slice can represent, for example, a resource or developmental context in which maintaining separate functional structures becomes progressively cheaper. With convex recovery, the environment at which differentiation first becomes profitable (`E_V`) necessarily precedes the environment at which sufficiently small release steps become uphill (`E_A`):

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

This is stronger than saying that environment changes the amount of selection for specialization. It predicts **turnover in the reason why the same multifunctional phenotype persists**. Along a geographic or environmental gradient, populations can therefore remain morphologically integrated even while the evolutionary state maintaining that integration changes.

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

## 10. Natural systems show multiple resolutions of functional conflict

The natural-history record already rejects a simple rule in which stronger conflict automatically produces more structural division of labor. Similar functional problems can be resolved by different combinations of spatial differentiation, temporal regulation, and retained multifunctionality (Fig. 3).

![](../figures/FIG3_EMPIRICAL_LADDER.svg)

**Figure 3. Natural systems use different resolutions to functional conflict.** In pollen-reward flowers, pollen is simultaneously a male gamete and food for pollinators. *Solanum rostratum* partitions these roles partly among different anther types, while also releasing pollen gradually across bee visits. In *Clarkia*, superficially similar heteranthery does not produce feeding versus pollinating anthers; the two whorls instead differ mainly in timing of pollen presentation. Across *Penstemon* and *Keckiella*, bee-adapted species release pollen more gradually than hummingbird-adapted relatives, showing that pollinator ecology changes the favored temporal solution. In *Pedicularis rex*, pollinator-mediated selection for floral exposure is opposed by seed-predator-mediated selection for protection, but the antagonist component varies strongly among populations. Cichlid oral and pharyngeal jaws illustrate a broader animal analogue: structural decoupling of prey capture and processing expanded trophic diversity, yet feeding ecology still produces correlated evolution between the two jaw systems.

### The same pollen conflict can be divided in space, divided in time, or both

Pollen-reward flowers provide the clearest natural comparison because the underlying conflict is unusually explicit: pollen must both attract or reward pollinators and survive as male gametes. In *Solanum rostratum*, feeding anthers are preferentially handled by bumble bees whereas pollinating anthers export proportionally more pollen, supporting genuine functional division of labor (Vallejo-Marín et al. 2009). Yet the same species also dispenses pollen gradually across successive bumble-bee buzzes (Vallejo-Marín and Lundgren 2026). Structural differentiation and temporal regulation therefore coexist in one natural system rather than representing mutually exclusive endpoints.

*Clarkia* reaches a different resolution. Its two anther whorls look like a classic division-of-labor system, but pollen from both whorls is collected and exported by bees in similar functional roles. Instead, delayed dehiscence of one whorl produces staggered pollen presentation (Kay et al. 2020). Thus morphological differentiation need not mean functional partitioning, and the same broad pollen-consumption conflict can be alleviated without assigning one organ type exclusively to reward and another to reproduction.

### Ecological partners change which resolution is favored

The temporal solution itself varies with pollinator ecology. Across *Penstemon* and *Keckiella*, transitions between hymenopteran and hummingbird pollination are associated with predictable changes in pollen presentation. After accounting for phylogeny, bee-adapted species dispense pollen more gradually, whereas hummingbird-adapted relatives present it more simultaneously; a species pair that appeared exceptional achieved comparable dosing through the timing of anther maturation (Castellanos et al. 2006). The relevant evolutionary outcome therefore depends not only on the plant's internal functional conflict but also on how efficiently its ecological partner removes, grooms, and delivers pollen.

The same ecological principle appears at the level of geographic variation within a species. In *Pedicularis rex*, greater corolla exsertion increases pollen receipt but also seed predation. Pollinator-mediated effects were comparatively consistent across the 14 populations studied, whereas seed-predator effects formed a geographic mosaic; observed seed predation ranged from less than 1% in some populations to more than 27% in another (Sun, Armbruster, and Huang 2016). The same integrated floral architecture can therefore experience very different balances of mutualist and antagonist selection across its range without first changing its gross morphology.

### Division of labor can release a trade-off without producing complete independence

Cichlid feeding systems show the same logic outside flowers. Separate oral and pharyngeal jaws decouple prey capture from prey processing and relax the force–mobility trade-off that constrains a single jaw system. Across Neotropical cichlids, this decoupling is associated with novel trait combinations and greater trophic diversity (Burress, Martinez, and Wainwright 2020). Yet the two jaw systems still show aligned evolutionary responses across feeding guilds. Ecology therefore partially re-couples structures that anatomy has decoupled.

Natural systems consequently do not fall neatly into "multifunctional" versus "divided." They occupy combinations of structural partitioning, temporal partitioning, plasticity, and ecological coupling. The theoretical contrast developed here should therefore be read as the axis of **structural release from a shared functional compromise**, not as a claim that evolution chooses only between two discrete organismal designs.

## 11. Downstream consequences after establishment

Once a differentiated type can establish, its eventual fixation or long-run prevalence depends on demography, stochasticity, and mutation. Those questions belong to a later population-genetic layer rather than to the origin of the multifunctional-versus-divided architecture itself. For the specific exponential Moran and symmetric rare-mutation process analyzed in the supporting theory, reciprocal fixation ordering and monomorphic occupancy re-align on the same `Phi=0` boundary, whereas invasion can still depend on frequency feedback. The full process derivation is retained in the supporting theory as a boundary on stronger claims, not as a fourth ecological explanation.

## 12. Discussion

The biological problem addressed here is why comparable functional conflicts generate different forms of biological organization. Natural flowers already show that there is no single answer. A pollen-consumption conflict can produce functional heteranthery, temporal pollen dosing, or both; pollinator identity can shift the favored presentation strategy; and geographically variable enemies can change the balance of opposing selection within one species. *Pedicularis rex* makes the latter problem tangible: greater floral exposure improves pollen receipt but also exposes reproductive tissues to seed predators, while water-filled bracts provide protection, and the strength of the antagonistic component varies geographically.

This view turns persistent multifunctionality from a single outcome into three alternative explanations. In the first, integration persists because it is still the better architecture after the costs of separation are paid. In the second, division of labor would be better if present, but the route from the current structure initially runs downhill in fitness. In the third, a differentiated form is both favorable and reachable but cannot spread from rarity because its ecological interactions are frequency dependent. These alternatives matter because they imply different evolutionary histories and, crucially, different responses to environmental change. An integrated structure that is itself favored should persist until the economics of architecture changes. A trapped structure can change abruptly when a new evolutionary route appears. An ecologically stabilized structure can change when its interacting community changes even if its intrinsic architecture has not.

The first alternative connects directly to existing theories of specialization. Rueffler, Hermisson, and Wagner (2012) showed that performance curvature, positional effects, and synergy determine when division of labor is favored; Guillaume and Otto (2012) showed similarly that the evolution of pleiotropy versus specialization depends on functional trade-offs and trait–fitness mappings. The molecular "escape from adaptive conflict" literature provides empirical examples in which duplication releases a multifunctional protein from antagonistic pleiotropy (Des Marais and Rausher 2008), while heteranthery provides a floral example in which distinct organs can perform different pollen functions (Vallejo-Marín et al. 2009). Our contribution is not to replace these theories. It is to treat persistent multifunctionality as one possible evolutionary resolution of conflict and to separate three ways in which that resolution can be maintained: **adaptive integration**, **historical or developmental trapping**, and **ecological stabilization**.

That distinction also clarifies what comparative data can and cannot show. A stronger measured conflict need not predict a greater incidence of division of labor, because the same conflict can differ in recoverability and in the cost of the alternative architecture. The expected macroevolutionary pattern is therefore not simply "more conflict -> more specialization." Reversals are possible: a lineage under stronger conflict can remain integrated while another under weaker conflict differentiates if the latter can release more of its compromise at lower cost. More generally, ecology can favor entirely different resolutions of the same conflict, as the contrast among functional heteranthery, temporal pollen dosing, and pollinator-dependent presentation strategies demonstrates.

Ecological context adds a second prediction, and a sharper one follows when value, reachability, and establishment are placed on the same gradient. The environment in which division of labor first becomes profitable need not be the environment in which a rare differentiated type can spread. Under convex recovery, the local-reachability crossing can lie between those two points. A set of populations can therefore remain visibly multifunctional while the limiting explanation changes from negative net value, to local inaccessibility, to rare-establishment failure. The phenotype can stay the same while the evolutionary reason for its persistence turns over. Frequency-dependent interactions can move the establishment boundary in either direction. In a floral system, for example, a new presentation architecture could have high intrinsic performance but receive poor service when rare if pollinators learn, assort, or respond to reward frequency; alternatively, negative-frequency dependence could allow a differentiated form to establish before it is intrinsically superior. Profitability and establishment are therefore distinct evolutionary transitions rather than two labels for a single "selection for specialization" process.

The *P. rex* case also shows why geography matters. The pollination benefit of floral exposure is opposed by protection from seed predators, but the antagonistic side of that conflict varies markedly among populations (Sun and Huang 2015; Sun, Armbruster, and Huang 2016). The same morphology can therefore sit in different selective environments across a species' range. The theory predicts that such geographic variation need not merely change the strength of selection on one trait; it can change which evolutionary state maintains integration and, eventually, whether structural division of labor becomes favorable or able to spread.

The finite-population fixation and weak-mutation occupancy results are retained only as downstream consequences after establishment. They are not additional explanations for multifunctionality and are not needed for the ecological argument developed here.

### Position relative to existing theory

The paper therefore sits between three established literatures. The specialization and pleiotropy literature identifies conditions favoring or opposing differentiated modules. The accessibility and adaptive-dynamics literature shows that evolutionary stability, attainability, and invasion need not coincide. Empirical conflict-resolution literatures—gene duplication, sexual dimorphism, and floral division of labor among them—document particular routes by which shared functions become decoupled. We connect these literatures around one empirical observation: **functional conflict has multiple evolutionary resolutions in nature**. The residual contribution is not another condition for specialization in isolation, but an account of why integrated architecture can remain adaptive, become historically trapped, or be stabilized by ecological interactions, and why the dominant resolution can change across environments.

Morphological differentiation alone does not demonstrate functional division of labor, as *Clarkia* makes clear (Kay et al. 2020). Conversely, morphological integration does not demonstrate weak conflict, as *P. rex* makes clear. The natural-history contrast is therefore substantive: similar conflicts can be resolved by spatial partitioning, temporal partitioning, persistent multifunctionality, or combinations of these strategies.

### Scope boundary

The present paper addresses structural release from a multifunctional compromise and its ecological context. It does not attempt a general theory of every form of modularity, temporal partitioning, plasticity, sexual conflict, gene duplication, social division of labor, or floral diversification. Those alternatives matter precisely because nature often combines them. The present analysis asks why structural division of labor becomes one resolution in some ecological settings while integrated architecture remains viable in others.

## Literature Cited

Bowers, R. G., A. Hoyle, A. White, and M. Boots. 2005. The geometric theory of adaptive evolution: trade-off and invasion plots. *Journal of Theoretical Biology* 233:363–377.

Burress, E. D., C. M. Martinez, and P. C. Wainwright. 2020. Decoupled jaws promote trophic diversity in cichlid fishes. *Evolution* 74:950–961.

Castellanos, M. C., P. Wilson, S. J. Keller, A. D. Wolfe, and J. D. Thomson. 2006. Anther evolution: pollen presentation strategies when pollinators differ. *The American Naturalist* 167:288–296.

Des Marais, D. L., and M. D. Rausher. 2008. Escape from adaptive conflict after duplication in an anthocyanin pathway gene. *Nature* 454:762–765.

Dieckmann, U., and R. Law. 1996. The dynamical theory of coevolution: a derivation from stochastic ecological processes. *Journal of Mathematical Biology* 34:579–612.

Egas, M., U. Dieckmann, and M. W. Sabelis. 2004. Evolution restricts the coexistence of specialists and generalists: the role of trade-off structure. *The American Naturalist* 163:518–531.

Fudenberg, D., M. A. Nowak, C. Taylor, and L. A. Imhof. 2006. Evolutionary game dynamics in finite populations with strong selection and weak mutation. *Theoretical Population Biology* 70:352–363.

Guillaume, F., and S. P. Otto. 2012. Gene functional trade-offs and the evolution of pleiotropy. *Genetics* 192:1389–1409.

Ingleby, F. C., I. Flis, and E. H. Morrow. 2015. Sex-biased gene expression and sexual conflict throughout development. *Cold Spring Harbor Perspectives in Biology* 7:a017632.

Kay, K. M., T. Jogesh, D. Tataru, and S. Akiba. 2020. Darwin's vexing contrivance: a new hypothesis for why some flowers have two kinds of anther. *Proceedings of the Royal Society B* 287:20202593.

Rueffler, C., J. Hermisson, and G. P. Wagner. 2012. Evolution of functional specialization and division of labor. *Proceedings of the National Academy of Sciences USA* 109:E326–E335.

Sun, S.-G., W. S. Armbruster, and S.-Q. Huang. 2016. Geographic consistency and variation in conflicting selection generated by pollinators and seed predators. *Annals of Botany* 118:227–237.

Sun, S.-G., and S.-Q. Huang. 2015. Rainwater in cupulate bracts repels seed herbivores in a bumblebee-pollinated subalpine flower. *AoB PLANTS* 7:plv019.

Taylor, C., D. Fudenberg, A. Sasaki, and M. A. Nowak. 2004. Evolutionary game dynamics in finite populations. *Bulletin of Mathematical Biology* 66:1621–1644.

Vallejo-Marín, M., and A. Lundgren. 2026. Gradual pollen release in a buzz-pollinated plant: investigating pollen presentation theory under bee visitation. *Functional Ecology* 40:476–485.

Vallejo-Marín, M., J. S. Manson, J. D. Thomson, and S. C. H. Barrett. 2009. Division of labour within flowers: heteranthery, a floral strategy to reconcile contrasting pollen fates. *Journal of Evolutionary Biology* 22:828–839.
