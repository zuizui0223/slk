# Pedicularis D0 calibration-based joint simulation specification V1

## Status

Prospective simulation specification only.

This document does not replace the conservative union-bound design in
`plan_pedicularis_y_d0_precision.py`.

The simulation becomes eligible to replace that fallback only after independent
D0-CAL data exist and the simulation code, planning alternatives, random seed,
replicate count and candidate sample-size grid are frozen before confirmatory
outcomes are opened.

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

CALIBRATION_JOINT_SIMULATION
= SPECIFIED_NOT_YET_IMPLEMENTED

ENDPOINT_DEMOTION
= NOT_AUTHORIZED

BIOLOGICAL_D0_RECEIPT
= ZERO
```
