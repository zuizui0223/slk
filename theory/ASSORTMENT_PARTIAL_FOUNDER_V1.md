# SLK supplementary ecological derivation — spatial assortment and founding clusters

## Why this matters biologically

A resident population can be resistant to a **single rare new architecture** but vulnerable to a local founding cluster of the same architecture. The global frequency of a structural innovation does not, by itself, determine how many partners of its own type it encounters. This supplement makes that distinction explicit for the already verified partial-division resident witness.

**Prior art:** Spatial sorting, partner matching, positive frequency dependence, alternative stable states, and clustered specialist patches are established ecological phenomena. See Lehtonen & Kokko (2012), Carlson, Akçay & Morsky (2023), and Zou & Rudolf (2023). This document is a **conditional transport of the existing SLK frequency frontier into an explicit encounter model**, not a first discovery of spatial rescue or assortative coordination.

## Encounter scheme and limits

Let `u` denote a divided variant and `v` its established resident. Write `p` for the **census frequency within a defined interaction region** of `u`, and `r in [0,1]` for non-random same-architecture assortment. The model defines conditional encounter probabilities:

```text
P(v encountered | focal u)=(1-r)(1-p)
P(u encountered | focal v)=(1-r)p
P(u encountered | focal u)=r+(1-r)p
P(v encountered | focal v)=r+(1-r)(1-p).
```

These probabilities satisfy encounter reciprocity:

```text
p P(v|u)=(1-p) P(u|v)=p(1-p)(1-r).
```

Thus `r` represents assortative encounters, **not population density, raw dispersal rate, or an extra fitness benefit**. It is meaningful only for an encounter network consistent with the declared conditional probabilities; it should be estimated from contacts or partner exposures rather than inferred from an aerial photograph of clumping.

For two degrees of division `u,v`, let `F` be the intrinsic architecture fitness and `M(u,v)>0` a symmetric nonnegative mismatch cost scaled by `eta>0`. Relative interaction fitness is

```text
W_u=F(u)-eta M(u,v) (1-r)(1-p),
W_v=F(v)-eta M(u,v) (1-r)p,
Delta(u,p|v,r)
  =F(u)-F(v)+eta M(u,v)(1-r)(2p-1).
```

This exactly recovers the existing two-type cusp or smooth-mismatch witness at `r=0`. For a strict two-type pair, the positive-frequency feedback strength is effectively attenuated to `eta(1-r)`, without changing the intrinsic architecture difference. Do **not** apply this multiplicative attenuation unmodified to games with asymmetric partner costs or many simultaneously interacting architectures.

## Conditional founder threshold and the frequency–assortment crossover

Put `A=F(u)-F(v)` and `B=eta M(u,v)>0`. When `r<1`, the zero-growth boundary is

```text
p_escape(r)=1/2-A/[2B(1-r)].
```

If `0<p_escape<1`, the invading `u` increases only when `p>p_escape`. When `p_escape<=0`, it increases at every `p in (0,1)`; when `p_escape>=1`, it fails for all interior frequencies. At `r=1`, partner-mismatch differences vanish and the sign is simply `sign(A)`.

If `0<A<B` (as in the partial-resident witness), a positive-frequency invasion barrier exists under random encounters and disappears when

```text
r>=r_crit=1-A/B.
```

Under the same fixed `F,M,eta`, increased assortative encounters therefore permit a clustered *multicell/multi-individual introduction* to spread even at a low census frequency. They **do not rescue an isolated single mutant** incapable of making same-type encounters: the `p->0,r>0` asymptotic describes a sequence of **globally rare but internally clustered propagules**, not a solitary allele with partners magically appearing.

The sign of the effect of assortment on relative fitness also reverses at equal representation:

```text
partial Delta / partial r
   = -eta M(u,v)(2p-1).

p<1/2: assortativity increases the divided variant's relative fitness;
p=1/2: assortativity has no effect on the *relative selection difference*;
p>1/2: assortativity decreases its relative advantage.
```

This is a **falsifiable crossover signature** of the symmetric matching-cost assumption, not a universal property of spatial structure. It differs from adding an unconditional density-related benefit to `u`, which would ordinarily shift relative fitness without this forced crossover. The signature may fail if architecture affects intrinsic productivity, encounter rates or demographic performance beyond the declared mismatch term.

## Exact conditional witness: full specialists versus an established partial resident

Use the existing registered parameters `u=1`, `v=d_*=1/7`, `F(d)=0.25d+d^2`, `w(d)=0.1d+0.9d^2`, `M_1(u,v)=|w(u)-w(v)|`, and `eta=3/2`.

```text
A=117/98 = 585/490,
B=711/490,
A/B=65/79.

p_escape(0)=7/79 = 0.0886075949...
r_crit=14/79 = 0.1772151899...
p_escape(1/10)=61/1422 = 0.0428973277...
p_escape(1/5)=-9/632 <0.
```

Hence, under random encounters, a complete specialist must exceed ~8.86% of the local interaction population before it increases. Under `r=0.1` this model threshold falls to ~4.29%; above `r=14/79`, the mismatch-mediated rarity barrier vanishes in the conditional limiting sense just explained. At `p=1/2`, relative fitness is always `117/98` regardless of `r`.

These fractions are **dimensionless properties of a deliberately constructed model**, not estimates from *Pedicularis*, bacteria, or any real species.

## Separating founding frequency, assortment, density and community composition

A direct ecological test uses a factorial design with two resident identities (integrated S and already established partial P), several founding fractions of full D, and randomized versus aggregated spatial arrangements *at matched total population density and matched census D frequency*. Measure both actual interaction/partner encounter matrices and full-cycle reproductive or population growth.

The focal prediction is not merely that clumping helps invasion. It is that (a) the **critical frequency changes with encounter assortment**, (b) its sign-sensitive dependence on `p` shows the equal-frequency crossover under symmetric mismatch costs, and (c) changing the resident from S to P changes the ecological barrier even with the identical D genotype. The matched-density arm is essential to distinguish partner assortment from crowding/resource concentration; a treatment altering spatial arrangement may also alter microenvironment or dispersal, and those effects must be quantified.

**Data needed:** local census and spatial arrangement, observed interaction matrix/partner identities, density/resources, complete-cycle growth of D relative to the relevant resident. A density-only treatment (as in existing *Pedicularis rex* observations) does **not** identify this D–P encounter mechanism. Nor does a D-in-S experiment identify invasion against an already established P.

## Strong boundary on what can be inferred

- The pairwise formula does not establish spatial population growth, invasion-wave speed, fixation probability, coexistence, mutation supply, or long-run evolutionary transition.
- If `r` itself varies with `p` or density, the simple linear frequency response can curve and the experimental design must estimate that joint dependence.
- If rare mutants appear one at a time, `r>0` may be biologically unavailable at first introduction.
- Spatial assortment is already a major theme in cooperation, mutualism, evolutionary games, and priority-effect research. The SLK-specific purpose is to show how ecological neighborhood composition can change the apparent persistence of an *unchanged partially divided architecture* while retaining the same intrinsic architecture value.

## Literature for ecological scope

- Lehtonen J, Kokko H. 2012. Positive feedback and alternative stable states in inbreeding, cooperation, sex roles and other evolutionary processes. *Philosophical Transactions of the Royal Society B* 367:211–221. DOI 10.1098/rstb.2011.0177.
- Carlson C, Akçay E, Morsky B. 2023. The evolution of partner specificity in mutualisms. *Evolution* 77:881–892. DOI 10.1093/evolut/qpac056. Spatial sorting and matched-specialist patches are already considered there.
- Zou H-X, Rudolf VHW. 2023. Bridging theory and experiments of priority effects. *Trends in Ecology & Evolution* 38:1203–1216. DOI 10.1016/j.tree.2023.08.001.
- Leibold MA and colleagues' broader literature on spatial priority effects, dispersal, and local community structure also sets an established prior-art boundary; no first-principles spatial-ecology discovery is claimed.
