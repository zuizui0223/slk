# SLK global macro bridge V1 — fruit-set pollen limitation versus selfing ability

## Biological question and why the two traits must be separated

**Does the ability to reproduce with self pollen (self-compatibility, SC) or without pollinator delivery (autofertility, AF) buffer reproductive pollen limitation across species and ecological contexts?**

These are distinct floral reproductive traits. Their difference is relevant to the SLK *ecological context* question, but neither directly measures pollen feeding/export division of labour, anther morphology, evolution of partial specialization, the candidate payoffs \`Phi\`/\`g0\`/\`Delta_R\`, or changing pollinator communities. This is a **new cross-database analysis of public primary datasets**, not a new field observation or a direct confirmation of the model.

## Locked independent public sources

- Bennett JM et al. 2018, *Scientific Data* 5:180249. GloPL source DOI: [10.5061/dryad.dt437](https://doi.org/10.5061/dryad.dt437); paper DOI: [10.1038/sdata.2018.249](https://doi.org/10.1038/sdata.2018.249). Public source CSV is pinned to \`idiv-biodiversity/pollen-limitation-data-descriptor\`, commit \`abbe193770981b2c61713e75a0f01e004bdded8e\`, Git blob \`ef3fbc9ac144da55a5f5ff936bbab734711d53d0\` and SHA256 \`264ca8c2237f126b3c209fcba039e19b291324ddf6e7a96992dc8235a55984de\`.
- Razanajatovo M et al. 2016, *Nature Communications* 7:13313, DOI [10.1038/ncomms13313](https://doi.org/10.1038/ncomms13313), Supplementary Data 1 XLSX (published 2016 breeding-system indices). SHA256: \`cb17009ae65c4f6cb2d28b21239714782600d0904effa77c5635249d28e62fc0\`.
- Each raw file is downloaded externally and verified by hash. SLK redistributes neither raw source. Code lives at \`scripts/analyze_glopl_context_variation.py\`, \`scripts/audit_glopl_breeding_overlap.py\`, and \`scripts/analyze_glopl_autofertility.py\`.
- Separate GitHub Actions \`GloPL within-species ecological-context pilot\`, \`GloPL × global breeding-system coverage audit\`, and \`GloPL × breeding-system macro association pilot\` regenerate independent derived JSON and taxon match receipts.

## Exactly what was compared

The pollen-limitation response is the **natural log response ratio** for supplemental versus natural pollen receipt measured as *fruit set*. The GloPL analysis retains \`Included_Bennett_et_al_meta_analysis=yes\`, \`PL_Effect_Size_Type1=FS\`, \`PL_Effect_Size_Type2=Sup\`, and \`Level_of_Supplementation=flower\`; \`Bagout\` is excluded.

Taxa are matched by **exact genus+species binomial**, with no fuzzy synonym expansion, life-history matching or taxonomic guessing. For each matched species we first median-collapse identical GloPL population/year/location contexts, then median across each independent literature study, then median across studies so each species counts **once**. For breeding traits we take within-species medians across published source observations. AF and SC derived from fruit set are kept separate and are not interchangeable with realized field selfing rate or pollen limitation.

Correlations use Spearman's rank coefficient and two-sided deterministic 9,999-permutation tests with species as independent resampling units; bootstrap resamples species 1,000 times to obtain descriptive percentile bounds. **Neither phylogenetic relatedness nor selective study inclusion is fully modeled**, and the analysis is observational and exploratory.

## Data coverage

| Screen | Number |
|---|---:|
| GloPL original published experiments | 2,969 |
| Reported species in source publication | 1,265 |
| Exact-binomial species found by conservative parser | 1,223 |
| Breeding-system source publication reported species | 1,752 |
| Exact-binomial species found by conservative parser | 1,695 |
| Exact binomial overlap, all GloPL experiments | **429 species** |
| GloPL fruit-set/Sup/flower subset | 522 original experimental records |
| Distinct species in exact-binomial GloPL fruit-set/Sup/flower subset | 242 |
| Species with a matching breeding-system record | **81** |
| SC fruit-set index observed among those | **68** |
| AF fruit-set index observed among those | **56** |
| Both SC and AF fruit-set indices observed | **54** |
| Within-species multi-context GloPL sample with a matched breeding record | **16** |
| Within-species multi-context + observed AF index | **8** |
| Within-species multi-context + observed SC index | **10** |

A species match does **not** imply that the breeding-system and pollen-limitation experiments were done in the same site, year or genotype. Only three matched species had more than one GloPL source study, and 16 matched species had more than one breeding-system source study.

## Main empirical results: mean pollen limitation across species

All correlation values below are exploratory and *unadjusted*. Higher pollen-limitation log response indicates stronger female fruit-set response to experimentally added pollen.

| Predictor | Species n | Spearman rho | Two-sided permutation p | Species bootstrap 95% percentile interval for rho |
|---|---:|---:|---:|---|
| **SC (fruit set)** | **68** | **−0.2824** | **0.0218** | −0.5037 to −0.0496 |
| **AF (fruit set)** | **56** | −0.0729 | 0.5944 | −0.3362 to +0.2056 |
| SC (seeds per flower) | 11 | −0.5727 | 0.0674 | −0.8972 to +0.1495 |
| AF (seeds per flower) | 8 | +0.0488 | 0.9279 | −0.9428 to +0.8228 |

The initial SC negative correlation is **not a confirmed distinct effect from AF**: sample sizes differ; four exploratory indices were screened; for example a conservative four-test Bonferroni adjustment would make the minimum unadjusted p=0.0218 become 0.0872. Study selection, nonshared geographic contexts, family/clade differences and experimental emasculation may bias these comparisons.

### Same 54 species with both traits observed

| Relationship | Spearman rho | Two-sided permutation p |
|---|---:|---:|
| SC versus pollen limitation | −0.2471 | 0.0693 |
| AF versus pollen limitation | −0.0453 | 0.7459 |
| SC versus AF | +0.4643 | 0.0003 |

The difference \`rho(SC, PL) − rho(AF, PL) = −0.2018\` has a **species-paired bootstrap 95% interval of −0.4661 to +0.0693**, spanning zero. Thus **we cannot conclude that the associations of SC and AF with pollen limitation differ**.

The positive SC–AF rank correlation is expected to some degree biologically—autofertility generally requires some mechanism to produce seed without pollen delivery, but does not necessarily imply a high fruit-set measure of SC under hand selfing. It is **not evidence** that increased autonomous reproduction has evolved because of GloPL pollen-limitation environments.

## Robustness and qualifications

- Family-level median aggregation (not full phylogenetic modeling) weakens the associations to \`rho_SC=-0.2051\` across 39 families and \`rho_AF=-0.1163\` across 36 families.
- Removing experiments marked \`Emasculated_treatment=yes\` changes SC rho from −0.2824 to **−0.1451** (56 species); AF rho is −0.1156 (51 species). This is a particularly important selection/protocol sensitivity, **not** a simple estimate of a natural breeding-system effect.
- Removing source records with added zero-cell constants gives SC rho **−0.3216** (67 species) and AF rho **−0.1051** (55 species). Excluding effects \`|lnRR|>3\` gives SC rho **−0.2444** (65 species) and AF rho **−0.0084** (54 species).
- Most matched species were perennials (76/81); annual/biennial species were only five, preventing a meaningful life-history interaction test. Among perennial species, SC rho was −0.2599 (64 species) and AF rho −0.0748 (53 species), still observational.
- Within-species site/year pollen limitation **range** was negatively associated with SC (10 species, rho −0.456, p=0.1863) and AF (8 species, rho −0.415, p=0.3142), but both tests are **underpowered and non-significant**. These are not estimates of temporal environmental buffering in the same genotype; range also rises mechanically with sampling effort.
- Data assembled from separate literature are nonrandom. Region, climate, life history, phylogeny, pollinator identity, pollen competition, pollen donor number and paternity are not jointly controlled. A cross-species association does **not** measure causal reproductive assurance or SLK evolutionary division of labour.

## Strongest supported takeaways and next scientific decision

1. **Supported independently by the original GloPL matched-context screen**: pollen-related fruit-set limitation varies among repeated ecological contexts in many species (31/58 matched experimental strata have log-response-ratio range ≥0.5). See \`docs/SLK_GLOPL_CONTEXT_PILOT_V1.md\`. These are *point-estimate differences*, not individual significant reversals.
2. **Exploratory, not yet a supported new general biological law**: SC may show a negative association with the magnitude of pollen limitation, but its evidence weakens with matched species, emasculation exclusion, and family aggregation; AF shows no convincing monotonic correlation in this restricted sample.
3. **Not demonstrated**: that AF buffers within-species environmental variability more than SC; the strictly matched sample with measured AF has only eight species. We do not promote that claim to the flagship.
4. **Required before journal-level causal interpretation**: independent taxonomic harmonization, phylogenetic control, study- and family-aware uncertainty, equal protocol control, broader repeated-population coverage, and direct pollinator/morphology data to connect pollen limitation back to the evolving flower organization.

**Publication choice:** retain as a separate independent *empirical bridge/pilot*, not part of the near-7,500-word flagship as if it directly measured specialization gates. This is a defensible first step toward a truly independent macroecological study, but it is not yet publishable evidence for the central SLK morphological maintenance mechanism.
