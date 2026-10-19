# SLK ↔ ANTO — a history-dependent ecological opportunity window

**Cross-repository theoretical interpretation — 19 October 2026. Not flagship empirical evidence.**

## Biological question

Why can two lineages experiencing the **same length of ecological conditions favorable to a differentiated architecture** differ in whether that architecture can be expressed repeatedly? Can the apparent advantage of an *earlier* favorable period even reverse?

SLK and ANTO answer **different** constraints:
- **SLK** asks whether an empirically identified multifunctional compromise has a profitable differentiated alternative (`Phi>0`), whether a declared local route initially rises in fitness (`g0>0`), and whether a specified variant can grow when rare in the ecological population (`Delta_R>0`). These conditions do **not** establish genetic competence, viability of all intermediate phenotypes, long-run population survival, or observed architectural evolution.
- **ANTO** asks whether joint genetic/developmental resources remain latent despite visible absence; how often they become expressed; whether expression repeats; and when those resources degrade or are reacquired. ANTO's three-generation expressed streak is **not** fitness establishment, fixation or a SLK division-of-labor transition.

The exact, theory-only interface is now implemented **once**, in [ANTO draft PR #16](https://github.com/zuizui0223/anto/pull/16), with [model](https://github.com/zuizui0223/anto/blob/theory/slk-anto-ecological-opportunity-window-20261019/src/anto_slk_ecological_window_v1.py), [independent tests](https://github.com/zuizui0223/anto/blob/theory/slk-anto-ecological-opportunity-window-20261019/tests/test_slk_anto_ecological_window_v1.py), and [scientific result interpretation](https://github.com/zuizui0223/anto/blob/theory/slk-anto-ecological-opportunity-window-20261019/docs/SLK_ANTO_ECOLOGICAL_WINDOW_V1.md). **Do not duplicate the numerical kernel or reinterpret the ANTO model as a measured SLK gate.**

## Declared overlap and scope

The two theories **only** intersect biologically when the latent/re-expressed phenotype of ANTO is itself a credible component of the *same* functionally differentiated architecture that SLK compares with its integrated alternative. Flower anthocyanin loss/regain is NOT automatically multifunctional anatomical division. The overlap needs separately verified shared functional conflict and candidate-specific architecture value, and same-lineage functional resource retention.

For a deliberately registered witness (not fitted to a species):

```
SLK R(x)=x+x², K(x,E)=k(E)x, x∈[0,1], eta(E) frequency feedback
   Phi=2-k; g0=1-k; rare-D Delta_R=Phi-eta
   strict positive-value/path/rare signs specify ecological eligibility

ANTO latent/native or resource-missing -> expression -> repeated expression
   a=activation, r=continuation, d=structural loss, g=toolkit acquisition
   theta=P(all required functionally competent modules co-retained)

Joint observable:
   P(at least one 3-consecutive-expression run within generations
     where ALL specified SLK gate signs are strictly positive).
```

All expression/resource transitions are unchanged by the ecological eligibility mask; a strict sign labels a *possible favorable opportunity* and does not supply a probability of population establishment. Counting three expressed snapshots is not a genetic fixation or lifetime reproductive fitness result.

## New conditional predictions with exact illustrative numbers

Using ANTO `theta=1/8, a=2/5, r=3/4, d=1/10, g=0` over 14 generations, a five-generation all-gate-positive ecological opportunity **early** (generations 1–5) gives **5.090625%** qualified three-snapshot events; the same-length opportunity **late** (generations 10–14) gives **2.291109%**. The unconditional probability of any expression is identical because the molecular/phenotype transition mechanism is unchanged.

**There is no universal "earlier is better" law.** With the identical toolkit-loss hazard `d=1/20`, identical initial resource frequency and exactly five favorable generations, the order reverses when latent activation is slower but expressed states persist:

| Conditional rates | Early opportunity | Late opportunity |
|---|---:|---:|
| a=0.40, r=0.75 | **5.435156%** | 3.901086% |
| a=0.05, r=0.95 | 1.528609% | **3.194658%** |

The late advantage in the second line is due to an explicitly assumed history of latent-resource activation and pre-existing expression *during ecologically unfavorable generations*. Such preconditioning might be suppressed by selection in real organisms; this is a **falsifiable extra biological assumption**. The timing-order effect can change sign even with fixed loss rate and favorable time duration.

With a decreasing architecture debit `k(t)=max(0,12/5-t/5)` and `eta=3/2`, the strict value, local-accessibility and rarity signs first become favorable in generations **3, 8 and 10**, respectively. The corresponding eligible three-snapshot probabilities are **5.983948%, 3.262062% and 2.291109%**. These nested conditional events are not probabilities that a flower actually becomes specialized.

**Hidden-competence consequence.** Identical individual and pairwise retention frequencies of necessary resources can leave `theta=P(111)` in `[0,1/4]`; the late example with no reacquisition then has a sharp conditional qualified-event interval `[0,4.582218%]` under ANTO's grouped-incomplete-state assumptions. This is a Fréchet/linear-transition **model interval, not statistical confidence or a global plant parameter**.

## v2 extension: silent preparedness without pre-window visible expression

The original timing example above permits visible expression before a favorable selective window. This is a real biological assumption, because expression itself could be selected against. The **separate** [ANTO v2 silent-priming extension](https://github.com/zuizui0223/anto/blob/theory/slk-anto-ecological-opportunity-window-20261019/docs/SLK_ANTO_SILENT_PRIMING_WINDOW_V2.md) tests the complementary condition: **zero visible expression throughout the ecologically nonqualifying period**, while retained but unused developmental modules become more readily inducible.

A structurally competent, unexpressed lineage has two hypothetical hidden regulatory-readiness states, unprimed U and primed P. In each nonqualifying generation, U becomes P at rate `b`, while either state loses the entire required toolkit at rate `d`. The genuinely qualifying SLK context arrives for three generations. Activation then has probability `a_U` from U and `a_P` from P, with conditional expressed-state continuation `r`.

For initial complete-toolkit fraction `theta`, the probability of a **three-consecutive-visible-expression coincidence, not actual establishment**, after `m` nonqualifying generations is exactly:

```
Q(m) = theta*r² * [
    a_U*(1-b-d)^m
    + a_P*((1-d)^m-(1-b-d)^m)
].
```

The biologically interpretable one-step timing switch is:

```
Q(1)>Q(0)  <=>  b*(a_P-a_U)>a_U*d    [theta*r>0].
```

The mechanism is a *competition between silent readiness and irreversible loss*. If a priming effect is real and exceeds the resource-erosion debit, some delay improves subsequent expression opportunity **without any visible precursor**. With positive d the effect is temporary, not an indefinitely increasing evolutionary gain. In a fixed illustrative exact model, the peak occurs after nine nonqualifying generations (**2.7238%** versus **0.8000%** with immediate qualifying conditions), followed by a decline. If `b=0` or `a_P=a_U`, later opportunities instead decay as `(1-d)^m`. These are **conditional constructed rates**, not natural generation estimates.

**A stronger same-present-phenotype distinction:** With the same selected candidate, same present SLK environment, same white visible history and exactly the same **retained complete toolkit fraction**, `b=0.15` versus `b=0` yields **2.7238% versus 0.5540%** qualifying three-snapshot events after nine generations. The hidden primed fraction differs, so a coding-gene-only assay omits a causally relevant present regulatory state. It does not contradict state sufficiency when that hidden state is actually measured.

**Experimentally falsifiable identifiability signature:** With separately measured toolkit survival `S=1-d` and matched cohorts pre-exposed for `m=0,1,2` generations before identical three-generation positive SLK conditions, let `y_m=Q(m)/Q(0)`, `v1=y1-S`, `v2=y2-S²`. Conditional on nonzero `v1` and fixed shared rates, `b=2S-v2/v1` and `a_P/a_U=1+v1/b`. A one-delay assay confounds priming frequency with activation efficacy; the third cohort can break that ambiguity. A further `m=3` cohort tests whether the constant-rate model is wrong. This is algebraic structural identification, not a powered field sampling design.

**Scope firewall:** This extension is *not* a new SLK fourth ecological-selective bottleneck, nor evidence of plant evolutionary reactivation. Priming may be transient developmental plasticity; its inheritance, actual target trait function, and genotyped ancestry are unmeasured. All Cirsium experimental use belongs to aza3. The published tissue-specific *Cirsium japonicum* source in ANTO v6 suggests only a possibility of nonfloral pathway preservation, not priming and not an SLK payoff difference.

## v3: why revived phenotype supply is not ecological rescue

The [ANTO v3 absolute-demography companion](https://github.com/zuizui0223/anto/blob/theory/slk-anto-ecological-opportunity-window-20261019/docs/SLK_ANTO_ABSOLUTE_DEMOGRAPHY_V3.md) closes **one limited additional gate**, not the whole biological question: given an expressed candidate that is **explicitly assumed heritable**, can a small descendant lineage still exist at a declared ecological census deadline?

The central SLK warning is important here: **the candidate's relative advantage over a resident does not identify absolute growth**. A positive candidate-specific SLK margin `Delta_R>0` in a fixed resident comparison cannot alone be converted to a plant population's capacity for demographic recovery. In particular, if the resident background is already declining, relative selection may favor a variant even while both populations shrink. One should not claim standard ecological invasion into a stable resident equilibrium from such a declining-background comparison.

To demonstrate this biological distinction without claiming any measured plant parameter, ANTO v3 retains the identical v2 hidden U/P competence trajectory and uses an *extra* offspring mechanism: each expressed **heritable** D founder yields 0, 1 or 2 descendants per generation, `Binomial(2,q_D)`. The unsimulated resident benchmark has `Binomial(2,q_S)`; two alternate backgrounds have the exact same D/S expected offspring ratio `13/11`:

| Source-independent illustrative context | q_S | q_D | Mean D offspring | Long-run D lineage nonextinction if conditions remain unchanged |
|---|---:|---:|---:|---:|
| Absolute-supercritical | 0.55 | 0.65 | 1.30 | 120/169 ≈ 71.01% |
| Absolute-subcritical | 0.33 | 0.39 | 0.78 | 0% |

The infinite-time branching formula above is an elementary established result, not the finite-census statistic. With 40 **hypothetical independent initial lineages**, census at generation 14, and threshold of ≥4 D descendants in **at least one** lineage, the exact model with 65-digit polynomial numerical evaluation gives:

| Evolutionary timing | Supercritical finite-census event | Subcritical finite-census event |
|---|---:|---:|
| Environmental selection becomes qualifying after 6 unfavorable generations | **64.68%** | 1.02% |
| Qualifying after 9 unfavorable generations | 55.08% | 1.62% |

These percentages do **not** estimate true establishment, population rescue, or genetic fixation. The subcritical world has **zero eventual nonextinction** in the assumed permanent environment even though four descendants can transiently appear by census, so the latter must not be called a successful reversal.

### The two-clock ecological prediction

Under a fixed deadline H, let `A(m)` be the fraction of lineages generating a hypothetical heritable D founder after m unfavorable generations, and `B_q(H-m,k)` the probability that an activated lineage reaches k descendants within the remaining time. The n-founder threshold event is `1-(1-A(m)*B_q(H-m,k))^n`. For positive denominators, shifting the switch later increases that event exactly when

```
A(m+1)/A(m) > B_q(H-m,k)/B_q(H-m-1,k).
```

The first ratio captures history-dependent competence/activation. The second captures the **cost or benefit of less time for demographic expansion**. Hence the best deadline for observation need not be the same as the best historical time to make a phenotypic founder. In this constructed example `A(m)` peaks at **m=9**, but the supercritical threshold event peaks **earlier at m=6**. The subcritical transient threshold peaks at m=9 without implying survival.

A real ecological SLK × ANTO experiment therefore must not stop at colour induction, flowering, pollen deposition or positive relative growth. It must additionally measure heritability and independent *absolute reproductive performance* in the specified ecological context. Even these observations cannot automatically infer Moran fixation or the original SLK symmetric occupancy invariant; the offspring model here is a separate branching process, not that canonical population game.

### Scientific originality and limitation

The distinction between relative selection, founder supply, and demographic persistence is prior art in evolutionary rescue theory, and SLK already recognizes absolute-demography limitations. The contribution of this interface is a **specific, falsifiable multi-clock biological prediction** that can be experimentally distinguished from phenotype-only historic memory: same developmental capability and relative functional advantage can conceal different prospective lineage fates. There is no direct positive plant test of this joint claim today. ANTO owns the code, SLK owns the causal architecture interpretation, and aza3 still exclusively owns Cirsium empirical sampling and genetics.

## Distinct biological mechanisms remain distinct

The same visible integrated morphology can persist with an unfavorable differentiated candidate, a local release obstacle, rarity-dependent exclusion, a vanished joint toolkit, or any combination. ANTO's hidden-state incompetence is **not** a fourth SLK selection-sign threshold; it changes the *supply and structural feasibility* of a declared phenotype, whereas SLK's signs concern **selection relative to a specified alternative**.

The main biological prediction worth testing is:

> The consequences of a shift in ecological selection for functional differentiation depend on its historical timing **relative to functional-module retention and inducibility**, and the direction of that timing effect can reverse with the activation-versus-persistence regime.

Different clades can therefore remain phenotypically similar yet have different prospective capacities to reorganize, even if their contemporary pollination ecology is alike. This is not a claim of empirically verified cross-angiosperm convergence or re-evolution.

## Independent empirical checks and manuscript boundary

A biological study requires (1) demonstrated opposing functions on one architecture; (2) matched complete-fitness benefit/cost comparisons for relevant alternative structures; (3) validated native/developmental modules co-retained in **the same biological unit**; (4) genuine stage-matched expression and heritable persistence; (5) environmental selection and frequency-dependent rare-performance contrasts; and (6) ancestry and gene-flow controls. Do not infer any of these from photo hue alone, a CDS similarity, a transient induced flower, or GloPL fruit-set differences.

SLK's current biology refocus is still on [draft PR #117](https://github.com/zuizui0223/slk/pull/117). ANTO's cross-taxon theory is on [draft PR #16](https://github.com/zuizui0223/anto/pull/16). Neither is a completed, same-system SLK × ANTO plant experiment. All Cirsium specimen-level genomic, phenotype, ecology and fitness work is owned by [aza3](https://github.com/zuizui0223/aza3), and existing Petunia, Penstemon and Iochrominae studies must not be treated as newly collected independent evolutionary replicates.

**Publication choice:** Retain separate SLK division-of-labor and ANTO trait-afterlife papers. The present cross-repository result is a theory-backed, hypothesis-generating bridge until new biological evidence identifies *both* the shared-function conflict and the latent trait's multi-generation evolutionary fate in matched lineages.
