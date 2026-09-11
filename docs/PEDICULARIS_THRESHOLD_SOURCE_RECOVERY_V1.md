# Pedicularis threshold-source recovery v1

Status: **PRIMARY-SOURCE AUDIT COMPLETE FOR CURRENT REGISTERED Qz/Qp/Qg THRESHOLDS**.

This audit asks which of the 36 numeric Pedicularis qualification thresholds can already be fixed from the registered design or primary literature, and which still require independent calibration, biological-relevance choices, or prospective power/precision work.

The rule is conservative: historical sample sizes, non-significant P-values, and effects from a different intervention are evidence anchors, not automatically valid confirmatory thresholds.

## Primary-source anchors

### Sun, Armbruster & Huang 2016 — `P. rex` geographic conflict

DOI `10.1093/aob/mcw097`.

Recovered scale information:

```text
14 populations
16-36 plants per population; mean 21.38 +/- 1.04
two flowers measured per plant for morphology
digital caliper precision = 0.1 mm
pollen loads: 299 plants / 598 flowers
seed outcomes: commonly six capsules from 20 plants per population
initial seed set: 31.10-48.53% across 12 populations
seed predation: 0.80-27.42% across populations.
```

This is strong evidence for conflict reality and field feasibility. It does not supply the variance structure of the new randomized Qz/Qp/Qg estimands.

### Sun & Huang 2015 — water-defence experiment

DOI `10.1093/aobpla/plv019`.

Recovered design/effect-scale information:

```text
six populations
40-60 individuals per population; mean 52.46
20-30 drained individuals per population
>=6 capsules counted per individual
mean ovules per flower = 25.96 +/- 0.58, N=120
capsules mature about 3 weeks after anthesis.
```

Published treatment coefficients include:

```text
pollinator visit beta =  0.012, P=0.958
initial seed-set beta =  0.001, P=0.906
final seed-set beta   =  0.025, P<0.0001
seed-predation beta   = -0.072, P<0.0001.
```

Predation increased after water drainage in five of six populations. This establishes that the water-defence axis is biologically consequential and preferentially loaded toward antagonist protection. It does not validate the new independent-predator Qg device, and its non-significant pollination effects are not equivalence margins.

### Huang, Wang & Sun 2016 — congeneric corolla manipulation

DOI `10.1111/jipb.12460`.

Recovered manipulation information:

```text
P. tricolor
72 shortened + 72 unmanipulated flowers
12 flowering individuals
corolla shortening by bending tubes and fixing them with clear sticky tape
first arrivals 89 vs 86
visits/census 2.70 +/- 0.34 vs 2.61 +/- 0.37
seed set 0.45 +/- 0.022 vs 0.48 +/- 0.018.
```

This establishes a non-destructive manipulation precedent and a feasibility scale. It does not establish acceptable off-target geometry or water effects in `P. rex`.

## Freeze-readiness classes

```text
FREEZE_NOW_DESIGN
    fixed by an already registered downstream design requirement.

POWER_PRECISION_REQUIRED
    sample floor must come from prospective power or CI-width planning using
    external/calibration variance.

CALIBRATION_REQUIRED
    tolerance or timing bound depends on focal measurement error, natural history,
    sham variation, or method-specific contamination.

BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION
    minimum useful treatment effect needs a predeclared biological meaning plus
    variance/effect-scale information.
```

## The one numeric threshold that can be fixed now

```text
Qz.min_z_levels = 5
```

Reason: the registered corrected V2 causal surface requires at least five informative realized-z levels, and Stage P0 exists to qualify the manipulation for that exact surface. Fewer than five usable levels therefore cannot enter the registered same-system experiment even if a treatment effect is statistically detectable.

This is a design floor, not an empirical effect-size claim. The machine-readable source preset is `data/PEDICULARIS_THRESHOLD_PRESET_V1.json`.

## Qz classification

| Threshold | Readiness | Current anchor | Remaining need |
|---|---|---|---|
| `min_z_levels` | **FREEZE_NOW_DESIGN = 5** | registered V2 surface | none beyond version lock |
| `min_flowers_per_level` | POWER_PRECISION_REQUIRED | congener 72+72 flowers; historical scale only | cluster-bootstrap precision target |
| `min_plants` | POWER_PRECISION_REQUIRED | P. rex commonly sampled at tens of plants/population | independent-plant precision target |
| `min_adjacent_exsertion_gap` | CALIBRATION_REQUIRED | component measurements had 0.1-mm precision; z is a ratio | propagated z error + useful dynamic range |
| `max_opening_width_relative_change` | CALIBRATION_REQUIRED | opening measured historically | repeatability + negligible-change margin |
| `max_tube_diameter_relative_change` | CALIBRATION_REQUIRED | tube diameter measured historically | same |
| `max_bract_height_relative_change` | CALIBRATION_REQUIRED | bract height measured historically | same |
| `max_lower_lip_angle_change_deg` | CALIBRATION_REQUIRED | no equivalence bound recovered | repeatability + negligible-change margin |
| `max_water_depth_change` | CALIBRATION_REQUIRED | water-y function established | water-depth repeatability + y-preservation margin |
| `max_flower_orientation_change_deg` | CALIBRATION_REQUIRED | no equivalence bound recovered | repeatability + negligible-change margin |
| `max_mechanical_damage_rate` | CALIBRATION_REQUIRED | tape manipulation precedent only | P. rex sham/handling calibration |

## Qp classification

| Threshold | Readiness | Current anchor | Remaining need |
|---|---|---|---|
| `min_paired_plants` | POWER_PRECISION_REQUIRED | historical studies used tens of plants | paired-plant power/precision |
| `min_flowers_per_treatment` | POWER_PRECISION_REQUIRED | repeated flowers/capsules historically feasible | within-plant precision target |
| `min_pollen_grain_delta` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | historical mean pollen load about 12.53 grains/stigma | useful increase + calibration variance |
| `min_initial_seed_set_delta` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | historical initial seed set 31.10-48.53% | useful reduction in pollen limitation + variance |
| `max_early_predator_attack_difference` | CALIBRATION_REQUIRED | no equivalence margin recovered | attack-score repeatability + margin |
| `max_z_relative_change` | CALIBRATION_REQUIRED | z defined observationally | sham repeatability on z scale |
| `max_bract_height_relative_change` | CALIBRATION_REQUIRED | bract height measured historically | repeatability + margin |
| `max_opening_width_relative_change` | CALIBRATION_REQUIRED | opening measured historically | repeatability + margin |
| `max_water_depth_change` | CALIBRATION_REQUIRED | water-y must remain fixed | water-depth repeatability + y-preservation margin |
| `max_mechanical_damage_rate` | CALIBRATION_REQUIRED | no supplementation-handling ceiling | sham-handling calibration |

## Qg classification

| Threshold | Readiness | Current anchor | Remaining need |
|---|---|---|---|
| method `min_paired_plants` | POWER_PRECISION_REQUIRED | 2015 used 40-60 individuals/population, different design | paired V3 precision/power |
| method `min_flowers_per_treatment` | POWER_PRECISION_REQUIRED | >=6 capsules/individual historically | V3 method-gate precision |
| `min_hours_after_anthesis_before_barrier` | CALIBRATION_REQUIRED | predators oviposit after flowers open | focal pollination-window timing calibration |
| `max_hours_after_anthesis_before_barrier` | CALIBRATION_REQUIRED | oviposition precedes ovary swelling | focal pre-swelling/attack-window calibration |
| predator `min_paired_plants` | POWER_PRECISION_REQUIRED | historical scale only | effect/selectivity power or precision |
| predator `min_flowers_per_treatment` | POWER_PRECISION_REQUIRED | historical scale only | effect/selectivity precision |
| `min_early_attack_reduction` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | independent device is new | useful suppression + variance |
| `min_predation_fraction_reduction` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | water treatment changed predation strongly, but differs from Qg | useful independent-device effect + context calibration |
| `min_final_seed_set_gain` | BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION | water treatment improved final seed set | useful gain + calibration |
| `max_initial_seed_set_difference` | CALIBRATION_REQUIRED | old water treatment had no detected effect | prospective equivalence margin |
| `max_pollen_grain_relative_change` | CALIBRATION_REQUIRED | no direct bound recovered | repeatability + margin |
| `max_pollinator_visit_relative_change` | CALIBRATION_REQUIRED | old water treatment beta 0.012, P=0.958 | repeatability + prospective equivalence margin |
| `max_z_relative_change` | CALIBRATION_REQUIRED | no barrier-specific bound | barrier-sham z repeatability |
| `max_water_depth_change` | CALIBRATION_REQUIRED | water-y must remain fixed | barrier effect on water-depth calibration |
| `max_damage_rate_difference` | CALIBRATION_REQUIRED | no barrier-specific bound | barrier/sham damage calibration |

## Net result across all 36 numeric thresholds

```text
FREEZE_NOW_DESIGN                         1
POWER_PRECISION_REQUIRED                  8
BIOLOGICAL_RELEVANCE_PLUS_CALIBRATION     5
CALIBRATION_REQUIRED                     22
TOTAL                                    36
```

So 35 values remain unresolved, but this does **not** mean 35 independent pilot studies. Most can be supplied by a compact set of reusable calibration blocks.

## Minimal calibration package

```text
C1 morphology / manipulation repeatability
   z, opening, tube diameter, bract height, lip angle, orientation, damage

C2 water-y repeatability
   water depth under repeated measurement and sham handling

C3 reproductive / consumer baseline variance
   pollen grains, initial seed set, early attack, predation, final seed set,
   pollinator visitation at the plant-cluster scale

C4 natural-history timing
   end of effective pollination window and onset of ovary swelling / predator-access window.
```

C1 can inform many Qz/Qp/Qg off-target margins simultaneously. C2 handles the shared requirement that water-y remain fixed. C3 supplies the variance needed for target-effect and sample-floor calculations. C4 supplies both Qg timing bounds.

## Why historical sample sizes remain anchors, not floors

The new gates use different estimators from the historical studies:

```text
Qz = plant-cluster bootstrap of z separation + maximum off-target shifts
Qp = paired-plant positive-effect + contamination bounds
Qg = paired-plant timed method + simultaneous efficacy/selectivity gates.
```

Therefore `historical n != confirmatory minimum n`. Published sample sizes can define feasible scenarios but cannot replace prospective precision/power planning.

## Why historical P-values remain evidence, not equivalence

```text
P > 0.05
!= biologically negligible effect
!= prospective equivalence margin.
```

This is especially important for the 2015 water experiment: its near-zero pollinator treatment coefficient is useful biological background but cannot define `max_pollinator_visit_relative_change` for a new exclusion device.

## Immediate source preset

The following source-independent design value is registered now:

```text
Qz.min_z_levels = 5
threshold_class = design_floor
source_type = combined_predeclared
source_reference = registered V2 surface + SLK field-execution policy
```

`combined_predeclared` is already accepted by the threshold validator and avoids mislabelling a design constraint as a recovered biological effect.

All other numeric values remain blocked by the readiness class above.

## Machine-readable companions

```text
data/PEDICULARIS_THRESHOLD_SOURCE_LEDGER_V1.csv
data/PEDICULARIS_THRESHOLD_PRESET_V1.json
```
