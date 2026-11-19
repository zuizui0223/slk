# SLK × ANTO v4 — a genuine same-F2-plant morphology ↔ deposited DNA sample bridge

**21 October 2026 | Original Johns et al. 2024 Aquilegia F2 phenotypes × ENA public run metadata | metadata join validated, not DNA genotyping or a newly discovered genetic mechanism.**

## Scientific advance: the phenotype–sequencing identity bridge exists

Our source-verified v1–v3 organ analyses found morphologically intermediate F2 states with positional nestedness, but could not assert an individual-level genotype from a phenotype-only supplementary CSV. The paper's Data Availability statement deposits genomic skim-sequencing under **NCBI BioProject PRJNA1089234**. Querying the public **EMBL-EBI ENA `read_run` metadata**, rather than downloading reads, reveals an explicit `F2.<plant number>` sample alias shared with the article's original Supplemental Material 3 phenotype `plant` column.

This is a substantial feasibility improvement: every one of the **231 scored F2 plant identifiers** has at least one matching original sequence-run alias. In principle, a source-controlled **same-F2-individual marker genotype × organ morphology** analysis is possible once actual allele calls and quality-control outcomes have been recovered. **Presence of a SRA alias is not a usable genotype nor a verified 231-individual successful mapping set.**

### Metadata joins directly verified

| Item | Public source-matched state |
|---|---:|
| Original publisher phenotyped F2 plants | **231** |
| F2 plant IDs with ≥1 same-number ENA `sample_alias` | **231/231** |
| ENA `read_run` metadata rows for this BioProject | **341** |
| F2-labelled source run rows | **340** |
| Unique canonical F2 number prefixes | **336** |
| Canonical F2 number prefixes without scored phenotypes | **105** |
| Canonical F2 numbers represented by >1 run | **4**: 16, 19, 36, 50 |
| Of those four duplicate-number groups also represented in the 231 phenotyped plants | **3**: 16, 36, 50 |
| Combined listed compressed FASTQ bytes, all 341 runs | **78,243,926,288 bytes (~78.24 GB)** |
| Listed compressed FASTQ bytes of runs whose F2 numbers appear in the 231 phenotype plants | **49,374,744,454 bytes (~49.37 GB)** |
| FASTQ file entries in this API snapshot | **681** |
| Raw FASTQ downloaded or SNP called in this extension | **0** |

**ENA source:** [read_run metadata at BioProject PRJNA1089234](https://www.ebi.ac.uk/ena/portal/api/filereport?accession=PRJNA1089234&result=read_run&fields=run_accession,sample_accession,sample_alias,experiment_accession,experiment_alias,library_name,fastq_bytes&format=tsv) (queried 21 Oct 2026). The authors' paper DOI is [10.1186/s13227-024-00225-3](https://doi.org/10.1186/s13227-024-00225-3). The ENA run metadata were frozen locally as a **public metadata-only JSON snapshot**, not downloaded sequencing data.

**Parent plant ID caveat:** a run alias `F2.16_1` or `F2.16_2` may indicate repeated sequencing, library preparation or non-identical sample labels; the ENA records have distinct `SAMN` BioSample accessions. The four number-colliding groups (16,19,36,50) **must not be silently merged as technical replicates or counted as extra unique genotypes**. Preserve exact sample aliases, BioSample IDs and SRR accessions until actual read/genotype concordance is checked and the source authors' allocation is reconciled.

### The current genetics limit in the original article

Johns et al. 2024 published a **polygenic QTL analysis** with **nine independent QTL** and 44–53% phenotypic variation explained under their reported models, using **329 successfully genotyped of 334 individuals considered for the genetic map** (article Results; methods report allele bins/marker filtering). The ENA's 336 canonical numerical F2 aliases and the 329 paper-quality mapping set are **different quantities**. The deposited run list does not certify per-run read depth, per-individual successful genotype imputation or inclusion in the authors' final QTL model. Without the original processed genetic map/marker calls (the paper advertises a Github code repository but its presently visible public content does not provide an inspectable QTL genotype matrix), no new QTL estimates are reported.

### Biological result this metadata join could actually test

A genuinely joined morphology–genotype study could compare F2 plants that all share the same spatial ancestry of target whorls yet differ in expression of organ subtraits, rather than treating eye-visible floral morphology as genomic competence itself. The published F2 original phenotypes demonstrate two properties:

1. **Strong within-flower positional constraint:** `AN_inner=1` without `AN_outer=1` was not observed in 400 flowers; `LE_outer≥2` without `LE_inner≥2` occurred only in one flower. The two rules jointly held in 399/400 flowers and 230/231 genotype-representative first flowers.
2. **Incomplete within-genotype visible expression:** among 169 plants with two flowers, the AN+LE+FU composite state appeared only in one of the flowers in 39 plants; after a negative first flower, 16/108 showed it in the second.

Both are actual **F2 developmental morphology**, not named functional loci. Existing positional QTL intervals, floral polarity-gene candidates and B-class organ identity evidence from the original papers make locus-level genotype re-analysis biologically meaningful. The falsifiable next question is whether **shared and whorl-specific genotypes predict partial organ reassembly beyond a flower's visible state**, and whether genuine segregating alleles constrain both positional containment rules. This does **not** test SLK ecological payoff until pollen fertility, mechanical guide/protection and complete reproductive outcome are measured on that same source population.

### Efficient and honest next source step, not an implicit 49 GB download

1. **Try to retrieve the source authors' already processed F2 R/qtl genotype/bin matrix, marker map, reference version and plant-ID crosswalk**. This is preferable to raw-genome reprocessing and would support actual AN/LE/FU loci association after sample QC. An SRA run alias by itself is not a marker matrix.
2. If unavailable, **stage a coverage/mapping pilot of selected uniquely identified F2 samples** against the appropriate `Aquilegia` reference and authors' candidate interval definitions. Record `_1/_2` BioSample ambiguities separately, verify accession read depth and variant concordance before combining, then scale based on evidence rather than retrieving all ~49 GB immediately.
3. Re-analyse per-plant phenotypes using both flowers as nested observations (not independent genotypes), explicit QTL genotype markers and uncertainty. Confirm published QTL effects before testing a novel developmental constraint; label previous authors' results as prior art.
4. Only then connect molecular paths to the actual **mechanical/pollen** functions of the organ under ecological partner manipulations; currently these functions were experimentally quantified in DIFFERENT genera (*Penstemon*, *Parnassia*), so a joint SLK–ANTO adaptive-genetic result is not yet established.

**No new genomic analysis, functional restoration, field phenotype manipulation or genetic locus-to-phenotype effect is claimed.** All *Cirsium* empirical work stays exclusively in aza3.

## Reproducible metadata ownership

- Published phenotype source and v1–v3 architecture: `data/external/johns2024_aquilegia_f2_phenotypes_source.csv` and `analysis/audit_aquilegia_f2_positional_nestedness_v3.py`.
- Original ENA snapshot with exact SRR, SAMN, sample alias, library name and byte length: `data/external/aquilegia_f2_PRJNA1089234_ena_run_metadata_v4.json`.
- Typed source-aware sample/phenotype bridge: `analysis/audit_aquilegia_f2_ena_identity_match_v4.py`.
- Dedicated source collision/identity negative tests: `tests/test_aquilegia_f2_ena_identity_match_v4.py`.
- Independent JavaScript 231-ID join receipt: `results/aquilegia_f2_ena_phenotype_sample_link_independent_JS_v4.json`.
- GitHub CI: `.github/workflows/aquilegia-f2-staminode-real-organ-v1.yml`, checks all 231 source ID↔SRR alias pairs, duplicate BioSample safeguards, source bytes and biological claim limits.
