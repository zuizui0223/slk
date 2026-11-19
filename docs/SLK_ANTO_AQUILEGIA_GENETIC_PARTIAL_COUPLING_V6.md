# Aquilegia v6: nested anatomical identities, partly separated published genetic control

**21 October 2026. Authentic original Johns et al. 2024 `Aquilegia` F2 phenotype reanalysis plus a _comparison of the original authors' published QTL support intervals_. There are no new SNP-genotype calls or new causal genes.** See source doi:[10.1186/s13227-024-00225-3](https://doi.org/10.1186/s13227-024-00225-3).

## The biological question

If a formerly sterile stamen whorl partly regains anther identity, must its filament-lamination and fusion program necessarily follow as one all-or-nothing unit? Is there evidence of a constrained yet partly separable developmental architecture, rather than either a rigid single switch or a freely combinable "flower LEGO"?

The F2 flower score source (231 F2 plants / 400 flowers / 800 two-whorl rows) already established **anther outer-first positional nesting** and **filament-lateral-expansion inner-first positional nesting**, with both rules satisfied in 399/400 flowers, and 230/231 first scored F2 flowers. This is a spatial relationship, NOT proof of the historical order of natural regain. AN-positive morphology does not demonstrate viable pollen.

## The original authors' genetic data provide a more revealing distinction

The authors' original published [Table 1](https://link.springer.com/article/10.1186/s13227-024-00225-3/tables/1), rearchived under a CC BY 4.0 attribution in `data/external/johns2024_aquilegia_qtl_table1_publisher_v6.md`, lists **16 trait-by-whorl QTL rows**, which share underlying support regions. The paper reports **nine independent QTL**, not 16 independent genes; 329 F2s passed the original authors' genetic-map QC. **We did not obtain or refit the 329×599 original marker matrix**.

We compared *only within-chromosome 1.5-LOD interval intersections in centimorgans*, preserving the same trait, spatial whorl and original source names:

| Source QTL contrast | Pairs on same chromosome | Pairs with overlapping 1.5-LOD intervals | Biological interpretation (limited) |
|---|---:|---:|---|
| Anther presence: inner vs outer | **3** (Chr2, Chr3, Chr5) | **3** | Strong **co-localization** of author-detected anther loci across both positional whorls |
| Lateral filament expansion: inner vs outer | **3** (two Chr2 pairs, one Chr3) | **0** | Detected LE support regions for inner/outer are separated at those original mapped intervals |
| Outer filament expansion vs filament fusion | **2** (Chr2, Chr3) | **2** | Strong co-localization of structural/adhesion trait support intervals |
| Inner filament expansion vs filament fusion | **3** (two Chr2, one Chr3) | **0** | Detected LE-inner intervals are separate from the source FU intervals where mapped on same chromosome |

**Original interval examples:**

- Chr3 AN-inner **24.4–27.6 cM** and AN-outer **15.9–29.2 cM** overlap, with **AN-inner** explaining 23.8% PVE at its original reported QTL.
- Chr3 LE-inner **31.7–34.8 cM** and LE-outer **24.4–27.1 cM** do **not** overlap. The original **LE-outer Q3** accounts for **25.5% PVE**, the paper's major-effect QTL. At Chr2 the inner LE intervals **8.6–28.0** and **47.2–56.3** lie on either side of the outer LE support region **38.8–44.6**, not overlapping it.
- Chr2 outer LE **38.8–44.6** and FU **38.8–44.6** are identical support intervals; their Chr3 regions **24.4–27.1** and **24.4–29.2** overlap.

These are original AUTHOR genetic associations, organized into comparative trait-support overlaps by our auditable algorithm. Overlap cannot establish a single pleiotropic causal allele (tight linkage is possible), and lack of overlap cannot establish complete genetic independence (undetected smaller effects and correlated developmental downstream functions remain possible). These are not independent replicates of allele gain and are not evidence of ecological adaptation.

### New program-level synthesis, not a claim to an unknown law

**Developmentally constrained combinations can coexist with partly separated mapped genetic effects.** The strict positional relation of morphologically anthered versus expanded filaments in the observed F2 does not require all three traits to be governed by one identical set of source-detected QTL. Conversely, partial separation of support regions does not imply every hypothetical organ mixture is developable.

This addresses an important incorrect identification shared across the two research programs:

- **SLK**: the existence of a formally profitable alternative architecture (positive `Phi`) does not mean any arbitrary intermediate on an x-axis is morphologically **accessible**. Accessible alternatives must respect observed spatial relationships (and ultimately mutations + viability). SLK's optional candidate paths are not newly fitted from these F2 data.
- **ANTO**: retention/reappearance of an *anther-positive morphological score* does not mean a lineage regained ancestral pollen fertility, that all genetic components co-retained, or that a species has re-evolved a native developmental program rather than producing hybrid segregants. A candidate toolkit with some position-shared and some region-specific control is consistent with the model's "resource availability ≠ expression ≠ fitness" structure, but ANTO rates are NOT calibrated by published QTL support intervals.

A decisive same-lineage genetic test would analyze the original authors' marker genotypes for the same 231 F2 plants and the respective per-plant AN/LE/FU phenotype scores, treating the 169 extra flowers as within-genotype replicates, and predict held-out conditional configurations. It must distinguish chr3 co-localized loci from independent causation. **No marker data were extracted from the public author repo**—it currently contains only a 57-byte README at 2024-03-19 commit `57502ecdf9325a87a771ef376ff830d26273ab2b`. That contradicts the paper's apparent statement of code availability at that location, but it does not imply the authors never used processed genotypes. Existing ENA runs have all 231 matching F2 number aliases, ~49.37GB of compressed FASTQ, and four ambiguous duplicate-number BioSamples (16/19/36/50).

A genuinely ecological joint study also needs **pollen viability**, flower-mechanical function (visitor handling, stigma contact, protection), fecundity and competing visitor/grazer context on the same matched organ and genetic lines. These are absent from the Aquilegia paper. Real functional studies of homologous modified stamens in `Penstemon` and `Parnassia` come from **different taxa** and cannot be treated as jointly measured genotypes.

## Auxiliary actual allometry sensitivity

An independent source-only count on 211 distinct F2 plants with nonmissing stamen numbers gives AN+LE≥2+FU mosaic in 17/67 low- (≤37), 26/72 middle- (38–43) and 28/72 high-stamen (≥44) F2 plants, preserving the same positional constraint (exceptions 1/0/0 across these size groups). A one-predictor logistic description yields **OR 1.20 per ten additional stamens (95% Wald CI 0.84–1.73)**. Thus there is no clear monotone association in this source subset; it does **not** prove zero organ-count influence, and source authors had already found small FON effects. The biology-first conclusion is the **coexistence of intermediate organ structures across substantial stamen-count differences**, not a new adaptive floral trait.

## What is and is not established

**Actual observation:** spatially highly ordered stamen/staminode morphological mosaics with incomplete same-genotype penetrance in greenhouse F2 plants.

**Original published genetics:** 9 independent QTL and the source's overlapping and disjoint trait-specific support intervals, reflecting some joint and some whorl-specific control; no one causal gene uniquely established.

**Not established:** single ancestral trait reacquisition at the genotype level, independent genetic modules, gamete fertility of AN-positive intermediates, functional advantages for a given pollinator, original gene expression retained during historical absence, SLK profitability, invasion, fixation or offspring lineage rescue.

This means the cross-repository biological question is now unusually concrete but remains *partially untested*: **Which components of the same stamen-derived organ are developmentally available, and which of those are worth preserving under actual pollination and florivory selection?** The reported QTL alone cannot answer its ecological-fitness half.

## Reproduction and owner boundaries

- Published primary Table 1, with CC BY 4.0 source attribution: `data/external/johns2024_aquilegia_qtl_table1_publisher_v6.md`.
- Pure-python reader/interval comparison: `analysis/audit_aquilegia_original_qtl_overlap_v6.py`.
- Independent JS source parser + interval overlap table: `results/aquilegia_published_QTL_interval_overlap_independent_JS_v6.json`.
- Eight focused source-semantic tests: `tests/test_aquilegia_original_qtl_overlap_v6.py`.
- Original phenotype source and missing processed genetic-data audit: `docs/SLK_ANTO_AQUILEGIA_ORGAN_ALLOMETRY_AND_GENOTYPE_GATE_V5.md`, `data/evidence/aquilegia_original_processed_qtl_public_source_audit_20261021_v1.json`.
- CI: `.github/workflows/aquilegia-f2-staminode-real-organ-v1.yml` on **SLK draft PR #121**.
- This is an `slk` source-controlled **non-Cirsium** biological bridge. Generic ANTO remains separate and `aza3` exclusively owns all Cirsium source data/experiments.

The independent code validates the published table, not an independent new QTL fit. No new plant samples or field operations were performed.
