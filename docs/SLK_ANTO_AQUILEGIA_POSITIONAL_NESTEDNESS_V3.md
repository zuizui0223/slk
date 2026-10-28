# SLK × ANTO v3 biology — organ reassembly is constrained by *position*, not free LEGO

**21 October 2026 | authentic original Johns et al. 2024 F2 phenotypes | nested organ-identity reanalysis | unmerged exploratory SLK PR #121.**

## Main result in organismal terms

In F2 flowers produced by crossing *Aquilegia jonesii* (whose normally staminodial whorls are stamen-like) with *A. coerulea* 'Origami' (normally staminodial), subtraits **can mix**, but they do not mix as unconstrained independent parts. The observed morphological presence of an anther in the **inner** target whorl is always accompanied by an anther in the **outer** target whorl, while high filament lateral expansion in the **outer** target whorl is almost always accompanied by high expansion in the **inner** whorl. These two spatial directions point in opposite directions.

The empirical result is an almost perfect **within-flower positional nestedness of two scored organ identities**, not a phylogenetic or temporal order of trait restoration. The original 2024 authors already established a "fading stamen–staminode boundary"; this quantitative full-CSV audit does **not** claim to be the first discovery of that developmental gradient. It supplies a source-locked, genotype-grain, threshold-sensitive bound on how freely the subtraits can combine.

### Exact source, measurements, and independent reproduction

- **Original source:** Johns et al. 2024, *EvoDevo* 15:6, DOI [10.1186/s13227-024-00225-3](https://doi.org/10.1186/s13227-024-00225-3), author publisher Supplementary Material 3 (CC BY 4.0).
- **Immutable source file:** `data/external/johns2024_aquilegia_f2_phenotypes_source.csv`, Git-blob SHA1 `9911d4a5e85fa8629ad9890f28992e0f07e5feca`.
- **Biological units:** 231 F2 plants, 400 flowers (62 plants with one measured flower, 169 with two), 800 inner/outer whorl-score rows. Repeated flowers from the same F2 are not independent genetic observations.
- **Traits:** `AN` = anther visible (not pollen viability), `LE` = ordinal filament side expansion 0–3, `FU` = interwhorl fusion scored once biologically per flower but duplicated in source rows.
- `LE≥2` means expanded at least halfway up the filament; `LE≥3` is the maximum score, more than halfway. The choice of score threshold must be disclosed.
- **Genotypes** are not included in this phenotype CSV; the original paper's 9 independent QTL on genotyped plants are the **authors' own result** and cannot be newly estimated from these 800 rows.

### Two opposed positional nestedness relations

Define **rule A**: inner anther present implies outer anther present (inner-yes/outer-no would violate). Define **rule B**: outer LE≥2 implies inner LE≥2 (outer-yes/inner-no would violate).

| Source-level observation | All 400 flowers | One prespecified flower per 231 F2 plants |
|---|---:|---:|
| Inner whorl AN=1 | 184 | 115 |
| Outer whorl AN=1 | 283 | 165 |
| **AN violation: inner yes, outer no** | **0** | **0** |
| AN outer yes, inner no | 99 | 50 |
| Inner LE≥2 | 323 | 186 |
| Outer LE≥2 | 243 | 141 |
| **LE violation: outer expanded, inner not** | **1** | **1** |
| **Both rules hold in same flower** | **399/400 (99.75%)** | **230/231 (99.57%)** |

The sole `LE≥2` exception is **plant 132, flower a** (inner score 1, outer score 2). A still weaker threshold `LE≥1` also finds one exception (**plant 39, flower a**, inner score 0, outer score 1), while `LE≥3` has **zero** exceptions. Thus the nesting is not manufactured by a single arbitrary expansion cutoff. The completely unconstrained assertion "every organ configuration should be freely available" is directly at odds with the observed F2 combination structure; it does **not** follow that these exceptions are biologically impossible in a larger population.

The first-flower-per-plant analysis is used for genotype-level sensitivity; flower-a and flower-b separately among the 169 duplicated plants yield 168/169 and 169/169 meeting both selected rules, respectively. This directional relationship is therefore not created by naively treating 400 flowers as 400 unrelated plants.

### Sensible negative control, not invented genetic independence

If the first-flower-per-plant marginal inner and outer whorl scores were **randomly shuffled among different F2 plants**, preserving their separate frequencies but breaking the within-flower relationship, the expected violations would be **32.857** for rule A and **27.468** for rule B, versus observed **0 and 1**. That counterfactual supports a strongly constrained *phenotypic* arrangement; it is **not** an ecological or genetic null that plants actually produce independent whorls. No p-value about gene-module independence or natural selection is inferred.

### Partial re-expression versus coupled architecture

Earlier v1/v2 reanalyses found:
- **187/800 whorl rows** jointly express anther presence with strong expanded/fused staminode-like filament morphology, corresponding to **129/400 flowers and 91/231 F2 plants**. Anther presence does not imply all other tissue characteristics are a normally fertile stamen.
- In **169** two-flower plants, the specific mosaic occurred in both flowers for **38**, only flower a for **23**, only flower b for **16**, and neither for **92**. A negative flower a followed by a positive flower b occurred in **16/108 (14.8%)** genotype-matched negatives.

Together, these facts show that **partial organ characteristics can be expressed conditionally within a plant, but the positional pattern of that partial reassembly remains highly structured**. This bears on what it is legitimate to call "available" in an evolutionary model: current absence of a morphology is not by itself evidence of inability, but observed developmental mosaics do not imply unrestricted module recombination.

## What belongs to SLK, what belongs to ANTO, and what is still unproven

**SLK implication:** comparisons of integrated versus specialized structures must not silently assume that any mathematical intermediate is a developmentally realizable floral configuration. A phenotype continuum along x can be useful as a **theoretical witness**, but the real Aquilegia candidate set appears to be spatially constrained at the measured two-whorl level. That is a warning against treating the entire Cartesian product of morphological parts as biologically accessible, **not** an estimated SLK `Phi`, local path derivative, invasion threshold or fitness map.

**ANTO implication:** ancestry-dependent positional programs may remain phenotypically detectable in tissues that have lost canonical staminode morphology. "An organ returned" cannot be assigned from AN alone; the original staminode sheath, pollen production, and new derived ecological functions are different possible trait endpoints. A duplicated flower developing an unobserved mosaic does not establish hidden conserved native coding modules, heritable ancestral reactivation or gene-flow-independent genetic restoration.

**Functional partner evidence is from separate taxon experiments, not these F2 plants:** Walker-Larsen & Harder 2001 `Penstemon` staminode removals found bee-dependent nectar barrier and stigma lever functions; Wen et al. 2024 `Parnassia` experiments found glossy staminodes attracting mutualists **and** florivores, with observed removal effects on seed production. Neither study measured Aquilegia F2 genotypes' ecological fitness. Source-based floral comparisons cannot be multiplied into a single "three-stage empirical demonstration."

### A truly falsifiable developmental/ecological bridge

**Constrained architectural route hypothesis:** In the same molecularly characterized staminode-loss lineage, whorl-specific developmental expression domains restrict which combinations of gamete-producing AN and lateral protective/guide/lever architecture can appear. Changing that regulatory boundary can permit otherwise rare floral combinations; only then can partner-dependent mechanical and pollen functions be independently tested for selective benefit.

Specifically, before any evolutionary claim, experimental researchers would need to trace **the same organ** across spatial whorl identity, verified anther pollen fertility, fused-filament structure, actual partner contact/pollen delivery and full seed/paternity outcome, as well as genotype-regulatory programs of the very same lines and progeny. Relevant author-cited candidates in Aquilegia include AqAP3-2 (anther-related knockdown), polarity-related YABBY homologs, and organ-adhesion candidates; these are **prior reported biological candidates**, not loci newly associated by the present data. Manipulations and field samples require proper approval, and none have been run in this project.

A different scale is represented by [aza3's actual Cirsium head-orientation × bract-posture combinations](https://github.com/zuizui0223/aza3/blob/main/docs/CIRSIUM_TWO_RADIATIONS_HEAD_GEOMETRY_MOSAIC_20261021.md): across 63 North American Cirsium labels all four coarse trait combinations exist, whereas within a single Aquilegia F2 flower two homologous-whorl organ identity traits show almost complete nestedness. **These are nonhomologous anatomical measurements at different biological grains**, not a direct comparison or evidence that Cirsium is genetically more evolvable. Together they caution against either "all traits are fixed in one package" or "all parts can be freely reassembled."

## Source-replay and evidence ceiling

- Real source morphology parser: `analysis/audit_aquilegia_f2_partial_reassembly_v1.py`.
- Within-plant two-flower parser: `analysis/audit_aquilegia_f2_within_plant_variability_v2.py`.
- **v3 positional independent scorer:** `analysis/audit_aquilegia_f2_positional_nestedness_v3.py`.
- **Independent raw-source JS receipt:** `results/aquilegia_f2_positional_nestedness_source_v3.json`.
- **Eight unit tests**, including original-source counts, alternate LE thresholds, genotype-level first flower, and deliberate violations: `tests/test_aquilegia_f2_positional_nestedness_v3.py`.
- Replayed with other source-derived v1/v2 analyses in `.github/workflows/aquilegia-f2-staminode-real-organ-v1.yml`.

**Supported:** actual constrained morphological assembly and within-genotype incomplete expression in F2. **Unmeasured:** true pollination fitness of those combinations, preserved allele-level functional afterlife, trait reconstruction in natural ancestral lineage, environmental selection dynamics and evolutionary fixation. Distinguish publisher authors' original conclusions from our conditional re-enumeration.
