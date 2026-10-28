# SLK × ANTO: what floral structures really do under conflicting ecological partners (22 Oct 2026)

**A biology-first synthesis of TWO original experimental systems and ONE original developmental-genetic F2, not a pooled meta-analysis or an observed ancestral regain.**

## Core question

**When floral structures have more than one ecological role, does their persistence actually preserve reproductive capability under enemy pressure, and which forms remain developmentally available for later reuse?**

The observed pieces are now sufficiently explicit to distinguish where the SLK opportunity/fitness bottleneck lies, and why ANTO's inherited functional-reexpression question is not automatically answered by current-year floral compensation.

### 1. Parnassia wightiana: benefits and beetle costs are real, but net ecological selection under beetle pressure is still unmeasured

**Source:** Wen et al. 2024, *Ecology and Evolution*, DOI [10.1002/ece3.70380](https://doi.org/10.1002/ece3.70380), PMC [PMC11442331](https://pmc.ncbi.nlm.nih.gov/articles/PMC11442331). The modified, sterile stamen **staminode** is a glossy false-nectary cue that prospective pollinators use, while the florivorous leaf beetle *Nonarthra variabilis* preferentially eats its apex.

- **Direct floral structural benefit:** removing all staminodes or clipping only the glossy tip lowered prospective pollinator visitation/handling and mature seeds per harvested fruit relative to intact controls, in the authors' reported comparisons. Reported 2013 harvested fruit counts: **64 intact, 30 whole-organ removed, 44 apex-clipped** (138 harvested of 170 initially tagged; initial treatment-specific denominators and causes of unrecovered fruits not completely known). In 2014 harvested fruits were **40/36/42** respectively. These are outcome denominators, not 120/170 repeated independent individuals.
- **Direct antagonist use:** beetles fed sequentially on glossy tips, whole staminodes, petal fringes, petals and stamens; ovaries were rarely observed chewed. Petri dish feeding trials (10 comparisons × 35–42 replicates; 405 total) supported some, not all, predicted staminode preferences. Preferential eating does **not** prove a sacrificial carpel-protection fitness benefit.
- **Experimental boundary central to SLK:** staminode removal/visitor work was deliberately conducted in the **less beetle-infested site B** because at highly infested site A beetles repeatedly chewed the marked flowers and peduncles. Thus the study directly verifies pollinator-attraction benefits mostly in a lower-beetle context. It does **not** provide a fully crossed `organ retained vs removed × beetles included vs excluded` response of mature seed count on matched plants in site A.
- **Beetle-occupied-site differences are confounded:** at site A the authors attempted 35 visibly beetle-occupied versus 35 initially unoccupied flowers; at harvest remaining **31 flowers were all beetle-infested**, so there was no contemporaneous uninfested within-site comparison. Pollen-tube counts were instead contrasted among 31 site-A, 33 site-B and 42 site-C flowers. Site C blooms about 20 days later. These comparisons reflect both beetle pressure **and** site/phenology; they do not identify a beetle-causal pollen-transfer effect.
- **Temporal confounding and attrition:** at site A in 2014, for each early, middle and late flowering stage **60 flowers were originally tagged**; only **31, 41, 25** fruits respectively were recovered. These correspond to recoveries **51.7%, 68.3%, 41.7%**; florivorous beetle presence went from none (early), to <20% (middle), to >70% (late). This is real stage-associated change but not an experimental assignment of beetles. Missing fruits and stage are potential contributors to apparent seed-trend changes. A crude late/middle harvested-fruit Fisher p=0.00568 is descriptive only: causes of loss and independence/randomization of the initial tagged samples are not controlled.
- **Raw source block persists:** the paper lists Dryad DOI [10.5061/dryad.b2rbnzsqg](https://doi.org/10.5061/dryad.b2rbnzsqg). We verified the Dryad API identifies internal dataset **139500** but reports `Identifier cannot be viewed...`; the public search returns **zero** matches for *Parnassia wightiana* and the published share link is 404. No independent raw seed/pollen effect size or fitted factorial fitness contrast has been computed from that inaccessible dataset.

**Strict result:** a homologous sterility-derived structure attracts a mutualist and an antagonist; the former has an experimental benefit and the latter eats the organ. A counterfactual **net adaptive advantage when florivores are abundant** has **not** been resolved.

### 2. Cirsium undulatum: a genuine same-mother reproductive alternative, with context-sensitive success

**Source:** West & Louda (2021), *American Journal of Botany*, DOI [10.1002/ajb2.1744](https://doi.org/10.1002/ajb2.1744). 2007–08 source records from USDA Data Commons [10.15482/USDA.ADC/1522649](https://doi.org/10.15482/USDA.ADC/1522649), CC0. **Empirical reanalysis is performed ONLY in aza3 PR [#76](https://github.com/zuizui0223/aza3/pull/76)**, using 106 source maternal rows and the 323-head archive. We summarize the result, without duplicating Cirsium raw files in SLK.

Unlike Parnassia's one **staminode**, *C. undulatum* offers two **spatially different capitulum positions** in the same maternal plant: an apical head and lateral heads. Experimental apical damage (`d` vs `nd`) and a broad insecticide treatment (`i` vs `ni`) were crossed in each of two years. The 2008 sample has all 67 mothers' apical+lateral source seed sums consistent, so four-route classification is directly observable:

| 2008 treatment | n | No good seed | Apical-only | Lateral-only | BOTH |
|---|---:|---:|---:|---:|---:|
| Undamaged/ambient insects | 15 | 12 | 1 | 1 | 1 |
| Damaged/ambient insects | 12 | 5 | 0 | **7** | 0 |
| Undamaged/insecticide | 21 | 0 | 7 | 1 | 13 |
| Damaged/insecticide | 19 | 0 | 4 | 8 | 7 |

**Two nontrivial field facts:**
1. **Same-mother fallback exists but does not guarantee seed production.** Seven 2008 mothers made good seeds exclusively via lateral heads under apical damage/ambient pressure; five made no good seeds. This is anatomical alternative reproduction in the current generation, not recovered genetic ancestry, no evidence that branches were induced or upgraded after damage.
2. **Ecological pressure strongly affects whether the alternative can succeed.** Intact-apex plants with ≥1 good lateral seed increased from **2/15 ambient to 14/21 insecticide** (nominal exact Fisher p=.00218, eight-comparison BH q=.0174). Apical damage in ambient insects gives 7/12 lateral-positive versus 2/15 (point +45 percentage points, nominal p=.0369) but **BH q=.1477**, so it is **not** a confirmed extra compensatory effect after multiplicity correction. In the damaged/insecticide group, **11/19** mothers still made positive **apical** seeds, showing damage ≠ full organ abolition.

The 2007 source contains a mother (2007|327) with `ap.hd=0`, `o.hds=1` and whole `plt.gsd=20`. This row must be excluded for *joint anatomical-route states* (new n=105/106), but retained for the original total-good-seed analyses; original authors' older results are not errors. The 2007/08 mothers are separate cohorts. Insecticide may affect pollinators and multiple antagonists simultaneously; there are no measured pollen-transfer or gene-expression data in this archival experiment.

**Ecological meaning:** the value of a partially redundant reproductive structure is conditional on its real operational success under ecological partner pressure. Merely having two possible sites to reproduce does not make the second one a guaranteed compensator.

### 3. Aquilegia: developmental access to alternative morphology is real but NOT ecological selection

The same [SLK PR #121](https://github.com/zuizui0223/slk/pull/121) source-audits Johns et al. (2024), *EvoDevo* DOI [10.1186/s13227-024-00225-3](https://doi.org/10.1186/s13227-024-00225-3): F2 individuals (231 plants, 400 measured flowers) create anther-positive yet expanded/fused staminode-like organs, but physical forms obey nearly invariant opposed inner/outer whorl constraints (399/400 flowers). The original authors' nine QTL have overlapping AN inner/outer, separate observed LE inner/outer support intervals and shared LE outer/FU support regions. A 231-sample F2 number-to-SRA alias join exists, but the processed original 329×599 genetic-map matrix is missing from its promised GitHub location (only README accessible). No source anther pollen viability or pollinator/seed payoff is measured in the F2.

The three systems measure **different complementary parts** of the science. Their data cannot be multiplied into a published `P(reversion | selection)` or a fitness of one universal stamen structure.

## What this changes in SLK's biological question

The superficial view is “trade-offs promote separation, and separation preserves a trait.” The source-backed biological insight is more specific:

- A structure may keep **two ecological signals** coupled (Parnassia attracts mutualists AND antagonists); an apparent functionally desirable organ cannot be assigned a net value without both pathways and their joint exposure.
- A plant may have a **spatial substitute** (Cirsium lateral heads), but that substitute may fail under the very enemy context causing apical failure; genuine source data show zero versus positive lateral output in matched anatomical inventories.
- An organism's phenotype repertoire is a **developmentally constrained set**, not every mathematical intermediate (Aquilegia's strong whorl-position-dependent mosaics). Access to genetic sequence read records is not verified ancestral functional capacity.

**Proposed central falsifiable biological hypothesis:** Ecological interactions maintain a modified stamen-derived structure only when the realized **whole-organ offspring benefit** under the full mutualist–antagonist combination exceeds the functional opportunity cost of its alternative fates, within the set of morphologies the organism can genuinely develop. Persistence of that organ may leave it available for later reconfiguration, but this evolutionary-afterlife step remains an untested genetic/fitness link.

A real test needs a same-genotype factorial `staminode structure (intact/tip-only/whole removal or precise sham) × florivore inclusion/exclusion × pollinator guild`, plus direct pollen stigma deposition and mature achene/viable seed and descendant recruitment on identifiable plants. Avoid interpreting clipped signaling surfaces as genetically evolved structural differences. Stage- and site-matched sampling, wounded/sham controls, and lost-fruit follow-up are crucial. **No new field permission or experimental action was obtained in this project.**

SLK's `Phi,g0,Delta_R` remain useful analytical eligibility criteria for an identified candidate, but none of the three public biological sources estimates those coefficients or the complete ecological selection landscape. ANTO's retained-function theory concerns ancestral native genetic programs, not lateral seed fallback after apical damage. This document is therefore a **positive, source-limited organismal bridge**, not proof of a unified causal theory or a new mathematical selection threshold.

## Reproduction and source status

- `aza3` owns all *Cirsium* original CSV, tests, CI and joint reproductive-route source calculations: [PR #76](https://github.com/zuizui0223/aza3/pull/76).
- This SLK file is a downstream evidence interpretation only; no Cirsium code is copied, and SLK main/Am Nat submission remains unmodified.
- *Parnassia* source results are author-reported experimental aggregates, because the authors' referenced Dryad file is presently not publicly retrievable through its DOI/API. No original individual-level controlled beetle manipulation dataset was recovered.
- Independent `Aquilegia` F2 source/QTL reruns and individual SRA sample aliases live in [SLK PR #121](https://github.com/zuizui0223/slk/pull/121).
- All numeric dose/selection claims are tagged to their original published source (above). No `anto` native trait-restoration rate is fitted.

## 23 October — Quantifying measured maternal coverage, not hypothetical anatomical removal

A new same-source original mother audit in [aza3 draft PR #84](https://github.com/zuizui0223/aza3/pull/84) corrects an ambiguity in phrases such as “lateral heads rescue the mother.” The 106-source-mother, 323-source-head dataset has a valid **joint apical+lateral seed accounting** for 105 mothers; original 2007|327 remains excluded from this paired route analysis only.

For each original mother, let A mean the apical head produced at least one author-scored good seed and L mean any lateral head produced at least one. The observed **joint route coverage** is `P(A∨L)`, and the **increment over the better individual route** is `P(A∨L)−max(P(A),P(L))=min(n_apical-only,n_lateral-only)/n`. This is a *real, descriptive set identity*, NOT the experimental fitness gain from deleting a floral organ.

| Original 2008 source regime | Apical-positive A | Lateral-positive L | Any-positive A∨L | Both fail | Observed extra coverage over better route |
|---|---:|---:|---:|---:|---:|
| Apex undamaged, ambient insects n15 | 2/15 | 2/15 | 3/15 | **12/15** | 1/15 (6.7pt) |
| Apex damaged, ambient n12 | 0/12 | 7/12 | 7/12 | **5/12** | **0** |
| Apex undamaged, insecticide n21 | 20/21 | 14/21 | **21/21** | 0/21 | 1/21 (4.8pt) |
| Apex damaged, insecticide n19 | 11/19 | 15/19 | **19/19** | 0/19 | **4/19 (21.1pt)** |

Under damaged apex+insecticide, real seed production was **apical-only in four mothers, lateral-only in eight, both in seven, neither in zero**, so the two routes jointly covered observed failures in different individual mothers. Under damaged apex+ambient insects, seven mothers used only lateral heads and five had **both seed routes fail**; merely having lateral heads was not enough for every maternal plant. **This is an observational pattern of alternative operational reproduction, not proof that one insect antagonist caused simultaneous failures or that anatomical duplication was favored by evolution.**

The two-source case comparison with original *C. arvense* 2022 (merged aza3 #83) adds a second **distinct bottleneck**: pollinator-exclusion bags reduced original author-classified viable seeds/head by ~41.6, with the source-accounting deficit concentrated in the viable-seed / floret conversion term rather than floret count. It is a DIFFERENT species and experimental system, and the bag altered visitor access plus potentially enemy exposure/microclimate. Thus even many available floral heads may share a downstream seed-conversion vulnerability; **do not infer experimentally proven common-mode failure or a new macroecological adaptive trade-off from joining independent taxa**.

**SLK's stronger falsifiable question** is therefore not “are there two floral modules?” but “when are their realized failures sufficiently noncoincident, under the *same* ecological conditions, to make alternative architecture worth maintaining?” A matched, explicitly authorized organ/partner factorial experiment must measure counterfactual fitness and head-specific pollen and seed-enemy activity to answer that. The v1–v6 SLK selection thresholds remain model-only and cannot be parameterized by this observed union probability. New exact source tests are green in [aza3 PR #84 CI](https://github.com/zuizui0223/aza3/actions/runs/39917712538); **all Cirsium raw empirical code remains exclusively in aza3**.


## 28 October — The ecological failure is not simply absence of the lateral structure

The already published West & Louda (2021) USDA *Cirsium undulatum* source has now been joined **across the original mother and individual-head grain**, through [aza3 source-owned draft PR #96](https://github.com/zuizui0223/aza3/pull/96). In 2008 the 67 source mothers have **67 apical + 111 nonapical individual-head rows**; their summed good seeds exactly reconcile with each mother's reported apical/nonapical totals in all 67 cases. The 2007 individual-head source is **not fully reconciled** (two mothers absent, three lateral-sum disagreements including 2007|327, two treatment-label discrepancies), so the new complete cross-grain analysis is deliberately restricted to 2008.

Under apical damage and ambient insects, all **five of five** mothers that produced *zero good seed at both apical and lateral positions* nevertheless had at least one **individually recorded nonapical head**. One had two scored nonapical heads; four had at least three buds in the mother's source bud-count field. Among intact-apex/ambient-insect mothers, **nine of twelve** joint seed failures had at least one scored lateral head, five of them at least two. Therefore **mere nonexistence of every side head is insufficient to explain the observed maternal failure**, although a scored head is not proof that it had reached anthesis, received pollen, or had an opportunity to mature its seeds. The original `no.flw` field is semantically ambiguous: ten mothers have it recorded as 0 despite positive source good seeds; do not treat it as a complete all-head opening assay.

The apparently simpler hypothesis that a single high **flowerhead damage score** perfectly predicts individual head failure is also contradicted as a deterministic rule: in the 2008 damaged-apex/ambient group, 17/23 scored lateral heads have the highest observed damage score `av.dam=0.88`, yet **six of those 17 heads still formed positive good seeds**. Of **12** mothers in all 2008 treatments that had both positive- and zero-seed lateral heads with nonmissing damage scores, within-mother mean damage was **lower** on seed-positive heads in five mothers, **higher** in five, and tied in two. These are descriptive original data and do not imply damage is harmless; the cause may involve pollination, timing, resources, enemy identity, or imperfect damage measurement. **Neither an unspecified common enemy nor direct adaptive compensation can be identified from this observation.**

**SLK payoff implication:** genetic or physical *presence* of an alternative floral component must be separated from the component's *ecologically realized reproductive function*; they are empirically different endpoints. A genuine functional division-of-labour explanation requires recording the same identified head's anthesis, arthropod arrival/entry, pollen deposition, developmental/consumption fate and descendant recruitment, and where ethically permitted randomized structural/ecological manipulations. Positive parent-level seed output alone cannot calibrate the candidate-specific value `Phi` or rare-lineage establishment.

**ANTO boundary:** an existing side head recorded but unable to make good seeds is not an ancestral morphology that disappeared in evolution; no gene function, native trait reacquisition, developmental-memory transition or multi-generation inheritance is assayed here. The result informs the ecological **performance** dimension, not the molecular **afterlife** dimension. Empirical code and original raw maternal/head tables remain only in aza3.


## 28 October v5 — Multi-position alternative heads are observed within the same mother

A subsequent source-authenticated expansion of [aza3 PR #96](https://github.com/zuizui0223/aza3/pull/96) identifies **67 exactly matched 2008 mothers, 111 individual nonapical heads** and, among those, **33 mothers with two or more individually recorded nonapical head positions**. The original West & Louda 2021 `hd` codes (200, 210, 300, 310, ...) encode **head positions**, not verified dates of anthesis or sequential developmental re-expression.

Four of the 33 multi-lateral-head mothers had good seed **zero at their lowest numbered nonapical position but positive at a higher numbered position**. Two of these, **ES68 and SD05**, came from the **2008 apical-damaged, ambient-insect group**, in which their apical heads also had zero good seeds. The latter is a direct observation of reproductive output at multiple structural positions of the **same plant**, not inferred functional genetics or a selection coefficient. In contrast, six of 33 mothers with multiple recorded lateral heads had zero good seeds at every lateral position.

The same 2008 mother dataset contains four original plant-identifier prefixes `ES`, `SD`, `WG`, `WR`. All four occur in the apical-damaged/ambient group; its **five zero-seed mothers** are spread over the prefixes **SD2, WG2, WR1** (ES0). These are merely **source identifier strata**, not independently verified geographic sites or phylogenetic replicates. Thus the observed failure is not a single anomalous mother or a single source prefix, but its causes are still unknown.

**Biological SLK implication:** there may be a nested set of reproductive opportunities within a single individual, rather than only one main and one backup head. What matters is whether the actual alternative positions can convert floral opportunity into good seeds in the observed partner environment. Do NOT treat higher numeric head code as later flowering, successful downstream reproduction as natural selection for differentiated floral architecture, or a present side head as ANTO ancestral gene reactivation. These observations tighten the ecological question but cannot supply the SLK fitness values or any native evolutionary regain rate. Full source tests and the independent JavaScript receipt remain **in aza3 only**.
