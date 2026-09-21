# INV1 executable validation receipt V1

## Purpose

This receipt records how the flagship fixation–occupancy invariant is verified in code.

The executable check is deliberately separated from manuscript/ledger synchronization tests.

## Registered process path

The code now constructs the registered canonical architecture game explicitly:

~~~text
A_SS = baseline
A_SD = A_DS = baseline + Phi - eta
A_DD = baseline + 2 Phi
~~~

and then evaluates the self-excluding exponential Moran birth–death process state by state.

For a population with i differentiated individuals,

~~~text
pi_D(i)
=
[(i-1) A_DD + (N-i) A_DS] / (N-1)

pi_S(i)
=
[i A_SD + (N-i-1) A_SS] / (N-1).
~~~

The Moran transition probabilities are computed from exponential fitness using log-scaled reproduction weights to avoid avoidable overflow.

The one-mutant fixation probabilities rho_D and rho_S are then obtained from the birth–death chain, not from the registered closed-form ratio.

## Independent INV1 path

The symmetric rare-mutation monomorphic chain is built from the two process-derived fixation probabilities:

~~~text
S -> D  proportional to rho_D
D -> S  proportional to rho_S.
~~~

Its stationary weights are

~~~text
Pi_S = rho_S / (rho_D + rho_S)
Pi_D = rho_D / (rho_D + rho_S).
~~~

Therefore the executable test compares

~~~text
rho_D / rho_S
~~~

with

~~~text
Pi_D / Pi_S
~~~

after calculating them through different code paths.

`occupancy_ratio()` no longer aliases `reciprocal_fixation_ratio()`.

## Closed-form recovery test

For the registered canonical game, process-derived reciprocal fixation is tested against

~~~text
exp[beta (N-2) Phi]
~~~

over the grid

~~~text
Phi in {-0.2, 0, 0.2}
eta in {-1, 0, 1.5}
N=20
beta=0.1.
~~~

The statewise Moran transition probabilities vary with eta, while the final reciprocal fixation ratio is required to collapse to the same Phi-only closed form.

This verifies the cancellation rather than assuming it.

## Canonical-mapping guard

The code distinguishes:

- `CanonicalArchitectureGame`, which explicitly declares the registered mapping;
- `SymmetricTwoStrategyGame`, which is a generic symmetric population game.

`validate_canonical_mapping()` requires

~~~text
(A_DD-A_SS)/2 = Phi
~~~

and

~~~text
(A_SS+A_DD)/2 - A_SD = eta
~~~

within the registered numerical tolerance.

A deliberately noncanonical game with unequal diagonal feedback is required to:

1. fail the canonical validation;
2. produce a process-derived fixation ratio that disagrees with the Phi-only prediction.

Thus the equal-diagonal-feedback assumption is executable rather than prose-only.

## Single source of architecture mathematics

`scripts/verify_amnat_claims.py` imports `ArchitecturePath` from `scripts/slk_threshold_atlas.py`.

The prior duplicated implementations of

~~~text
R(d)=d+d^2
Phi=R-K
~~~

inside the verifier have been removed.

The anonymous review bundle contains the same authoritative module used by the repository tests.

## Numerical policy

The authoritative module defines:

~~~text
DEFAULT_ABS_TOL  = 1e-12
DEFAULT_REL_TOL  = 1e-10
DEFAULT_ZERO_TOL = 1e-12.
~~~

Core theoretical comparisons use `numerically_close()`.

Denominators and environmental slopes with absolute magnitude at or below `DEFAULT_ZERO_TOL` are rejected as numerically singular rather than being tested with exact `== 0`.

The tolerance is a numerical implementation policy, not a biological equivalence margin.

## Test classes

Pytest markers distinguish:

~~~text
theory_numeric
theory_process
document_sync
protocol_schema.
~~~

CI first runs

~~~text
theory_numeric or theory_process
~~~

as the scientific numerical/process check, then runs the complete repository suite separately.

Manuscript string and ledger synchronization tests are therefore not presented as independent process validation.

## Canonical files

- `scripts/slk_threshold_atlas.py`
- `scripts/verify_amnat_claims.py`
- `tests/test_moran_process_invariant.py`
- `tests/test_unified_threshold_atlas.py`
- `pytest.ini`
