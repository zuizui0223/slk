# SLK empirical bridge: within-species pollen limitation across ecological contexts (pilot V1)

## Biological question

**Can plants of the same species encounter substantially different pollen-related reproductive limitation across places or years?**

The main SLK model concerns the evolutionary value, accessibility, and establishment of structural division of labour. This empirical pilot tests **only a necessary ecological component**: variation in the reproductive consequences of pollination across populations and years while holding *species identity* and the main experimental protocol constant. It does **not** identify unchanged floral morphology, pollen-reward versus pollen-export conflict, trait-specific selection, evolutionary thresholds, or the causal identity of environmental changes.

This is an original *filtering and matched-context description of an existing public global database*, **not newly collected primary data**, a first discovery that pollen limitation varies in nature, or confirmation of SLK's three theoretical gates.

## Provenance and reproducibility

- Source: Bennett JM et al. (2018), **GloPL, a global database on pollen limitation of plant reproduction**, *Scientific Data* 5:180249. DOI https://doi.org/10.1038/sdata.2018.249
- Public dataset: https://doi.org/10.5061/dryad.dt437
- Reproducible source mirror: https://github.com/idiv-biodiversity/pollen-limitation-data-descriptor
- Pinned upstream commit: \`abbe193770981b2c61713e75a0f01e004bdded8e\`
- CSV path: \`Output/GloPL.csv\` (Git blob SHA \`ef3fbc9ac144da55a5f5ff936bbab734711d53d0\`)
- Script: \`scripts/analyze_glopl_context_variation.py\`
- Synthetic regression: \`tests/test_glopl_context_variation.py\`
- Source data are downloaded and verified against the pinned Git blob; they are **not redistributed** inside SLK.
- Full source-size and metadata baseline: **2,969 experimental records, 1,265 species**. These source-level numbers are not the sample size of the matched-context SLK pilot.

Run with network access:

\`\`\`bash
python scripts/analyze_glopl_context_variation.py \
  --download --assert-pilot \
  --out /tmp/SLK_GLOPL_CONTEXT_RECEIPT.json \
  --groups /tmp/SLK_GLOPL_MATCHED_GROUPS.csv
\`\`\`

The independent GitHub Actions job \`GloPL within-species ecological-context pilot\` validates the pinned CSV and uploads **only derived receipts**.

## Predeclared ecological estimand

GloPL \`PL_Effect_Size\` is the natural-log response ratio of reproductive output after hand-pollen supplementation relative to natural pollination. A difference of 0.5 between contexts means approximately \`exp(0.5)=1.65\`-fold difference in that **ratio**, not 65% higher natural seed output and not an estimate of the selection differential on structural division.

For the **primary descriptive analysis**, require:

1. Original GloPL record flagged \`Included_Bennett_et_al_meta_analysis=yes\`.
2. Exactly **fruit set** (\`PL_Effect_Size_Type1=FS\`), **pollen supplementation** (\`PL_Effect_Size_Type2=Sup\`) and **flower-level** (\`Level_of_Supplementation=flower\`). This avoids pooling incomparable reproductive endpoints and bagged outcrossing treatments.
3. One study × accepted species × outcome × treatment stratum identified by \`Author, Year, DOI, Species_accepted_names\` and fixed method.
4. Collapse repeated entries at the **same population + study-year + geographic coordinates** to the median effect; this prevents multiple treatments/morph entries from being independently counted as replicates of a site-year.
5. Retain matched strata with at least two distinct contexts and at least two different geographic sites or two explicitly coded, valid four-digit study-years. Missing/interval-coded years are **not** treated as temporal contrasts.

Do not assume identical plants, genotypes, developmental states, pollinator assemblages, selection gradients, or floral architecture across matched contexts merely because the species name is the same.

## Observed results: strict matched ecological comparisons

The following are **descriptive**, not proof of causal environmental change. Counts were independently derived from the pinned public CSV; the locked GitHub Actions dataset replay is a separate verification step.

| Audit stage or result | Value |
|---|---:|
| Included fruit-set / Sup / flower-level original experimental rows | **522** |
| Species in those rows | **249** |
| Unique study × population × site-year contexts after collapsing same-context entries | **451** |
| Strict site/year-replicated comparison strata | **58** |
| Distinct plant species among those strata | **53** |
| Total context entries contributing to 58 strata | **227** |
| Median within-stratum effect range (maximum minus minimum log ratio) | **0.529742** |
| Matched strata with log-effect range ≥ 0.5 | **31/58 = 53.4%** |
| Matched strata with log-effect range ≥ ln(2) | **21/58 = 36.2%** |
| Strata containing effect point estimates on both sides of zero | **17/58** |

For the 31/58 fraction, **species-cluster** bootstrap with seed 137, 3,000 replicates produced descriptive percentile bounds around **0.393–0.677**. For the median range, the corresponding bounds were around **0.320–0.681**. The bootstrap measures sampling variation **within this non-random subset of repeatedly studied species**, not uncertainty about all global angiosperms or the statistical significance of individual contrasts.

### Spatial and temporal restricted comparisons

| Same-protocol matched contrast | Comparison strata | Distinct species | Effect range ≥ 0.5 |
|---|---:|---:|---:|
| Distinct sites **within the same explicitly recorded year** | 19 | 9 | 11 |
| Distinct explicitly coded **years at the same site/population** | 37 | 22 | 13 |

These are overlapping sensitivity samples and **must not be summed** as independent groups. Missing and multi-year-range codes are excluded from the year-specific rows. Coordinates reflect the source dataset's precision and may include geocoding from location descriptions rather than exact field GPS positions.

### Robustness and analytic limitations

- Excluding records requiring added constants for zero responses retained **58 matched strata**, **31** with range ≥ 0.5.
- Excluding individual log-ratio estimates with absolute value above 3 retained **56 strata**, **29** with range ≥ 0.5.
- Requiring at least 3 distinct contexts gave **30 strata**, **21** with range ≥ 0.5; larger numbers of contexts mechanically increase the expected observed max–min range, so this is **not** an unbiased effect-size comparison with two-context strata.
- Some records contain emasculation and auxiliary treatment information; study-specific trait/population subconditions could remain mixed after collapsing. Sensitivity to emasculation and heterogeneity in published study design must be checked before any stronger evolutionary inference.
- Individual pollen-limitation effects are estimates with measurement error; crossing zero **does not establish a significant biological change or a true reversal of selection**.
- The GloPL database is literature-assembled and selectively samples systems already considered interesting for reproduction, with repeated-site and repeated-year coverage **not randomly distributed**.
- Fruit set is a female-reproductive stage and does not capture pollen harvest by visitors, male paternity, inbreeding depression, complete lifetime fitness, or the relative value of two floral architectures.

## What this adds to SLK — and what it does not

**Supported ecological component:** within the subset of repeatedly studied species, the reproductive gain from added pollen can vary substantially across spatial and temporal contexts even under matched study and measurement categories. This is compatible with SLK's biological premise that a multifunctional structure faces shifting reproductive contexts.

**Not tested:** whether the original multifunctional phenotype stayed structurally unchanged; whether a selective compromise \`L>0\` exists; the gain from separating functions \`R\`; structural cost \`K\`; accessibility \`g0\`; rare establishment \`Delta_R\`; time to partial versus full differentiation; whether pollen limitation is due specifically to pollinator abundance, pollinator identity, climate, or endogenous resource status.

**Falsifiable next bridge:** independently assemble comparable data on floral specialism, self-compatibility versus autonomous selfing, and/or measured pollinator communities across the same taxa and sites. Require a sufficiently large taxonomic overlap **before** claiming a macro association. Test whether greater autonomous reproduction buffers **within-species** pollen-limitation variation, controlling for study, outcome, phylogeny and life history. The independent Razanajatovo et al. (2016) breeding-system data were subsequently matched by exact binomials; see `docs/SLK_GLOPL_BREEDING_MACRO_PILOT_V1.md`. Among these 53 original within-species repeated-context species, **16** have a matching breeding record, **8** have an autofertility index, and **10** a self-compatibility index. The pilot finds **no statistically supported buffering relationship** at this sample size. A sufficiently powered phylogenetic, study-aware test still requires more directly matched populations and pollinator-community measurements.

**Manuscript decision:** Keep this as an independent exploratory empirical-bridge receipt until an ecologically explanatory cross-database predictor and sensitivity to study/population dependence are verified. Do not insert it into the already near-limit *American Naturalist* flagship as if it confirmed three-gate bottleneck turnover.
