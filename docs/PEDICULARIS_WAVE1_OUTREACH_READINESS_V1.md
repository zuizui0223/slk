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

The canonical CLI now uses the repository-tracked prospectively frozen production follow-up policy by default:

```text
data/PEDICULARIS_WAVE1_PERMISSION_FOLLOWUP_POLICY_V1.json
```

Human-reviewed `READY_FOR_MANUAL_SEND` candidate message bundles remain local working inputs.

Requester identity is filled through a local, gitignored profile rather than being committed:

```text
data/PEDICULARIS_PERMISSION_REQUESTER_PROFILE_TEMPLATE_V1.json
scripts/compile_pedicularis_permission_requester_profile.py
```

The filled local profile supplies name, institution and reply email to the bilingual drafts, but it cannot approve them. The resulting state is:

```text
DRAFT_REQUESTER_FILLED_AWAITING_HUMAN_REVIEW
```

The next local step is to generate a route-level human-review receipt with `scripts/generate_pedicularis_permission_message_review.py`. Every route is bound to the exact bilingual message hash and seven explicit checks. The manual-send guard requires a filled `HUMAN_REVIEW_APPROVED` receipt before `READY_FOR_MANUAL_SEND`. The readiness audit never invents requester identity or review approval.

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

The production follow-up policy is now prospectively frozen before any real send:

```text
day 7   first follow-up
day 14  second follow-up
day 21  manual escalation review
automatic close after silence = false.
```

With repository-tracked canonical state and no local requester-filled message bundles, the expected state is therefore:

```text
7 WAVE1 routes
all NOT_SENT
follow-up policy FROZEN_AND_VALIDATED
human-reviewed send-ready messages not provided.
```

The current administrative next action is now:

```text
FILL_LOCAL_REQUESTER_PROFILE_COMPILE_GENERATE_AND_APPROVE_HUMAN_REVIEW_RECEIPT
```

After a candidate's route messages pass the manual-send guard, the readiness audit will promote only those routes to `READY_FOR_MANUAL_SEND`; automatic sending remains forbidden.

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
