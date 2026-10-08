# SLK — partial division after establishment: evolutionary arrest is not identified by invasion from integration

## Biological question

A partially divided architecture can increase when rare against an integrated resident, even while the completely divided architecture declines. Does that partial form then stop evolution toward complete division, or can specialization continue once partial forms become common?

**Result:** both histories are compatible with exactly the same frequency response for every pair `{integrated S, divided variant d}`. Fitness against an integrated resident identifies establishment, not the evolutionary fate of partial division after it has replaced integration. The distinction depends on interactions between *two nonzero degrees of differentiation*.

## Starting point: the existing and tested SLK family

Let `d in [0,1]` denote structural division and `S=0`. With the existing rare-path witness at `E=2.25`,

```text
F(d) = 0.25 d + d^2,
w(d) = 0.1 d + 0.9 d^2,
eta = 1.5,
Delta(d,p | S) = F(d) + eta w(d)(2p-1).
```

Here `p` is the frequency of variant `d` in a two-type population of `S` and `d`. The rare-invasion payoff is

```text
H(d)=Delta(d,0 | S)=F(d)-eta w(d)
    =0.1d-0.35d^2.
```

Thus `d in (0,2/7)` invades integration, `d=1` fails (`H(1)=-1/4`), and `d_*=1/7` maximizes rare invasion from S (`H(d_*)=1/140>0`). These are **invasion statements**, not stability conclusions.

## A consistent multi-architecture interaction model

Assign each focal architecture `u` an intrinsic fitness `F(u)` and a symmetric mismatch cost whenever it encounters an architecture `v` with a different degree of dependence `w(v)`:

```text
A_0(u,v)=F(u)-eta |w(u)-w(v)|.
```

This is one **extra ecological assumption**, not something identified by the original two-type selection difference. In a population of S and d, the frequency-weighted payoffs are

```text
W_d(p)=F(d)-eta (1-p)w(d),
W_S(p)=-eta p w(d),
W_d(p)-W_S(p)=F(d)+eta w(d)(2p-1).
```

So this extension exactly recovers all existing S-versus-d selection curves, not merely the rare endpoint. The invasion fitness of a rare mutant `u` against a monomorphic resident `v` is now

```text
I_0(u|v)=A_0(u,v)-A_0(v,v)
        =F(u)-F(v)-eta |w(u)-w(v)|.
```

If `u>v` and `w` increases, `I_0(u|v)=H(u)-H(v)`, where `H=F-eta w`. If `u<v`, `I_0(u|v)=J(u)-J(v)`, where `J=F+eta w`.

In the witness, `J(d)=0.4d+2.35d^2` is strictly increasing, while `H(d)=0.1d-0.35d^2` has a strict maximum at `d_*=1/7`. Consequently:

- For every resident `v in [1/7,1]`, all `u<v` have `I_0(u|v)<0` (since J increases), and all `u>v` have `I_0(u|v)<0` (since H decreases after 1/7).
- Thus **every** monomorphic resident degree `v in [1/7,1]` is strictly uninvadable by a single rare, different degree under this specific symmetric mismatch model.
- Among very small positive variants introduced into S, larger degrees are favored until `d_*=1/7`. Under successive sufficiently small successful substitutions from S, `d_*` is a possible evolutionary arrest point; it is **not a unique global optimum**. Large introductions and different histories can settle at other resistant degrees, including full division.
- In the S–`d_*` two-type competition, `Delta(d_*,0|S)>0` and its slope in p is positive, so after successful initial invasion it is favored at every frequency and can replace S. This still does not prove it is universally evolutionarily or ecologically stable under other interaction models.

The result is a local and global **single-rare-mutant invasion** conclusion, not a theorem about polymorphic coalitions, fluctuating environments, finite-population fixation, or mutation supply.

## Rare-mutant resistance is not resistance to finite introduction

Both mismatch models have exactly the same fitness difference for a focal pair `u,v` at every introduction frequency `p` of `u`, once their respective symmetric mismatch magnitudes `M(u,v)>0` are specified:

```text
Delta(u,p | v)
  = [F(u)-F(v)] + eta M(u,v)(2p-1).

p_escape(u|v)
  = 1/2 - [F(u)-F(v)]/[2 eta M(u,v)].
```

When `0<p_escape<1`, the pair has an unstable internal frequency threshold: `u` loses from rarity against `v`, but increases if introduced above `p_escape`. For `u>v` in this witness, `F(u)>F(v)`, and when rare invasion fails the positive threshold lies below one half. This is **positive frequency-dependent bistability** in an explicitly declared pairwise resident context, not unconditional stability of a partial phenotype.

For the cusp-like symmetric mismatch `M_1=|w(u)-w(v)|`, resident `v=d_*=1/7`, and complete mutant `u=1`:

```text
F(1)-F(1/7) = 117/98,
eta M_1(1,1/7) = 711/490,

Delta(1,0 | 1/7) = -9/35,
p_escape(1|1/7) = 7/79 = 0.0886075949...
```

Therefore a complete specialist initially making up more than **8.86% of this two-architecture population** is favored under the same model in which a single rare complete specialist cannot invade the partially divided resident. This exact percentage is a **model-witness threshold**, not an empirical estimate or a prediction for any specific natural organism. If the underlying deterministic two-type frequency dynamics are replicator-like, frequencies above the unstable boundary increase toward full division, while those below decline. Drift, demography, spatial clustering, recombination, and immigration require explicit extensions.

The absence of a uniform resilience margin is sharper still. Put `u=d_*+delta` with `0<delta<=6/7`. Direct substitution gives

```text
Delta(u,0 | d_*) = -(7/20) delta^2,
p_escape(d_*+delta | d_*)
  = 49 delta/(150+378 delta).
```

Although **every** distinct rare mutant is selected against the monomorphic `d_*` resident in the cusp model, its founding-frequency threshold tends to **zero** as the mutant's phenotypic distance `delta` tends to zero. This distinction is important: pointwise uninvadability of each rare type does not provide a nonzero frequency threshold that protects the resident uniformly against all nearby types. The ecological meaning is an increasingly weak barrier to *slightly further differentiation*, not evidence of realized evolution.

### Fixed finite coalitions cannot bypass strictly negative rarity fitness arbitrarily close to zero

For completeness, fix a finite set of mutant phenotypes `u_i != v` with `I(u_i|v)<0` individually and hold their internal relative composition `q_i` fixed. With total mutant frequency `epsilon` in a finite continuous payoff game, the difference in fitness between each mutant and the resident is continuous and equals `I(u_i|v)` at `epsilon=0`. Thus there exists a common sufficiently small positive `epsilon_0` such that all mutant types decline relative to the resident for `0<epsilon<epsilon_0`. A coalition of fixed variants therefore does not magically overcome the rare-establishment gate **at arbitrarily low total frequency**.

This statement does *not* supply a uniform `epsilon_0` for arbitrarily many mutants approaching `v` or for mechanisms with discontinuous collective assembly. Finite founding clusters can still cross the frequency frontier, and the smooth-mismatch evolutionary relay below changes the resident between mutation events. These are separate biological mechanisms.

## A second *symmetric* model: smooth mismatch permits onward specialization

The arrest of partial division under `A_0` is caused by an ecological mismatch penalty that is **first order** in even tiny differences between already differentiated forms. This is not forced by any of the binary S-versus-d experiments. Consider an alternative symmetric, nonnegative mismatch cost:

```text
M_q(u,v)
= |w(u)-w(v)|^q / [w(u)+w(v)]^(q-1),
  when w(u)+w(v)>0;
M_q(0,0)=0,
A_q(u,v)=F(u)-eta M_q(u,v).
```

For `q=1`, `M_1(u,v)=|w(u)-w(v)|`, recovering the preceding cusp-cost model. For `q=2`, `M_2=(w(u)-w(v))^2/[w(u)+w(v)]`, which is smooth at any resident `v>0` where `w(v)>0`.

The key identity holds for **every q>=1**:

```text
M_q(d,0)=w(d), M_q(d,d)=0.
```

Accordingly, the models have exactly the same `S`–`d` payoff matrices, at every frequency and every structural degree. But their infinitesimal invasion behavior against a resident `v>0` differs:

```text
I_q(v+epsilon|v)
 = F(v+epsilon)-F(v)-eta M_q(v+epsilon,v).

For q=1 and epsilon>0:
  lim I_1(v+epsilon|v)/epsilon = F'(v)-eta w'(v)=H'(v).

For q>1 and v>0:
  M_q(v+epsilon,v)=O(|epsilon|^q),
  lim I_q(v+epsilon|v)/epsilon = F'(v).
```

Because `F'(v)=0.25+2v>0` throughout the witness, **every partial resident `v in (0,1)` can be invaded by a sufficiently nearby *more differentiated* mutant under q=2**, while nearby downward mutants are disfavored. Under `q=1`, by contrast, any resident `v>=1/7` resists both directions. Thus the same symmetric matching idea, but with **linear versus superlinear onset of the cost of mismatching already-specialized types**, gives arrest versus a possible gradual route toward full specialization.

A more concrete **ecological stepping-stone** effect follows from this smooth model. Full differentiation does not invade `S` (`I_2(1|0)=-0.25`) or the initially favorable resident `d_*=1/7` (`I_2(1|1/7)≈-0.165379`). But as successive favorable small-step replacements increase the resident degree, the full endpoint becomes invasible once the resident exceeds the nontrivial root `v_threshold≈0.2861530260` of

```text
I_2(1|v)
=F(1)-F(v)-eta [1-w(v)]^2/[1+w(v)]
=0.
```

In the present witness this threshold lies *just above* `2/7≈0.285714`, the neutral upper boundary of degrees that can invade `S`. Thus an intermediate degree that cannot itself establish directly from integration can nevertheless become established by sequential replacement and then open the door to complete division. This ordering and numerical proximity are **witness-specific**. `I_2(1|v)>0` for residents immediately above the lower crossing, while `I_2(1|1)=0` trivially because the mutant equals the resident; do not treat the endpoint equality as a second distinct invasion event.

This is not an assertion of guaranteed global convergence of a stochastic evolutionary process. The smooth example establishes an open direction of favorable small mutations from each interior resident; whether successive successful mutants are supplied and establish over evolutionary time is an additional population-genetic question.

The `q=2` smooth mismatch model provides the cleanest demonstration of why `S`–`d` assays cannot decide partial stability **without assuming directional competitive dominance**. The following `lambda` example is retained to show a stronger, additional possibility: a fully divided mutant can even invade an already established partial form *directly*, when asymmetric interactions among differentiated forms are allowed.

## A counterexample with exactly the same S-versus-d evidence

Add a directional effect of encounters between two already differentiated forms:

```text
A_lambda(u,v)=F(u)-eta |w(u)-w(v)|+lambda u v (u-v).
```

For `u=0` or `v=0`, the added term vanishes; it also vanishes in monomorphic populations (`u=v`). Therefore **all** S-versus-d pairwise comparisons at **all frequencies** are exactly identical for every `lambda`, and resident baseline fitness is still `F(v)`.

But for `u,v>0` the rare-mutant difference becomes

```text
I_lambda(u|v)
  =F(u)-F(v)-eta |w(u)-w(v)|+lambda u v (u-v).
```

At the same `d_*=1/7`, the completely divided mutant's invasion fitness is

```text
I_lambda(1|d_*)
=H(1)-H(d_*)+lambda d_*(1-d_*)
=-9/35+(6/49)lambda.
```

This crosses zero at `lambda=21/10=2.1`. Thus `lambda=0` makes `d_*` strictly resistant, but `lambda=3` makes `d=1` invade `d_*` from rarity, even though `d=1` still **cannot** invade S from rarity.

More strongly, for `lambda=3` every resident `v in [0,1)` can be invaded by a sufficiently close larger `u=v+epsilon`, since the one-sided upward invasion gradient is

```text
lim_{epsilon->0+} I_3(v+epsilon|v)/epsilon
  =H'(v)+3v^2
  =0.1-0.7v+3v^2
 >=0.1-0.49/12 > 0.
```

Lower-degree rare mutants cannot invade such a resident because `J` is increasing and the added term is negative when `u<v`. Thus the same initial partial-only invasion observation admits a model where a chain of increasingly specialized, nearby invaders can reach full division, rather than stop at a partially divided state.

The `lambda u v(u-v)` interaction is an illustrative asymmetry favoring the more differentiated competitor in encounters between already-differentiated architectures. It is **not** asserted to be a universal ecological mechanism or measured effect.

## What is actually learned

The positive finding is about biological process and limits of inference:

1. Partial differentiation can be a self-maintaining architecture under partner-mismatch costs; completion need not follow initial invasion.
2. The identical S-versus-d invasion and frequency data can also permit onward evolution to full specialization.
3. To distinguish arrest from onward specialization, experiments must compare the fitness of a higher-degree newcomer against an **established partial resident**, not only against the original integrated type.
4. The intermediate-resident interaction is a biological cause, not simply another way to classify the original endpoint threshold.

This is a theory-only **conditional counterexample / model comparison**. It does not establish that one of these outcomes occurs in plants, microbial consortia, or animals, nor does it prove population-level long-run convergence. It is not a novelty claim about evolutionary stability, adaptive dynamics, coordination games, or priority effects; those theoretical elements are prior art.

## Relation to established evolutionary theory

This is **not** a claim to have discovered ESS, convergence stability, adaptive dynamics, multistability, evolutionary hysteresis, or mixed generalist-specialist organization. Established theory explicitly distinguishes evolutionary uninvadability from convergence stability (Waxman and Gavrilets 2005), and models of division of labour already predict extreme specialization, stable generalist/specialist group configurations, and contingent multistability under partner acquisition (Cooper & West 2018; Uchiumi & Sasaki 2020). The specific contribution of this comparison is a **matched-assay counterexample**: every integration-versus-candidate frequency curve can be held fixed while the later evolutionary fate of an established partial architecture changes.

Three more directly relevant precedents narrow the scope of any claimed conceptual advance:

- Wahl (2002) explicitly modeled evolving mixtures of generalists and specialists, stable task allocation, and a continuous division-of-labour extension. Therefore **stable incomplete division of labour is established prior art**, not a new biological prediction in isolation.
- D'Orazio & Waite (2008) showed that error-prone, inefficient generalists can stably coexist with specialists under incomplete division of labour. Thus the persistence of multifunctional participants among specialized ones is also prior art; a *monomorphic resident's intermediate trait degree* is not automatically equivalent to such within-group polymorphic organization.
- Komarova, Urwin & Wodarz (2012) showed theoretically that cooperative division of labour and cheating can speed the emergence of complex fully mutated phenotypes across a fitness valley. Thus calling **partial division a stepping stone** is not a first-discovery claim. Their mechanism is product sharing and cheating in spatial/aerial asexual populations, not the present invariant `S`–`d` payoff-comparison construction.
- Ribeck & Lenski (2015) emphasized that accurate frequency-dependent fitness measurement must account for changes during competition, and analyzed the form of frequency dependence in microbial cross-feeding. Thus the claim that *the shape of frequency dependence matters* is also prior art.

**Remaining narrow result:** for two explicit multi-architecture payoff extensions, all binary integrated-resident comparisons (including full frequency-response curves for every partial degree) are identical while selective consequences for partial residents differ. The exact (7/79) founder threshold and the smooth-mismatch relay threshold are transparent **model witnesses**, not generally valid new natural laws.

- Waxman D, Gavrilets S. 2005. 20 questions on adaptive dynamics. *Journal of Evolutionary Biology* 18:1139–1154. https://doi.org/10.1111/j.1420-9101.2005.00948.x (Background on what invasion fitness can and cannot determine.)
- Abrams PA. 2005. 'Adaptive dynamics' vs. 'adaptive dynamics'. *Journal of Evolutionary Biology* 18:1162–1165. https://doi.org/10.1111/j.1420-9101.2004.00843.x (Scope of evolutionary path interpretation.)
- Cooper GA, West SA. 2018. Division of labour and the evolution of extreme specialization. *Nature Ecology & Evolution* 2:1161–1167. https://doi.org/10.1038/s41559-018-0564-9
- Uchiumi Y, Sasaki A. 2020. Evolution of division of labour in mutualistic symbiosis. *Proceedings of the Royal Society B* 287:20200669. https://doi.org/10.1098/rspb.2020.0669
- Carlson C, Akçay E, Morsky B. 2023. The evolution of partner specificity in mutualisms. *Evolution* 77:881–892. https://doi.org/10.1093/evolut/qpac056 (For matched-partner bistability.)

- Wahl LM. 2002. Evolving the division of labour: generalists, specialists and task allocation. *Journal of Theoretical Biology* 219:371–388. https://doi.org/10.1006/jtbi.2002.3133
- D'Orazio AE, Waite TA. 2008. Incomplete division of labor: error-prone multitaskers coexist with specialists. *Journal of Theoretical Biology* 250:449–460. https://doi.org/10.1016/j.jtbi.2007.09.040
- Komarova NL, Urwin E, Wodarz D. 2012. Accelerated crossing of fitness valleys through division of labor and cheating in asexual populations. *Scientific Reports* 2:917. https://doi.org/10.1038/srep00917
- Ribeck N, Lenski RE. 2015. Modeling and quantifying frequency-dependent fitness in microbial populations with cross-feeding interactions. *Evolution* 69:1313–1320. https://doi.org/10.1111/evo.12645

## Minimal discriminating biological test

At the same environment and background community, compare established nearly monomorphic resident types `S`, `d_*`, and `d=1`. Introduce rare `d_*` into S, rare full D into S, and crucially rare full D into `d_*`. Both models predict the first two outcomes (partial grows; full declines). They differ on the third: symmetric mismatch cost excludes full D from a resident `d_*`, whereas `lambda=3` permits it. Measure **relative lifetime or complete-cycle growth**, not merely visitor frequency or a single-stage fitness component.

This three-resident comparison distinguishes the two explicit models but is not sufficient to identify all possible multi-architecture ecological interactions.
