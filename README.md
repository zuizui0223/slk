# SLK — Why Multifunctional Structures Persist under Conflicting Selection

SLK asks a biological question: **when does functional conflict lead to division of labor, and when does a multifunctional structure persist instead?**

The project draws on several linked theory modules, but the modules are not the subject of the paper. Their roles are:

- [`sch`](https://github.com/zuizui0223/sch): establishes whether opposing functions genuinely conflict on a shared phenotypic coordinate and supplies the conflict quantity `L`.
- [`balance`](https://github.com/zuizui0223/balance): develops diagnostics for the region in which conflict is real but differentiated architecture is not yet favored.
- [`slk`](https://github.com/zuizui0223/slk): asks why documented conflict can remain unresolved by division of labor.
- [`bita`](https://github.com/zuizui0223/bita): separately asks which ecological mechanism generates an observed trait interaction.
- [`payoff`](https://github.com/zuizui0223/payoff): retains broader mathematical extensions used when later population or dynamical questions require them.

## Central question

> **Why can the same outcome—persistent multifunctionality—remain after strong functional conflict?**

SLK separates three biological explanations.

```text
documented functional conflict
          |
          v
would division of labor pay?
          |
   Phi = R - K
      /       \
 Phi < 0     Phi > 0
    |           |
cause 1         v
does not pay   can a fitter state be reached?
                    /       \
                 no          yes
                 |            |
              cause 2         v
          local barrier     can it establish when rare?
                                /       \
                              no         yes
                              |           |
                           cause 3    early causes excluded
```

The three causes are:

1. **Differentiation does not pay.** Conflict is real, but the recoverable benefit `R` is too small relative to architecture cost `K`, so `Phi=R-K<0`.
2. **A fitter differentiated state is locally difficult to reach.** `Phi>0`, but sufficiently small changes away from integration are selected against.
3. **A favorable and reachable differentiated type cannot establish when rare.** Frequency-dependent ecology reverses the fitness verdict at low frequency.

These states can look identical if one only observes that the structure remains multifunctional.

![Figure 1. Three causes of persistent multifunctionality under functional conflict.](figures/FIG1_LOGIC_DIAGRAM.svg)

![Figure 2. Natural systems use different resolutions of functional conflict.](figures/FIG2_PHASE_MAP.svg)

![Figure 3. Architecture value, accessibility and establishment can cross under different conditions.](figures/FIG3_EMPIRICAL_LADDER.svg)

## Biological predictions

The framework makes two primary predictions.

**Conflict strength alone should not rank the tendency toward division of labor.** Two systems with different conflict loads can reverse their ordering in differentiation if they differ in how much conflict can be released or in the cost of the alternative architecture.

**The reason for persistence can change before the phenotype does.** If environment progressively lowers the marginal cost of architectural release, strict convexity makes profitability cross before local reachability. With sufficiently strong positive frequency feedback, rare establishment crosses later still. A transect can therefore remain visibly multifunctional while the limiting explanation changes from negative net value, to local inaccessibility, to rare-establishment failure.

**Profitability and establishment can occur at different ecological conditions.** Along an environmental gradient, the point where differentiated architecture first has positive net value need not be the point where a rare differentiated type can spread. In the local canonical model the displacement is

```text
E_I - E_V = eta / a.
```

The sign of frequency dependence determines whether rare establishment is delayed beyond or advanced ahead of the architecture-value crossing.

## Running biological example

The manuscript uses *Pedicularis rex* as a literature-based running example. Existing work documents opposing pollinator- and seed-predator-mediated selection on floral exsertion and experimentally supports a defensive role of water held by cup-like bracts. That establishes the biological motivation—real conflict in a multifunctional structure—but it does **not** yet identify why integration persists.

The important biological point is that the balance of this conflict already varies geographically: seed-predator effects change strongly among populations while the pollinator side is more consistent. The same integrated floral architecture can therefore occupy different selective environments across the species' range.

No new *P. rex* biological result is claimed by this repository.

## What the theory contributes

The mathematical machinery supports the biological diagnosis rather than replacing it. The main contributions are:

1. a common fitness comparison `Phi=R-K` that separates conflict strength from the net value of division of labor;
2. a demonstration that positive endpoint value can coexist with a local accessibility barrier under convex recovery;
3. a population-level establishment test showing that frequency-dependent ecology can reverse the endpoint verdict when a differentiated type is rare;
4. a three-way diagnosis of persistent multifunctionality into failure of value, reachability, or establishment;
5. the comparative prediction that stronger conflict need not imply more differentiation;
6. the ecological prediction that profitability and rare establishment can be displaced along environmental gradients;
7. the prediction that ecological context can change the evolutionary resolution of conflict, including cases in which the same phenotype persists for different reasons across environments.

Finite-population fixation and weak-mutation occupancy remain valid **downstream extensions**. Under the specified symmetric rare-mutation exponential-Moran process, reciprocal fixation ordering and stationary monomorphic occupancy re-align at `Phi=0`. Those process results are retained because they delimit stronger evolutionary claims, not because they are a fourth explanation for persistent multifunctionality.

## Prior-art boundary

SLK does **not** claim a first theory of modularity, specialization, division of labor, pleiotropy, mutational accessibility, invasion fitness, fixation, or weak-mutation dynamics. Existing specialization theory already shows that whether division of labor is favored depends on performance curvature, trade-off structure, positional effects, synergy, and fitness mapping. Gene duplication, sexual dimorphism, and floral heteranthery provide established biological routes by which shared functions can become decoupled.

The narrower contribution is to make **the evolutionary resolution of documented functional conflict** the object to be explained: why some systems divide functions structurally, others retain integration, and ecological context can shift the balance among these outcomes.

## Architecture cost K

`K` is the net optimized fitness debit attributable to the differentiated architecture relative to its matched pre-cost comparison, on the same fitness scale and time horizon as `R`. It is comparison-specific rather than a universal physiological quantity. Empirical use must declare comparison states, scale, time horizon, included/excluded cost channels, uncertainty, and how double counting with `R` was prevented. See `docs/K_OPERATIONAL_DEFINITION_V1.md`.

## Empirical anchor and repository boundary

The first prospectively registered same-system empirical anchor is `Pedicularis rex`. Its role is to test whether the abstract ladder can be closed in one biological system:

```text
identified conflict
-> L
-> R
-> K
-> Phi
-> stronger realization claims only with their additional measurements
```

The current biological claim ceiling is unchanged: **no real Pedicularis G1-G5 receipt has yet been produced**. Design readiness is not empirical closure.

Candidate-specific permission, outreach, access, scouting, field-packet, receipt, and handoff machinery is operational support rather than part of the flagship theory contribution. New operational machinery should be developed in a Pedicularis empirical companion unless it changes an SLK estimand, theorem, generic measurement gate, or manuscript claim ceiling. The migration rule is frozen in `docs/REPOSITORY_SCOPE_BOUNDARY_V1.md`.

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
2. `figures/FIG1_LOGIC_DIAGRAM.svg` — three evolutionary states behind persistent multifunctionality.
3. `figures/FIG2_PHASE_MAP.svg` — natural examples showing structural partitioning, temporal partitioning, geographic variation, frequency dependence, and ecological re-coupling.
4. `figures/FIG3_EMPIRICAL_LADDER.svg` — profitability, reachability, rare establishment, and environmental turnover of the state maintaining integration.
5. `theory/UNIFIED_THRESHOLD_ATLAS_V1.md` — full supporting mathematics, including witness families, environmental predictions, and downstream process results.
6. `theory/SLK_CORE_THEORY_V1.md` — minimal mathematical spine.
7. `docs/THEOREM_CLAIM_LEDGER_V1.md` — theorem, derived-consequence, diagnostic, and empirical-handoff status.
8. `docs/INV1_EXECUTABLE_VALIDATION_V1.md` — independent process validation.
9. `docs/PRIOR_ART_BOUNDARY_V1.md` — novelty boundary.
10. `docs/REPOSITORY_SCOPE_BOUNDARY_V1.md` — theory-core versus empirical-companion boundary.

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
FINITE_FREQUENCY_ENDPOINT_CERTIFICATION_REGISTERED
UTA1_10_GATE_LOCALIZATION_REGISTERED
UTA1_11_INTERVAL_COMPATIBLE_STATE_SET_REGISTERED
NATURAL_SYSTEM_RESOLUTION_SYNTHESIS_REGISTERED
PEDICULARIS_PROSPECTIVE_ANCHOR_REGISTERED
PEDICULARIS_REAL_DATA_G1_G5_RECEIPTS_ZERO
PEDICULARIS_OPERATIONS_COMPANION_BOUNDARY_REGISTERED
PEDICULARIS_OPERATIONS_FLAGSHIP_GROWTH_CI_BLOCKED
PEDICULARIS_OPERATIONS_DELETION_FOR_MIGRATION_ALLOWED
EMPIRICAL_COMPANION_160_FILE_MANIFEST_FROZEN
EMPIRICAL_COMPANION_DESTINATION_VERIFICATION_REQUIRED_BEFORE_PRUNING
AMNAT_REFOCUSED_REVIEW_PACKAGE_BUILD_PASS
AMNAT_FULL_PAGE_REVIEW_QA_REOPENED_AFTER_REFOCUS
AMNAT_REVIEWER_ZIP_REBUILD_REQUIRED
AMNAT_ZENODO_ARCHIVE_PAYLOAD_REBUILD_REQUIRED
AMNAT_PORTAL_READINESS_GATE_REGISTERED
AMNAT_EDITORIAL_MANAGER_UPLOAD_KIT_REBUILD_REQUIRED
AMNAT_INTERNAL_BLOCKER_REBUILD_SUBMISSION_PACKAGE
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
