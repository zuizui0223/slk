# SLK Pedicularis prospective threshold-freeze protocol v1

Status: **PROSPECTIVE / REQUIRED BEFORE FIELD QUALIFICATION**.

The Pedicularis G2 route is now limited less by theory or software than by one practical requirement: all decision thresholds used by the Qz, Qp and Qg field evaluators must be frozen before confirmatory treatment outcomes are opened.

The current SCH templates deliberately contain `REQUIRED_BEFORE_USE` placeholders. This protocol defines how those placeholders may be replaced without turning the fail-closed design into post-hoc tuning.

## 1. Scope

This protocol covers three SCH qualification configs:

```text
Qz
empirical/architecture/PEDICULARIS_STAGE_P0_CONFIG_TEMPLATE_V1.json

Qp
empirical/architecture/PEDICULARIS_POLLINATION_WEIGHT_CONFIG_TEMPLATE_V1.json

Qg
empirical/architecture/PEDICULARIS_PREDATOR_METHOD_CONFIG_V3.json
```

It does not prescribe universal numeric cutoffs. Numeric values must be justified from independent calibration, prior literature, measurement precision, biological relevance, or prospective power/precision analysis.

## 2. Core anti-peeking rule

For every threshold used to determine whether a gate passes:

```text
threshold source
must be independent of
confirmatory treatment-outcome contrast used to test that threshold.
```

Allowed sources include:

```text
published primary-source measurements
independent pilot/calibration flowers not reused in qualification
measurement-repeatability data collected without opening treatment contrasts
predeclared biological meaningful-effect arguments
prospective power / CI-width calculations based on external or calibration variance.
```

Forbidden sources include:

```text
choosing a cutoff after inspecting the confirmatory treatment effect
shrinking an equivalence margin because the observed effect is convenient
raising a minimum-effect threshold after seeing a large effect
lowering a minimum-effect threshold after seeing a weak effect
changing sample floors after unblinded outcome inspection
redefining a timing window to rescue a failed exclusion method.
```

## 3. Calibration and qualification data must be separated

A single field season may contain both calibration and qualification work, but the units must be disjoint.

```text
CALIBRATION SET
    used to estimate measurement repeatability, natural variability,
    handling artefacts, timing windows or plausible variance.
    never enters the confirmatory Qz/Qp/Qg treatment-effect analysis.

QUALIFICATION SET
    analyzed only after the threshold manifest is frozen.
```

If calibration and qualification occur on the same plant, flowers must be distinct and the plant-level dependence must be declared in the design rationale. Prefer separate plants where feasible.

## 4. Threshold classes

Each required threshold belongs to one of four classes.

### A. design-floor thresholds

Examples:

```text
minimum plants
minimum flowers per treatment / z level
minimum number of z levels.
```

These must be frozen from prospective precision/power requirements and field-capacity constraints before treatment outcomes are opened.

A design floor is not allowed to be reduced merely because fewer successful flowers survived.

### B. target-effect thresholds

Examples:

```text
minimum adjacent realized-exsertion gap
minimum pollen-grain increase
minimum initial-seed-set increase
minimum early-attack reduction
minimum predation-fraction reduction
minimum final-seed-set gain.
```

These represent the smallest effect that would make the intervention biologically useful for the next stage.

They should be derived from one or more of:

```text
external published effect sizes
independent calibration / pilot evidence
biologically meaningful change on the registered reproductive scale
minimum effect needed to create enough dynamic range for the later surface.
```

They may not be chosen simply to ensure statistical significance.

### C. equivalence / off-target tolerances

Examples:

```text
maximum change in corolla opening
tube diameter
bract height
lower-lip angle
flower orientation
water depth
mechanical damage
early predator attack during the P pilot
pollen receipt / pollinator visitation during the G pilot
realized z during P/G pilots.
```

These are upper bounds on contamination. They must represent the largest change still considered biologically negligible for the intended interpretation.

A non-significant difference is not sufficient evidence of equivalence.

### D. natural-history timing thresholds

Examples:

```text
minimum hours after anthesis before predator barrier
maximum hours after anthesis before predator barrier.
```

These may be estimated from a dedicated natural-history timing calibration, because the SCH Stage-G contract explicitly requires the pollination window and pre-ovary-swelling window to be established in the focal system.

The timing calibration must be frozen before the confirmatory predator-method qualification set is analyzed.

## 5. Qz threshold inventory

The following fields must be assigned numeric values before Qz can run:

```text
min_z_levels
min_flowers_per_level
min_plants
min_adjacent_exsertion_gap
max_opening_width_relative_change
max_tube_diameter_relative_change
max_bract_height_relative_change
max_lower_lip_angle_change_deg
max_water_depth_change
max_flower_orientation_change_deg
max_mechanical_damage_rate
```

Recommended justification types:

| field | threshold class | preferred justification |
|---|---|---|
| `min_z_levels` | design floor | minimum support needed for the registered multi-level surface |
| `min_flowers_per_level` | design floor | prospective CI-width / bootstrap stability target |
| `min_plants` | design floor | plant-cluster precision target |
| `min_adjacent_exsertion_gap` | target effect | measurement resolution + biologically useful z separation |
| geometry tolerances | equivalence | repeatability + negligible-change argument |
| `max_water_depth_change` | equivalence | preserve Chapter-2 water-y axis |
| `max_mechanical_damage_rate` | equivalence | handling artefact ceiling |

## 6. Qp threshold inventory

Required fields:

```text
min_paired_plants
min_flowers_per_treatment
min_pollen_grain_delta
min_initial_seed_set_delta
max_early_predator_attack_difference
max_z_relative_change
max_bract_height_relative_change
max_opening_width_relative_change
max_water_depth_change
max_mechanical_damage_rate
```

The two positive-effect thresholds must reflect meaningful reduction of pollen limitation, not merely detectability.

The antagonist and geometry tolerances must be frozen independently of the supplementation effect.

## 7. Qg threshold inventory

### Method/timing block

```text
min_paired_plants
min_flowers_per_treatment
min_hours_after_anthesis_before_barrier
max_hours_after_anthesis_before_barrier
```

The existing boolean requirements remain fixed as `true` unless a new method version is prospectively registered:

```text
require_pollination_window_complete
require_ovary_not_swollen
require_barrier_not_cover_pollinator_entry
require_sham_on_exposed.
```

### Predator-effect/selectivity block

```text
min_paired_plants
min_flowers_per_treatment
min_early_attack_reduction
min_predation_fraction_reduction
min_final_seed_set_gain
max_initial_seed_set_difference
max_pollen_grain_relative_change
max_pollinator_visit_relative_change
max_z_relative_change
max_water_depth_change
max_damage_rate_difference
```

Qg contains both positive efficacy requirements and negative contamination bounds. Both classes must pass; a very effective exclusion device is still invalid if it changes pollination or water-y.

## 8. Precision-based sample-floor rule

SLK does not register one universal `n` for Pedicularis.

Instead the field plan must declare the criterion used to determine `min_plants` and `min_flowers_per_*` before confirmatory outcomes are opened.

Admissible criteria include:

```text
target power for a predeclared minimum effect
or
target maximum CI width around the gate-defining effect / equivalence estimate.
```

Because the source evaluators use plant-cluster or paired-plant bootstrap logic, the primary replication unit for precision planning must be the plant rather than raw flower count.

Flowers increase within-plant precision; they do not replace independent plants.

## 9. Freeze manifest

Before any Qz/Qp/Qg qualification analysis, create one frozen manifest containing every threshold.

Each parameter entry must include:

```text
value
units
threshold_class
biological_rationale
source_type
source_reference
calibration_dataset_id if applicable
frozen_before_confirmatory_outcomes = true
```

The manifest must also record:

```text
population_id
season_id
protocol_version
SCH source commit
SLK source commit
freeze timestamp / commit
who or what generated each threshold rationale.
```

The machine-readable template is:

```text
data/PEDICULARIS_THRESHOLD_FREEZE_TEMPLATE_V1.json
```

## 10. Freeze order

Recommended order:

```text
1. recover measurement protocol and natural-history calibration
2. define biologically negligible off-target margins
3. define minimum useful target effects
4. run prospective precision / power calculation
5. freeze design floors
6. write all values + provenance into the manifest
7. validate the manifest
8. only then open / analyze Qz/Qp/Qg qualification outcomes.
```

This order prevents sample size or margins from being tuned to the realized effect.

## 11. Population-specific thresholds are allowed

Some thresholds, especially natural-history timing and measurement-scale tolerances, may need to be population/season specific.

That is acceptable if they are frozen from independent calibration before the confirmatory qualification set is opened.

Population specificity must not be confused with post-hoc flexibility.

## 12. What may remain common across populations

Where the measurement instrument, scoring protocol, manipulation material and biological interpretation are unchanged, a threshold may be carried forward to later populations.

Any carry-forward decision must be declared before seeing the new population's treatment contrast.

## 13. Qualification failure after freezing

Once the manifest is frozen:

```text
failure means failure for that protocol/context.
```

Allowed responses are:

```text
report the failed gate
change context / population
or prospectively register a new method version.
```

Not allowed:

```text
editing the existing threshold after seeing the result
and rerunning the same data as if prospectively specified.
```

A revised method may use the failed run as development data, but it requires a new independent qualification set.

## 14. Flagship consequence

The threshold-freeze protocol does not promote Pedicularis to G1 or G2.

It changes the status from:

```text
software ready but field decision criteria unspecified
```

to:

```text
field decision criteria have a prospective route to being frozen and audited.
```

The first real empirical promotion still requires actual Qz/Qp/Qg receipts and then the V2 causal surface.

## 15. Current bottleneck

As of the current source state, all three SCH config templates still contain `REQUIRED_BEFORE_USE` placeholders.

Therefore the next executable Pedicularis task is:

```text
collect or recover independent calibration information
-> freeze threshold manifest
-> qualify Qg/Qz/Qp on disjoint confirmatory units.
```
