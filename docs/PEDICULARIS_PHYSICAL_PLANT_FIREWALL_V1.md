# Pedicularis physical-plant identity firewall v1

Status: **PROSPECTIVE / EXECUTABLE UNIT-IDENTITY CONTRACT / NO BIOLOGICAL RESULT**.

## 1. Why this firewall exists

SLK requires several Pedicularis cohorts to be biologically independent:

~~~text
Y-CAL
D0-CAL
D0 confirmatory qualification
G3-G5 decomposition
optional independent direct-Phi block
and, where relevant, external SCH G1-G2 experimental units.
~~~

Dataset-local assignment identifiers such as YCAL-001, D0L-001, D0Q-L-001 or G35-L-001 cannot prove that these are different physical plants. The same plant could be renamed in a later dataset and silently violate the independence firewall.

Therefore every physical plant used in the programme receives a permanent field tag.

## 2. Two identifiers with different jobs

~~~text
plant_id
    dataset-local analysis/randomization identifier

physical_plant_tag
    permanent identity of the real plant in the field
~~~

Rules:

1. plant_id may differ across datasets.
2. physical_plant_tag must never change for the same real plant.
3. one plant_id may have multiple flower/treatment rows, but all must carry the same physical_plant_tag.
4. one physical_plant_tag may map to only one plant_id within a dataset.
5. any reuse of a previously forbidden physical tag in a later confirmatory cohort is a hard error.

The physical tag should be attached to the plant before outcomes are opened and should not encode the treatment assignment.

## 3. Calibration field workflow

The Y-CAL and D0-CAL generated CSVs now contain a blank physical_plant_tag field.

After recruitment and before outcome measurement:

~~~text
attach / verify a permanent field tag on each recruited plant
-> copy that tag into every registered row for that plant
-> do not derive the tag from the dataset-local plant_id
-> validate the calibration layout
-> build the cross-cohort physical registry.
~~~

Build a registry with:

~~~bash
python scripts/build_pedicularis_physical_plant_registry.py \
  --context-id <context> \
  --population-id <population> \
  --season-id <season> \
  --cohort YCAL=PEDICULARIS_Y_CAL_FIELD_V1.csv \
  --cohort D0CAL=PEDICULARIS_D0_CAL_FIELD_V1.csv \
  --output PEDICULARIS_PHYSICAL_PLANT_REGISTRY_CALIBRATION_V1.json
~~~

The registry rejects one assignment id mapped to multiple physical tags, one physical tag hidden behind multiple assignment ids, physical-tag overlap across cohorts, and context/population/season mismatch.

## 4. Hash-locked handoff to the next cohort

The registry exports all_prior_physical_plant_tags, all_prior_tag_set_sha256 and next_stage_firewall_block.

Copy the exported firewall block into the next prospective freeze. The freeze records both the forbidden tag list and its SHA256. The analyzer recomputes the hash and fails if the list changes after freezing.

The hash is an integrity receipt; it is not a privacy or cryptographic anonymization claim.

## 5. D0 confirmatory qualification

PEDICULARIS_D0_CONFIRMATORY_ANALYSIS_FREEZE_V1 now requires a physical_unit_firewall block.

The generated confirmatory field sheet includes a blank physical_plant_tag field. After recruitment, but before confirmatory outcomes, fill every physical tag, verify the one-to-one mapping and verify no tag occurs in the frozen prior calibration registry.

The D0 adjudicator refuses missing physical tags, assignment ids mapped to multiple physical tags, a physical tag hidden behind multiple assignment ids, or any physical tag present in the frozen prior-tag set. The D0 receipt records the current cohort tag-set hash.

## 6. G3-G5 effect experiment

The G3-G5 freeze likewise carries a physical_unit_firewall.

Its forbidden set should contain all physical plants that are ineligible for G3-G5 effect estimation, including at minimum Y-CAL, D0-CAL, D0 confirmatory qualification, structural-y function calibration units and any same-context G1-G2 units that the external SCH programme declares effect-estimation-ineligible.

For the optional independent direct-Phi route the adjudicator additionally requires:

~~~text
decomposition physical tags
intersect
direct-Phi physical tags
=
empty set.
~~~

This check uses physical_plant_tag, not the dataset-local plant_id.

## 7. External G1-G2 / SCH units

SLK does not own the SCH raw-data schema. If G1-G2 units come from another repository, their permanent plant tags must nevertheless be exported into the SLK prior-tag registry or equivalent frozen forbidden-tag list before G3-G5 recruitment.

A prose statement that the cohorts are independent is not a substitute for the tag receipt when tags are available.

## 8. What the firewall proves

The executable firewall can establish that registered physical plants are disjoint across the supplied cohorts.

It does not establish random sampling from the population, absence of spatial kinship, absence of shared maternal family, biological independence of flowers within one plant, or correct treatment execution.

## 9. Canonical implementation

~~~text
scripts/pedicularis_physical_units.py
scripts/build_pedicularis_physical_plant_registry.py
tests/test_pedicularis_physical_units.py
scripts/generate_pedicularis_d0_confirmatory_layout.py
scripts/adjudicate_pedicularis_d0_confirmatory.py
scripts/generate_pedicularis_g3_g5_layout.py
scripts/adjudicate_pedicularis_g3_g5_effect.py
~~~

## 10. Claim ceiling

~~~text
PHYSICAL_UNIT_DISJOINTNESS_ONLY
NO_BIOLOGICAL_GATE_RESULT
NO_CAUSAL_EFFECT_RESULT
~~~
