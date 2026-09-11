# Pedicularis threshold-source recovery v1

Status: **PRIMARY-SOURCE AUDIT COMPLETE FOR CURRENT REGISTERED Qz/Qp/Qg THRESHOLDS**.

This document asks a narrower question than the threshold-freeze protocol:

> Which Pedicularis qualification thresholds can already be frozen from the registered theory/design or existing primary literature, and which still require independent calibration, biological-relevance choices, or prospective precision/power work?

The purpose is to minimize unnecessary pilot work without laundering historical sample sizes, P-values, or a different manipulation into confirmatory thresholds.

## 1. Audited primary sources

### Sun, Armbruster & Huang 2016 — `Pedicularis rex` geographic conflict

DOI `10.1093/aob/mcw097`.

Recovered design facts:

```text
14 populations
16-36 plants per population
mean 21.38 +/- 1.04 plants per population
two flowers measured per plant for morphology
digital caliper precision = 0.1 mm
pollen loads measured on 299 plants / 598 flowers
seed production / predation commonly based on six capsules from 20 plants per population
seed predation across populations = 0.80% to 27.42%
initial seed set across 12 populations = 31.10% to 48.53%.
```

The study establishes strong observational conflict geometry and gives useful scales for plant replication and measurement resolution. It does **not** provide the variance structure of the new randomized Qz/Qp/Qg procedures and therefore cannot by itself determine their confirmatory sample floors or equivalence margins.

### Sun & Huang 2015 — cupulate-bract water experiment

DOI `10.1093/aobpla/plv019`.

Recovered design and effect-scale facts:

```text
six populations
40-60 individuals per population, mean 52.46
20-30 individuals per population assigned to water drainage
at least six capsules counted per individual
mean ovules per flower = 25.96 +/- 0.58, N=120
capsules mature about three weeks after anthesis.
```

Published treatment coefficients on the authors' model scale include:

```text
pollinator visit treatment beta = 0.012, P=0.958
initial seed-set treatment beta  = 0.001, P=0.906
final seed-set treatment beta    = 0.025, P<0.0001
seed-predation treatment beta    = -0.072, P<0.0001.
```

Seed predation increased after drainage in five of six populations.

These results strongly support the biological usefulness and preferential loading of the water-defence `y` axis. They are **not** a validation dataset for the corrected independent-predator Qg device. In particular, non-significant pollination effects are not equivalence margins.

### Huang, Wang & Sun 2016 — congeneric corolla manipulation

DOI `10.1111/jipb.12460`.

Recovered manipulation facts:

```text
P. tricolor:
72 shortened flowers + 72 unmanipulated flowers
12 flowering individuals
corolla shortening by bending tubes and fixing with clear sticky tape

first arrivals: 89 shortened vs 86 control
visits/census: 2.70 +/- 0.34 vs 2.61 +/- 0.37
seed set:       0.45 +/- 0.022 vs 0.48 +/- 0.018.
```

This establishes a non-destructive manipulation precedent and an order-of-magnitude field sample scale. It does not establish that the same manipulation has acceptable off-target geometry or water effects in `P. rex`.

## 2. Freeze-readiness classes

Each of the 36 numeric production thresholds is assigned to one of four statuses.

```text
FREEZE_NOW_DESIGN
    A value follows directly from the already registered SLK/SCH design and does not depend
    on empirical treatment outcomes.

POWER_PRECISION_REQUIRED
    A confirmatory sample floor must be chosen prospectively from a power or CI-width target
    using external/calibration variance; historical sample sizes are only scale anchors.

CALIBRATION_REQUIRED
    A tolerance or timing bound depends on focal-method measurement error, natural history,
    or off-target variability that existing sources do not quantify adequately.

BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION
    A minimum useful treatment effect must be chosen prospectively from biological meaning,
    with existing sources usable only as effect-scale anchors when the intervention differs.
```

## 3. One threshold can be frozen now

### Qz `min_z_levels = 5`

This is the sole numeric threshold currently licensed for direct freeze without new calibration.

Reason:

```text
registered V2 causal surface requires >=5 informative realized z levels
and
Stage-P0 exists to qualify a manipulation for that exact downstream surface.
```

Thus fewer than five usable realized levels cannot satisfy the registered same-system programme even if the manipulation is statistically detectable.

This is a **design requirement**, not a recovered biological effect size.

## 4. Why historical sample sizes do not become new sample floors

The primary studies show that Pedicularis field work at roughly tens of plants per population is feasible and that previous analyses used 12-60 individuals depending on question. But the SLK qualification estimators are different:

```text
Qz: plant-cluster bootstrap of minimum adjacent z separation and maximum off-target shifts
Qp: paired-plant bootstrap of positive pollen/seed-set effects plus equivalence-style contamination bounds
Qg: paired-plant bootstrap plus a timed exclusion-method gate and simultaneous efficacy/selectivity criteria.
```

Consequently:

```text
historical n != confirmatory minimum n.
```

The historical n values can seed a feasibility scenario or variance prior, but the production floors must be selected from prospective power or precision calculations for the registered estimands.

## 5. Why historical P-values do not become equivalence margins

The 2015 water experiment found no detected treatment effect on pollinator visitation or initial seed set. This supports the qualitative proposition that water defence can be preferentially loaded toward antagonist protection. It does not imply a maximum acceptable cross-effect for Qg.

Formally:

```text
P > 0.05
!= effect is biologically negligible
!= an equivalence bound
!= a prospective contamination tolerance.
```

The Qp/Qg `max_*` thresholds therefore require independently justified negligible-effect margins and/or measurement-repeatability calibration.

## 6. Qz classification

| Threshold | Status | Best currently available evidence | What is still required |
|---|---|---|---|
| `min_z_levels` | **FREEZE_NOW_DESIGN = 5** | registered V2 requires >=5 informative realized z levels | none beyond version lock |
| `min_flowers_per_level` | POWER_PRECISION_REQUIRED | congener had 72 treated/72 controls; P. rex observational work used repeated flowers/capsules | prospective cluster-bootstrap precision target |
| `min_plants` | POWER_PRECISION_REQUIRED | P. rex studies commonly used tens of plants per population | prospective independent-plant precision target |
| `min_adjacent_exsertion_gap` | CALIBRATION_REQUIRED | P. rex morphology measured at 0.1 mm precision; z is a ratio | propagated z measurement error + minimum useful dynamic range |
| `max_opening_width_relative_change` | CALIBRATION_REQUIRED | opening measured in 2016 | repeated-measurement / sham variability + negligible-change rationale |
| `max_tube_diameter_relative_change` | CALIBRATION_REQUIRED | tube diameter measured in 2016 | same |
| `max_bract_height_relative_change` | CALIBRATION_REQUIRED | bract height measured in 2016 | same |
| `max_lower_lip_angle_change_deg` | CALIBRATION_REQUIRED | no primary-source equivalence margin recovered | focal measurement repeatability + negligible-change rationale |
| `max_water_depth_change` | CALIBRATION_REQUIRED | water function established, not measurement equivalence | focal water-depth repeatability + downstream-y preservation margin |
| `max_flower_orientation_change_deg` | CALIBRATION_REQUIRED | no primary-source equivalence margin recovered | focal repeatability + negligible-change rationale |
| `max_mechanical_damage_rate` | CALIBRATION_REQUIRED | congener tape manipulation shows feasibility, not P. rex damage rate | sham/handling calibration + acceptable failure rate |

## 7. Qp classification

| Threshold | Status | Best currently available evidence | What is still required |
|---|---|---|---|
| `min_paired_plants` | POWER_PRECISION_REQUIRED | P. rex is pollen limited at population level; historical studies use tens of plants | prospective paired-plant precision/power |
| `min_flowers_per_treatment` | POWER_PRECISION_REQUIRED | multiple flowers/capsules per plant were used historically | within-plant precision target after plant floor is set |
| `min_pollen_grain_delta` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | mean historical pollen load ~12.53 grains/stigma and mean ~25.96 ovules/flower | define pollen increase large enough to alter dependence + calibration variance |
| `min_initial_seed_set_delta` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | historical initial seed set 31.10-48.53% across populations | minimum useful suppression of pollen limitation + calibration variance |
| `max_early_predator_attack_difference` | CALIBRATION_REQUIRED | contamination must be near zero; no equivalence margin exists | attack-score repeatability + negligible-change margin |
| `max_z_relative_change` | CALIBRATION_REQUIRED | z measurement defined and source precision known in mm components | sham repeatability on ratio scale |
| `max_bract_height_relative_change` | CALIBRATION_REQUIRED | bract height measured historically | sham repeatability + negligible-change margin |
| `max_opening_width_relative_change` | CALIBRATION_REQUIRED | opening measured historically | same |
| `max_water_depth_change` | CALIBRATION_REQUIRED | water-y must remain fixed | water-depth repeatability + y-preservation margin |
| `max_mechanical_damage_rate` | CALIBRATION_REQUIRED | no P. rex supplementation-handling damage ceiling recovered | sham-handling calibration |

## 8. Qg classification

| Threshold | Status | Best currently available evidence | What is still required |
|---|---|---|---|
| method `min_paired_plants` | POWER_PRECISION_REQUIRED | 2015 water experiment used 40-60 individuals/population but was not paired V3 | prospective paired-plant precision/power |
| method `min_flowers_per_treatment` | POWER_PRECISION_REQUIRED | >=6 capsules/individual in 2015 outcome scoring | precision target for V3 method gate |
| `min_hours_after_anthesis_before_barrier` | CALIBRATION_REQUIRED | predators oviposit after flowers open | focal pollination-window timing calibration |
| `max_hours_after_anthesis_before_barrier` | CALIBRATION_REQUIRED | oviposition precedes ovary swelling | focal pre-swelling / attack-window calibration |
| predator `min_paired_plants` | POWER_PRECISION_REQUIRED | historical scale only | prospective effect/selectivity precision/power |
| predator `min_flowers_per_treatment` | POWER_PRECISION_REQUIRED | historical scale only | same |
| `min_early_attack_reduction` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | independent Qg method is new; old water treatment not equivalent | define useful attack suppression + pilot/calibration variance |
| `min_predation_fraction_reduction` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | water treatment reduced predation strongly and variably among populations | minimum useful effect for independent device + context calibration |
| `min_final_seed_set_gain` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | water treatment improved final seed set | minimum useful gain for independent device + calibration |
| `max_initial_seed_set_difference` | CALIBRATION_REQUIRED | old water treatment had no detected initial-seed-set effect | prospective equivalence margin, not P-value reuse |
| `max_pollen_grain_relative_change` | CALIBRATION_REQUIRED | no direct equivalence bound recovered | pollen measurement repeatability + negligible-change margin |
| `max_pollinator_visit_relative_change` | CALIBRATION_REQUIRED | old water treatment had beta 0.012, P=0.958 | prospective equivalence margin + visitation repeatability |
| `max_z_relative_change` | CALIBRATION_REQUIRED | z ratio defined, no barrier-specific bound | barrier sham repeatability |
| `max_water_depth_change` | CALIBRATION_REQUIRED | water-y must remain fixed | barrier effect on water-depth calibration |
| `max_damage_rate_difference` | CALIBRATION_REQUIRED | no barrier-specific damage bound recovered | barrier/sham handling calibration |

## 9. Net result

Across the 36 numeric production thresholds:

```text
FREEZE_NOW_DESIGN                         1
POWER_PRECISION_REQUIRED                  7
BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION     5
CALIBRATION_REQUIRED                     23
TOTAL                                    36
```

The apparent burden is smaller than “36 independent experiments.” Many of the 23 calibration-required margins can be estimated from the same compact sham/repeatability dataset because geometry, water depth, orientation, damage and measurement repeatability can be recorded together.

Likewise, one natural-history timing calibration can inform both Qg timing bounds.

## 10. Minimal calibration package

A practical pre-qualification calibration package should therefore target four reusable information blocks:

```text
C1 morphology / manipulation repeatability
   -> z, opening, tube diameter, bract height, lip angle, orientation, damage

C2 water-y repeatability
   -> water-depth stability and handling effect

C3 reproductive / consumer baseline variance
   -> pollen grains, initial seed set, early attack, predation, final seed set,
      pollinator visitation at the plant-cluster scale

C4 natural-history timing
   -> end of effective pollination window and onset of ovary swelling / predator access window.
```

These blocks can then feed a prospective power/precision calculation and the biological-relevance decisions for target effects.

## 11. What should not be done next

Do not populate all remaining placeholders simply from the numerical values in the historical papers.

In particular:

```text
2015 water-effect beta != Qg independent-device minimum effect
2015 non-significant pollination effect != Qg equivalence margin
2016 historical n != new paired-bootstrap minimum n
0.1-mm caliper resolution != minimum meaningful z gap without error propagation.
```

## 12. Immediate promotion allowed

The threshold manifest may now prospectively register:

```text
Qz.min_z_levels = 5
threshold_class = design_floor
source_type = biological_relevance / registered_design
```

For compatibility with the current validator's source ontology, encode the source type as `biological_relevance` and cite the registered V2 surface contract / SLK execution policy as the source reference.

All other numeric fields remain blocked pending the information class listed above.

## 13. Machine-readable companion

The row-level audit is stored at:

```text
data/PEDICULARIS_THRESHOLD_SOURCE_LEDGER_V1.csv
```
