# SLK supplementary derivation — demographic survival while ecological partners assemble

## Why the deterministic minimum is not an extinction probability

The preceding assortment supplement derives a temporary dip in the *expected relative frequency* of a rare architecture while favorable interactions form. It does **not** identify its probability of establishment, because selective advantage against the resident is not an absolute birth or death rate.

Biologically, two independently measurable clocks matter:

1. **Partner-assembly delay**: time until contacts become sufficiently favorable for a specialized variant to increase.
2. **Demographic turnover**: births and deaths occurring while the variant is initially declining.

The same mean rare-variant trajectory can coexist with sharply different probabilities that any introduced founder lineage remains and ultimately survives. This follows from classical continuous-time branching-process theory; neither birth–death stochasticity nor rescue windows are new discoveries.

## Conditional two-phase ecological witness

In the prior full-D versus partial-P mismatch example,

```text
F(d)=0.25d+d^2, w(d)=0.1d+0.9d^2,
u=1, v=1/7, eta=3/2,
A=F(u)-F(v)=117/98,
B=eta|w(u)-w(v)|=711/490,
g(r,p->0)=A-B(1-r).
```

For initial random encounters `r0=0` and the hypothetical eventual assortativity `r_inf=0.4`,

```text
g_pre = -9/35 = -0.257142857...,
g_post = A-(3/5)B = 0.323265306... .
```

**Additional demographic assumption:** identify these *relative* selection differences with the mutant lineage's **absolute** per-capita net growth rates `b-d` while the resident background is held fixed and time units are calibrated accordingly. This is not identified by the SLK payoff experiments. Without this assumption, the following stochastic calculation cannot be transported to an empirical system.

Replace the earlier continuous contact relaxation with a deliberate **two-phase approximation**: `r=r0` and net growth `g_pre<0` for `0<=t<T`; after a contact-assembly delay `T`, `r=r_inf` and net growth `g_post>0` forever. Birth and death events are independent per individual and the rare lineage is described by a linear continuous-time birth–death branching process, with no density regulation, partner feedback, spatial correlations, immigration, or recurrent mutation.

Specify separately:

```text
b_pre-d_pre=g_pre<0,
b_post-d_post=g_post>0,
b_pre>=0, d_pre>=0, b_post>0, d_post>=0.
```

This makes it possible to compare distinct absolute birth–death turnover rates while **holding the entire expected pre-assembly abundance trajectory identical**, `E[N(t)]=n0 exp(g_pre t)`, for the same initial founder count `n0`.

## Exact eventual lineage survival after the switch

In the favorable post-assembly environment, the extinction probability of one initial individual is the standard birth–death result

```text
q_post=d_post/b_post<1.
```

Let `G_pre(s,T)=E[s^{N(T)} | N(0)=1]` be the one-lineage probability generating function during the adverse pre-assembly phase. For `0<=b_pre<d_pre`, write `z=exp[-(d_pre-b_pre)T]`. Then

```text
G_pre(s,T)
=
{d_pre(1-s) z - (d_pre-b_pre s)}
/
{b_pre(1-s) z - (d_pre-b_pre s)}.
```

The expression has the correct initial and long-delay limits:

```text
G_pre(s,0)=s,
lim_{T->infty} G_pre(s,T)=1,
G_pre(1,T)=1.
```

Every surviving pre-assembly lineage produces an independent post-assembly descendant process. Therefore with `n0` initial founders the **exact eventual nonextinction probability** in this specified unbounded model is

```text
P_eventual_persistence(n0,T)
=1 - [G_pre(q_post,T)]^n0.
```

The probability that at least one member is still alive *at the assembly switch* is separately

```text
P_alive_at_switch(n0,T)
=1 - [G_pre(0,T)]^n0.
```

These are not the same quantity. Even a lineage that survives the adverse phase can go extinct after contacts become favorable, because favorable **net** growth does not eliminate individual mortality. Nor does eventual nonextinction of this unbounded branching process imply fixation, spatial wave invasion, coexistence, or the persistence of the full complementary collective.

## Same evolutionary value and mean decline, different survival

Keep the previous structural and ecological `g_pre`, `g_post` fixed. Let the **post** environment be identical in both cases:

```text
b_post=1.2,
d_post=1.2-g_post=0.87673469387755...,
q_post=0.73061224489796....
```

Compare two pre-assembly turnover regimes at the same net growth `g_pre=-9/35`:

```text
LOW TURNOVER:  b_pre=0.4, d_pre=0.4+9/35
HIGH TURNOVER: b_pre=1.4, d_pre=1.4+9/35.
```

At `T=3`, both have **exactly the same expected pre-assembly abundance fraction** `exp(-27/35)=0.46235209...`. Yet for `n0=5` initial specialized founders:

| Outcome at T=3 | Low turnover | High turnover |
|---|---:|---:|
| Expected founder abundance fraction | 46.24% | 46.24% |
| At least one descendant alive at switch | 76.55% | 46.54% |
| Eventual nonextinction in post environment | 41.49% | 30.30% |

The distinction does not rely on the spatial contrast changing: it arises because **absolute demographic turnover is an extra ecological axis not identified by relative fitness**. High birth/death turnover can give a lower survival probability despite identical expected net growth. The listed values are exactly calculated, dimensionless synthetic model witnesses — **not field or microbial measurements**.

### Where delayed rescue stops being a biological explanation

- Contact formation cannot happen after a complementary founder lineage goes extinct. The deterministic `r(t)` trajectory must not be extrapolated as an automatic rescue mechanism for an isolated extinct type.
- The two-phase switch is assumed externally in the stochastic witness. It may represent an environmental or resident-community change that can occur without the focal rare lineage, or an experimental addition of matching partners. If **the rare lineage itself must create the partners**, joint partner-lineage dynamics are required, and this one-type branching model is inappropriate.
- Turning a selection difference into a net growth rate needs calibration of absolute natality and mortality; if the resident background is changing, the fixed-background approximation is invalid.
- Density dependence, survival of both required roles, clustering, bottleneck-induced loss of partner diversity, spatial assortment and stochastic establishment of *both* interacting types need explicit multi-type models.
- Changing the mutation rate or initial frequency can change founder supply even if conditional single-founder establishment is fixed.

## Why this is already close to existing biology and theory

Goldberg & Friedman (2021, *PLOS Computational Biology* 17:e1008732, DOI 10.1371/journal.pcbi.1008732) explicitly studied evolutionary rescue under within-population cooperation and between-population mutualisms. Cooperation imposed a critical population-size requirement and a narrower rescue window; mutualistic rescue was further hindered by dependence on adaptation of both partners. Their work is direct prior art for the insight that eventual cooperative gain does not ensure rescue during a vulnerable transient. It is *not* direct evidence of three structural SLK bottlenecks for the same resident architecture.

Kim, Levy & Foster (2016, *Nature Communications* 7:10508, DOI 10.1038/ncomms10508) experimentally showed delayed collective spreading when the M and D forms must arise through mutation, and prompt spreading when both are mixed. Their result makes **the timing of role availability** a concrete biological phenomenon, but it does not estimate the stochastic founder risk of a structurally differentiated architecture relative to an integrated resident. This study also measured negative frequency dependence within the divided collective, not the positive-feedback mismatch witness used for the numbers above.

**Defensible residual statement:** in a fully declared extra demographic extension of SLK, the prior relative-fitness and contact-assortment data do not determine demographic establishment probability. Two environments can share the same architecture benefit, same pre/post selective difference, same mean transient decline, and same eventual contact regime, yet have different survival probabilities because of birth and death turnover. This is a biological *scope boundary and illustrative prediction*, not a novel result in birth–death theory or a new empirical discovery.

## Empirical discriminator

An informative, ethically and logistically feasible microbial experiment would use a fixed partially specialized resident and introduce marked fully specialized founders at controlled initial count. Keep matched total cell density, nutrient conditions and final partner availability while varying (a) lag before complementary partners become available and (b) absolute growth–death turnover at matched **net** growth, verified through time-resolved viability and division measurements. Score founder lineage persistence across independent replicates, not just endpoint abundance or relative fitness. In parallel measure encounter/partner topology. Distinct establishment probabilities at the same net selection contrast would support demographic turnover as an additional ecological determinant; such a difference would not automatically identify the mechanism generating persistent multifunctionality in nature.

This is a supplementary design, not an observation already made in these cited papers and not a requirement for submitting the current theory-focused flagship.
