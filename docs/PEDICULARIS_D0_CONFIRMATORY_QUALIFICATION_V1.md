# Pedicularis D0 independent confirmatory qualification v1

Status: **PROSPECTIVE / D0 QUALIFICATION ONLY / G3-G5 EFFECT DATA REMAIN UNOPENED**.

## 1. Purpose

Calibration can tell us how variable the measurements are, how large the confirmatory experiment must be, and what biological margins should be frozen. It cannot itself certify the `D0` comparator used to decompose architecture value.

This layer therefore introduces a new independent partition:

```text
PED_D0_QUAL_CONFIRM_V1
```

whose only job is to adjudicate:

```text
D0-Q1 geometry / z preservation
D0-Q2 benefit matching to natural D
D0-Q3 pollination-facing equivalence
D0-Q4 retention-channel fidelity
D0-Q5 apparatus burden accounting
D0-Q6 common time horizon.
```

These units are explicitly barred from the later G3-G5 effect experiment.

## 2. Inputs frozen before outcomes

A D0 confirmatory layout may be generated only after the following exist:

```text
1. structural-y Y0/Y1 receipt with frozen LOW/HIGH recruitment bands;
2. frozen D0 biological margin manifest;
3. independent D0-CAL variance receipt;
4. compiled precision input;
5. precision planner output with provenance;
6. D0 confirmatory analysis freeze.
```

The confirmatory analysis freeze fixes:

```text
context / population / season
primary y metric
fitness scale / time horizon
Q5 burden route
bootstrap seed and reps
90% equivalence CI
one-sided 5% superiority rule
95% burden-precision CI
randomization/layout contract.
```

No margin, endpoint, route, or sample-size floor can be changed after confirmatory outcomes are opened.

## 3. Precision provenance

`plan_pedicularis_y_d0_precision.py` now carries forward the compiler's `input_provenance` into the precision plan.

Therefore the D0 confirmatory layer checks that the required sample size was generated for the same:

```text
population_id
season_id
fitness_scale_id
time_horizon_id
confirmatory_dataset_id
q5_route
margin_freeze_commit.
```

A sample size computed for another population, margin version, or Q5 burden route is rejected rather than silently reused.

## 4. Confirmatory allocation

The field layout is generated from the incompatible precision maxima without collapsing their units.

Let:

```text
n_pair  = maximum inflated paired-plants requirement
n_total = maximum inflated total-plants requirement
n_group = maximum inflated plants-per-group requirement.
```

Then:

```text
N_LOW  = max(n_pair, n_total, n_group)
N_HIGH = n_group.
```

Each LOW-Y plant receives randomized within-plant flowers:

```text
S_QUAL
SHAM_QUAL
D0_QUAL.
```

Each HIGH-Y plant contributes:

```text
D_QUAL.
```

The generated rows carry:

```text
analysis_partition = D0_CONFIRMATORY_QUALIFICATION_ONLY
d0_qualification_eligible = true
g3_g5_eligible = false.
```

Changing `g3_g5_eligible` to true is a protocol violation, not a promotion.

## 5. Structural-y band recheck

New confirmatory plants must still satisfy the Y-CAL state definitions on the same frozen primary y metric:

```text
LOW-Y natural S state <= frozen LOW-Y ceiling
HIGH-Y natural D state >= frozen HIGH-Y floor.
```

This prevents recruitment drift from turning the nominal LOW/HIGH comparison into an unregistered intermediate-state comparison.

## 6. Endpoint adjudication

### D0-Q1 — z and geometry preservation

Use paired LOW-Y differences:

```text
D0_QUAL - SHAM_QUAL
```

for:

```text
exsertion z
corolla opening
stigma position
orientation
mechanical damage.
```

Each 90% bootstrap CI must lie wholly within its independently frozen equivalence/contamination margin.

### D0-Q2 — functional benefit matching

Compare independent groups:

```text
LOW-Y D0_QUAL
versus
HIGH-Y D_QUAL
```

for:

```text
retained volume
retention duration
protected fraction
early attack / protection outcome.
```

Each D0-minus-D 90% bootstrap CI must lie wholly inside its frozen equivalence margin.

Q2 is the central pre-cost-comparator requirement. If it fails, `D0` is not qualified even if every off-target effect is small.

### D0-Q3 — pollination-facing equivalence

Use paired:

```text
D0_QUAL - SHAM_QUAL
```

for:

```text
visit rate
pollen receipt
initial seed set.
```

Again, non-significance is not enough: every 90% CI must fit inside the frozen margin.

### D0-Q4 — antagonist-channel fidelity

Two contrasts are required:

```text
wet protection effect:
    SHAM_QUAL - D0_QUAL on early attack
    -> one-sided 5% bootstrap lower bound > frozen minimum useful effect

dry physical-device residual:
    SHAM_QUAL - S_QUAL on early attack
    -> 90% CI inside the frozen contamination bound.
```

This is the confirmatory version of the earlier correction that SHAM is the registered **non-retaining physical-device control**. The dry residual is therefore `SHAM-S`, not an invented dry-device-minus-SHAM contrast.

### D0-Q5 — apparatus burden

Two prospectively distinct routes remain.

#### Negligible-burden route

```text
S_QUAL - SHAM_QUAL
```

must have its 90% CI within the frozen viable-seed equivalence margin.

#### Measured-burden adjustment route

The same paired burden contrast is estimated rather than required to be zero. Its 95% bootstrap CI must have half-width no larger than the frozen downstream decision-resolution target.

Passing this route yields a burden estimate/interval that the later K analysis must carry explicitly.

### D0-Q6 — common horizon

All rows must carry the same registered `time_horizon_id` used by the G1-G5 chain. There is no approximate matching rule for Q6.

## 7. Final statuses

```text
D0_FULLY_QUALIFIED
    Q1-Q6 all pass and structural-y band membership remains valid.

D0_FUNCTION_MATCH_ONLY
    Q2 benefit matching passes, but at least one geometry, pollination,
    channel-fidelity or burden gate fails.

D0_NOT_QUALIFIED
    Q2 benefit matching itself fails.
```

`D0_QUALIFIED_WITH_BOUNDED_BURDEN` remains reserved for a future explicit bounded-burden implementation. It is not silently emitted by v1.

## 8. Critical firewall

A `D0_FULLY_QUALIFIED` receipt changes the experimental programme from:

```text
pre-cost comparator concept exists
```

to:

```text
pre-cost comparator has passed an independent biological qualification test.
```

It still does **not** estimate:

```text
R
K
Phi.
```

Those quantities require a new independent G3-G5 experiment with prospectively registered S/D0/D worldlines.

This separation prevents the experiment used to decide whether D0 is a valid comparator from also supplying the payoff estimate whose interpretation depends on D0 having passed.

## 9. Execution

Generate layout:

```bash
python scripts/generate_pedicularis_d0_confirmatory_layout.py \
  PEDICULARIS_Y_D0_PRECISION_PLAN_V1.json \
  PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1.json \
  PEDICULARIS_D0_CONFIRMATORY_ANALYSIS_FREEZE_V1.json \
  --randomization-seed <frozen-seed> \
  --output-dir <D0-qualification-directory>
```

After all endpoints mature, adjudicate:

```bash
python scripts/adjudicate_pedicularis_d0_confirmatory.py \
  PEDICULARIS_D0_QUAL_CONFIRM_FIELD_V1.csv \
  PEDICULARIS_D0_MARGIN_FREEZE_V1.json \
  PEDICULARIS_Y_D0_PRECISION_PLAN_V1.json \
  PEDICULARIS_STRUCTURAL_Y_CALIBRATION_RECEIPT_V1.json \
  PEDICULARIS_D0_CONFIRMATORY_ANALYSIS_FREEZE_V1.json \
  --output PEDICULARIS_D0_CONFIRMATORY_RECEIPT_V1.json
```

Only `D0_FULLY_QUALIFIED` unlocks the point-identified G3/G4 decomposition route under the current protocol.
