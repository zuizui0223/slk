# SLK three-strategy value / evolutionary-origin gate: shared, reversible, structurally separated

Date: 2026-10-20. **Status: generic empirical-identification extension to SLK G1–G9; source-backed examples plus conditional mathematical implications, not a completed G2–G9 biological receipt.** This document is companion material. It does not change the frozen *American Naturalist* flagship manuscript, import candidate-specific operations, or grant SLK ownership of the PAYOFF source derivation.

## Scientific update

An evolving organism need not choose directly between permanently sharing one multifunctional coordinate and permanently differentiating it. The minimal admissible comparison is

    SHARED           static / shared multifunctional coordinate
    PLASTIC          reversibly regulated shared coordinate, with cue history and response costs
    DIFFERENTIATED   genetically/developmentally stable alternative functional coordinates or organization

**A change in expressed phenotype within an individual is not a historical origin of a heritable module.** The empirical claim "functional trade-off caused new structure" requires **(i)** identification of the same-coordinate functional conflict, **(ii)** an alternative that actually changes the feasible simultaneous functional relationship and has positive net relative fitness **after comparison against real plastic responses**, **(iii)** genetically accessible/invasible variants and **(iv)** independently reconstructed historical origin with alternatives tested. Neither finding two functions in one flower nor finding two flower shapes is sufficient.

## G1–G9 preserving scientific ownership

The canonical [SLK empirical G1–G9 ledger](EMPIRICAL_G1_G9_SOURCE_LEDGER_V1.md), [K operational definition](K_OPERATIONAL_DEFINITION_V1.md) and [ownership handoff](OWNERSHIP_AND_HANDOFF.md) remain authoritative.

| Item | Required value / event | Scientific owner / evidence ceiling |
| --- | --- | --- |
| G1–G2 | **Simultaneous** opposing function-specific optima on the **same manipulated trait coordinate** and admissible loss `L`; distinguish optima derived from ecological states from true pure-function optima | SCH. Observing pollen reward + transfer, or changing selection between treatments, is insufficient without function contrast |
| New comparison guard before G3–G5 | Registered `W_S^*`, `W_P^*`, `W_D^*` or matched losses, each on **one reproductive-fitness horizon**; include actual switching, sensing, production and structural costs, and feasible shared/plastic/extra-axis architectures | BALANCE worldline methodology; SLK owns value comparator; PAYOFF develops restricted dynamical models |
| G3–G5 | `R,K,Phi=R-K` for a declared *matched* architectural counterfactual; `R=sL` **only** for its registered quadratic coupling construction. In the three-strategy comparison, explicitly state which reference has been selected | SLK. A `W_D-W_P` net advantage alone does not identify `K` |
| G6 | Actual heritable developmental/mutational path to the proposed new structure, accounting for endpoints separated by an adaptive valley or a finite jump | SLK/PAYOFF path and accessible-neighborhood models. Morphological divergence or plastid marker proximity cannot close it |
| G7–G9 | Actual genotype-architecture frequency-dependent relative fitness, finite-population fixation and mutation/immigration occupancy in the correctly mapped architecture pair | SLK downstream process gate. `I_D=Phi-eta` requires the declared binary frequency game and measured/justified feedback |
| Historical origin (distinct from G1–G9) | Correct temporal order of conflict and new heritable structure, phylogenetic replicated origin opportunities, and matched models for selection, drift, ancestral retention, plasticity, introgression and exaptation | Separate evolutionary-history evidence; completion of contemporary value gates does not identify historical cause |
| Post-formation ecological route | Trait × trait effects broken down into selective mutualist/antagonist and other independently measured contributions | BITA. Trait interaction ≠ unique mechanism; its residual ≠ structure cost |

The three-strategy extension **does not relabel all BALANCE `TEMPORAL_SEPARATION` as reversible PLASTIC**. Separate timing of male/female function, fixed dichogamy, genotype-plastic sex expression, and a plastic response to an environmental cue have different developmental/inheritance assumptions. A module that partitions functions across **different individual plants** (e.g. dioecy) is not identical to the PAYOFF ideal *within-individual* coexpressed two-coordinate module, because its payoff includes partner availability, mating and population-level pollen transmission.

## Mathematical source and the two distinct robust conclusions

PAYOFF [memoryless comparison](https://github.com/zuizui0223/payoff/blob/theory/plastic-compromise-to-modules-20261020/theory/PLASTIC_COMPROMISE_VERSUS_FIXED_ARCHITECTURE.md), [two-cue robustness](https://github.com/zuizui0223/payoff/blob/theory/plastic-compromise-to-modules-20261020/theory/TWO_CUE_MEMORY_AND_IRREDUCIBLE_CONFLICT.md), and independently implemented [arbitrary-history bound](https://github.com/zuizui0223/payoff/blob/theory/plastic-compromise-to-modules-20261020/theory/HISTORY_AWARE_COMPROMISE_ROBUSTNESS_V1.md) are **source theory**, not biological observations.

Under the declared *same single coordinate and two simultaneously active functions* model,

    F_E(x) = C + (a+b)*(x-x_E*)^2  >= C,
    C=ab*Delta^2/(a+b).

Any shared-coordinate policy with nonnegative sensing/memory/switching costs must incur at least `C` per time step, **even with perfect knowledge of the environment**. Therefore, a **viable, correctly matched** two-coordinate coexpressing module whose full intrinsic per-period debit satisfies `K<C` defeats any such single-coordinate response. This does not assert genetic accessibility or invasion.

The separately derived physical switching bound is

    psi(c) = c*d - (c*d)^2/(4T)   if c*d <= 2T
           = T                    otherwise,
    L_nonmodule >= min(C+T, C+B+rho*psi(c)).

For an explicitly synthetic witness with `C=3, T=1, B=.05, d=1, c=1, K=3.6`, a feasible plastic response beats modules at `rho=.1` (loss 3.590316 versus K=3.6) while all shared-coordinate controllers have loss `>=3.725>K` at `rho=.9` (even with future environmental information). `rho>11/15` is **sufficient, not exact** for the high-turnover module result in this model slice.

**Crucial falsification:** another exploratory synthetic cost `K=3.87` yields a PLASTIC→MODULE→PLASTIC apparent pattern **when only two observed cues may control phenotype**. In PAYOFF's independent 6-cue convex optimization, feasible plastic loss is **3.867409, 3.862357, 3.828762** at `rho=.90,.95,.99`, all **below** `K=3.87`. Therefore the apparent module-favored middle point at `rho=.95` is **not** a valid unrestricted-history claim. Do not generalize model-induced plastic-to-module transition from turnover frequency alone without measuring predictability and available memory/policies. In particular `rho` is the **actual ecological state flip probability**, not marked-plant sex-expression frequency.

The assumptions `a,b,Delta,q,rho,c,B,K` have **not been measured** in a single source biological system. Its two-coordinate ideal is not automatically a dioecy model. None of the numerical witness claims are empirical estimates.

## A direct empirical falsifier of morphology and binary-conflict proxies

[BALANCE U3 matched extraction](https://github.com/zuizui0223/balance/blob/main/data/BALANCE_PLANT_U3_MATCHED_EXTRACTION_V1.csv) contains **four matched case/control pairs** selected from original heteranthery research, clustered into **three independent taxonomic/dependence blocks** (Solanum, Melastomateae, Senna). Within this selected sample:

| Taxon | Visible heteranthery | Source-tested pollen use conflict | Source-qualified routing architecture |
| --- | --- | --- | --- |
| *Solanum rostratum* | PRESENT | POSITIVE | WITHIN_FLOWER_DIVISION_OF_LABOUR |
| *Solanum lycocarpum* | ABSENT | POSITIVE | AMONG_FLOWER_MODULE_DIVISION |
| *Senna alata* | PRESENT | POSITIVE | WITHIN_FLOWER_DIVISION_OF_LABOUR |
| *Senna spectabilis* | ABSENT (equal fertile stamens) | POSITIVE | WITHIN_FLOWER_DIVISION_OF_LABOUR |
| *Senna covesii* | ABSENT | POSITIVE | UNRESOLVED broader routing |
| *Osbeckia chinensis* | ABSENT | UNRESOLVED | UNRESOLVED |

Other U3 cases *Melastoma malabathricum* and *Senna bicapsularis* are also POSITIVE within-flower division. Thus among four case taxa **4/4 are positive** by discovery design; among four nonheterantherous controls **3/4 are directly positive**, and the remaining is **unresolved**, not an absence. Resolving the latter as either `POSITIVE` or `NO_DEMONSTRATED_CONFLICT` cannot produce a finite matched conflict-presence logistic coefficient under the registered pair structure. Independent BALANCE [partial-identification analysis](https://github.com/zuizui0223/balance/blob/main/docs/BALANCE_PLANT_U3_MATCHED_EXTRACTION_DIAGNOSTIC_V6.md) records a raw positive-rate difference bounded **[0,0.25]**, not a population effect.

The key **architecture rather than morphology** control is *S. spectabilis* versus *S. alata*: both show within-flower functional routing despite different apparent stamen dimorphism. Conversely *S. lycocarpum* and *S. spectabilis* are both nonheterantherous and conflict-positive, but route function among flowers versus within flowers, in distinct dependence blocks. Neither comparison establishes the origin of heteranthery, an actual `Phi`, or reversible response.

**Practical implication:** choose source-qualified same-flower coexpression/functional separation as one ecological dimension and visible organ dimorphism as a separate phenotype. Do not encode "heteranthery absent" as "shared functional architecture"; do not treat a species-phylogenetic ancestral polarity based solely on visible stamens as the origin of ecological function routing.

## Independent source challenge: Clarkia heteranthery favors temporal pollen dosing, not classic anther-role specialization

A separate original research programme, Kay et al. (2020), *Proc. R. Soc. B* 287:20202593, [DOI 10.1098/rspb.2020.2593](https://doi.org/10.1098/rspb.2020.2593), contrasts classic pollen-reward-versus-export division of labour with *pollen dosing* via delayed pollen exposure. The [BALANCE original-source claim and provenance audit](https://github.com/zuizui0223/balance/blob/data/clarkia-heteranthery-mechanism-20261020/docs/BALANCE_CLARKIA_COMPETING_MECHANISMS_V1.md) makes this distinct from the *Solanum rostratum* functional division case.

- In the original *Clarkia* paper, anther timing was assayed across **six heterantherous and five nonheterantherous species**; the authors report a phylogenetic timing difference (`F=75.71, p=.002`).
- Pollen from **both inner and outer whorls** occurred in both bee scopae and flower stigmas in *C. cylindrica*; their destination contrast was not detected (`p=.17`). This is **not** equivalence, zero conflict, or proof of no partial specialization.
- A dosing-vs-fully-exposed greenhouse manipulation in *C. unguiculata* (13 vs 15 original experimental arrays) reported **4.6 versus 1.9 mm exposed pollen** (~2.42×, `p<.001`) while stigma pollen delivery did **not** show a statistically established increase under dosing (the published no-dose log coefficient `-0.3507`, `p=.27`). Treatment flowers also differed in age by one day; do not claim isolated effect of developmental timing on lifetime male fitness.

The original article argues that staggered pollen presentation better explains *Clarkia* heteranthery than two anther whorls with **exclusive** simultaneous food-versus-gamete functions. **A morphologically differentiated floral architecture can therefore implement a timed-release schedule without identifying simultaneously differentiated pure-function modules.** This is a direct biological constraint on mapping SLK/PAYOFF's idealized coexpressed two-coordinate advantage `K<C` to visible anther morphology.

The minimum three-strategy **SHARED / reversible cue PLASTIC / coexpressed DIFFERENTIATED** comparison is a theoretical comparison contract, **not an exhaustive botanical strategy inventory**. For empirical flowering plants a fourth distinct option may exist: **PROGRAMMED_TEMPORAL_PRESENTATION**, with an irreversible, ontogenetically scheduled exposure/release profile. It is not necessarily reversible, cue-triggered or optimal under a stationary Markov-memory strategy and cannot be coded as `PLASTIC` by default. Distinguish it from both within-flower concurrent functional division and among-flower sexual function partition.

**Raw-data gate:** Dryad's public API gives the 2020 article's 29-file metadata, version ID **97733** and declared digests, but anonymous archive/file content retrieval returned **401/403** in source-acquisition tests. BALANCE therefore froze **published statistics only** and a metadata-source HOLD rather than reporting recalculated raw effect sizes. The source's archive manifest lists a greenhouse analysis script `BombusTrials2018.R` but not the data file `BombusTrials2018.csv` mentioned in its usage notes. No new numerical male-fitness or historical transition estimate is promoted from that missing dataset.

This **source-selected, two-programme mechanistic contrast** (*Solanum* versus *Clarkia*) is a strong falsifier of the deterministic morphology→same ecological function route; it does not estimate how frequent each mechanism is in nature, identify a new module's historically selective cause, or close SLK G2-G5.

### Mechanism taxonomy required before attempting architecture fitness comparisons

The companion [BALANCE selected-source mechanism crosscheck](https://github.com/zuizui0223/balance/blob/data/clarkia-heteranthery-mechanism-20261020/docs/BALANCE_HETERANTHERY_MORPHOLOGY_FUNCTION_TIME_NONBIJECTION_V1.md) now executes a direct **ten-taxon source-preserving comparison** of original U3 pollen routing and Kay2020 published Clarkia evidence. Of six taxa called visibly heterantherous by their respective source programmes, **four U3 taxa** have original-screened within-flower *different-function* pollen routing; **two Clarkia study taxa** have evidence favouring *delayed release of both anther whorls*. Of four nonheterantherous U3 controls, one has within-flower functional routing, one among-flower division and two remain unresolved. These source-selected taxa are nested in **three U3 matched taxonomic-dependence blocks plus one Clarkia genus/study block**, not ten independent transitions or any natural frequency denominator.

The original papers' visible-heteranthery definitions and experiment designs are **not identical** (Kay defined its comparative character by anther-whorl colour; U3 study cases use different morphological features). This coarsened morphological category is adequate only to refute deterministic **binary** morphology→function predictions; it cannot estimate an effect of the same quantitative anther-shape coordinate on routing across taxa.

**Correct empirical strategy state space:** `STATIC_SHARED`, `CUE_REVERSIBLE_SHARED`, `PROGRAMMED_TEMPORAL_RELEASE`, `PARALLEL_DIFFERENT_FUNCTION_ORGANS`, plus separately classified `AMONG_FLOWERS`, `AMONG_INDIVIDUALS`, `MOSAIC`, `UNRESOLVED`. This is a *measurement ontology*, not a universal ranking or mutually exhaustive theoretical population game. Time-programmed organs can be architecturally differentiated yet still deliver **the same two functions over time**; their presence is not evidence of the pure-component simultaneous optima release `R=sL`, the fixed idealization `K<C`, or a heritable new module origin. The original PAYOFF mathematical test still compares its declared strategies and must not be mechanically generalized to temporal floral organs.

**Next meaningful identification:** within a single qualified lineage, compare viable contemporaneous different-function division, programmed pollen dosing and within-genotype reversible regulation on a common scale of **male pollen siring and maternal reproductive fitness**, while controlling flower age/visit duration and adding independently measured costs. A source-known study reporting two mechanisms is not a causal architecture-selection experiment.

## Real plasticity alternative: Wurmbea is informative but not the same architectural experiment

[BALANCE's source-matched Wurmbea case audit](https://github.com/zuizui0223/balance/blob/analysis/wurmbea-genbank-history-20261019/docs/BALANCE_WURMBEA_CASE2008_REAL_GENBANK_VOUCHER_QC_RESULT_20261019.md) separately documents original measured sex expression and provenance. A marked male-expression *W. dioica* plant can produce hermaphroditic flowers in a later year; manipulated resources change the fraction of subdioecious males expressing perfect flowers (**66% vs 42%**). Female seed-fitness advantage changes (**3.7 vs 1.4**) under manipulated mating context. Those values neither define cue accuracy `q` nor structural `K` or total lifetime fitness. A tissue/plant sex expression change is NOT an independently heritable novelty.

The GenBank source audit recovered 22/22 original ndhF accession bytes and 23/23 focal-locus accession bytes, but 2/23 focal paper-voucher↔archive assignments conflict. Strict MR2(M)–MR4(D) comparison is **0/1,628 aligned sites over two source-agreed loci**; *W. dioica* AC53(M)–AC38(D) is **16/5,004 over four loci**. Closely related maternally inherited markers cannot identify nuclear sex architecture, genetic accessibility or independent evolutionary origin. The two disputed labels remain HOLD.

Therefore **heteranthery and Wurmbea are complementary, not interchangeable biological validations**: heteranthery exemplifies within-flower differentiated routes amid pollen fates, while Wurmbea exemplifies within-individual sex-expression plasticity and between-plant reproductive states. At present **neither** has same-context randomized phenotypic optimum comparisons, matched S/P/D lifetime fitness, cost `K`, heritable mutant path and independent historical transitions jointly measured.

## New empirical source-support diagnosis: simultaneity is not an identified architecture driver

The [BALANCE source-hashed timing × function pair × architecture audit](https://github.com/zuizui0223/balance/blob/analysis/source-stratified-trait-architecture-20261019/docs/BALANCE_TIMING_FUNCTION_ARCHITECTURE_COMMON_SUPPORT_V1.md) now directly reads its existing U2 sexual-interference original-review screen (**22 source species, 8 conflict-positive**) and independently the selected plant pilot (**29 source-context rows, 16 conflict-positive**), with U3 kept in its separate frozen matched-source frame.

- In U2, exactly **one of eight** positive screens is tagged `SIMULTANEOUS`, and its observed architecture is `SHARED_INTEGRATED`. The other seven are source-coded `MIXED` (five) or `SEQUENTIAL_WITHIN_UNIT` (two), and some separate functions spatially/temporally.
- In the pilot, exactly **eight of sixteen** positive rows are source-tagged `SIMULTANEOUS`: four shared pollinator–antagonist systems; three within-flower pollen-reward/gamete division systems; and one spatially separated pollinator–prey system.
- **None of the registered positive functional-pair families has all four populated source cells** in the simultaneous/other × structural/nonstructural comparison. Therefore a function-pair-conditional association between source simultaneity and strict structural differentiation lacks complete common support. The anecdotal four-shared/three-within-flower contrast is aliased with the biological function-pair selection process.
- The U3 reality control still consists of **four PASS matched pairs in three dependence blocks**, not an independent eight-taxon macro denominator. The positive nonheterantherous *S. spectabilis* and *S. lycocarpum* have different source routes even though both lack visible focal stamen dimorphism.

**Implication for SLK G1/G2:** the study screen's `conflict_timing_geometry=SIMULTANEOUS` is an author's coded temporal geometry, **not** direct evidence that two opposed *pure-function* optima occupy the same coordinate simultaneously or a measured model `C`. No source field measures within-genotype reversible policy cost `W_P`, direct module cost `K`, or a heritable structural origin. These data narrow the *necessary prospective* measurements but do not promote SLK's empirical G1–G5 gates or identify a general effect. The screening frames must remain separate from the independent BALANCE V4 confirmatory universe.

## Independent conflict-first empirical denominator: U6 is prospective, not a claimed module effect

The [new BALANCE outcome-blind U6 source opportunity and accepted-name audit](https://github.com/zuizui0223/balance/blob/audit/u6-preoutcome-taxonomy-20261021/docs/BALANCE_U6_SOURCE_OPPORTUNITY_AND_TAXON_ALIAS_AUDIT_V1.md) extends the evidence basis **beyond heteranthery-selected cases** without breaking its pre-registered outcome freeze.

U6 selected **21 source groups solely by published pollen-theft/inefficient-transfer evidence**, before opening any architecture. Review-side source recovery is 15 RESOLVED / 6 EVIDENCE_CEILING, with 63/63 source-screened predictor receipts and **zero independently adjudicated predictors**. Both coder A and B remain **UNSTARTED for all 21 groups** (42 unresolved architectural source slots); SLK G2–G5 direct architecture benefit is therefore **not currently estimable** from U6.

Its original source-bearing pollen pool is `SINGLE_OR_CONTINUOUS` for all 21 and spatial geometry `SAME_UNIT` for all 21; U6 has **zero within-frame predictor contrast** for these dimensions, even if its architecture coding were completed. The original source timing tags, in contrast, include **18 simultaneous / 3 sequential** groups. The sequential evidence concerns *visitor ordering at the pollen pool* (`Clusia arrudae`, `Crescentia alata`, `Tolmiea menziesii`), not directly programmed delayed anther release as in *Clarkia*. These codes are not a `do(z)` functional conflict load, a quantified PAYOFF `C`, or a time-series measured `rho`.

The canonical U6 dependence map **already** records two nonindependent taxonomic blocks with other universes: `Impatiens_capensis` exact species with U1, and `Melastoma_affine` with U3 `Melastoma_malabathricum` at a conservative accepted-species concept level. [Kew POWO](https://powo.science.kew.org/taxon/urn:lsid:ipni.org:names:570553-1) synonymizes *M. affine* to *M. malabathricum* subsp. *malabathricum*. The frozen Pass-1 prose declaring U3 had no overlap is stale relative to the canonical map, **not newly corrected source data**. Original experimental plant populations remain unverified; these are conservative shared taxon blocks, not duplicated proven biological experiments.

Thus **19/21** U6 groups are U6-only relative to current U1/U2/U3 exact/accepted species mappings, not 19 independent evolutionary origins. The future hypothesis `timing × function-route anatomy` can be tested **only after genuinely independent U6 architecture coding** and source/phylogenetic dependence. Do not repair source 18/3 imbalance by importing known morphological successes from U3/Clarkia, or infer a missing function-structure effect from the current absence of architecture labels.

## Minimal outcome-independent macro + intervention execution contract

The first meaningful comparative unit is

    accepted taxon/lineage × function pair × anatomical coordinate ×
    ecological overlap regime × source/study programme × phylogenetic block

before observing or filtering for an attractive outcome. Keep all of the following **separate**, including `UNRESOLVED` states:

| Field | Source measure | Bad proxy to reject |
| --- | --- | --- |
| Same-coordinate antagonistic selection | crossed or function-isolating fitness-gradient intervention | two pollinator guilds, two ecological states, or general multifunctionality alone |
| Simultaneous exposure / competing function fates | same observational time window plus functional route manipulation | pollen use conflict assumed to be constant through time |
| Cue predictability and temporal state dynamics | repeated environmental state/cue time series, measured `q` and transition dependence | weather variance, 66%/42% phenotypic plasticity or rho from expression changes |
| Shared versus reversible response | marked individuals and genotype-level repeated structural measurement under common conditions | fixed dichogamy, among-flower division, one observed photo |
| Qualified differentiated architectural state | experimentally distinct dimension, with preferential function loading, and reliable phenotype measurement | visible stamen inequality or heterogeneous organ size alone |
| Actual combined fitness `W_S^*,W_P^*,W_D^*` and K | matched same-population same-horizon seed/siring output, architecture maintenance/reconstruction costs or bounded pre-cost counterfactuals | pollination rate, pollen counts alone, source review prevalence or BITA residual |
| Heritability, invasion, and historical origin | nuclear genealogies, independent transitions, population-frequency fitness, alternatives | plastid similarity, phylogenetic tip co-occurrence, species name joins |

This research design must be tested on a **species-first sampling frame** with ascertainment and source dependence explicit. BALANCE U3 case recruitment was heteranthery-selected; U2/U3 and pilot review rows must never be pooled as natural taxon prevalence. AusTraits' wind/insect–sex system contrast is an independent *opportunity/morphology* baseline but contains almost no within-genus pollination-mode common support, and does not measure pollen functional conflict.

## Conclusion and publication ceiling

**Model-supported:** the same-coordinate simultaneous conflict floor persists with unlimited temporal memory; under a separate switching-cost model, stationary environmental turnover can make ideal fixed modules intrinsically preferable even to an informed controller.

**Source biological pattern recovered:** pollen conflict often routes through different structures even where the focal stamen morphology is equivalent or undifferentiated; real sex expression may switch within marked individuals; architecture form, phenotype and function can be decoupled.

**Not demonstrated:** trade-offs historically *caused* new heritable trait architecture to originate, a causal natural `Phi` sign, a genetic frequency-invasion margin, or general population prevalence of structural modularization. The flagship remains a theory/identification framework until independent same-lineage measurements close those gates.
