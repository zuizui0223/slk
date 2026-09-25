# Pedicularis WAVE1 permission follow-up policy v1

Status: **PROSPECTIVE ADMINISTRATIVE POLICY / NO AUTOMATIC CONTACT / NO PERMISSION / NO BIOLOGICAL RESULT**.

## Purpose

After an initial permission inquiry is manually sent, no-response handling must not be invented after seeing which candidate or authority is slow to respond.

This protocol therefore separates:

```text
the follow-up timing policy
from
the observed response history.
```

The repository provides the policy machinery but does **not** choose the production cadence automatically.

## Prospective freeze

Canonical template:

```text
data/PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_TEMPLATE_V1.json
```

Before the first real WAVE1 inquiry is sent, freeze:

```text
followup_offsets_days
escalation_review_after_days
policy_rationale_reference
freeze commit / timestamp.
```

The offsets are measured from the **initial send date** in calendar days and must be positive, unique and strictly increasing.

The escalation review day must occur after the last planned follow-up.

The policy must retain:

```text
automatic_close_allowed = false
response_receipt_preempts_followup = true
routing_response_preempts_same_route_followup = true
frozen_before_first_send = true.
```

The validator is:

```text
scripts/validate_pedicularis_wave1_permission_followup_policy.py
```

The freeze timestamp must be timezone-aware.

## First-send firewall

The initial manual-send receipt is not accepted unless the frozen follow-up policy is supplied to:

```text
scripts/apply_pedicularis_permission_send_receipt.py
```

and its freeze timestamp is no later than the actual manual send timestamp.

Thus a follow-up policy created after the inquiry has already been sent cannot be presented as prospective.

The send-event receipt records the policy freeze commit, timestamp, offsets and escalation-review day.

## Outreach ledger fields

The outreach ledger tracks:

```text
followup_attempts_completed
last_followup_date
last_followup_reference.
```

Rules:

```text
NOT_SENT
    -> followup_attempts_completed = 0
    -> no last-followup evidence

0 completed follow-ups
    -> no last-followup date/reference

>=1 completed follow-up
    -> last-followup date and reference required
    -> last-followup date cannot precede initial outreach.
```

These are administrative evidence fields. They do not imply any authority response.

## Follow-up planner

Use:

```text
scripts/plan_pedicularis_wave1_permission_followups.py
```

with:

```text
a validated outreach ledger
a frozen follow-up policy
an explicit as_of_date.
```

Possible actions are:

```text
SEND_INITIAL_INQUIRY
WAIT_UNTIL_FOLLOWUP
FOLLOWUP_DUE
WAIT_UNTIL_ESCALATION_REVIEW
ESCALATION_REVIEW_DUE
RESPONSE_RECORDED_NO_FOLLOWUP
NO_FOLLOWUP_ROUTE_NOT_AWAITING_RESPONSE.
```

A response always preempts same-route follow-up planning.

After all prospectively frozen follow-up attempts are exhausted, the planner produces an **escalation review**, not automatic closure.

## What this protocol does not do

It does not:

```text
send a follow-up
choose the production cadence
close a route automatically
interpret silence as refusal
interpret silence as permission
change candidate priority
create a fresh-context or biological result.
```

## Claim ceiling

```text
ADMINISTRATIVE_FOLLOWUP_TIMING_ONLY
NO_AUTOMATIC_CONTACT
NO_AUTOMATIC_CLOSURE
NO_PERMISSION
NO_FRESH_CONTEXT
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
