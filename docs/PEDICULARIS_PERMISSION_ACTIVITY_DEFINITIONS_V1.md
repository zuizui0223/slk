# Pedicularis permission activity-definition registry v1

Status: **CANONICAL ACTIVITY SEMANTICS / HASH-LOCKED CONDITION REVIEW INPUT / NO PERMISSION RESULT**.

## Purpose

Permission condition compatibility is meaningful only relative to a stable definition of the activity being reviewed.

A symbolic reference such as:

```text
SLK_PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1#C
```

is not sufficient by itself if the underlying definition could later change while the reference string remains unchanged.

Therefore every positive permission-condition review is bound to both:

```text
registered_activity_definition_reference
registered_activity_definition_sha256
registered_activity_registry_sha256
registered_activity_definition_hash_algorithm
```

with:

```text
registered_activity_definition_hash_algorithm = SHA256_CANONICAL_JSON_V1.
```

## Canonical registry

```text
data/PEDICULARIS_PERMISSION_ACTIVITY_DEFINITIONS_V1.json
scripts/pedicularis_permission_activity_definitions.py
```

The canonical activity inventory is A-F.

A-C define the default non-destructive recovery/P0 scope.

D-F are destructive optional activities and require separate permission when used.

## Hash semantics

For each activity, SHA-256 is calculated over canonical JSON containing:

```text
activity_id
label
definition_reference
registered_definition
destructive
required_for_default_recovery_p0_scope
```

with sorted keys and compact JSON separators.

A second SHA-256 is calculated over the canonical A-F registry.

Thus a condition review is valid only for the exact activity semantics that were reviewed.

If a registered activity definition changes:

```text
old condition review hash
!=
current canonical definition hash
```

and adjudication fails closed.

The review must be redone against the updated activity definition.

## Relationship to authority responses

The activity-definition hash is an internal project provenance field. It is not supplied by, and must not be attributed to, the authority or site manager.

The authority supplies:

```text
decision
response reference
validity
conditions.
```

The project supplies the later condition-compatibility review and its hash-locked activity definition.

## Claim ceiling

```text
ACTIVITY_DEFINITION_PROVENANCE_ONLY
NO_PERMISSION_GRANTED
NO_FRESH_CONTEXT
NO_P0_SIGNAL
NO_G1_G5_RESULT
```
