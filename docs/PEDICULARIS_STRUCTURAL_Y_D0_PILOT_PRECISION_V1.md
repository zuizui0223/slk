# Pedicularis structural-y + D0 pilot and precision plan v1

Status: **PROSPECTIVE / CALIBRATION ONLY / CONFIRMATORY UNOPENED**.

## 1. Purpose

This document converts the registered Pedicularis G1-G5 and D0 feasibility contracts into an executable calibration programme.

The pilot has one job:

```text
estimate measurement repeatability, natural y range, paired-difference SDs,
D0-vs-D matching variance, apparatus-burden variance, and channel-fidelity variance
```

so that the later confirmatory qualification sample sizes and equivalence tests can be frozen without inspecting confirmatory outcomes.

The pilot does **not** close G3, G4, or G5. Every plant and flower used here is excluded from confirmatory G3-G5 estimation.

## 2. Biological quantities

Keep the registered coordinates:

```text
z = realized corolla exsertion above the cupulate bract
y = standardized structural water-retention performance
```

Primary y measurements:

```text
maximum retained water volume
standardized water depth
retention half-life / duration
leakage rate
protected fraction of the vulnerable ovary/corolla-base region during the attack window
```

Primary common reproductive scale for later confirmation remains:

```text
undamaged mature viable seeds per focal flower
```

The pilot may use earlier mechanistic readouts such as pollen receipt, early attack, and water retention because its purpose is qualification and variance recovery.

## 3. Stage Y-CAL — structural-y calibration

### Sampling floor

Register one focal population-season and sample:

```text
36 independent flowering plants
3 flowers from different whorls per plant
2 standardized retention trials per focal flower where non-destructive
```

This yields up to:

```text
36 plant clusters
108 flowers
216 repeated retention measurements
```

The plant is the independent replication unit. Repeated flowers and repeated wetting trials estimate within-plant and measurement variance; they do not increase the independent n.

### Why 36 plants

Published P. rex trait surveys used 16-36 plants per population, showing that 36 plants is within demonstrated field feasibility. Under a simple normal-variance approximation, the relative standard error of an SD estimated from 36 independent plants is about

```text
1 / sqrt[2(36-1)] ~= 0.12.
```

That is sufficiently stable for a calibration input while remaining a pilot rather than a hidden confirmatory experiment.

### Measurements on every Y-CAL plant

Record:

```text
plant_id
flower_id / whorl_id
flowering date and local block
flower length
bract height
realized exsertion z
corolla opening width
stigma position
flower orientation
maximum retained volume
standardized water depth
retention time series
retention half-life / duration
leakage rate
initial mechanical condition
```

Where feasible, also record pollen receipt and early predator evidence on flowers not used for destructive retention trials.

### Outputs

Estimate, with plant-cluster uncertainty:

```text
between-plant SD(y)
within-plant SD(y)
measurement/repeat-trial SD(y)
repeatability / ICC(y)
x-y and z-y covariance
natural y range
correlations among alternative y definitions
```

No low/high structural-y cutoff may be chosen using confirmatory reproductive outcomes.

## 4. Prospective structural-y bands after Y-CAL

The Y-CAL set may be used to freeze recruitment bands for a *new, disjoint* D0 calibration set.

Default recruitment rule:

```text
LOW-Y  = at or below the Y-CAL 1/3 quantile
HIGH-Y = at or above the Y-CAL 2/3 quantile
```

This tertile rule is chosen before D0 outcomes are observed to balance phenotype separation against field recruitment feasibility.

Before using these bands, require a dynamic-range check:

```text
median(HIGH-Y) - median(LOW-Y)
    >= max(1 between-plant SD(y), 2 measurement-error SD(y)).
```

If the tertile bands fail this check, structural y has insufficient resolved range for the registered low/high comparison in that population-season. Do not move cutoffs post hoc to manufacture separation; register a new population or a new prospective protocol.

## 5. Stage D0-CAL — pre-cost-comparator calibration

Use plants disjoint from Y-CAL.

### Sampling floor

Recruit:

```text
24 independent LOW-Y plants
24 independent HIGH-Y plants
```

for a total calibration floor of 48 independent plants.

With 24 plants per phenotype stratum, a simple normal approximation gives a relative SD standard error near 15%, adequate for planning later equivalence and minimum-effect sample sizes. Historical P. rex drainage work used roughly 40-60 individuals per population, so the total scale is biologically field-plausible, while the current programme remains explicitly calibration-only.

### LOW-Y within-plant block

On each LOW-Y plant allocate three comparable focal flowers, preferably from matched whorls or flowering positions:

```text
S_CAL     no external retention apparatus
SHAM_CAL  physically matched apparatus that does not retain the target water profile
D0_CAL    externalized retention support tuned to the frozen target y profile
```

Randomize flower-to-treatment assignment within plant where feasible.

The SHAM must match material, handling, attachment, and gross geometry. Its defining difference from D0 is the absence of the target retention function, not the absence of the device.

Target maximum:

```text
24 plants x 3 flowers = 72 LOW-Y focal flowers.
```

### HIGH-Y block

On each HIGH-Y plant allocate two comparable flowers:

```text
D_CAL          natural structural-y state intact
D_DRAIN_CAL    natural structure present but target water-retention state disabled/drained
```

The drained flower is a functional-channel calibration, not the structural D counterfactual used for G4.

Target maximum:

```text
24 plants x 2 flowers = 48 HIGH-Y focal flowers.
```

Total Stage D0-CAL target:

```text
48 plants
120 focal flowers
```

Losses are recorded, not silently replaced after outcome inspection. Recruitment may exceed the floor prospectively to cover expected pre-outcome attrition, but the inflation rule must be declared before treatment outcomes are opened.

## 6. What each D0-CAL contrast estimates

### Q1 — geometry preservation

Use paired LOW-Y contrast:

```text
D0_CAL - SHAM_CAL
```

for:

```text
z
corolla opening
stigma position
orientation
bract compression
mechanical damage.
```

These contrasts supply paired-difference SDs for later equivalence planning.

### Q2 — functional-benefit matching

Compare the D0 retention profile with natural D:

```text
D0_CAL versus D_CAL.
```

Primary matching dimensions should include at least retention magnitude and retention duration. If seed-predator protection depends on duration, matching only maximum water volume is insufficient.

### Q3 — pollination-facing equivalence

Primary pilot readouts:

```text
pollen receipt / grains per stigma
legitimate handling or stigma-contact proxy
initial seed set where feasible.
```

Use both:

```text
D0_CAL versus SHAM_CAL
D0_CAL versus D_CAL.
```

### Q4 — antagonist-channel fidelity

The key within-LOW-Y comparison is:

```text
D0_CAL versus SHAM_CAL
```

because both contain the apparatus. A reduction in attack only when the target water-retention function is active supports the intended water-mediated route rather than simple physical exclusion.

Cross-check against:

```text
D_CAL versus D_DRAIN_CAL.
```

The direction and timing of the D0 water effect should be compatible with the natural structural-y water effect.

### Q5 — apparatus burden

Use paired:

```text
S_CAL versus SHAM_CAL
```

for geometry, pollen-facing measures, damage, and—if the season allows—reproductive outcome. This supplies the burden estimate or bound used by the later K analysis.

### Q6 — horizon

All reproductive pilot endpoints, if collected, use one frozen interval:

```text
treatment assignment at focal flower
-> mature viable undamaged seeds.
```

## 7. Pilot analysis outputs

For every gate-defining variable export:

```text
endpoint_id
design = paired or two_group
scale / transformation
cluster unit
mean or median by treatment
SD at the independent-unit scale
paired-difference SD where applicable
ICC / repeatability where applicable
missingness and failure rate
candidate equivalence margin source
candidate minimum useful effect source
```

The pilot output is a variance/feasibility object. It does not contain a confirmatory pass/fail field for G3-G5.

## 8. Confirmatory sample-size rule

After pilot outputs are frozen, choose biological equivalence margins and minimum useful effects **without using confirmatory treatment outcomes**.

For each later gate compute the independent-plant requirement using the registered precision planner:

```text
scripts/plan_pedicularis_y_d0_precision.py
```

Supported planning objects:

```text
paired equivalence
independent two-group equivalence
paired superiority / minimum useful effect
independent two-group superiority
mean CI half-width
```

The final confirmatory plant floor is the maximum required n over all gate-defining primary endpoints, then prospectively inflated for expected pre-outcome loss.

Flowers per plant are chosen to reduce within-plant noise until the plant-level SD stabilizes; flowers never substitute for independent plants.

## 9. Default inferential settings

Unless a gate has a stronger biological reason, the planning defaults are:

```text
alpha = 0.05
power = 0.80
expected pre-outcome attrition inflation = 15%
```

Equivalence uses two one-sided tests conceptually; the normal-approximation planner uses `z_(1-alpha) + z_power`. Superiority planning defaults to a two-sided alpha unless the frozen gate is explicitly directional.

These defaults are planning conventions, not biological equivalence margins. Every margin/effect size must still have its own biological or measurement rationale.

## 10. Margin firewall

Do not define equivalence as a fraction of the observed D0 effect merely because that value makes the test pass.

Admissible margin sources are:

```text
instrument/measurement precision + biological negligible-change argument
independent Y-CAL or D0-CAL variability combined with a predeclared biological tolerance
published natural-history/functional scale
minimum change that would alter the downstream interpretation.
```

The margin source and exact numeric value must be committed before confirmatory outcomes are opened.

## 11. Stop rules

Stop structural-y / D0 promotion if:

```text
Y-CAL cannot resolve repeatable y above measurement error;
tertile recruitment bands fail the frozen dynamic-range check;
D0 cannot reproduce both magnitude and duration of natural D retention;
SHAM changes pollination geometry beyond any biologically defensible margin;
D0 reduces attack through physical exclusion rather than the water-retention route;
plant-level variance is so large that the required confirmatory n exceeds the prospectively declared field-capacity ceiling.
```

The last outcome is an identifiability/feasibility result, not permission to weaken the margin or reduce power after seeing the estimate.

## 12. Data separation

Use distinct identifiers:

```text
PED_Y_CAL_V1      structural-y calibration
PED_D0_CAL_V1     D0/sham calibration
PED_G1_G2_CONF_*  G1-G2 confirmatory
PED_G3_G5_CONF_*  future architecture-value confirmation
```

No plant or focal flower from `PED_Y_CAL_V1` or `PED_D0_CAL_V1` may enter `PED_G3_G5_CONF_*`.

## 13. Immediate field sequence

```text
A. 36-plant Y-CAL
   -> repeatability, y range, z-y covariance, measurement error

B. freeze LOW-Y / HIGH-Y recruitment bands
   -> apply tertile + dynamic-range rule

C. 48-plant D0-CAL
   -> 24 LOW-Y: S / SHAM / D0
   -> 24 HIGH-Y: D / D-drain

D. freeze biological margins and minimum useful effects

E. run precision planner
   -> final independent-plant n for every primary qualification gate
   -> take maximum + frozen attrition inflation

F. only then open the disjoint confirmatory structural-y / D0 qualification experiment.
```

## 14. What this changes for SLK

Before this protocol the G1-G5 programme had a conceptual D0 but no explicit route from pilot variance to a frozen confirmatory sample size.

After this protocol, the remaining empirical sequence is finite and auditable:

```text
calibrate y
-> qualify D0 feasibility
-> freeze margins + n
-> confirm structural y / D0
-> estimate R, K_incremental_y, Phi.
```

No new theorem is needed for this step.