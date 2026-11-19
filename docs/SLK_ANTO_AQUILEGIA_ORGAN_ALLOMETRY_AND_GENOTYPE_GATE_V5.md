# SLK × ANTO v5 — developmental whorl identity is not reducible to floral organ number; original QTL source gate

**21 October 2026 | real Aquilegia F2 original phenotype reanalysis, independent source-locked JS/Python results.** This is a biologically motivated descriptive sensitivity check, NOT newly validated genetic loci, natural reversal, genomic afterlife or field fitness.

## Main source-backed result

A previous source audit in SLK PR #121 demonstrated that anthers are positionally nested **outer → inner**, whereas strongly expanded filaments are nested **inner → outer**, in the inner two F2 whorls of the same *Aquilegia jonesii × A. coerulea 'Origami'* F2 flowers. These are opposite **spatial** containment relations, not a demonstrated developmental transition sequence.

The specific alternative being checked now is whether this order is a trivial byproduct of having many versus few stamens throughout the flower (floral organ number, FON). The 2024 study already reported weak FON effects (≤3% PVE for its QTL covariate assessments and an OR near 0.97 for several subtraits), so merely rediscovering its small effect would not be new. The independent F2 source reanalysis instead checks the **same scoring configuration** across FON strata, with missingness and one-flower-per-plant sampling accounted for.

### Authentic original data and fixed selection

- Johns JW et al. 2024, *EvoDevo* 15:6, DOI [10.1186/s13227-024-00225-3](https://doi.org/10.1186/s13227-024-00225-3). Original publisher CC BY 4.0 Supplement 3, [immutable source copy](../data/external/johns2024_aquilegia_f2_phenotypes_source.csv), Git blob `9911d4a5e85fa8629ad9890f28992e0f07e5feca`.
- 231 source F2 plants, 400 flowers, 800 scored inner/outer rows. **33/400 flowers** have missing stamen counts; 367 have a usable number. Selecting one original a-flower per plant (or b if a was never scored) leaves **211 plants with stamen counts**, 20 with missing stamen number.
- A scored organ mosaic is AN=1 (anther present but **not proven fertile pollen**) with LE≥2 (flattened filament expanded halfway up or more) and FU=1 (fusion **between** staminodial/stamen whorls), in **either** of the two source-whorl rows.
- To avoid an arbitrary post-hoc 'big versus small' contrast, size-class cutpoints are empirical tertiles of ALL 367 flowers with observed stamen counts: lower 37, upper 43. The one-per-F2-plant sensitivity uses the same boundaries rather than redefining the size distribution.
- Unit for the inferential descriptive model: 211 distinct F2 plants, one scored flower each, **not** 367 or 800 independent genomes.

### Positive actual F2 finding: size does not eliminate organ mosaics or positioning constraints

| Original total fertile-stamen count class | Scored F2 individuals with stamen count | AN+LE+FU mosaic in sampled F2 individuals | Directional nesting exception |
|---|---:|---:|---:|
| ≤37 stamens | 67 | **17 (25.4%)** | 1 |
| 38–43 stamens | 72 | **26 (36.1%)** | 0 |
| ≥44 stamens | 72 | **28 (38.9%)** | 0 |
| **Total** | **211** | **71 (33.6%)** | **1** |

The same grouping of **all 367** flowers with known stamen counts produces n=(126,127,114), with mosaic n=(32,45,42) and positional-rule exceptions (1,0,0). These are **repeated within-genotype observations**, and the group totals must not be treated as independent genotype sample sizes.

For a transparent one-predictor descriptive logistic fit on the 211 F2 plants (outcome: binary AN+LE+FU in selected flower; covariate: `(stamens-40)/10`), the resulting **odds ratio for ten additional stamens = 1.2042**, classical independent-F2-plant **95% Wald interval 0.8358–1.7350**. The estimated positive direction is **uncertain**; this DOES NOT prove FON has zero effect nor identify a gene-by-FON developmental interaction. Source phenotypic subset ascertainment, F2 linkage, morphology scoring and missing FON could matter. The 2024 original authors already linked stamen/staminode morphology and FON; our additional combination score is a pre-specified source-indexed *relabeling* of three traits, not newly collected data.

**Biological interpretation:** within the scored F2 morphology, the two opposite whorl nesting rules are not simply erased when total stamen counts differ greatly. The anther/expanded/fused mosaic exists throughout the sampled size range. Therefore a model in which whole-flower organ number is the *sole deterministic switch* permitting these scored configurations is contradicted by observed low, intermediate and high FON plants. This remains compatible with small allometric genetic influences, species-specific boundary genes and nonrandom F2 segregant distributions.

## Genomic intake gate: original map not deposited where the paper promises it

The article explicitly states that source code is available in [the named authors' GitHub repository](https://github.com/jasonwjohns/aquilegia_staminodes). We inspected the original public repo REST **file tree, all available branches and complete one-commit public history** on 21 October 2026:

- Default/only branch `main`, HEAD commit **57502ecdf9325a87a771ef376ff830d26273ab2b** dated 19 March 2024.
- Its complete non-truncated file tree contains **only a 57-byte `README.md`**, saying the repo is for staminode data/code. **No accessible processed genotype matrix, R/qtl map/bin matrix, association scripts, variant calls, or 231-ID QC crosswalk** occur within the named repository or earlier commits.
- This does **not** imply that the authors never computed a genetic map or that no such file exists anywhere. It is a precise, time- and location-bounded limitation on the public source promised by the article.

The published *EvoDevo* report itself describes **849,724 useful SNPs across 599 marker bins**, 329 QC-usable of 334 genetic-map individuals, **9 independent QTL**, total model PVE 44–53%, and a major outer-whorl lateral-expansion QTL on chromosome 3 (25.5% PVE). These numbers are **the original authors' published estimates, not our refit**. Other reported chr2/chr3 intervals overlap between some scores, but QTL overlap itself cannot distinguish pleiotropy from tight linkage or prove developmentally modular genes.

An independent [ENA read_run manifest for PRJNA1089234](SLK_ANTO_AQUILEGIA_SAME_PLANT_SRA_ID_LINK_V4.md) directly matches all 231 phenotyped F2 IDs to sequence-run aliases, but the compressed reads for those IDs sum to ~49.37 GB. Public ENA has **336 canonical numeric F2 aliases, not necessarily the same as the 329 usable R/qtl individuals**. Four alias prefixes have distinct source BioSample records; they must not be merged without author provenance and genotype concordance.

### Actual biological decision at this boundary

**Do not start a blind 49 GB sequencing retrieval or invent a new QTL.** First obtain the authors' marker-bin genotype matrix and the original map, with F2 sample IDs, quality masks and genotype encoding; a direct versioned source from the investigators is preferable. On valid acquisition, the highest-yield genetic test is whether **outer anther presence and inner filament expansion are genetically coupled by the same QTL or separable by whorl-specific segregation, accounting for both measured flowers within plant**. A stronger biological test still needs actual **pollen fertility** of AN-positive chimeras and mechanical/protective function under matched ecological partner conditions.

The source-led organismal conclusion remains deliberately narrower than a full SLK–ANTO integration: **partial, spatially constrained morphological reassembly is observed in one genetically defined F2 source, whereas the known ecological payoff of staminodes is measured in different taxa** (e.g. *Penstemon* and *Parnassia*). That is not a single native-lineage re-expression, profitable structural division of labour, or empirical evolutionary-genetic rescue event.

## Repeatability and provenance

- Original phenotype file and data quality: `data/external/johns2024_aquilegia_f2_phenotypes_source.csv`.
- [Source-matched FON–mosaic Python analysis](../analysis/audit_aquilegia_f2_allometry_v5.py) with fail-closed missing fields and one-flower-per-plant model.
- [Independent JavaScript source recount and logistic receipt](../results/aquilegia_f2_mosaic_allometry_JS_receipt_v5.json).
- [Negative controls and source-grade unit tests](../tests/test_aquilegia_f2_allometry_v5.py).
- [Audited public author-repository tree and original-genotype availability gate](../data/evidence/aquilegia_original_processed_qtl_public_source_audit_20261021_v1.json).
- [Reproduction and original data source CI](../.github/workflows/aquilegia-f2-staminode-real-organ-v1.yml) on [SLK draft PR #121](https://github.com/zuizui0223/slk/pull/121).
- Other taxa used for the *different* functional side: Walker-Larsen & Harder 2001 *Penstemon* (DOI 10.1111/j.0014-3820.2001.tb00782.x), Wen et al. 2024 *Parnassia* (DOI 10.1002/ece3.70380).

No original DNA FASTQ was downloaded, no genotype marker reconstructed, no newly assayed plant/pollen/fitness observation was invented, and no Cirsium empirical code was moved outside aza3.
