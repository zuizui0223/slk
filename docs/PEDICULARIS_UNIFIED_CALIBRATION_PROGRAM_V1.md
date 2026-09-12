# Pedicularis unified calibration programme v1

Status: **PROSPECTIVE / CALIBRATION-ONLY / CONFIRMATORY UNOPENED**.

## 1. Purpose

The Pedicularis programme now contains several prospective gates:

```text
upstream Qz / Qp / Qg qualification
-> G1-G2 conflict receipt
-> structural-y qualification
-> D0 qualification
-> G3 R / G4 K / G5 Phi.
```

Each gate needs repeatability, nuisance-effect, natural-history, or variance information. That does **not** imply a separate pilot study for every threshold.

This document defines a shared calibration architecture whose data may inform multiple prospective thresholds while preserving the firewall that calibration units never become confirmatory units.

The objective is:

```text
minimum number of independent calibration modules
with maximum legitimate reuse of measurements,
without reusing calibration observations as confirmatory evidence.
```

## 2. Two kinds of reuse must stay distinct

### A. calibration-data reuse

The same independent calibration plant or flower may inform more than one threshold when the measurements are compatible and all uses are declared prospectively.

Example:

```text
repeated z / opening / orientation measurements on Y-CAL plants
-> Qz measurement repeatability
-> Qp/Qg off-target precision inputs
-> D0-Q1 geometry precision inputs.
```

This is efficient and valid because the unit remains calibration-only everywhere.

### B. numeric-margin reuse

A numeric equivalence margin may be copied from one gate to another only when the endpoint definition, units, biological interpretation, and population/season transport assumptions are all compatible.

Example:

```text
same z coordinate + same relative-change scale + same biological neutrality definition
-> a frozen z off-target margin may be portable across Qp/Qg/D0-Q1.
```

By contrast:

```text
upstream max_water_depth_change
```

asks whether water-y stayed fixed, whereas

```text
D0-Q2 water-depth equivalence
```

asks whether D0 and natural D deliver the same y-mediated protection. The same calibration measurements may help both, but the numeric margins are not automatically interchangeable.

## 3. Universal firewall

All shared calibration modules obey:

```text
CALIBRATION UNIT
    may contribute to multiple threshold derivations / variance estimates
    may not enter Qz/Qp/Qg confirmatory qualification
    may not enter the G1 causal surface
    may not enter G2 L estimation
    may not enter structural D0 confirmatory qualification
    may not enter G3-G5 estimation.
```

If the same plant contributes several calibration flowers, the plant remains the dependence cluster for every downstream variance calculation.

A flower used for a destructive or carryover-producing manipulation is not reused for another incompatible calibration contrast.

## 4. UC1 — morphology and geometry repeatability

Primary registered source:

```text
Y-CAL: 36 independent plants
3 flowers / plant
2 repeated measurements where non-destructive.
```

Core measurements:

```text
flower length
bract height
realized exsertion z
corolla opening width
stigma position
flower orientation
basic mechanical condition
```

Supports:

```text
Qz
  min_adjacent_exsertion_gap precision floor
  opening / bract / orientation off-target calibration

Qp / Qg
  max_z_relative_change
  geometry/damage repeatability where endpoint definitions match

structural-y
  x-y / z-y covariance and measurement independence

D0-Q1
  z / opening / stigma / orientation variance inputs
  geometry-to-function sensitivity design.
```

Numeric-margin portability:

```text
z:          CONDITIONAL
opening:    CONDITIONAL
orientation:CONDITIONAL
stigma:     NEW D0-specific biological sensitivity unless an upstream equivalent is registered.
```

The criterion for portability is biological neutrality, not merely use of the same instrument.

## 5. UC2 — water-y repeatability and structural range

Primary registered source:

```text
Y-CAL retention trials.
```

Measurements:

```text
maximum retained volume
standardized water depth
retention time series / half-life
leakage rate
protected vulnerable-region fraction
repeatability / ICC
natural LOW-Y to HIGH-Y range.
```

Supports:

```text
Qz/Qp/Qg
  calibration of whether manipulations unintentionally alter water-y

structural-y Y0-Y2
  repeatable y variation
  y range
  x-y covariance

D0-Q2
  physical benefit-matching variance
  D0-D retention magnitude/duration/coverage comparisons.
```

Margin reuse rule:

```text
upstream y-preservation margin != D0-Q2 benefit-matching margin by default.
```

The first is a nuisance-preservation bound. The second must be tied to functional protection equivalence.

## 6. UC3 — pollination sensitivity calibration

Purpose:

Map geometry and apparatus perturbations onto the pollination-facing function so equivalence margins are biological rather than variance-derived.

Measurements, on calibration-only flowers:

```text
legitimate visitation / first-arrival / handling
contact geometry where feasible
pollen receipt
initial seed set
registered geometry covariates.
```

Preferred design:

```text
untreated / sham or graded non-destructive perturbations
on flowers distinct from retention-destructive or confirmatory flowers.
```

Supports:

```text
Qp
  baseline variance / meaningful pollen-limitation effects

Qg
  max_pollinator_visit_relative_change
  max_pollen_grain_relative_change
  max_initial_seed_set_difference

D0-Q1
  opening / stigma / orientation -> pollination function sensitivity

D0-Q3
  visitation / pollen / initial-seed equivalence margins.
```

Candidate numeric-margin reuse:

```text
Qg visit margin   -> D0-Q3 visit       CONDITIONAL
Qg pollen margin  -> D0-Q3 pollen      CONDITIONAL
Qg initial-seed margin -> D0-Q3 initial seed CONDITIONAL
```

Reuse requires identical endpoint scaling and the same definition of biologically negligible pollination contamination.

The 2015 water-defence non-significant pollination coefficients remain background only; they do not replace UC3.

## 7. UC4 — antagonist timing and protection sensitivity

Purpose:

Tie retention magnitude/duration to the biological attack window and distinguish a water-mediated protection effect from physical exclusion.

Measurements:

```text
anthesis time
end of effective pollination window
onset / timing of oviposition or early attack
ovary swelling timing
early attack
subsequent predation
viable-seed loss
retention state / duration.
```

Supports:

```text
Qg
  minimum / maximum barrier timing
  useful early-attack / predation reduction

D0-Q2
  duration and coverage functional-equivalence margins
  D0-D protection equivalence

D0-Q4
  wet-channel minimum useful effect
  dry-device physical-exclusion residual.
```

Calibration data may be shared. Numeric margins are portable only when the exact biological contrast is the same.

## 8. UC5 — D0 apparatus and sham calibration

Primary registered source:

```text
D0-CAL: 48 independent plants
LOW-Y: 24 plants with S / SHAM / D0 flowers
HIGH-Y: 24 plants with D / D-drain flowers.
```

Supports:

```text
D0-Q1
  apparatus-induced geometry / damage

D0-Q2
  D0 versus natural-D y matching

D0-Q3
  apparatus pollination contamination

D0-Q4
  wet versus dry channel fidelity

D0-Q5
  S versus SHAM apparatus burden

precision planner
  paired-difference SDs and two-group SDs.
```

UC5 is D0-specific. Its apparatus-effect estimates should not be transported backward into Qz/Qp/Qg unless a new upstream method explicitly uses the same apparatus.

## 9. UC6 — reproductive fitness-scale baseline and burden precision

Measurements on calibration-only flowers followed to maturity:

```text
initial ovule / seed state where relevant
final mature viable undamaged seeds
seed predation
fruit/capsule failure
apparatus/sham loss.
```

Supports:

```text
Qp/Qg
  reproductive endpoint variance and useful-effect scale

D0-Q5
  B_device variance / CI-width planning

G3-G5 planning
  expected fitness-scale resolution only.
```

UC6 does not supply G3-G5 effect estimates because its units remain calibration-only.

## 10. Minimal field architecture

The default first attempt is not six disjoint plant cohorts.

```text
Y-CAL cohort: 36 independent plants
    -> UC1 morphology
    -> UC2 y repeatability/range
    -> selected UC3/UC4 observations on distinct flowers where feasible

D0-CAL cohort: 48 independent plants
    -> UC5 apparatus/sham contrasts
    -> selected UC3/UC4 apparatus-facing measurements
    -> UC6 reproductive follow-through

additional natural-history calibration flowers/plants
    -> only if UC4 timing cannot be estimated without compromising the registered Y-CAL/D0-CAL flowers.
```

The existing 36 + 48 plant floors therefore remain the base calibration architecture. This document does **not** claim that 84 plants are automatically sufficient for every endpoint. The precision planner may require an expanded calibration or confirmatory sample if an endpoint is too noisy.

## 11. Flower allocation rule

Reuse plants before reusing flowers.

Preferred hierarchy:

```text
same calibration plant, different flowers
    > same flower with only non-destructive sequential measurements
    > same flower across carryover-producing manipulations (avoid).
```

Every flower receives a calibration-role label before outcomes are opened:

```text
UC1_GEOMETRY
UC2_RETENTION
UC3_POLLINATION
UC4_ATTACK_TIMING
UC5_D0_APPARATUS
UC6_REPRODUCTIVE_FOLLOWUP
```

Multiple labels are allowed only when measurement order is prospectively compatible and no prior measurement changes the later endpoint.

## 12. Candidate margin-reuse map

The following are **conditional handoffs**, not automatic values.

```text
upstream Qp/Qg max_z_relative_change
    -> D0_Q1_Z

Qz/Qp opening-width tolerance
    -> D0_Q1_OPENING

Qz orientation tolerance
    -> D0_Q1_ORIENTATION

Qg max_pollinator_visit_relative_change
    -> D0_Q3_VISIT

Qg max_pollen_grain_relative_change
    -> D0_Q3_POLLEN

Qg max_initial_seed_set_difference
    -> D0_Q3_INITIAL_SEED

Qg damage contamination bound
    -> D0_Q1_DAMAGE
```

Promotion requires all of:

```text
same endpoint definition
same units / transformation
same biological interpretation
same or prospectively bridged population-season
source margin itself prospectively frozen
D0 confirmatory outcomes unopened.
```

If two valid upstream margins map to one D0 endpoint, use the stricter bound unless a prospectively declared transformation justifies another combination.

## 13. What cannot be inherited directly

The following remain D0-specific or require a new functional bridge:

```text
D0_Q1_STIGMA
D0_Q2_VOLUME
D0_Q2_DURATION
D0_Q2_COVERAGE
D0_Q2_PROTECTION
D0_Q4_WET_EFFECT
D0_Q4_DRY_RESIDUAL
D0_Q5_BURDEN_EQ / BURDEN_PRECISION
D0_Q6_HORIZON identity.
```

Some use the same calibration data as upstream gates, but their biological questions differ.

## 14. Execution order

The efficient order is:

```text
1. UC1 + UC2 on Y-CAL
2. UC3 + UC4 natural-history/sensitivity measurements on calibration-only flowers
3. freeze reusable upstream Qz/Qp/Qg biological margins where justified
4. derive/freeze D0 margins using the portability rules
5. UC5 + UC6 on D0-CAL
6. populate the D0 variance manifest
7. validate margin manifest
8. compile margin + variance into precision input
9. run precision planner
10. freeze confirmatory Qz/Qp/Qg and D0 allocations
11. only then open confirmatory outcomes.
```

## 15. Net consequence

The current bottleneck is no longer "35 upstream thresholds plus 16 D0 thresholds require dozens of separate pilots."

It is better represented as:

```text
UC1 geometry/repeatability
UC2 structural-y/retention
UC3 pollination sensitivity
UC4 antagonist timing/protection
UC5 D0 apparatus/sham
UC6 reproductive follow-through
```

with most measurements embedded in the already registered Y-CAL and D0-CAL cohorts.

The programme therefore remains experimentally demanding, but it is finite, auditable, and substantially less redundant than treating every gate threshold as an independent experiment.
