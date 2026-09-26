# Pedicularis WAVE1 permission outreach readiness audit v1

Status: **ADMINISTRATIVE READINESS SUMMARY / NOT A NEW PERMISSION GATE / NO CONTACT EXECUTED**.

## Purpose

The WAVE1 permission workflow now has separate contracts for candidate selection, contact routing, bilingual inquiry drafts, human review, manual-send receipts, follow-up timing, incoming replies and permission adjudication.

This audit does not add another scientific or permission gate. It only answers:

```text
What administrative pieces are still missing before a registered route can be manually sent?
What is the current next action for routes that have already been sent or answered?
```

Canonical script:

```text
scripts/audit_pedicularis_wave1_outreach_readiness.py
```

## Inputs

The canonical outreach ledger is used by default:

```text
data/PEDICULARIS_WAVE1_PERMISSION_OUTREACH_LEDGER_TEMPLATE_V1.csv
```

Optional working inputs are local:

```text
a prospectively frozen follow-up policy
one or more human-reviewed READY_FOR_MANUAL_SEND candidate message bundles.
```

The audit never fills these missing inputs automatically.

## Pre-send blockers

For a `NOT_SENT` route, readiness requires both:

```text
frozen follow-up policy
AND
human-reviewed route message with valid CN / EN / BILINGUAL hashes.
```

If either is absent, the route is:

```text
BLOCKED_BEFORE_FIRST_SEND
```

with explicit administrative blocker codes such as:

```text
FOLLOWUP_POLICY_NOT_FROZEN
HUMAN_REVIEWED_MESSAGE_NOT_READY.
```

These are not biological failures and do not alter candidate status.

## Route states summarized

The audit maps already validated outreach states to operational summaries:

```text
NOT_SENT + prerequisites complete
    -> READY_FOR_MANUAL_SEND

SENT_AWAITING_RESPONSE
    -> AWAITING_RESPONSE_OR_FOLLOWUP

ROUTED_TO_ANOTHER_AUTHORITY
    -> ROUTING_DESTINATION_REQUIRES_CANONICAL_REGISTRATION

RESPONSE_RECEIVED + both authorizing sides complete
    -> READY_TO_BUILD_PERMISSION_RESPONSE_DRAFT

RESPONSE_RECEIVED + one authorizing side still missing
    -> AWAITING_OTHER_AUTHORIZING_RESPONSE.
```

The audit does not itself send, follow up, register a routed authority, interpret a response, or build a permission receipt.

## Manual-send firewall

Every send-ready route remains:

```text
manual_send_only = true
automatic_send_allowed = false.
```

The auditor recomputes all three reviewed message hashes:

```text
CN
EN
BILINGUAL
```

before calling a route ready.

## Current canonical state

With only repository-tracked canonical templates and no local production working files, the expected state is:

```text
7 WAVE1 routes
all NOT_SENT
follow-up policy not yet production-frozen
human-reviewed send-ready messages not provided.
```

Therefore the current administrative next action remains:

```text
FREEZE_FOLLOWUP_POLICY_BEFORE_FIRST_SEND
```

followed by completion and human review of the actual requester-filled messages.

This statement is an administrative readiness result only. It does not mean any WAVE1 biological candidate has failed.

## Claim ceiling

```text
ADMINISTRATIVE_READINESS_SUMMARY_ONLY
NO_AUTOMATIC_CONTACT
NO_PERMISSION
NO_FRESH_CONTEXT
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
