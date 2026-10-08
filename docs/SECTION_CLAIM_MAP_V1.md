# SLK manuscript section-to-claim map V3

This document maps the biology-refocused journal manuscript to the canonical theorem-claim ledger. The manuscript is organized around a biological result: one persistent multifunctional phenotype can be maintained by different evolutionary bottlenecks, and the limiting bottleneck can turn over before morphology changes. The theory supports that claim; it is not the manuscript's subject.

## Section map

| Manuscript section | Claim IDs / evidence role | Primary biological role | Claim ceiling |
|---|---|---|---|
| Abstract | C1-C7, UTA1.4c, UTA1.4e-f, UTA1.5, UTA1.10 | state hidden bottleneck turnover and the joint architecture-frequency escape frontier | conditional prediction; no completed natural-system turnover claimed |
| 1. Introduction | C1-C7, UTA1.4c/e, UTA1.10 + prior art | pose persistence of multifunctionality as the biological problem | do not claim first theory of specialization, system drift, hysteresis, or invasion |
| 2. Functional conflict creates the problem, not its resolution | C1 | separate documented conflict from its evolutionary resolution | conflict magnitude does not identify the favored organization |
| 3. Natural systems show multiple resolutions of functional conflict | literature synthesis + `docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md` | establish biological reality of structural, temporal, integrated, frequency-dependent, and re-coupled outcomes, and map empirical systems onto distinct SLK decision layers | component plausibility and cross-system bridges only; no analogue is promoted to a direct gate estimate without a matching estimand |
| 4. When is retaining multifunctionality favored over a structural alternative? | C2-C5, UTA1.5 | define candidate-relative architecture value, `Phi=R-K`, and conflict/differentiation discordance | `Phi<0` favors integration only relative to the specified divided alternative |
| 5. When can evolutionary history preserve multifunctionality? | C6, UTA1.4d, UTA1.4e | separate endpoint value from local path accessibility and derive path legacy | small-step path result; no claim of absolute historical impossibility |
| 6. How can ecology stabilize multifunctionality? | C7, UTA1.2, UTA1.8 | add rare-type establishment and frequency-dependent ecology | canonical linear frequency map is illustrative; endpoint invasion is the general criterion |
| 7. Three evolutionary bottlenecks behind one persistent phenotype | UTA1.10 | map architecture value, path accessibility, and rare establishment onto one visible outcome | the three bottlenecks are not exhaustive causes of persistence |
| 8. Formal backbone | UTA1, NE1-NE3 | provide the minimal model needed for the biological argument | fuller fixation/occupancy machinery remains supporting theory |
| 9. Ecological and evolutionary consequences | UTA1.4c, UTA1.4d, UTA1.4e, UTA1.4f, UTA1.5 | derive bottleneck turnover, hysteresis, the architecture-frequency escape frontier, and comparative discordance | `E_V<E_A` follows under the declared cost-lowering convex slice; frontier slice identities and environmental erosion hold across positive identity-preserving feedback scalings, while monotonic novelty-abundance compensation additionally uses proportional scaling |
| 10. Discussion | synthesis + prior-art boundary + empirical bridge ledger | distinguish selective-bottleneck turnover from system drift and state empirical status | no claim that phenotypic constancy hiding mechanism change is new; no natural system yet closes the full ordered turnover |

## Reader-facing biological spine

```text
documented functional conflict
        |
        v
does the focal divided architecture repay its cost?       Phi = R-K
        |
        +-- no -> architecture-value bottleneck
        |
        v
is movement toward the higher-value state locally uphill? g0 = R'(0)-k
        |
        +-- no -> evolutionary-path bottleneck
        |
        v
can the divided type increase when rare?                  Delta_R
        |
        +-- no -> ecological-establishment bottleneck
        |
        v
the three early bottlenecks are excluded
```

All three failures can produce the same visible outcome: persistent multifunctionality.

## Environmental turnover claim

Along the registered cost-lowering environmental slice,

```text
k(E)=k0-c(E-E0), c>0
```

strict convexity forces

```text
E_V < E_A.
```

This ordering is a derived consequence of the recovery geometry, not an imposed ordering of labels.

A distinct ecology-only persistence interval occurs only when

```text
Delta_R(E_A) < 0.
```

For the canonical constant-`eta` pair this is equivalent to

```text
eta > dmax (k_global-k_local),
```

which yields

```text
E_V < E_A < E_I.
```

Thus the full architecture -> path -> ecology sequence is a conditional biological prediction, not a universal law.

## Escape-frontier claim

Under the registered constant-positive-feedback extension,

```text
p_escape(d)
=
1/2-[R(d)-kd]/(2eta).
```

The earlier thresholds become orthogonal slices:

```text
p_escape(d_J)=1/2
p_escape(dmax)=p_C.
```

Thus structural novelty and demographic support can compensate for one another. Lowering architecture cost shifts the whole frontier toward smaller release and/or lower initial frequency before visible structural reorganization.

The headline claim is therefore not merely that identical phenotypes can have different hidden mechanisms or that traits interact with propagule pressure. Those are established ideas. SLK predicts that the **selective bottleneck preventing a specified alternative architecture from replacing an unchanged resident architecture can turn over**, while the viable combinations of architectural and demographic perturbation expand along a model-specific escape frontier.

### Empirical evidence surface

`docs/EMPIRICAL_BRIDGE_EVIDENCE_V1.md` is the canonical evidence ledger for cross-system support. It separates: field selection mosaics under persistent integration; direct or adjacent architecture-value experiments; developmental-accessibility anchors; rare-establishment analogues against generalist residents; and positive controls in which value, access, and rare-type performance are all permissive.

The ledger is deliberately stricter than a narrative literature review. A system can support one SLK decision layer without being promoted to `Phi`, `g0`, or `Delta_R`, and an unresolved invasion treatment remains unresolved rather than being classified as failure.

## Natural-history evidence boundary

The manuscript's natural systems establish component facts:

- functional conflict has structural and temporal resolutions;
- structural differentiation need not equal functional division of labor;
- ecological partners can alter presentation and selection;
- rarity can be advantageous or disadvantageous;
- multifunctional architectures can experience geographic selection mosaics;
- anatomical decoupling can remain ecologically re-coupled.

They do not establish that one natural lineage has already crossed all three SLK bottlenecks in order. That remains the prospective empirical test.

## Theory support retained outside the manuscript foreground

The full theory repository still contains:

- NE4-NE5 fixation/occupancy witnesses;
- INV1;
- UTA1.4b environmental feedback-gradient extensions;
- UTA1.6-UTA1.9 frequency-response identification and endpoint-certification machinery;
- UTA1.11 interval-compatible state propagation.

These remain valid support and downstream extensions. Their presence does not make them the biological subject of the manuscript.

## Endpoint-exclusion versus resident-persistence audit

The manuscript's three labels `Phi`, `g0`, and `Delta_R` diagnose the status of a **specified completed** divided alternative. They do not prove that an integrated population remains dynamically stable against all accessible partial variants. The continuous model demonstrates both outcomes: proportional feedback and convex recovery transmit full-endpoint exclusion to every partial degree, while superlinear feedback allows partial invasion despite failure of the full endpoint. Thus the `E_V<E_A<E_I` ordering is an ordering of reference criteria; evidence of unchanged realized morphology also requires ecological fitness of reachable partial alternatives and the evolutionary history of their appearance. Proof and test: `theory/ENDPOINT_EXCLUSION_VS_PERSISTENCE_V1.md` and `tests/test_endpoint_exclusion_vs_persistence.py`.

## Manuscript rule

Any substantive future manuscript claim must map to an existing claim ID, be explicitly marked literature synthesis or interpretation, or receive a new ledger ID before promotion. The journal-facing manuscript may simplify notation but may not strengthen the registered theory, the natural-history evidence, or the empirical ceiling.
