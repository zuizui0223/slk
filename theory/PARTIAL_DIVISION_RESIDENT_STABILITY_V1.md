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

## A second biological threshold: when the *first* partial founder directly unlocks complete division

The cusp-versus-smooth result can be sharpened without changing **any** measurement against the integrated phenotype. This calculation concerns the same already-declared symmetric mismatch family `M_q`; it introduces no additional interaction function. For every `q>=1`, all selection curves in a population of integration `S=0` and any partial/full architecture `d` are **exactly identical at every frequency** because `M_q(d,0)=w(d)` and `M_q(d,d)=0`.

Focus on the already favored first partial founder `v=d_*=1/7` and ask whether a rare complete specialist `u=1` can invade **that new resident**, without requiring additional intermediate morphologies. In the registered `F(d)=d/4+d²`, `w(d)=d/10+9d²/10`, `eta=3/2` witness,

```text
w(1/7)=8/245,                    F(1)-F(1/7)=117/98,
w(1)-w(1/7)=237/245,            w(1)+w(1/7)=253/245,

I_q(1 | 1/7) =
   117/98 - (711/490) * (237/253)^(q-1).

I_q(1 | 1/7) > 0  exactly when

q > q_critical
  = 1 + log(65/79)/log(237/253)
  = 3.98580331443734... .
```

The ratio `237/253` is strictly between zero and one, so `I_q(1 | 1/7)` increases **strictly** with `q`; there is exactly one crossing in this one-parameter family. At equality the full specialist is *neutral when rare*, not positively invasible. This is a threshold in the **shape of ecological mismatch costs between already differentiated residents**, not a change in intrinsic fitness or a claim that any natural population has `q=4`.

| Mismatch exponent `q` | Rare full specialist against established `d=1/7` | Finite-introduction frequency boundary `p_critical` | Interpretation |
|---:|---:|---:|---|
| 1 | -0.257142857 | 0.088607595 = 7/79 | Rare complete division excluded; it gains when introduced above 8.86% |
| 2 | -0.165378721 | 0.060834268 | Direct rare invasion excluded; gradual onward changes can invade |
| 3 | -0.079417850 | 0.031185949 | Direct rare invasion excluded; founder barrier smaller |
| 4 | +0.001106761 | below 0 | Full specialist can already invade the *first* partial resident when rare |
| 5 | +0.076538905 | below 0 | Same direct two-step route with a larger deterministic margin |

Here `p_critical=1/2-[F(1)-F(d_*)]/[2 eta M_q(1,d_*)]` whenever the value lies in `(0,1)`. When the formal threshold becomes negative, **no positive founding-frequency threshold remains** in this pairwise selection comparison. The relative selection difference is increasing in founder frequency under the declared positive mismatch interaction, so a positive rare-invasion margin stays positive for all `p in [0,1]` (apart from the trivial zero-mutant endpoint as a population state).

This yields three **conditional ecological fates of the same initially favored partial structure**:

1. **First-order mismatch (`q=1`):** the `d_*` resident resists each different rare mutant in the declared single-mutant model. Yet a sufficiently concentrated full-specialist introduction can still cross the known `7/79` threshold; “resistance when rare” must not be called absolute permanence.
2. **Smooth-but-not-yet-direct completion (`1<q<q_critical`):** at each positive partial resident `v>0`, sufficiently nearby further division is favored because mismatch costs are `o(|u-v|)` while intrinsic value has `F'(v)>0`. The full specialist remains excluded **from rare introduction at the first founder `d_*`** and requires a further resident shift, a sufficiently large founding frequency, or another mechanism. Such possible substitutions do not establish realized evolutionary completion.
3. **Direct two-step route (`q>q_critical`):** `d_*` invades `S` from rarity, and the full specialist subsequently invades `d_*` from rarity. Both pairwise selection differences remain positive as the invading type becomes common. A sequential `S -> d_* -> D` trajectory is therefore *permitted under a rare-mutation, pairwise-replacement interpretation* without introducing yet another partial degree. It is not evidence that mutation supply, actual establishment or whole-population dynamics follow this trajectory in nature.

The ecological distinction is **not simply whether a partially differentiated morphology exists**: it is whether two already differentiated architectures experience sufficiently weak incremental mismatch penalties for specialization to continue. The model also produces a continuum in the *minimum partially differentiated resident degree allowing direct full-specialist invasion*: for `q=1.1, 1.5, 2, 3, 4` the model's numerical first crossing in `v in (0,1)` is approximately `0.902506, 0.431462, 0.286153, 0.185564, 0.142408`. These numbers apply only to the registered fixed `F,w,eta` witness. In particular, `q=2` recovers the independently checked `0.286153026...` relay threshold already established above; `q=4` puts that crossing just *below* `d_*=1/7`.

**Scientific ceiling and prior art.** Smoothness of invasion fitness, the form of partner-competition kernels, convergence, and trait-substitution sequences are established subjects of evolutionary ecology (Waxman & Gavrilets 2005; Boldin & Diekmann 2014, DOI 10.1007/s00285-013-0725-z). This calculation is **not** the first discovery that interaction regularity affects evolution. Its narrower contribution is an **exact, reproducible switching boundary inside the specific SLK matched-assay family**: all initial integrated-resident assays can be identical while the ecological state reached after partial specialization admits a finite-founder-only escape, an intermediate relay, or an immediate rare-invasion route to completed division. These are illustrative model predictions; there is no fitted ecological `q` and no observed cross-taxon two-step evolutionary transition.

## Finite populations: the deterministic direct-completion boundary is not a fixation threshold

The exact `q_critical` result classifies **deterministic growth from infinitesimal rarity**, not the probability that one rare complete specialist eventually fixes in a finite population. Classic frequency-dependent evolutionary-game theory already distinguishes these endpoints: in coordination games a type can be disfavored when rare while fixation from one individual remains possible, and even exceed the neutral `1/N` benchmark (Ohtsuki et al. 2007, DOI 10.1016/j.jtbi.2007.07.005). The following is a **process-specific application** of that established result to the same SLK conditional witness, not a novel fixation-process theorem.

Fix two viable architectures `u,v` and their symmetric positive mismatch `m=M_q(u,v)`. In the pairwise ecological payoff specification, a focal individual with architecture `u` receives `A(u,u)=F(u)` against its own type and `A(u,v)=F(u)-eta*m` against `v`. The reverse focal payoffs are `A(v,u)=F(v)-eta*m` and `A(v,v)=F(v)`. **These four entries do not form the equal-off-diagonal three-entry canonical game** used for the separate `INV1` reference calculation; applying that reference game's fixation ratio to this pair would silently change the fitness process.

Under a fixed finite population `N>=3`, uniformly random encounters **without self-interaction**, exponential reproductive weights `exp(beta*payoff)`, `beta>0`, and uniform random death, when `i` of `N` individuals are the focal `u` type,

```text
B   = F(u)-F(v),              X = eta * M_q(u,v),
pi_u(i) = F(u) - X*(N-i)/(N-1),
pi_v(i) = F(v) - X*i/(N-1),

Delta_i = pi_u(i)-pi_v(i)
        = B + X*(2i-N)/(N-1).

T_minus(i)/T_plus(i) = exp(-beta * Delta_i).
```

The finite-population Moran fixation probability of **one** focal mutant is therefore exactly

```text
rho_u|v =
  1 / sum_{j=0}^{N-1} exp[-beta * A_j],

A_j = j*B + X*j*(j+1-N)/(N-1).
```

The expression is finite, strictly positive and continuous in `q` for `u!=v>0` and finite `N,beta`. Hence the deterministic `q_critical=3.985803...` produces **no discontinuous jump in fixation probability**. For the declared `eta>0`, `M_q(u,v)` strictly decreases with `q` when both types are positive and distinct; all nontrivial terms in the denominator then decrease, so `rho_u|v` **strictly increases** with `q` at fixed `N,beta,B`. This continuous stochastic improvement occurs even *below* the deterministic direct-completion boundary.

The numerical finite-population example uses the **previously registered** `F(d)=d/4+d²`, `w(d)=d/10+9d²/10`, `eta=1.5`, complete mutant `u=1` and first partial resident `v=1/7`, with `N=100`, `beta=0.1`:

| Mismatch shape `q` | Deterministic rare-invasion margin `I_q(1|1/7)` | Exact one-mutant fixation `rho` |
|---:|---:|---:|
| 1 | -0.257142857 | 0.027876352 |
| 2 | -0.165378721 | 0.031383661 |
| 3 | -0.079417850 | 0.034930 (rounded) |
| 4 | +0.001106761 | 0.038482155 |
| 5 | +0.076538905 | 0.042008718 |

The neutral reference is `1/N=0.01`. Even at `q=1`, a complete specialist selected **against at rarity** has fixation probability `2.79%` in this particular process because its higher intrinsic payoff becomes valuable once its frequency rises. This is not a model of dispersal, mutation supply, genetic linkage, individual plant survival, or observed lineage evolution. It **does not** invalidate negative rarity invasion: rarity invasion and one-founder fixation are distinct quantities.

A further exact identity from the symmetric mismatch `M_q(u,v)=M_q(v,u)` is

```text
rho_u|v / rho_v|u = exp[ beta*(N-1)*(F(u)-F(v)) ].
```

The mismatch terms cancel because `sum_{i=1}^{N-1} (2i-N)=0`. The reciprocal fixation ratio is therefore independent of `q` *under this four-entry payoff and update process*, although **both absolute fixation probabilities and the rate of turnover change with `q`**. For `u=1, v=1/7, N=100, beta=0.1`, the ratio is about `135861.02335` in every `q` case. Under additional **symmetric rare-mutation** assumptions, long-run monomorphic occupancy odds share this same ratio, but expected substitution waiting times do not. This resembles but **is not numerically interchangeable with** the distinct canonical `INV1` identity with its different game/payoff map.

**Biological consequence, with a hard ceiling.** The first partial structure can alter both the *deterministic* opportunity for additional specialization and the *finite-population probability* of eventual replacement. The former has the sharp `q_critical` invasion boundary; the latter has a continuous probabilistic transition depending on `N`, `beta`, and the frequency path. Therefore the SLK ecological statement must remain **“rare completed division declines or increases”**, not **“completed division cannot evolve”**. No natural system supplies these `N,` `beta,` or `q` parameter estimates, and a mutation-limited waiting time or evolutionary history cannot be inferred from the one-mutant fixation calculation without an explicit mutation process.

Prior art: Ohtsuki H, Bordalo P, Nowak MA. 2007. The one-third law of evolutionary dynamics. *Journal of Theoretical Biology* 249:289–295. DOI 10.1016/j.jtbi.2007.07.005 (the one-third law is a separate **weak-selection limiting result**, not asserted to hold exactly for the exponential-fitness example above).

## A finite ecological window: identical long-run architecture odds but different routes and waiting times

A deterministic invasion boundary is not the same question as **how far specialization progresses before an ecological context changes**. The already derived four-entry exponential-Moran fixation probabilities give a minimal origin-fixation substitution chain across three monomorphic architectural states. The approximation requires **rare mutation** but does **not** require weak selection:

```text
S = 0 (integrated),   P = d_* = 1/7 (partial),   D = 1 (complete).
```

Assume mutation is **rare compared with within-population absorption**: one substitution resolves before another arrives. For each permitted directed evolutionary transition `i -> j`, an attempted new mutant is supplied at rate `mu_ij`, and its fixation probability is `rho_(j|i)` from the previously defined **self-excluding four-entry exponential Moran process**. The origin-fixation transition rate is

```text
Q_ij = mu_ij * rho_(j|i)          for i != j.
```

This is a standard origin-fixation chain, not a new theory of evolutionary waiting times (Sella & Hirsh 2005; McCandlish 2011, DOI 10.1111/j.1558-5646.2011.01236.x). In particular, McCandlish explicitly distinguishes stationary probabilities from approach-to-equilibrium dynamics on mutational networks. Here the **biological question** is how partial division changes the next specialization step while all initial integrated-resident assays are invariant to ecological mismatch curvature `q`.

### Long-run architectural occupancy under symmetric mutation opportunities

For any pair of degrees `u,v`, the fixation odds from the declared four-entry mismatch model obey

```text
rho_(u|v)/rho_(v|u) = exp[beta*(N-1)*(F(u)-F(v))].
```

This ratio is exactly independent of `q`. For a finite, **connected** set of architectural states with **symmetric** permitted mutation rates (`mu_ij=mu_ji`; zero for both directions on missing edges), the rare-mutation substitution chain is reversible and satisfies detailed balance with

```text
pi_i = exp[beta*(N-1)*F(i)] /
       sum_j exp[beta*(N-1)*F(j)].
```

Thus identical intrinsic `F` predicts identical *asymptotic* monomorphic architecture occupancy at all `q` in this family, **even when mutational connectivity excludes direct S-to-D transitions**. The equality does **not** survive arbitrary asymmetric mutation rates, altered four-entry payoffs, finite mutation supply producing polymorphism, or changed intrinsic `F`. Nor does it imply the same transition rates, the same time to specialization, or the same route through intermediate states.

### First passage through a partial-specialization resident

For three monomorphic states, define the rates **before multiplying by a shared, sufficiently small mutation supply `mu`**:

```text
a = rho_(P|S),    b = rho_(D|S),
c = rho_(S|P),    d = rho_(D|P).
```

If all three undirected mutation edges are available with equal directional supply `mu`, the two-state transient generator (before the *first* appearance of a fixed D state) is

```text
Q_transient/mu = [[-(a+b), a],
                  [c, -(c+d)]].
```

Direct solution of the first-step recursions gives the dimensionless mean **first-passage time from integrated S to the first fixed D population**

```text
mu * E[T_(S->D)] = (a+c+d)/(a*d + b*(c+d)).
```

The probability that the *first* fixation of D enters from P rather than directly from S is `a*d/[a*d+b*(c+d)]`. This is a route-of-first-arrival probability, not the fraction of time subsequently spent in P. When large S-to-D structural mutations are developmentally inaccessible, set **`b=0` in the transition graph only** (not in the fitness model): then every route to D must pass through P, and

```text
mu * E[T_(S->D)] = (a+c+d)/(a*d).
```

A finite ecological window may close before D is reached. Let `tau=mu*t`, `g=sqrt((a+b-c-d)^2+4*a*c)`, and `r_slow, r_fast=(a+b+c+d ∓ g)/2`. The **exact** probability of having reached a fixed D at least once by that normalized horizon is

```text
P(hit D by tau) = 1 -
  [(r_fast-b)/g]*exp(-r_slow*tau)
  -[(b-r_slow)/g]*exp(-r_fast*tau).
```

This is a *first-hitting* probability that treats D as absorbing **only for the first-passage calculation**; the full reversible origin-fixation chain permits later reversions.

### Three-state SLK numerical witness: partial division as a temporal gate

Take the same `F(d)=d/4+d^2`, `w(d)=d/10+9d^2/10`, `eta=1.5`, `N=100`, and `beta=1`. Keep mutation opportunities symmetric and restrict mutation graph accessibility to **S <-> P <-> D**, so direct S-to-D mutation is *not supplied* (`b=0`) while pairwise S-to-D fitness remains defined and identical at all `q`.

| Quantity (same initial S-versus-d assays) | `q=1` | `q=4` |
|---|---:|---:|
| `rho_(P|S)=a` | 0.029404746476 | 0.029404746476 |
| `rho_(S|P)=c` | 0.000113611977 | 0.000113611977 |
| `rho_(D|P)=d` | 0.023423120313 | 0.117256955418 |
| `mu E[T_(S->D)]` | **76.86592882** | **42.56934471** |
| `P(hit D by mu*t=40)` | **0.28137875** | **0.59108238** |

These are **not** generation counts and `mu=1` is **not** assumed biologically: the displayed waiting-time and finite-window values are expressed in *mutation-opportunity units*, valid under `mu` small enough that each population fixation/loss episode ends before the next eligible mutant arrives. For instance an ecological opportunity lasting `t=40/mu` time units would have a model first-completion probability of about **28% versus 59%** under the two alternative interaction curvatures, even though all integration-resident assays and eventual stationary probabilities agree. If rare long-distance architecture changes S-to-D are supplied too, the same calculation (with `b=rho_(D|S)`) yields `mu E[T]=40.37744337` for `q=1` versus `22.40262892` for `q=4`, demonstrating explicit **dependence on mutational access** as well as specialist-specialist ecology.

This means *two lineages with identical current fitness ranking and the same asymptotic preference for full division could occupy different architectural states throughout a finite environmental window*. One may appear indefinitely partially specialized on observational timescales although the equilibrium occupancy is overwhelmingly fully specialized. The ecological window duration and the mutation topology are distinct hypotheses; no time scale, demographic size, selection intensity, q or mutation network was inferred for a natural lineage.

**Scope / prior-art boundary.** Time-dependent fitness landscape evolution, reversible origin-fixation dynamics and mutational-network bottlenecks are established theory (Sella & Hirsh 2005; McCandlish 2011). SLK's limited numerical contribution is the **specified partial-specialization witness**: q-independent original assays and stationary occupancy coexist with q-dependent specialist-to-specialist substitution rates and finite-time completion, making evolutionary stasis **history- and time-horizon dependent** even before invoking phenotype-specific costs that change with environment. This is not a fourth universal SLK gate or field validation of a real trajectory.

Citation: McCandlish DM. 2011. Visualizing fitness landscapes. *Evolution* 65:1544–1558. DOI 10.1111/j.1558-5646.2011.01236.x. (Reversible origin-fixation landscapes, stationary distributions, and their transient dynamics.)

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

- Boldin B, Diekmann O. 2014. An extension of the classification of evolutionary singular strategies in Adaptive Dynamics. *Journal of Mathematical Biology* 69:905–940. https://doi.org/10.1007/s00285-013-0725-z (General prior art: invadability can depend on regularity of invasion fitness; not an SLK model analysis.)
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
