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


## Activity-decision evidence extraction

A resolved activity decision cannot be justified only by citing the response as a whole. For every:

```text
ALLOWED
NO_PERMISSION_REQUIRED
PROHIBITED
```

activity row, the bundle must also record:

```text
decision_evidence_locator
decision_extracted_by
decision_extraction_date
decision_extraction_reference
decision_extraction_rationale.
```

The evidence locator must identify where the decision came from inside the audited source response. Registered prefixes are:

```text
BODY:
ATTACHMENT:
CALL_NOTE:
IN_PERSON_NOTE:
```

Examples:

```text
BODY:paragraph-4
ATTACHMENT:permit-letter.pdf#p2-item-C
CALL_NOTE:lines-18-24
IN_PERSON_NOTE:section-3.
```


The locator prefix must match the incoming-response channel:

```text
EMAIL / WEB_PORTAL / LETTER
    -> BODY: or ATTACHMENT:

PHONE_CALL
    -> CALL_NOTE:

IN_PERSON
    -> IN_PERSON_NOTE:
```

Thus a phone response cannot be cited as a document paragraph unless the relevant written material was separately captured as a document response event.

The extraction date must fall on or after the authority/site response date and no later than permission-bundle adjudication. The source response hash remains the immutable parent provenance; the evidence locator identifies the specific passage/material used for the activity-level interpretation.

`UNRESOLVED` rows do not require decision-extraction metadata because no substantive activity decision has been made.

## Condition-compatibility review

An authority can return a formally positive decision whose conditions make the registered field activity impossible. Therefore raw authorization and effective project scope are separated.

Every positive activity row must also record:

```text
conditions
conditions_compatible_with_registered_activity
conditions_review_reference
registered_activity_definition_reference
conditions_reviewed_by
conditions_review_date
conditions_review_rationale.
```

The activity definition reference must match the canonical registry:

```text
data/PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json
```

for the same activity A-F. The review date must be on or after the authority/site response date and no later than the permission-bundle adjudication date. The reviewer and rationale are required so `compatible=true` cannot be a context-free checkbox.


`conditions` must be explicit. If the authority/site states that there are no additional conditions, record:

```text
NO_ADDITIONAL_CONDITIONS
```

rather than leaving the field blank. Missing condition text is unresolved and cannot support a positive effective scope.

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

## Incoming-response provenance requirement

Every authority/site response used in a permission bundle must originate from an audited incoming-response event. Each response therefore carries:

```text
source_response_event_id
source_response_received_at
source_response_receive_channel
source_response_content_sha256
source_response_classification_review_reference.
```

The source receipt date must equal the response date, the content hash must be SHA-256, and a single incoming-response event cannot be reused as two distinct authority/site responses in the same bundle.

The outreach-to-response compiler copies these fields automatically from the validated outreach ledger. A hand-written `FILLED_AUTHORITY_RESPONSES` bundle that omits the source event provenance fails closed.

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
data/PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json
data/PEDICULARIS_WAVE1_INCOMING_RESPONSE_RECEIPT_TEMPLATE_V1.json
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
