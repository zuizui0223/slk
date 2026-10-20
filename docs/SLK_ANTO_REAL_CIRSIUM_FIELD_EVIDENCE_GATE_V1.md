# SLK × ANTO — biological evidence gate after real Cirsium visitation reanalysis (2026-10-20)

**Status: real insect observations admitted for ecological exposure only. No observed natural functional re-evolution or model-payoff calibration.** The canonical empirical source and executable code belong exclusively to [aza3 PR #58](https://github.com/zuizui0223/aza3/pull/58); this is a scientifically scoped interpretation in SLK draft #119, not an independent replicate or second data pipeline.

## The new biological observation

The original 2022 *Cirsium arvense* field study (Karpate and colleagues, 2025 Research Square **preprint** DOI [10.21203/rs.3.rs-6634172/v1](https://doi.org/10.21203/rs.3.rs-6634172/v1)) published contemporaneous timed insect visitation records alongside other original reproductive datasets. The [author's fixed source commit](https://github.com/Yogita25/Multitrophic_Interactions/tree/8a151c62ed069f775a16b9bc5fbdce209cbb8691) carries two genuinely original files:

- `Pollinators.csv`: 120 site/block/treatment visitation-bout rows, ten calendar days across 4 sites during July 2–20, 2022 (not plant generations).
- `Pollinator_Id.csv`: 649 visitor observation lines, including the original order classification and pollination-role labels. The author labels are not verified stigma pollen transfer or seed fecundity.

The new [aza3 source verifier](https://github.com/zuizui0223/aza3/blob/research/slk-anto-real-arvense-visitor-clock-20261020/analysis/audit_arvense_original_visitor_clock_v1.py) checks the *exact Git blob SHA1* of both CSVs and requires a unique original observation-bout key. Four bout keys were reused and 77 taxonomically named visitor rows referencing them were conservatively excluded, along with one unmatched visitor key and 23 blank-order lines. The resulting **548 named-order insect observation lines join unambiguously to 92 observer bouts**; **48/92** of those bouts contain records from **both Hymenoptera and Diptera**. These short windows are observations at a surveyed plant, not proof that insects touched the very same head, of realized pollination, or of antagonistic payoff.

There is exploratory evidence of short-season variation: comparing the first and last observation date within each of four sites, a Hymenoptera fraction computed by weighting insect-record counts rose at all four sites, but **only two sites rose when each bout was weighted equally**. Sampling/treatment/photographic effort and site-day variability remain confounded. This is not a formally identified calendar trend or stochastic ecological Markov parameter.

The original field study also includes seed/fruit results (615 original head rows, independently audited in aza3; 39 site-block treatment pairs), but no verified **same biological individual / same head** join to the visit-bout records or head differentiation and functional genetic modules. No new combined effect size has been authorized by these distinct ledgers. Especially, an organza bag that excludes pollinators may also physically exclude egg-laying seed predators; do not automatically interpret seed differences as pollinator-only mediation.

## What is now observationally positive, and what remains hypothetical?

| Biologically necessary link | Evidence status | Why it matters |
|---|---|---|
| Real Cirsium individuals are observed by more than one broad insect order over short intervals | **Supported descriptively** by original bouts, not effective pollen transfer | Ecological partner identities can overlap rather than provide mutually exclusive A/B habitats |
| Within a flowering season, insect-order record composition varies by site and date | **Descriptive, not causal; highly denominator-sensitive** | Environmental state needs an explicit operational definition rather than averaged insect photos |
| Floral shared organ faces truly opposing pollinator-versus-antagonist selection gradients | **Not tested** by these visitor counts | SLK `L>0` cannot be inferred from presence of insects |
| A structurally divided or retained support alternative has better complete-cycle fitness | **Not tested** | SLK `Phi=R-K`, relative invasion and developmental accessibility are not observed |
| The same genetically defined plant/descendants carry all required functional modules while the phenotype is off | **Not measured** | ANTO competence and re-expression remain theoretical |
| Measured ecological autocorrelation changes the fate of a functional module across true generations | **Not measured** | ANTO v6 Markov parameter, transition `p`, cannot be fitted to 10 opportunistic site-days |

## Correct integration and the next discriminating organismal test

A plant's **interaction history**, **visible anatomy**, **genetic competence**, and **reproductive fate** must all be attached to the same source-resolvable plant/genealogy before using ANTO v6 as an empirical explanation for SLK morphological stasis.

A useful local, stage-aware experimental contrast is: identify one focal accessible architecture `H` combining reproductive differentiation and supportive scaffold, another architecture `F` retaining mechanical support while reducing reproductive-class specialization, and an appropriate integrated comparison, under repeated visitor contexts with explicit genuine pollen-transfer/seed and seed-enemy-access endpoints. Measure:

- real `H`/ `F` structural traits, not insect classification as a proxy for morphology;
- successful pollination/paternity and filled viable achenes, plus enemy oviposition/damage in the **same heads**;
- absolute complete-cycle fitness and evidence of the cost of differential anatomy, not only visits or pollen removal;
- functional retained and regulatory modules across properly tracked offspring and environmental histories, not leaf transcript-family homology alone;
- alternative routes (standing variation, plasticity, de novo mutations, hybrid donor, dispersal), and actual founder availability.

The preliminary *C. arvense* visitation evidence makes temporal context worth measuring, not already causal. There is no evidence of the required linkage for *C. sieboldii* planned 40 (no matched observed same-individual/genomic/fitness dataset or field permit), Ryukyu-coloured and white Cirsium young-leaf RNA (different plants from this study, functional pigment unvalidated), or a published heterantherous *Solanum* mechanical comparison (no ancestor-to-descendant re-expression assay).

**Scientific claim ceiling:** SLK still explains candidate-specific selective barriers to division of labour; ANTO concerns latent resources and trait re-expression. The new source-backed observation establishes short-timescale partner coexistence and measurement sensitivity in Cirsium, and identifies a nontrivial empirical gap. It does NOT confirm the joint theory, nor yield a new ecological evolutionary effect size.

**Ownership and status:** original ecological receipt / seven tests / source-pinned workflow / Japanese biological report in [aza3 PR #58](https://github.com/zuizui0223/aza3/pull/58). Existing SLK [draft #119](https://github.com/zuizui0223/slk/pull/119) adds this memo only; original Am Nat manuscript remains untouched. The ANTO theoretical Markov extension resides in [draft #19](https://github.com/zuizui0223/anto/pull/19), not merged main.
