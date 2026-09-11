# SLK Am Nat reviewer-risk audit V1

This audit asks how a skeptical theory/evolution reviewer could reject the SLK flagship and what must still change before submission.

## Bottom line

The manuscript is viable only if novelty is framed as an **architecture-specific integration theorem and measurement hierarchy**, not as a first theory of trade-offs, modularity, specialization, evolvability, evolutionary games, fixation, or weak-mutation stationary dynamics.

The strongest publishable object is now

```text
identified conflict budget L
-> recoverable architecture benefit R
-> general architecture margin Phi=R-K
-> local accessibility
-> rare invasion
-> fixation criteria
-> weak-mutation occupancy
```

with `R=sL` retained only as the registered quadratic partial-release corollary, explicit constructive separations at selected transitions, and an exact fixation-occupancy invariant under declared process assumptions.

## Risk 1 — prior art already explains why modularity/specialization can be favored

### Reviewer attack

"Conflict among functions favoring modularity or specialization is old. Why is this not a re-parameterized cost-benefit model?"

### Current response

The Introduction now explicitly acknowledges Wagner & Altenberg (1996) and Rueffler, Hermisson & Wagner (2012) as antecedents. It also acknowledges Taylor et al. (2004) and Fudenberg et al. (2006) for invasion/fixation and weak-mutation population theory. SLK no longer claims novelty for the generic statement that specialization resolves functional conflict or that population criteria differ.

The claimed novelty is restricted to:

1. one estimand transport beginning from an identified shared-coordinate conflict receipt;
2. the general handoff `Phi=R-K`;
3. architecture-specific constructive split witnesses;
4. the exact placement of a fixation-occupancy invariant inside the hierarchy;
5. the G1-G9 empirical claim ceiling.

### Status

**REDUCED TO MEDIUM.** The obvious framing blocker is closed; exhaustive neighboring-literature audit remains.

## Risk 2 — the central theorem could look like a collection of standard observations

### Reviewer attack

"Of course optimality, accessibility, invasion, fixation, and stationary abundance are different concepts."

### Current response

The theorem is no longer sold as a verbal observation. `theory/NON_EQUIVALENCE_THEOREM_V1.md` gives explicit architecture-specific witness regimes, while Figure 1 shows both split points and the exact re-alignment under INV1. Figure 2 prevents false projection of accessibility/invasion onto the same `L-Phi` plane, and Figure 3 maps the theory to empirical claim ceilings.

### Status

**MEDIUM.** Substantially improved; remaining risk is whether reviewers regard the integrated mapping itself as sufficiently conceptually important.

## Risk 3 — `R=sL` is model specific

### Reviewer attack

"The flagship appears to depend on a quadratic identity that need not hold generally."

### Current response

Closed. The manuscript now uses

```text
Phi=R-K
```

as the general architecture identity and presents

```text
R=sL
```

strictly as the quadratic partial-release corollary. The general hierarchy is

```text
L -> R -> Phi=R-K -> accessibility -> invasion -> fixation -> occupancy.
```

Section map, ownership, provenance, and README use the same boundary.

### Status

**RESOLVED for framing/generalization.** Any future occurrence of `R=sL` must explicitly carry the quadratic qualification.

## Risk 4 — `K` is biologically underdefined

### Reviewer attack

"Developmental, maintenance, regulatory, and mutational costs are not interchangeable. What exactly is K?"

### Current response

Closed at the theoretical-definition level. `docs/K_OPERATIONAL_DEFINITION_V1.md` defines `K` as the net optimized fitness debit attributable to the differentiated architecture relative to its matched pre-cost comparison, on the same fitness scale and time horizon as `R`. The manuscript now requires comparison states, time horizon, included/excluded channels, overlap checks with `R`, uncertainty, and bounds.

Endpoint architecture difference is explicitly treated as `R-K`, not as a direct estimate of `K`.

### Status

**RESOLVED as a definition; OPEN EMPIRICALLY.** No biological system yet provides the full registered `K` receipt.

## Risk 5 — accessibility is not identifiable from endpoint architecture comparison

### Reviewer attack

"Your accessibility result depends entirely on the chosen mutation/release coordinate."

### Current response

Agree explicitly. `Phi>0` is endpoint value. Accessibility requires a registered local neighborhood/path geometry. Figure 2 keeps accessibility outside the universal `L-Phi` classification plane.

### Status

**LOW-MEDIUM.** Correctly bounded in the manuscript.

## Risk 6 — population transport is process specific

### Reviewer attack

"The fixation and occupancy results are artifacts of an exponential Moran process and symmetric rare mutation."

### Current response

C8/C9/INV1 remain explicitly process-specific. Their role is demonstrative: adding a population process can create new separations and can also impose exact invariants. SLK does not claim the formulas are universal.

### Status

**MEDIUM.** A stronger submission could add one alternative process as a robustness/generalization test, but this is not logically required for the present theorem.

## Risk 7 — no end-to-end empirical system

### Reviewer attack

"This is a theory assembled from abstractions without a biological system that estimates L, R, K, accessibility, invasion, fixation, and occupancy."

### Current response

The manuscript makes this absence explicit. Figure 3 turns it into the G1-G9 empirical programme rather than hiding it. Formal contribution, empirical measurability, and completed empirical validation are separated.

### Status

**HIGH for any broad empirical claim; ACCEPTABLE for a clearly theoretical paper.** A complete focal system would materially strengthen the paper but is not silently assumed.

## Risk 8 — terminology may overstate novelty

Avoid unqualified phrases such as:

- "first theory of trait architecture";
- "general theory of specialization";
- "new theory of modularity";
- "universal evolutionary hierarchy".

Preferred wording:

- "integrated estimand hierarchy";
- "architecture-specific transport framework";
- "constructive split-and-invariant theorem";
- "measurement ladder connecting functional conflict to evolutionary realization".

### Status

**CONTROLLED** in current manuscript language.

## Submission-level novelty sentence

> Existing theories explain why functional interference can favor specialization or modular organization and population-genetic theory distinguishes invasion, fixation, and weak-mutation dynamics. SLK contributes one architecture-specific estimand hierarchy linking an identified shared-coordinate conflict budget to recoverable architecture value and then to evolutionary realization, with explicit parameter witnesses for where criteria separate, an exact process-level invariant where reciprocal fixation and weak-mutation occupancy re-align, and a gate-by-gate empirical claim ceiling.

## Remaining work before submission

1. Conduct a broader prior-art audit around adaptive dynamics, fitness-landscape accessibility, modularity, and stochastic evolutionary games; current four-paper boundary covers the obvious antecedents but is not exhaustive.
2. Decide whether to add an alternative population process as robustness for C8/C9/INV1 or keep those results explicitly exemplar/process-specific.
3. Convert the current repository-style manuscript to journal prose: remove internal claim-map labels from reader-facing text or move them to Supplement while preserving the audit ledger internally.
4. Build a journal-formatted Literature Cited section beyond the four novelty-boundary anchors.
5. Decide whether the paper remains pure theory or includes one partial empirical worked example; do not imply G1-G9 completion either way.
6. Run a final theorem/formula consistency audit across manuscript, figures, ledger, and source repositories.

## Audit verdict after first repair round

```text
THEORY_SPINE:             STRONG
PRIOR_ART_FRAMING:        FIRST BLOCKER CLOSED; BROADER AUDIT OPEN
R=sL GENERALITY RISK:     RESOLVED
K DEFINITION RISK:        RESOLVED THEORETICALLY / OPEN EMPIRICALLY
SPLIT-INVARIANT NOVELTY:  DEFENSIBLE, STILL NEEDS BROADER PRIOR-ART STRESS TEST
GENERALITY:               MODERATE; strongest through Phi=R-K
EMPIRICAL_CEILING:        CLEAR BUT LOW
AM_NAT_READINESS:         PRE-SUBMISSION DEVELOPMENT, NO LONGER BLOCKED BY R=sL OR K DEFINITION
```
