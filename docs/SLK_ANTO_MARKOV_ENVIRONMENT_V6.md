# SLK ↔ ANTO v6: ecological persistence can filter future functional architectures

**20 October 2026. Theory-only biological bridge to [ANTO v6 draft #19](https://github.com/zuizui0223/anto/pull/19). No plant data or SLK payoff calibration.**

## Ecological question

When two ecological partner environments are equally common and select opposite architectural forms, can the *duration* of those partner states determine whether a lineage retains the ability to express a formerly useful structural specialization?

SLK asks what **functional structure** is advantageous relative to other viable alternatives in the current ecological partner context. ANTO asks whether its **necessary genetic/developmental resources** remain in reproducing lineages after the visible form disappears. Neither question is equivalent to frequency of floral colours alone.

V4 of the bridge assumed one ecology; v5 prescribed ABAB... versus AAAABBBB... deterministic cycles. ANTO v6 extends v4's *unchanged offspring kernel* to a **stationary shared two-state Markov environment**, not an independent environmental lottery for each individual. A and B each have stationary probability 1/2 at every generation; environment persistence changes only autocorrelation and mean run length.

## Positive model result and useful controls

In the constructed biological comparison, environment A favors expressing competent D (`q_D=.9,q_C=.4`), environment B favors nonexpressing yet reproducing competent C (`q_D=.4,q_C=.9`). Functional toolkit retention is .8 per child in both. Start from one nonexpressing competent C before a stationary random A/B environment.

| Offspring D↔C switching | A/B environment switches with 90% probability each generation | A/B environment stays with 90% probability |
|---|---:|---:|
| 10%: parent expression relatively stable | **16.17%** competent descendants at generation 14 | **34.50%** |
| 50%: no parental expression memory | 23.91% | 23.91% |
| 90%: child expression tends to flip | **34.50%** | **16.17%** |

All percentages concern **at least one functionally competent descendant at generation 14**, whether or not that descendant presently expresses the focal trait. They are **not** probabilities of plant survival, fixation, ecological rescue or durable architecture adaptation.

Within each offspring-switching comparison, stationary environmental occupancy and the **first-generation probability of producing an expressed D child from C** are exactly the same. For 10% switching that probability is 10.0896% in either Markov environment regime. So neither average partner ecology nor a one-shot expression experiment distinguishes the prospective genealogical outcome in this witness.

An independent sampled **pathwise growth** calculation (three seeded 100,000-generation Markov sequences, not a certified Lyapunov theorem) also reverses: offspring switching 10% yields typical multipliers approximately .977 with frequent environmental alternation versus 1.189 with persistent runs; offspring switching 90% reverses those values. The arithmetic mean offspring matrix instead has multiplier 1.04 for all comparisons. The sign of sampled growth must not be presented as an exact extinction certificate.

### SLK caveat: the comparison must include all viable states

This result does **not** assert an SLK `Phi>0` architecture always wins. D and C alternate in reproductive advantage, and C is a biologically viable, nonexpressing alternative. If an alternative architecture retains mechanical support while its reproductive specialization changes, comparing D only to an unsupported simplified form will omit that alternative. SLK's [scaffold-bypass comparison](https://github.com/zuizui0223/slk/blob/biology/scaffold-bypass-test-20261014/theory/FLORAL_SCAFFOLD_BYPASS_V1.md) already makes this candidate-set issue explicit.

ANTO supplies retained developmental competence, expression-state switching and irreversible toolkit loss. The overlap becomes empirically substantive only if a measured D/C comparison concerns the **same multifunctional flower part** identified by SLK, rather than unrelated pigment colour alone.

## Falsifiable organismal prediction and publication limits

A concrete, not-yet-tested prediction is that plant lineages with comparable **average** pollinator composition and measured intact developmental resources will show different stability of functionally competent genealogies depending on the **autocorrelation of pollinator conditions relative to the inheritance of expression states**. Future data need independent biological lineages with time-resolved partner interactions, actual structural D/C states, inherited functional module assays, absolute reproductive output, and controls for geography, ancestry and gene flow.

This does not say that random versus periodic environments are interchangeable, that either switching rate is an evolved optimum, or that flowers recoloured in Ryukyu Cirsium. Markov environmental conditions are hypothetical. Plant toolkit loss is not organism extinction, and 14-generation presence is not eventual fixation.

Environmental timescale/phenotypic switching theory is prior art: Acar et al. 2008, DOI 10.1038/ng.110; branching random Markov ecology and Lyapunov exponents: Hautphenne & Latouche 2016, DOI 10.1007/s10955-016-1474-3. The present novel-to-program application is the source-registered retained-capacity **biological interpretation**, with exact environmental-sequence enumeration at finite H and independent negative controls—not a claim to have discovered a new theorem.

The numerical model, 13 focused tests and full-suite CI are owned solely by [ANTO v6 PR #19](https://github.com/zuizui0223/anto/pull/19). SLK contains only this scope-aware organismal inference. SLK's main Am Nat manuscript is not changed; both original parent PRs remain draft. [aza3](https://github.com/zuizui0223/aza3) exclusively owns Cirsium empirical material.

## Real ecology source audit: what is observable now (20 October 2026)

A genuinely original published-author field-data comparison is now available from [aza3's source-verified *Cirsium arvense* visitor-and-seed PR #62](https://github.com/zuizui0223/aza3/pull/62), building on [its 10-day visitor-clock PR #58](https://github.com/zuizui0223/aza3/pull/58). It pairs three immutable author CSVs (615 heads, 120 timed visitor bouts, 649 visitor identification lines) by the shared **site × block × treatment** label. This is an inferred plant-treatment unit, **not** an authenticated same-head visitor→pollen→seed event. After removing ambiguous visitor UUID assignments and invalid time/open-head denominators, 81 source-label groups are eligible; 68 support the ratio of recorded hymenopteran to hymenopteran-plus-dipteran visited-flower counts.

The descriptive Pearson correlation of that ratio with measured viable-seed fraction is **+0.210** pooled and **+0.285** after centering within site × treatment. However, site-wise signs are NOT uniformly positive: campus **−0.014**, construction **−0.175**, ditch **+0.503**, rapseed **+0.446**. The one-observation-bout subset gives **+0.104**, whereas 14 multiply observed groups give **+0.649**, so observation effort and selective repeat exposure matter. A nominal visit-count-per-open-head-hour measure yields **+0.113**, but trimming the largest ~5% changes the pooled sign to **−0.027**. Every statistic is a **post-hoc observational source-label correlation**: none identifies genuine effective pollination, selection on an anatomical axis, or historical evolutionary reacquisition. Original experiment: Karpate et al. 2025 Research Square preprint, DOI 10.21203/rs.3.rs-6634172/v1; source is not an independent second dataset merely because more than one repository cites it.

**Scientific effect on this integration:** an actual plant study supplies a modest, source-verified ecological starting point—within one source species, guild composition and seed fate coexist and the descriptive association is context sensitive. It does **not** supply the structural SLK functional-conflict payoff or the generational ANTO genomic resource transitions. Ten intermittently sampled field days are *not* the stationary Markov environmental transitions across generations assumed in the v6 model. Thus neither the stochastic fitness signs nor the 14-generation competent genealogy survival may be calibrated from these records.

A decisive same-organism test remains missing: matched head anatomy, actual visitor contact and pollen fate, direct seed-enemy access, filled achenes, functional co-retained molecular modules, and parent-offspring continuity under measured partner turnover. Source-level fields in this archive have no measured bract geometry or functional genetic modules. Cirsium data and future authorized assays remain exclusively in aza3; SLK/ANTO keep separate theory/manuscript ownership.
