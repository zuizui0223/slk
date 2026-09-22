# Pedicularis P0 natural-history calibration v1

Status: **PROSPECTIVE / SOURCE-QUALIFICATION CALIBRATION ONLY / P0 NOT YET EXECUTED**.

## 1. Why this calibration exists

Primary-source adjudication leaves three P0 biological minimum-relevance inputs unresolved:

```text
legitimate pollinator visit rate / flower-minute
early attack / oviposition-positive flower prevalence
water-positive flowering-plant prevalence.
```

The literature establishes that all three biological processes are real, but it does not currently provide three directly transportable numeric production values for a fresh population-season.

The clean fallback is therefore a small **independent natural-history calibration** before P0.

This calibration is not P0 itself and is not a confirmatory biological experiment.

## 2. Universal firewall

All calibration units are permanently:

```text
calibration_only = true
p0_decision_eligible = false
downstream_confirmatory_eligible = false.
```

They may not enter:

```text
P0 context adjudication
Qz / Qp / Qg
G1 / G2
Y-CAL / D0-CAL
D0 confirmatory qualification
G3-G5 effect estimation.
```

Their sole use is to supply conservative signal-floor inputs for **P0 effort planning**.

## 3. Registered endpoints

### Pollinator

```text
LEGITIMATE_VISITS_PER_FLOWER_MINUTE
```

Each independent temporal bout records:

```text
observed minutes
simultaneously open focal P. rex flowers
legitimate visits.
```

The point estimate is:

```text
total legitimate visits / total flower-minutes.
```

Bootstrap resampling unit:

```text
independent temporal bout.
```

### Predator

```text
EARLY_ATTACK_OR_OVIPOSITION_POSITIVE_FLOWERS_PER_SCREENED_FLOWERS.
```

This is deliberately the same upstream antagonist endpoint required by P0 and the later Qg method-development logic. Final seed predation is not substituted.

Bootstrap unit:

```text
independent focal flower.
```

### Water state

```text
WATER_POSITIVE_FLOWERING_PLANTS_PER_SCREENED_FLOWERING_PLANTS.
```

The observation definition and weather/timing window must be frozen before calibration outcomes.

Bootstrap unit:

```text
independent flowering plant.
```

## 4. Why the calibration value is a lower signal bound

P0 is a logistical detectability screen, not an effect-size claim. For a fresh calibration route, the registered value passed to P0 is therefore not the raw observed mean.

Instead, prospectively freeze:

```text
ONE_SIDED_INDEPENDENT_UNIT_BOOTSTRAP_LOWER_QUANTILE.
```

For each endpoint:

```text
point estimate
bootstrap distribution across independent units
frozen lower quantile
-> lower signal bound.
```

The calibration qualifies only when **all three lower bounds are strictly positive**.

This rule is conservative in the relevant direction:

```text
more uncertainty
-> smaller lower signal bound
-> more P0 detection effort.
```

It does not widen an equivalence margin or strengthen a biological claim when data are noisy.

## 5. Zero-compatible calibration

If any lower bound equals zero:

```text
P0_RELEVANCE_FRESH_CALIBRATION_ZERO_COMPATIBLE_UNRESOLVED.
```

That result means the current calibration does not establish a positive planning floor at the frozen resolution.

It does **not** mean:

```text
pollinators absent
predators absent
water state absent.
```

Permitted next actions are:

```text
new prospectively frozen calibration wave with greater effort
OR
move to another candidate population-season.
```

The failed wave may not be rescued by changing the bootstrap quantile after looking at outcomes.

## 6. Freeze and field packet

Fill and commit:

```text
data/PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_TEMPLATE_V1.json
```

The freeze registers:

```text
candidate population / season
calibration window
future P0 screen window
sampling floors
sampling-floor rationale
one-sided lower quantile
bootstrap seed / reps
endpoint definitions
all firewalls.
```

Then generate:

```bash
python scripts/generate_pedicularis_p0_natural_history_calibration_packet.py \
  PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_V1.json \
  --output PEDICULARIS_P0_NAT_HIST_CAL_FIELD_V1.csv
```

The generated pollinator rows distinguish:

```text
planned_minutes
observed_minutes.
```

Observed minutes are never prefilled.

## 7. Summarize

After collection:

```bash
python scripts/summarize_pedicularis_p0_natural_history_calibration.py \
  PEDICULARIS_P0_NAT_HIST_CAL_FIELD_V1.csv \
  PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_FREEZE_V1.json \
  --output PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_RECEIPT_V1.json
```

Possible statuses:

```text
P0_RELEVANCE_FRESH_CALIBRATION_QUALIFIED
P0_RELEVANCE_FRESH_CALIBRATION_ZERO_COMPATIBLE_UNRESOLVED
P0_RELEVANCE_FRESH_CALIBRATION_INCOMPLETE.
```

Only the first status supplies recommended minimum-relevance values.

## 8. Handoff to the source-qualification gate

A qualified calibration can populate the relevance-source qualification template:

```bash
python scripts/compile_pedicularis_p0_fresh_calibration_qualification.py \
  PEDICULARIS_P0_NATURAL_HISTORY_CALIBRATION_RECEIPT_V1.json \
  data/PEDICULARIS_P0_RELEVANCE_QUALIFICATION_TEMPLATE_V1.json \
  --output PEDICULARIS_P0_RELEVANCE_QUALIFICATION_FROM_CAL_V1.json
```

The compiler output is intentionally not final. It must still be reviewed, committed and supplied with qualification metadata before:

```text
scripts/validate_pedicularis_p0_relevance_qualification.py
```

can issue:

```text
P0_MINIMUM_RELEVANCE_INPUTS_QUALIFIED.
```

That qualification receipt can then be compiled into the P0 effort-freeze template.

## 9. Full fresh route

The current shortest fully auditable path is:

```text
historical candidate recovery
-> fresh natural-history calibration freeze
-> calibration field packet
-> bootstrap lower-bound receipt
-> relevance-source qualification
-> P0 effort freeze
-> effort planner
-> final P0 freeze
-> fresh P0 context screen
-> calibration/Qz/Qp/Qg programme.
```

## 10. Current claim ceiling

The natural-history calibration may establish conservative planning values only.

```text
NO_P0_PASS
NO_Q_GATE
NO_G1_G2
NO_Y_D0
NO_R_K_PHI.
```


## 11. Completion and missingness audit

Every generated calibration row is registered prospectively. The summary receipt reports:

```text
registered rows
completed pollinator bouts
completed predator flowers
completed water-state plants
incomplete records
reason counts
record-level details.
```

A registered calibration row with a missing required measurement is not silently discarded.

Because fresh calibration values become numeric lower signal bounds for later P0 effort planning, v1 requires:

```text
all registered calibration rows complete
AND
all frozen sampling floors met
```

before the calibration can earn `P0_RELEVANCE_FRESH_CALIBRATION_QUALIFIED`.

Thus extra completed rows do not rescue an incomplete registered row inside the same frozen packet. A new prospectively frozen calibration wave is the clean route if the original packet is incomplete.

The receipt also carries the frozen bootstrap `minimum_valid_fraction`; this is a bootstrap-replicate validity rule, not an outcome-completeness threshold.
