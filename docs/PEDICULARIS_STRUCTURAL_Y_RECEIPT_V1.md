# Pedicularis structural-y calibration receipt v1

Status: **PROSPECTIVE / Y-CAL ANALYSIS CONTRACT / NO Y2-Y3 OR G3-G5 CLAIM**.

## Purpose

This layer turns the registered 36-plant Y-CAL cohort into an auditable answer to two narrow questions:

```text
Y0: is water-retention performance a repeatable, resolved among-plant phenotype?
Y1: how strongly is that phenotype coupled to the registered exsertion coordinate z?
```

It does not establish preferential functional loading (Y2), intervention/natural-experiment identification (Y3), D0 qualification, R, K or Phi.

## Primary-y anti-selection rule

Before Y-CAL outcomes are opened, freeze one primary structural-y metric from:

```text
RETENTION_MEAN_MAX_ML
RETENTION_MEAN_DEPTH_MM
RETENTION_MEAN_HALF_LIFE_MIN
RETENTION_MEAN_PROTECTED_FRACTION
```

using `data/PEDICULARIS_STRUCTURAL_Y_METRIC_FREEZE_TEMPLATE_V1.json`.

The primary metric may not be selected because it has the smallest pilot variance, the largest observed LOW/HIGH gap, or the strongest downstream fitness association. Those are outcome-dependent selection rules and would make the structural-y claim post hoc.

## Registered Y-CAL input

```text
36 independent plants
3 Y-CAL flowers per plant
2 repeated retention trials per flower
confirmatory_eligible = false
```

The plant is the independent unit. Flower means estimate within-plant variation. Trial pairs estimate measurement error.

## Variance decomposition

For the frozen primary y metric, first average the two repeat trials within each flower. With three flower means per plant, use the balanced one-way random-effects decomposition:

```text
sigma_between^2 = max[(MS_between - MS_within) / 3, 0]
sigma_within^2  = MS_within
ICC              = sigma_between^2 / (sigma_between^2 + sigma_within^2).
```

Separately estimate repeat-trial measurement error as:

```text
measurement_error_SD = SD(trial1 - trial2) / sqrt(2).
```

Only complete 3-flower plants contribute to these quantities. Trial differences from an incomplete plant are discarded together with that plant, preventing partial-plant leakage into the error estimate.

## LOW-Y / HIGH-Y recruitment bands

On the 36 plant means:

```text
LOW-Y ceiling  = Y-CAL 1/3 quantile
HIGH-Y floor   = Y-CAL 2/3 quantile.
```

The bands are usable only if the already registered dynamic-range rule passes:

```text
median(HIGH-Y) - median(LOW-Y)
    >= max(
         between-plant SD(y),
         2 * measurement-error SD(y)
       ).
```

This rule is intentionally stricter than merely finding a statistically non-zero variance. It requires the prospective phenotype strata to be separated by at least one resolved among-plant scale and by at least twice the repeat-trial error scale.

If it fails, do not move the tertile cutpoints after seeing the data. The population-season is unresolved for the registered structural-y comparison; use a new prospectively registered population/protocol instead.

## z-y coupling audit

Compute plant-level mean z and primary y, then report:

```text
cov(z,y)
cor(z,y).
```

This is an audit, not a universal exclusion threshold. Strong coupling can lower the biological claim from near-independent modules to partial functional modularity, but it does not by itself erase a repeatable second functional phenotype.

If correlation cannot be estimated because one coordinate has no resolved variation, Y1 remains unresolved and D0-CAL recruitment is not authorized under v1.

## Receipt statuses

```text
STRUCTURAL_Y_CALIBRATION_INCOMPLETE
    fewer than 36 complete independent Y-CAL plants.

STRUCTURAL_Y_CALIBRATION_COMPLETE_RANGE_UNRESOLVED
    36 complete plants but the frozen dynamic-range rule fails.

STRUCTURAL_Y_RANGE_QUALIFIED_Y1_UNRESOLVED
    dynamic range passes but z-y coupling cannot be audited.

STRUCTURAL_Y_Y0_RANGE_QUALIFIED_Y1_AUDITED
    36 complete plants, dynamic range passes, and z-y coupling is estimable.
```

Only the final status authorizes recruitment of a **disjoint** D0-CAL cohort using the frozen LOW-Y/HIGH-Y bands.

## Claim ceiling

Even the strongest v1 receipt means only:

```text
repeatable/resolved structural-y range
+ audited x/y coupling
+ prospectively frozen D0-CAL recruitment bands.
```

It does not yet mean:

```text
Y2 preferential loading
Y3 causal/exogenous structural-y variation
trait-level dimensional release
D0 qualified pre-cost comparison
G3 R
G4 K
G5 Phi.
```

Those remain separate downstream gates.

## Execution

```bash
python scripts/summarize_pedicularis_structural_y_calibration.py \
  PEDICULARIS_Y_CAL_FIELD_V1.csv \
  PEDICULARIS_STRUCTURAL_Y_METRIC_FREEZE_V1.json \
  --output PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1.json
```

The metric-freeze file must be committed before Y-CAL outcomes are opened. The resulting receipt may freeze LOW/HIGH recruitment for new D0-CAL plants, but Y-CAL plants themselves remain permanently confirmatory-ineligible.
