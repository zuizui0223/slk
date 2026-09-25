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

Therefore the minimum permission scope required to unlock P0a is:

```text
RECOVERY_PLUS_P0A_NONDESTRUCTIVE
```

The following activities are deliberately outside this minimum gate:

```text
D  voucher specimen collection
E  leaf / tissue sampling
F  seed / fruit collection
```

D-F may remain unresolved or prohibited without blocking P-1/P0a. They require separate authorization if later used.

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

A positive A-C response is not timeless. Every `ALLOWED` or `NO_PERMISSION_REQUIRED` response that contributes to the required scope must record:

```text
response_date
valid_from
valid_through.
```

The adjudicator validates ISO dates, rejects reversed intervals, and records the positive validity intervals separately for every:

```text
activity A-C
x
REGULATORY / SITE side.
```

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
RECOVERY_P0A_PERMISSION_SCOPE_CONFIRMED
RECOVERY_P0A_PERMISSION_SCOPE_INCOMPLETE
RECOVERY_P0A_PERMISSION_SCOPE_BLOCKED
RECOVERY_P0A_PERMISSION_SCOPE_CONFLICTING
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
sampling_permission_scope  = RECOVERY_PLUS_P0A_NONDESTRUCTIVE
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
RECOVERY_PLUS_P0A_NONDESTRUCTIVE_PERMISSION_SCOPE_ONLY
NO_D_TO_F_PERMISSION_INFERENCE
NO_FRESH_CONTEXT_RESULT
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
