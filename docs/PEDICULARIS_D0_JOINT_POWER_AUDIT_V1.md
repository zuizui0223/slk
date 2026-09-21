# Pedicularis D0 joint-power audit V1

## Status

Prospective design audit. No biological D0 result exists.

## Why this audit exists

Full D0 qualification is an intersection-union decision. Under the negligible-burden route, the current production manifest contains:

- Q1: 5 stochastic geometry/contamination endpoints;
- Q2: 4 stochastic benefit-matching endpoints;
- Q3: 3 stochastic pollination-facing endpoints;
- Q4: 2 stochastic channel-fidelity endpoints;
- Q5: 1 stochastic burden endpoint;
- Q6: 1 exact time-horizon identity.

Therefore the full stochastic all-pass event contains 15 endpoints.

The previous precision planner treated endpoint-level power as if it were enough to characterize the full qualification design. It is not.

## Old versus corrected paired-equivalence planning

For a symmetric equivalence margin Delta, paired-difference SD sigma, one-sided TOST alpha and planning truth difference 0,

```text
Power
=
2 Phi(
    Delta sqrt(n)/sigma
    - z_(1-alpha)
)
- 1.
```

Solving for n gives

```text
n
=
[
  (z_(1-alpha) + z_((1+power)/2))
  sigma / Delta
]^2.
```

For

```text
sigma = 1
Delta = 0.5
alpha = 0.05
power = 0.80
```

the old formula returned n=25, whose normal-approximation power is approximately 0.6075.

The corrected formula returns

```text
paired n = 35.
```

## Full-qualification power

For marginal endpoint pass probabilities p_1,...,p_m,

```text
max(0, 1 - sum_j (1-p_j))
<=
P(all pass)
<=
min_j p_j.
```

These are dependence-agnostic Frechet bounds.

The independence product

```text
prod_j p_j
```

is a reference only and is not a guaranteed joint power.

### Old nominal 80% endpoint design

For 15 endpoints with p_j=0.80,

```text
Frechet lower bound = 0
Frechet upper bound = 0.80
independence reference = 0.80^15 ~= 0.035.
```

Thus marginal 80% endpoints do not constitute an 80% D0 qualification design.

### Registered conservative 80% all-pass target

Allocate the failure budget as

```text
p_endpoint
>=
1 - (1-p_joint)/m.
```

With

```text
p_joint = 0.80
m = 15,
```

this gives

```text
p_endpoint >= 0.986666...
```

and therefore

```text
Frechet all-pass lower bound >= 0.80.
```

For the same sigma=1 and Delta=0.5 reference:

```text
paired equivalence raw n = 68
two-group equivalence raw n = 136 per group.
```

This is deliberately conservative and makes no endpoint-independence assumption.

## Why the endpoints are not demoted yet

The protocol defines several gates as multidimensional biological requirements rather than interchangeable replicate readouts.

### Q1 geometry/coordinate preservation

The external comparator must not alter the registered z axis or pollinator-entry geometry. Exsertion, opening, stigma position, orientation and damage capture different off-target routes.

### Q2 functional-benefit matching

Q2 is the central D0 requirement. The protocol explicitly rejects matching only one mean when duration, protected area or realized protection differs. The target is a y-performance profile, not one scalar endpoint.

### Q3 pollination-facing neutrality

Visit behavior, pollen receipt and initial seed set occur at different steps of the pollination path. Dropping an endpoint before calibration would weaken the registered off-target-contamination claim.

### Q4 channel fidelity

Wet efficacy and dry-device residual answer logically distinct questions and both are required.

### Q5 apparatus burden

Only one prospectively selected Q5 lane is active in a given qualification experiment.

Therefore a numerical primary/secondary demotion should not be made merely to lower n.

## Preferred next efficiency improvement

The current union-bound plan is a safe fallback, not necessarily the final efficient design.

After independent D0 calibration data exist, preserve the full endpoint inventory and estimate the joint multivariate dependence structure at the independent-plant level.

Then prospectively simulate the complete confirmatory procedure, including:

- shared LOW-Y plants across paired Q1/Q3/Q4/Q5 contrasts;
- joint covariance among paired endpoints;
- covariance among Q2 D0-D endpoints;
- the registered bootstrap estimators;
- the selected Q5 route;
- attrition and endpoint missingness assumptions;
- the all-gates-pass adjudication rule.

Choose recruitment n by the simulated probability

```text
P(D0_FULLY_QUALIFIED | registered planning alternative)
>=
target_all_pass_power.
```

Only a prospectively frozen simulation with independent calibration inputs may replace the union-bound design.

## Q5 measured-burden lane

The measured-burden route uses a CI-half-width criterion rather than a standard superiority/equivalence power endpoint.

The current planner therefore reports

```text
JOINT_POWER_INCOMPLETE_PRECISION_ENDPOINT_REQUIRES_SIMULATION
```

for that route until a dedicated prospective pass-probability simulation is supplied.

## Recruitment versus analyzable n

The planner now distinguishes:

```text
raw_required_n
= minimum analyzable complete-case floor

inflated_required_n
= prospective recruitment target after attrition inflation.
```

The adjudicator uses raw_required_n after data collection. It does not require all prospectively inflated recruits to remain complete.

## Missingness

Complete-case exclusions are now reported endpoint by endpoint with plant IDs and reasons.

Missingness does not automatically invalidate the endpoint if the raw powered floor remains satisfied, but any exclusion sets

```text
missingness_sensitivity_required = true.
```

Outcome-dependent missingness can bias equivalence toward zero and therefore requires substantive sensitivity analysis.

## Current decision

```text
ENDPOINT_DEMOTION = NOT_JUSTIFIED_YET
BONFERRONI_FAILURE_BUDGET = SAFE_PROSPECTIVE_FALLBACK
CALIBRATION_BASED_FULL_PIPELINE_SIMULATION = PREFERRED_EFFICIENCY_UPGRADE
Q5_MEASURED_ADJUSTMENT_JOINT_POWER = OPEN
BIOLOGICAL_D0_RECEIPT = ZERO
```
