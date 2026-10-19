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

## Distinct biological mechanisms remain distinct

The same visible integrated morphology can persist with an unfavorable differentiated candidate, a local release obstacle, rarity-dependent exclusion, a vanished joint toolkit, or any combination. ANTO's hidden-state incompetence is **not** a fourth SLK selection-sign threshold; it changes the *supply and structural feasibility* of a declared phenotype, whereas SLK's signs concern **selection relative to a specified alternative**.

The main biological prediction worth testing is:

> The consequences of a shift in ecological selection for functional differentiation depend on its historical timing **relative to functional-module retention and inducibility**, and the direction of that timing effect can reverse with the activation-versus-persistence regime.

Different clades can therefore remain phenotypically similar yet have different prospective capacities to reorganize, even if their contemporary pollination ecology is alike. This is not a claim of empirically verified cross-angiosperm convergence or re-evolution.

## Independent empirical checks and manuscript boundary

A biological study requires (1) demonstrated opposing functions on one architecture; (2) matched complete-fitness benefit/cost comparisons for relevant alternative structures; (3) validated native/developmental modules co-retained in **the same biological unit**; (4) genuine stage-matched expression and heritable persistence; (5) environmental selection and frequency-dependent rare-performance contrasts; and (6) ancestry and gene-flow controls. Do not infer any of these from photo hue alone, a CDS similarity, a transient induced flower, or GloPL fruit-set differences.

SLK's current biology refocus is still on [draft PR #117](https://github.com/zuizui0223/slk/pull/117). ANTO's cross-taxon theory is on [draft PR #16](https://github.com/zuizui0223/anto/pull/16). Neither is a completed, same-system SLK × ANTO plant experiment. All Cirsium specimen-level genomic, phenotype, ecology and fitness work is owned by [aza3](https://github.com/zuizui0223/aza3), and existing Petunia, Penstemon and Iochrominae studies must not be treated as newly collected independent evolutionary replicates.

**Publication choice:** Retain separate SLK division-of-labor and ANTO trait-afterlife papers. The present cross-repository result is a theory-backed, hypothesis-generating bridge until new biological evidence identifies *both* the shared-function conflict and the latent trait's multi-generation evolutionary fate in matched lineages.
