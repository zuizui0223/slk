# SLK — Multifunctional Structures Can Persist While Barriers to Division of Labor Change

SLK asks a biological question: **when does functional conflict lead to division of labor, and when does a multifunctional structure persist instead?**

The project draws on several linked theory modules, but the modules are not the subject of the paper. Their roles are:

- [`sch`](https://github.com/zuizui0223/sch): establishes whether opposing functions genuinely conflict on a shared phenotypic coordinate and supplies the conflict quantity `L`.
- [`balance`](https://github.com/zuizui0223/balance): develops diagnostics for the region in which conflict is real but differentiated architecture is not yet favored.
- [`slk`](https://github.com/zuizui0223/slk): asks why documented conflict can remain unresolved by division of labor.
- [`bita`](https://github.com/zuizui0223/bita): separately asks which ecological mechanism generates an observed trait interaction.
- [`payoff`](https://github.com/zuizui0223/payoff): retains broader mathematical extensions used when later population or dynamical questions require them.

## Central question

> **When does functional conflict favor structural division of labor, and when does a multifunctional structure persist instead—and why can the reason for persistence change across ecological contexts?**

For the persistent-integration branch, the central result is a many-to-one mapping: the same visible multifunctional phenotype can persist behind three different evolutionary bottlenecks:

```text
adaptive integration
  Phi < 0
  the focal divided alternative has lower net value

historical / developmental trapping
  Phi > 0, g0 < 0
  a better divided state exists, but the available path is unfavorable

ecological stabilization
  Phi > 0, g0 > 0, Delta_R < 0
  division of labor is favorable and reachable, but fails when rare
```

Architecture economics, evolutionary history, and ecological interactions can therefore maintain the same morphology for different reasons. Environmental change can switch the limiting bottleneck before morphology changes, and the structural or demographic perturbation required for reorganization can shrink during that stasis. The formal comparison is candidate-relative: SLK does not rank structural division against every temporal, plastic, or alternative structural solution.

![Figure 1. One persistent phenotype can hide different evolutionary bottlenecks.](figures/FIG1_LOGIC_DIAGRAM.svg)

![Figure 2. Natural systems use different resolutions of functional conflict.](figures/FIG2_PHASE_MAP.svg)

![Figure 3. Multifunctionality can lose evolutionary resistance before morphology changes.](figures/FIG3_EMPIRICAL_LADDER.svg)

## Biological predictions

The framework now makes four natural-history predictions.

**1. Conflict strength alone should not rank the tendency toward division of labor.** A system with stronger conflict can remain integrated if little of that conflict is recoverable or if the divided architecture is costly, whereas weaker conflict can be resolved structurally when release is efficient and cheap.

**2. The same integrated morphology can persist behind different evolutionary bottlenecks across environments.** Under the ordered environmental slice, architecture value, local accessibility and rare establishment cross at different conditions. A transect can therefore remain visibly multifunctional while the state maintaining integration shifts from adaptive integration, to historical/developmental trapping, to ecological stabilization.

**3. Historical trapping and ecological stabilization predict different geographic mosaics.** Strict convex recovery creates architecture-path hysteresis: forward and reverse environmental change can retain different architectures even when frequency dependence is absent. Positive frequency dependence instead creates resident-frequency priority effects and alternative locally stable architectures; negative frequency dependence predicts stable coexistence or mixed zones.

**4. Persistence can become easier to overturn before morphology changes.** Within the historical-trapping state, the minimum favorable one-step structural release `d_J` shrinks toward zero as the accessibility boundary is approached. Under positive frequency dependence, the critical initial frequency `p_C=(eta-Phi)/(2eta)` then shrinks toward zero as rare establishment becomes possible. An apparently stable integrated phenotype can therefore become progressively more susceptible to architectural innovation, clustering, immigration or repeated origin before a visible transition occurs.

The strongest new prediction is not that hysteresis, coexistence or frequency dependence exist; all are established phenomena. It is their ordered placement within one multifunctional-to-divided architecture problem.

## Running biological example

The manuscript uses *Pedicularis rex* as a literature-based running example. Existing work documents opposing pollinator- and seed-predator-mediated selection on floral exsertion and experimentally supports a defensive role of water held by cup-like bracts. That establishes the biological motivation—real conflict in a multifunctional structure—but it does **not** yet identify why integration persists.

The important biological point is that the balance of this conflict already varies geographically: seed-predator effects change strongly among populations while the pollinator side is more consistent. The same integrated floral architecture can therefore occupy different selective environments across the species' range.

No new *P. rex* biological result is claimed by this repository.

## What the theory contributes

The mathematical machinery supports the biological theory rather than replacing it. The main contributions are:

1. a common fitness comparison `Phi=R-K` that separates conflict strength from the net value of division of labor;
2. a demonstration that positive endpoint value can coexist with a local accessibility barrier under convex recovery;
3. a population-level establishment test showing that frequency-dependent ecology can reverse the endpoint verdict when a differentiated type is rare;
4. three ways persistent integration can be maintained: adaptive integration, historical/developmental trapping, or ecological stabilization;
5. the comparative prediction that stronger conflict need not imply more differentiation;
6. the ecological prediction that profitability and rare establishment can be displaced along environmental gradients;
7. the prediction that ecological context can change the evolutionary resolution of conflict, including cases in which the same phenotype persists for different reasons across environments;
8. the prediction that phenotypic stasis can conceal declining evolutionary resistance: the structural jump and/or local frequency needed to trigger reorganization can shrink before morphology changes.

Finite-population fixation and weak-mutation occupancy remain valid **downstream extensions**. Under the specified symmetric rare-mutation exponential-Moran process, reciprocal fixation ordering and stationary monomorphic occupancy re-align at `Phi=0`. Those process results are retained because they delimit stronger evolutionary claims, not because they are a fourth explanation for persistent multifunctionality.

## Prior-art boundary

SLK does **not** claim a first theory of modularity, specialization, division of labor, pleiotropy, mutational accessibility, invasion fitness, fixation, or weak-mutation dynamics. Existing specialization theory already shows that whether division of labor is favored depends on performance curvature, trade-off structure, positional effects, synergy, and fitness mapping. Gene duplication, sexual dimorphism, and floral heteranthery provide established biological routes by which shared functions can become decoupled.

The narrower contribution is to make **the evolutionary resolution of documented functional conflict** the object to be explained: why some systems divide functions structurally, others retain integration, and why the selective state maintaining the same integrated architecture can change with environment before morphology changes.

## Biological interpretation of architecture cost

`K` is the net fitness debit of maintaining the divided architecture relative to the matched integrated comparison. Biologically, it can include additional developmental, regulatory, structural, or maintenance burdens, provided they are not already counted as lost recovered performance. Its role is simple: even severe functional conflict need not favor division of labor when the architecture that resolves it is too expensive.

## Pedicularis rex as a prospective biological test

*Pedicularis rex* remains the focal prospective system because the functional conflict is already documented: greater floral exposure improves pollen receipt but also increases seed predation, while water-filled bracts reduce seed-predator damage. The unresolved biological question is whether populations exposed to different antagonist and density regimes remain integrated because integration is adaptive, because structural release is historically constrained, or because a divided alternative would be ecologically disadvantaged when rare.

No new *P. rex* biological result is claimed here. The field programme belongs to a separate empirical companion; operational permission, outreach, access, and field logistics are not part of the flagship argument.

## Publication architecture outside the flagship

The source repositories are no longer treated as one-paper-per-repository. Their current roles are:

- **SCH — active full paper:** causal identification of functional conflict; `multifunctionality != conflict`; contextual-versus-pure-function optimum promotion gate; empirical crossed-design programme.
- **BITA — active full paper:** ecological mechanism identification after trait interaction; `interaction != mechanism`; partial-identification workflow and route synthesis.
- **PAYOFF-B — active short Note:** exact anti-phase two-patch/two-season temporal solution and unique finite migration optimum.
- **BALANCE — DOI technical module / dormant paper branch:** middle-world certification, direct worldline identification, reserve/depth/topology and persistence/hysteresis methods.
- **PAYOFF-A / spatial / topology — DOI technical modules / dormant paper branches:** continuous architecture and branching, general spatial spectral transport, and edgewise/topological extensions.

These modules may be cited by SLK without being promoted to independent manuscripts. Dormant branches can be reactivated only when they acquire a genuinely independent theorem family or decisive empirical anchor. See `docs/PAPER_ROADMAP.md`.

## Canonical reader path

For the flagship argument, the canonical path is deliberately short:

1. `manuscript/SLK_MANUSCRIPT_AMNAT_V4.md` — current journal-facing manuscript.
2. `figures/FIG1_LOGIC_DIAGRAM.svg` — one persistent phenotype mapped to distinct architecture, path, and establishment bottlenecks.
3. `figures/FIG2_PHASE_MAP.svg` — natural examples showing structural partitioning, temporal partitioning, geographic variation, frequency dependence, and ecological re-coupling.
4. `figures/FIG3_EMPIRICAL_LADDER.svg` — hidden erosion of evolutionary resistance, path hysteresis, clustered establishment, and environmental turnover of the bottleneck maintaining integration.
5. `docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md` — cross-system evidence ledger showing which real systems inform architecture value, developmental access, and rare establishment, while preserving the boundary between analogues and direct SLK gate estimates.
6. `theory/UNIFIED_THRESHOLD_ATLAS_V1.md` — full supporting mathematics, including witness families, environmental predictions, and downstream process results.
7. `theory/SLK_CORE_THEORY_V1.md` — minimal mathematical spine.
8. `docs/THEOREM_CLAIM_LEDGER_V1.md` — theorem and derived-consequence status.
9. `docs/INV1_EXECUTABLE_VALIDATION_V1.md` — independent process validation.
10. `docs/PRIOR_ART_BOUNDARY_V1.md` — novelty boundary.
11. `docs/REPOSITORY_SCOPE_BOUNDARY_V1.md` — theory-core versus empirical-companion boundary.

Pedicularis execution documents are retained for provenance during migration but are not part of the canonical reader path.

## Current status

```text
FLAGSHIP_MANUSCRIPT_V4_ACTIVE
GENERAL_PHI_EQUALS_R_MINUS_K_SPINE_DEFINED
UNIFIED_CRITICAL_SURFACE_ATLAS_REGISTERED
ONE_FAMILY_WITNESS_SYSTEM_REGISTERED
FIXATION_OCCUPANCY_INVARIANT_REGISTERED
ECOLOGICAL_THRESHOLD_DISPLACEMENT_REGISTERED
ENVIRONMENTAL_PERSISTENCE_BARRIER_TURNOVER_REGISTERED
ARCHITECTURE_PATH_HYSTERESIS_REGISTERED
HIDDEN_RESISTANCE_EROSION_REGISTERED
FREQUENCY_DEPENDENT_SPATIAL_OUTCOMES_REGISTERED
NATURAL_SYSTEM_RESOLUTION_SYNTHESIS_REGISTERED
EMPIRICAL_BRIDGE_EVIDENCE_LEDGER_REGISTERED
PEDICULARIS_PROSPECTIVE_ANCHOR_REGISTERED
PEDICULARIS_REAL_DATA_G1_G5_RECEIPTS_ZERO
PEDICULARIS_OPERATIONS_COMPANION_BOUNDARY_REGISTERED
PEDICULARIS_OPERATIONS_FLAGSHIP_GROWTH_CI_BLOCKED
PEDICULARIS_OPERATIONS_DELETION_FOR_MIGRATION_ALLOWED
EMPIRICAL_COMPANION_160_FILE_MANIFEST_FROZEN
EMPIRICAL_COMPANION_DESTINATION_VERIFICATION_REQUIRED_BEFORE_PRUNING
AMNAT_REFOCUSED_REVIEW_PACKAGE_BUILD_PASS
AMNAT_RENDERED_LAYOUT_QA_PASS_28_28
AMNAT_REVIEWER_ZIP_READY_CURRENT
AMNAT_ZENODO_ARCHIVE_PAYLOAD_READY_CURRENT
AMNAT_PORTAL_READINESS_GATE_REGISTERED
AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT_READY_CURRENT
AMNAT_INTERNAL_BLOCKERS_NONE
EMPIRICAL_CLAIM_CEILING_UNCHANGED
```

## Journal decision rule

The present flagship target remains **The American Naturalist**. The end-to-end Pedicularis machinery improves credibility and executability but does not itself raise the empirical claim ceiling.

Reassess an **Ecology Letters** submission only after a real same-system G1-G5 receipt exists. The strongest trigger is a sharp biological separation such as:

```text
L > 0
R > 0
Phi < 0
```

or, after one focal G1-G5 context has already closed, a prospectively registered environmental crossing of `Phi = 0`.

SLK does not turn theoretical quantities or prospective protocols into empirical measurements by declaration. Any empirical use of `L`, `R`, `s`, `K`, `Phi`, accessibility, invasion, fixation, or occupancy must retain the identification requirements and uncertainty of the source analysis.
