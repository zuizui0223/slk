# Pedicularis WAVE1 permission-response adjudication v1

Status: **PROSPECTIVE RESPONSE RECEIPT / RECOVERY + P0a NON-DESTRUCTIVE SCOPE ONLY / NO BIOLOGICAL RESULT**.

## Purpose

The WAVE1 permission-routing layer identifies whom to ask. This protocol defines what a returned written response must establish before the fresh context-recovery gate can treat permission as resolved.

A phone number, email address, public opening notice or unsent inquiry draft is never a permission.

## Minimum scope for P-1 -> P0a

The first downstream biological step after fresh context recovery is the P0 natural-history calibration. Its registered endpoints are observational:

```text
A  visual observation
B  photography / morphology documentation
C  non-destructive measurement
```

Therefore the minimum permission scope required to unlock the recovery → P0a → P0b non-destructive path is:

```text
RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE
```

The following activities are deliberately outside this minimum gate:

```text
D  voucher specimen collection
E  leaf / tissue sampling
F  seed / fruit collection
```

D-F may remain unresolved or prohibited without blocking the default non-destructive P-1/P0a/P0b path. They require separate authorization if later used.

There is one explicit conditional exception: if the fresh taxon-identification route uses a **new field voucher**, activity D becomes required for that recovery record. The permission receipt therefore preserves A-F decisions and validity intervals even though only A-C define the default scope. A positive D response must also carry `valid_from` / `valid_through`; the recovery gate checks D on the actual voucher/recovery date.

## Two-sided permission requirement

For each of A-C, the adjudicator requires:

```text
REGULATORY side = PASS
AND
SITE side       = PASS.
```

A side passes when a registered response says either:

```text
ALLOWED
or
NO_PERMISSION_REQUIRED.
```

A `LOCAL_TERRITORIAL_ROUTING` contact is routing-only. It may identify the actual site manager, but it cannot satisfy the SITE permission side.

For example, the Jiantang Town route for Wufeng cannot itself authorize A-C. Wufeng remains incomplete until an actual site-management route is registered and responds.

## Validity-window requirement

A positive activity decision is not timeless. Each A-F activity row is adjudicated separately. Every `ALLOWED` or `NO_PERMISSION_REQUIRED` activity decision must record:

```text
activity_id
decision
response_reference
valid_from
valid_through
conditions.
```

`response_date` remains response-level provenance, but a response-wide validity window does **not** substitute for activity-level dates.

This matters because one authority may say, for example:

```text
A-C non-destructive work: valid through September
D voucher collection:    valid only June 10-20.
```

The adjudicator validates ISO dates and records positive intervals separately for every:

```text
activity A-F
x
REGULATORY / SITE side.
```

Only A-C define the default non-destructive scope. D-F are retained so later destructive routes cannot silently inherit A-C validity.


## Condition-compatibility review

An authority can return a formally positive decision whose conditions make the registered field activity impossible. Therefore raw authorization and effective project scope are separated.

Every positive activity row must also record:

```text
conditions
conditions_compatible_with_registered_activity
conditions_review_reference.
```

If `conditions_compatible_with_registered_activity = true`, the positive decision may contribute a validity interval to that authority side.

If it is `false`, the raw authority decision remains visible as `ALLOWED` or `NO_PERMISSION_REQUIRED`, but the **effective scope decision is BLOCKED** for the registered protocol. The receipt does not silently reinterpret restrictive conditions as permission.

For example:

```text
raw decision:
    C = ALLOWED

condition:
    no touching or measuring flowers

registered C activity:
    non-destructive floral measurement

effective project scope:
    C = BLOCKED.
```

Condition review is performed activity-by-activity. An incompatible D voucher condition does not by itself block the default A-C path, but it prevents D from being used for a new-voucher taxon route.

The recovery gate then asks whether the **actual fresh-recovery date** falls inside at least one positive interval for every required cell.

The P0a freeze independently asks whether the **entire planned natural-history calibration date interval** is covered by at least one positive interval for every required cell.

Thus:

```text
permission scope confirmed
!=
permission valid forever.
```

An expired permission cannot be rescued by retaining the old receipt.

## Response statuses

```text
RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFIRMED
RECOVERY_P0A_P0B_PERMISSION_SCOPE_INCOMPLETE
RECOVERY_P0A_P0B_PERMISSION_SCOPE_BLOCKED
RECOVERY_P0A_P0B_PERMISSION_SCOPE_CONFLICTING
```

Rules:

```text
confirmed:
    every A-C cell is PASS on both regulatory and site sides

incomplete:
    one or more required cells remains unresolved

blocked:
    one or more required cell is explicitly prohibited

conflicting:
    a required side contains both a positive authorization/no-permission-needed response
    and an explicit prohibition.
```

Conflicting responses are not resolved by choosing the more convenient answer.

## Canonical files

```text
data/PEDICULARIS_WAVE1_PERMISSION_RESPONSE_TEMPLATE_V1.json
scripts/adjudicate_pedicularis_wave1_permission_responses.py
scripts/compile_pedicularis_permission_scope_into_recovery.py
tests/test_pedicularis_wave1_permission_responses.py
```

## Recovery handoff

Only a confirmed permission-scope receipt may populate:

```text
sampling_permission_status = CONFIRMED
sampling_permission_scope  = RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE
sampling_permission_reference
permission_scope_receipt.
```

The context-recovery adjudicator independently rechecks the embedded receipt:

```text
candidate id
receipt schema/status
scope
A-C regulatory PASS
A-C site PASS.
```

A manually typed `sampling_permission_status=CONFIRMED` without the receipt fails closed.

## Claim ceiling

```text
RECOVERY_PLUS_P0A_PLUS_P0B_NONDESTRUCTIVE_PERMISSION_SCOPE_ONLY
NO_D_TO_F_PERMISSION_INFERENCE
NO_FRESH_CONTEXT_RESULT
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
