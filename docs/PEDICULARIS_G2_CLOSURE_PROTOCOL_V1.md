# SLK Pedicularis G2 closure protocol v1

Status: **PROSPECTIVE / FAIL-CLOSED**.

This protocol turns the highest-leverage empirical gap in the current SLK ledger into one explicit cross-repository receipt.

The target is not merely a positive `Pedicularis rex` trade-off. The target is a biological, fitness-scale conflict budget that can enter SLK G2 and then be handed to BALANCE and BITA without circularly reusing the Chapter-2 water-defence axis.

## 1. Flagship target

SLK G2 requires a valid conflict-load receipt on one common reproductive fitness scale.

For the current Pedicularis programme the admissible quantity is

```text
L = L_S,component*
  = max_z F1_bar(z)
  + max_z F2_bar(z)
  - max_z [F1_bar(z) + F2_bar(z)].
```

with

```text
F1_bar(z) = 0.5 * [(W10-W00) + (W11-W01)]
F2_bar(z) = 0.5 * [(W01-W00) + (W11-W10)].
```

The primary fitness scale is the same across all four states:

```text
undamaged mature viable seeds per focal flower / capsule.
```

A trait-space optimum separation alone does not close G2.

## 2. Canonical source path

For same-species SCH -> BALANCE -> BITA use, SLK recognizes only the non-circular Pedicularis V2 path:

```text
SCH_PEDICULARIS_STAGE_P0_Z_MANIPULATION_V1
        +
SCH_PEDICULARIS_POLLINATION_WEIGHT_V1
        +
SCH_PEDICULARIS_PREDATOR_METHOD_V3
        |
        v
SCH_PEDICULARIS_FULL_SURFACE_READINESS_V3
        |
        v
SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2
        |
        v
SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1
        |
        v
CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED
        |
        v
SCH_COMPONENT_CONFLICT_BUDGET_V1
        |
        v
THREE_WORLD_CONFLICT_HANDOFF_V1
        |
        +--> BALANCE matched worldline
        +--> BITA non-circular water-y release
```

The older path in which water retained/drained was used as the SCH antagonist `G` is not admissible for this flagship chain.

## 3. Anti-circularity requirement

Chapter 1 and Chapter 2 must use different causal contrasts.

### SCH / G1-G2

```text
z = realized exsertion above the cupulate bract
P0 = standardized pollen supplementation
P1 = natural pollination dependence
G0 = independently predator-excluded
G1 = predator-exposed / sham
water-defence y = held fixed across all SCH cells.
```

### BITA / later G3 route

```text
x = the same validated exsertion coordinate
y0 = water defence disabled / drained
y1 = water defence active / protected.
```

Therefore the composite G2 receipt must contain

```text
system_wrapper_schema_version = SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2
water_y = HELD_FIXED_ACROSS_ALL_SCH_CELLS
readiness_reference.g_schema = SCH_PEDICULARIS_PREDATOR_METHOD_V3
predator_method_requirement includes POLLINATOR_ACCESS_PRESERVED.
```

Any receipt built from the deprecated water-as-G surface is rejected even if its numerical `L` is positive.

## 4. Pre-observation freeze

Before the confirmatory surface is opened, freeze:

```text
context_id
population_id
season_id
fitness_scale_id
z definition
minimum number of informative realized z levels
z manipulation tolerances
pollination-weight selectivity criterion
predator-exclusion effect criterion
predator-exclusion pollinator-access criterion
water-depth equivalence/tolerance criterion
component-optimum equivalence bounds
interior-optimum support rule
cluster/bootstrap unit
primary uncertainty interval.
```

The same `context_id`, `population_id`, `season_id`, and `fitness_scale_id` must be carried unchanged into the three-world handoff and any matched BALANCE/BITA experiment.

## 5. Execution sequence

### Gate P0 — validate the shared coordinate

Validate a non-destructive multi-level exsertion manipulation in `P. rex`.

The confirmatory surface requires at least five informative realized `z` levels if feasible. Reject the manipulation if it materially changes water protection, pollinator handling geometry, stigma position, corolla opening, flower orientation, or mechanical condition beyond prospectively frozen tolerances.

### Gate P1 — validate pollination dependence

Use the V2 mapping:

```text
P0 = SUPPLEMENTED
P1 = NATURAL.
```

Supplementation must reduce dependence on natural pollen delivery without changing seed-predator access or the water-defence state beyond tolerance.

### Gate G — validate an independent predator contrast

Use an antagonist intervention independent of water retention.

The method must qualify as `SCH_PEDICULARIS_PREDATOR_METHOD_V3`, including both biological effect/selectivity and method-timing/access criteria. A preferred route is a registered post-pollination lower-flower/fruit shield or another locally validated barrier that reduces predator access without covering the pollinator-entry zone.

The existing water retained/drained experiment is background evidence for the later `y` axis, not the SCH `G` intervention.

### Gate S — run the V2 causal surface

Run the randomized same-context surface

```text
>=5 realized z levels
x P0/P1
x G0/G1
```

with water defence held fixed.

The four states are

```text
W00 = supplemented + predator excluded
W10 = natural      + predator excluded
W01 = supplemented + predator exposed
W11 = natural      + predator exposed.
```

A positive G1 result must come from `SCH_PEDICULARIS_FULL_SURFACE_WRAPPER_V2` and retain the generic core schema `SCH_CAUSAL_COMPROMISE_STATE_OPTIMA_V1`.

### Gate C — component-optimum upgrade

G2 does not consume state optima alone.

Run the registered component contrasts and require

```text
optimum(M_G0) ~= optimum(M_G1)
optimum(H_P0) ~= optimum(H_P1)
```

within frozen equivalence bounds, with all component optima sufficiently supported as interior concave optima under the registered plant-cluster bootstrap.

Required status:

```text
CONTEXT_STABLE_COMPONENT_OPTIMA_IDENTIFIED.
```

If this gate fails, retain the valid G1 causal-compromise result but do not promote Pedicularis to SLK G2.

### Gate L — estimate the fitness-scale conflict budget

Use the SCH conflict-budget analyzer to produce

```text
receipt_schema_version = SCH_COMPONENT_CONFLICT_BUDGET_V1
status = FITNESS_SCALE_SHARED_CONFLICT_BUDGET_IDENTIFIED
criticality_export.L_S_component
criticality_export.L_S_component_95_ci
fitness_scale_id.
```

The point estimate must be non-negative and lie inside its uncertainty interval.

### Gate H — export the cross-repository handoff

Export

```text
receipt_schema_version = THREE_WORLD_CONFLICT_HANDOFF_V1
status = THREE_WORLD_CONFLICT_CONTEXT_IDENTIFIED.
```

The handoff must carry

```text
context_id
system = Pedicularis rex
population_id
season_id
fitness_scale_id
conflict_load.point
conflict_load.lower_95
conflict_load.upper_95.
```

## 6. SLK adjudication

The composite receipt distinguishes measurement from a positive downstream handoff.

```text
G2_VALID_MEASUREMENT
    all V2 provenance, component-identification, scale and uncertainty checks pass.

G2_DIRECT_PASS_POSITIVE
    G2_VALID_MEASUREMENT
    AND conflict_load.lower_95 > 0.

G2_MEASURED_BUT_ZERO_COMPATIBLE
    G2_VALID_MEASUREMENT
    AND conflict_load.lower_95 <= 0 <= conflict_load.upper_95.
```

Only `G2_DIRECT_PASS_POSITIVE` is eligible for the current bounded BALANCE classification rules that require `L.lower95 > 0`.

A zero-compatible interval is not a failed experiment. It means the conflict magnitude was measured but the current context does not support a positive bounded handoff.

## 7. Downstream lock

After `G2_DIRECT_PASS_POSITIVE`, downstream receipts must preserve exact context identity.

BALANCE requires the same

```text
context_id
population_id
season_id
fitness_scale_id
```

when comparing optimized shared/disabled and differentiated-accessible worldlines.

BITA additionally requires that the inherited SCH reference used independent predator exposure while water-y was held fixed. The later water `y0/y1` experiment may then test state-specific dimensional release without circularity.

## 8. Stop rules

Fail closed if any of the following occurs:

```text
water retained/drained used as SCH G for the same-species BITA chain;
<5 informative realized z levels remain without an explicit redesign;
z manipulation changes water/pollinator geometry beyond tolerance;
pollination supplementation changes antagonist exposure beyond tolerance;
independent predator method fails effect/selectivity or pollinator-access timing gates;
water depth differs materially among SCH P/G/z cells;
primary fitness scale differs among cells;
full-surface wrapper is not V2;
component-optimum upgrade is not identified;
conflict-budget receipt is absent or on a mismatched scale;
context/population/season changes at the BALANCE/BITA handoff.
```

## 9. What closes, and what does not

A positive composite receipt closes

```text
SLK G1: direct same-context shared-axis causal conflict
SLK G2: positive fitness-scale conflict load L.
```

It still does not identify

```text
G3 recoverable architecture benefit R
G4 architecture cost K
G5 Phi = R-K
G6 local accessibility
G7 architecture-specific invasion
G8 fixation
G9 occupancy.
```

That boundary is the point of the protocol: the first biological flagship quantity becomes real without borrowing evidence from later gates.

## 10. Current status

Against the frozen source repositories used by the current SLK ledger:

```text
observational shared-conflict reality:                 RECOVERED
V2 non-circular analysis contracts:                    IMPLEMENTED
multi-level P. rex z validation:                       NOT YET EXECUTED
same-context pollination-weight pilot:                 NOT YET EXECUTED
independent method-qualified predator exclusion:       NOT YET EXECUTED
V2 full causal surface:                                NOT YET EXECUTED
context-stable component-optimum upgrade:              NOT YET EXECUTED
biological SCH_COMPONENT_CONFLICT_BUDGET_V1 receipt:  NOT YET EXECUTED
THREE_WORLD_CONFLICT_HANDOFF_V1 biological receipt:   NOT YET EXECUTED
SLK G2:                                                OPEN.
```

The immediate experimental bottleneck is therefore not the `L` formula. It is qualification of the non-destructive `z` manipulation and an independent predator-exclusion method in the same focal population/season.