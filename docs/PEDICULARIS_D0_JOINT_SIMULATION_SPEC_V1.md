# Pedicularis D0 calibration-based joint simulation specification V1

## Status

Prospective simulation specification with an executable normal-approximation implementation. No biological D0 result exists.

This document does not replace the conservative union-bound design in
`plan_pedicularis_y_d0_precision.py`.

The executable implementation is `scripts/simulate_pedicularis_d0_joint_power.py`. It becomes eligible to replace the conservative fallback only after independent D0-CAL data exist and a `SLK_PEDICULARIS_D0_JOINT_POWER_SIMULATION_FREEZE_V1` receipt freezes the planning alternatives, simulation model, random seed, replicate count, Monte Carlo interval, candidate sample-size grid and burden weights before confirmatory outcomes are opened.

## Goal

Estimate directly

```text
P(D0_FULLY_QUALIFIED | registered planning alternative)
```

while preserving the dependence among D0 qualification endpoints.

The current Bonferroni failure-budget plan guarantees the target without any
dependence assumption, but may be conservative because many endpoints are
measured on the same plants.

The simulation is intended to recover that efficiency without deleting
biologically registered endpoints.

## Resampling units

### LOW-Y calibration plants

Resample LOW-Y D0-CAL plants as whole multivariate units.

For each resampled plant preserve together all available paired contrasts used
by:

```text
Q1 geometry / coordinate preservation
Q3 pollination-facing neutrality
Q4 wet efficacy
Q4 dry residual
Q5 burden
```

This preserves cross-endpoint covariance and calibration missingness patterns.

### HIGH-Y calibration plants

Resample HIGH-Y D-CAL plants independently as whole multivariate units for the
Q2 benefit-matching endpoints.

### Q2 LOW-Y side

The LOW-Y D0-CAL endpoint vector used in Q2 is taken from the same resampled
LOW-Y plant pool, so its dependence with paired LOW-Y endpoints is retained
where the raw calibration design allows it.

## Planning truth

The simulation must not use observed confirmatory effects.

For each endpoint, calibration observations are centered and shifted to a
prospectively declared planning truth.

### Equivalence / contamination endpoints

Registered planning truth:

```text
difference = 0
```

unless another nonzero but equivalence-contained planning truth is explicitly
frozen before confirmatory outcomes.

### Q4 wet-channel superiority

Registered planning truth:

```text
planning_effect
>
minimum_useful_effect.
```

The planning effect must come from independent calibration and is already
required by the precision compiler.

### Q5 measured-burden precision route

The center may be nonzero. Qualification depends on precision rather than zero
burden, so the simulation must use the prospectively frozen planning burden
distribution and the CI-half-width rule.

## Attrition

For candidate recruitment sizes

```text
n_low_recruit
n_high_recruit,
```

simulate prospectively frozen whole-plant attrition before endpoint
adjudication.

Whole-plant attrition is applied at the registered attrition rate.

Endpoint-specific missingness already present in the calibration plant vector is
preserved by whole-vector resampling.

Any additional endpoint-specific missingness model must be separately frozen;
it may not be estimated from confirmatory outcomes.

## Endpoint adjudication inside each simulation replicate

Each simulated replicate uses the same criterion classes as the confirmatory
adjudicator:

```text
equivalence / contamination:
    confidence interval wholly inside [-margin,+margin]

minimum useful effect:
    lower one-sided bound > frozen threshold

burden precision:
    CI half-width <= frozen precision target

Q6:
    exact identity by design.
```

The first implementation may use the same normal-approximation planning model
as the analytical precision planner.

A later exact-analysis simulation may nest the registered bootstrap
adjudication, but the approximation class must be declared and frozen.

## Joint output

For each candidate allocation report:

```text
n_low_recruit
n_high_recruit
estimated_all_pass_probability
Monte Carlo uncertainty interval
per-gate pass probabilities
per-endpoint pass probabilities
failure-pattern frequencies
missingness-floor failure frequency
Q5-route-specific status.
```

The primary selection criterion is:

```text
lower Monte Carlo confidence bound
for P(D0_FULLY_QUALIFIED)
>=
target_all_pass_power.
```

Using only the point estimate is not sufficient.

## Candidate allocation search

Search over prospectively declared candidate pairs

```text
(n_low_recruit, n_high_recruit)
```

and choose the feasible allocation minimizing registered field burden.

A default burden metric may be

```text
3 * n_low_recruit + 1 * n_high_recruit
```

because LOW-Y plants carry three randomized qualification flowers while HIGH-Y
plants carry one natural-D flower.

Any alternative cost function must be frozen before the search.

## Comparison with the conservative fallback

For every candidate selected by simulation, also report the analytical
union-bound plan.

The simulation-based design may reduce recruitment only when:

1. calibration data are independent of confirmatory units;
2. the endpoint inventory is unchanged;
3. planning truths and margins are frozen;
4. the simulation preserves the registered dependence structure;
5. the lower Monte Carlo confidence bound reaches the joint target;
6. no confirmatory outcomes have been opened.

## Why endpoint deletion is not the first efficiency step

The current Q1-Q4 endpoint inventory encodes distinct biological failure modes.

Deleting endpoints solely because the conservative n is large would alter the
D0 estimand.

Calibration-based joint simulation instead asks whether the same biological
qualification can be achieved with a less conservative dependence model.

Only if later biological work demonstrates that an endpoint is genuinely
redundant for identification should an endpoint be demoted, and that change
requires a new protocol version rather than a sample-size patch.

## Current promotion rule

```text
UNION_BOUND_PLANNER
= ACTIVE_SAFE_FALLBACK

CALIBRATION_JOINT_SIMULATION_NORMAL_APPROX
= IMPLEMENTED_REQUIRES_PROSPECTIVE_FREEZE

EXACT_BOOTSTRAP_CONFIRMATORY_SIMULATION
= OPTIONAL_FUTURE_UPGRADE

ENDPOINT_DEMOTION
= NOT_AUTHORIZED

BIOLOGICAL_D0_RECEIPT
= ZERO
```

## Executable implementation

The first registered implementation uses:

```text
whole-plant empirical resampling of independent D0-CAL units
+ frozen whole-plant attrition
+ calibration missingness patterns
+ endpoint-specific planning-truth shifts
+ normal-approximation endpoint adjudication
+ exact all-endpoints-pass aggregation
+ Wilson Monte Carlo interval for the all-pass probability.
```

LOW-Y multivariate endpoint vectors are resampled as whole plants, preserving covariance among Q1/Q3/Q4/Q5 contrasts and the LOW-Y side of Q2. HIGH-Y D-CAL vectors are resampled independently as whole plants for Q2.

Candidate allocations are eligible only when the lower Monte Carlo confidence bound for full qualification reaches the frozen joint target.

The output also reports the conservative analytical union-bound allocation so that any efficiency gain is explicit rather than assumed.

The implementation intentionally does not impose the union-bound raw required sample size as a floor inside the simulation. Doing so would prevent the simulation from identifying a smaller dependence-aware design. Candidate n is judged by its simulated all-pass probability.

## Freeze requirement

Use `data/PEDICULARIS_D0_JOINT_POWER_SIMULATION_FREEZE_TEMPLATE_V1.json` and freeze, at minimum:

```text
population / season / fitness scale / horizon
confirmatory dataset id
margin freeze commit
candidate allocation grid
simulation model
random seed
replicate count
Monte Carlo interval level
target all-pass power
field-burden weights.
```

The simulator rejects context drift, target drift, duplicate candidates, unfrozen candidate grids, unfrozen seeds and opened confirmatory outcomes.


## Calibration-sample uncertainty boundary

The executable V1 simulation is an **inner empirical-resampling design calculation**. It preserves the observed plant-level covariance and missingness structure, but conditions on the finite D0-CAL empirical distribution.

Therefore the reported Monte Carlo confidence interval quantifies uncertainty from the finite number of simulation replicates. It does **not** by itself include uncertainty caused by having only a finite calibration sample.

Before a simulation-selected design replaces the conservative union-bound fallback, report at minimum:

1. the number of LOW-Y and HIGH-Y calibration plants;
2. endpoint-specific calibration completeness;
3. sensitivity of the selected allocation to plausible perturbations or an outer calibration bootstrap;
4. the analytical union-bound fallback beside the simulation choice.

If outer-bootstrap calibration uncertainty materially lowers the qualification-power lower bound, retain the more conservative allocation.

An outer calibration bootstrap is an optional future implementation upgrade; V1 must not describe its inner Monte Carlo interval as a full predictive uncertainty interval.
