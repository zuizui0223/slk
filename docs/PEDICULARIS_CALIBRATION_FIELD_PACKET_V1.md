# Pedicularis calibration field packet v1

Status: **PROSPECTIVE / LAYOUT GENERATOR REGISTERED / NO FIELD DATA CLAIMED**.

## 1. Purpose

This packet turns the unified calibration programme into a reproducible field layout for the two registered calibration cohorts:

```text
Y-CAL   36 independent plants x 3 flowers
D0-CAL  24 LOW-Y plants x 3 flowers
        24 HIGH-Y plants x 2 flowers.
```

The generator freezes plant/flower identifiers and D0 treatment-slot assignment using a declared randomization seed. The validator checks cohort size, treatment completeness, context identity, and the calibration/confirmatory firewall.

No generated row is a biological observation until field measurements are entered.

## 2. Generate the field packet

Run:

```bash
python scripts/generate_pedicularis_calibration_layout.py \
  --context-id <population-season-protocol-id> \
  --population-id <population-id> \
  --season-id <season-id> \
  --randomization-seed <integer> \
  --output-dir <field-packet-directory>
```

Outputs:

```text
PEDICULARIS_Y_CAL_FIELD_V1.csv
PEDICULARIS_D0_CAL_FIELD_V1.csv
PEDICULARIS_CALIBRATION_LAYOUT_METADATA_V1.json
```

Commit the metadata and assignment files before opening treatment outcomes if the packet is to become the registered field allocation.

## 3. Y-CAL layout

Default floor:

```text
36 independent plants
3 focal flowers per plant
108 rows.
```

Every generated row begins as:

```text
dataset_id = PED_Y_CAL_V1
phenotype_stratum = UNCLASSIFIED_Y_CAL
treatment = Y_CAL_REPEATED_MEASUREMENT
calibration_roles = UC1_GEOMETRY;UC2_RETENTION
confirmatory_eligible = false.
```

The three flower slots are placeholders for distinct focal flowers. Record actual `whorl_id`, flowering date, and block at field assignment.

The default roles do not prevent adding prospectively compatible UC3/UC4 measurements to distinct calibration-only flowers. If additional flowers are added, retain the same plant cluster and `confirmatory_eligible=false`.

## 4. D0-CAL layout

Default floor:

```text
24 LOW-Y plants
24 HIGH-Y plants
48 independent plants total
120 focal rows.
```

LOW-Y plants receive one flower each assigned to:

```text
S_CAL
SHAM_CAL
D0_CAL
```

HIGH-Y plants receive one flower each assigned to:

```text
D_CAL
D_DRAIN_CAL.
```

Within each plant, treatment order across numbered flower slots is randomized using the frozen seed. The same seed reproduces the same assignment exactly.

The seed randomizes slots; it does not justify choosing phenotype strata after outcome inspection. LOW-Y/HIGH-Y recruitment must still follow the independently frozen Y-CAL structural-y rule.

## 5. Core columns

The generated CSVs include identifiers, allocation metadata, and blank measurement fields covering:

```text
plant / flower / whorl / block
flower length / bract height / exsertion
opening width / stigma position / orientation
mechanical condition
retention magnitude / depth / half-life / leakage / protected fraction
pollinator visits / handling / pollen receipt / initial seed set
anthesis / pollination-window / first-attack / ovary-swelling timing
early attack / seed predation
mature viable undamaged seeds.
```

The wide format is deliberate for field use. Later analysis may reshape to long format, but raw IDs and treatment labels must remain unchanged.

## 6. Calibration firewall

Every generated row has:

```text
confirmatory_eligible = false.
```

Changing this flag to true does not promote the observation. The layout validator treats it as an error.

Calibration plants may inform:

```text
measurement repeatability
natural range
sensitivity functions
equivalence-margin derivation
pilot SD / ICC
sample-size planning.
```

They may not enter:

```text
Qz/Qp/Qg qualification effects
G1 causal conflict surface
G2 L
D0 confirmatory qualification
G3 R
G4 K
G5 Phi.
```

## 7. Validate before field use

Run:

```bash
python scripts/validate_pedicularis_calibration_layout.py \
  PEDICULARIS_Y_CAL_FIELD_V1.csv \
  PEDICULARIS_D0_CAL_FIELD_V1.csv
```

The validator requires:

```text
Y-CAL >= 36 independent plants
Y-CAL >= 3 rows / plant
D0-CAL >= 24 LOW-Y plants
D0-CAL >= 24 HIGH-Y plants
complete LOW-Y S/SHAM/D0 treatment set per plant
complete HIGH-Y D/D-drain treatment set per plant
unique flower IDs
Y-CAL and D0-CAL plant IDs disjoint
one matching context/population/season
one recorded D0 randomization seed
all assignments frozen
all rows confirmatory-ineligible.
```

A valid result is only:

```text
CALIBRATION_LAYOUT_VALIDATED
```

with claim ceiling:

```text
LAYOUT_ONLY_NO_CALIBRATION_OR_BIOLOGICAL_GATE_RESULT.
```

## 8. Measurement-order rule

Where multiple UC roles are recorded on one flower, use only prospectively compatible non-destructive measurements before any manipulation with carryover.

Preferred order:

```text
1. identifiers / geometry
2. pre-treatment pollination-facing observations where applicable
3. treatment / apparatus assignment
4. retention / water measurements
5. antagonist observations
6. reproductive follow-through.
```

Do not perform repeated wetting, drainage, bending, or apparatus manipulations before a measurement that is supposed to represent the undisturbed state.

## 9. Missing flowers and replacement

A flower lost before any treatment/outcome is observed may be replaced under a prospectively declared replacement rule.

After treatment outcome information is available, do not selectively replace failed flowers to restore balance. Record the failure and handle it under the predeclared missingness rule.

If plant-level attrition reduces the independent-plant floor below the registered requirement, the calibration cohort is incomplete until additional plants are recruited under the same prospective rule.

## 10. Relationship to precision planning

The field packet is upstream of the margin/variance compiler:

```text
field packet
-> Y-CAL / D0-CAL measurements
-> biological-margin freeze + independent variance receipt
-> compile_pedicularis_d0_precision_input.py
-> plan_pedicularis_y_d0_precision.py
-> confirmatory allocation freeze.
```

The randomization seed and raw calibration IDs should be carried into every later variance/provenance receipt.

## 11. Immediate executable action

Before a real field season:

```text
1. choose focal Pedicularis population-season
2. assign context_id
3. freeze randomization seed
4. generate field packet
5. validate layout
6. commit packet / metadata
7. collect calibration measurements without opening confirmatory outcomes.
```

At that point the Pedicularis programme has crossed from a conceptual experimental design into a reproducible field-ready calibration workflow, while the biological G1-G5 claim ceiling remains unchanged until real data are collected.
