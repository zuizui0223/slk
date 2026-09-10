# SLK Am Nat reviewer-risk audit V1

This audit asks how a skeptical theory/evolution reviewer could reject the SLK flagship and what must be changed before submission.

## Bottom line

The manuscript is viable only if novelty is framed as an **integration theorem and measurement hierarchy**, not as a first theory of trade-offs, modularity, specialization, evolvability, evolutionary games, fixation, or weak-mutation stationary dynamics.

The strongest publishable object is:

```text
identified conflict budget L
-> architecture value Phi=sL-K
-> local accessibility
-> rare invasion
-> fixation criteria
-> weak-mutation occupancy
```

with explicit constructive separations at selected transitions and an exact fixation-occupancy invariant under declared process assumptions.

## Risk 1 — prior art already explains why modularity/specialization can be favored

### Reviewer attack

"Conflict among functions favoring modularity or specialization is old. Why is Phi=sL-K not just a re-parameterized cost-benefit model?"

### Relevant prior-art boundary

- Wagner & Altenberg (1996) explicitly connect modular organization to improved evolvability by reducing interference among functions.
- Rueffler, Hermisson & Wagner (2012) develop a general theory of functional specialization and division of labor.

### Required SLK response

Do **not** claim novelty for the generic statement that specialization/modularity can resolve functional conflict.

SLK novelty must instead be stated as:

1. a common estimand chain connecting an empirically identified shared-coordinate conflict budget to architecture payoff and then to evolutionary realization criteria;
2. explicit witness regions showing where successive criteria separate;
3. an exact statement of where separation fails because reciprocal fixation and symmetric weak-mutation occupancy re-align;
4. a gate-by-gate empirical claim ceiling.

### Status

HIGH RISK but addressable by framing.

## Risk 2 — the central theorem could look like a collection of standard observations

### Reviewer attack

"Of course optimality, accessibility, invasion, fixation, and stationary abundance are different concepts."

### Required SLK response

The theorem must not be sold as the verbal observation that concepts differ. It must be sold as a **constructive architecture-specific mapping** with a single upstream quantity and explicit witnesses:

```text
L>0 !=> Phi>0
Phi>0 !=> local accessibility
accessible + Phi>0 !=> invasion
invasion !=> reciprocal fixation superiority
absolute fixation advantage !=> occupancy ordering
```

plus

```text
reciprocal fixation ordering <=> occupancy ordering
```

under the registered symmetric rare-mutation exponential-Moran assumptions.

The paper becomes stronger when it states both the failures and the invariant.

### Status

MEDIUM-HIGH RISK. Figure 1 and `NON_EQUIVALENCE_THEOREM_V1.md` substantially reduce it.

## Risk 3 — `R=sL` is model specific

### Reviewer attack

"The flagship appears to depend on a quadratic identity that need not hold generally."

### Required SLK response

Keep the general architecture identity as

```text
Phi=R-K
```

and present

```text
R=sL
```

strictly as the quadratic partial-release corollary.

The general flagship hierarchy should therefore be written as

```text
L -> R -> Phi=R-K -> accessibility -> invasion -> fixation -> occupancy
```

with `R=sL` as one operational bridge, not the universal definition of `R`.

### Status

HIGH RISK in the current title/abstract emphasis. Must be fixed before submission.

## Risk 4 — `K` is biologically underdefined

### Reviewer attack

"Developmental, maintenance, regulatory, and mutational costs are not interchangeable. What exactly is K?"

### Required SLK response

Define `K` narrowly as the **net optimized fitness debit attributable to the differentiated architecture relative to the matched pre-cost comparison, on the same scale used for R**.

Do not present `K` as a directly measurable universal developmental cost. It can be measured, bounded, or experimentally constructed, but its operationalization is system-specific.

A valid empirical application must document:

```text
comparison state
fitness scale
time horizon
included cost channels
excluded cost channels
uncertainty or bound
```

### Status

HIGH RISK and currently an empirical bottleneck.

## Risk 5 — accessibility is not identifiable from endpoint architecture comparison

### Reviewer attack

"Your accessibility result depends entirely on the chosen mutation/release coordinate."

### Required SLK response

Agree explicitly. This is the point of the hierarchy.

`Phi>0` is endpoint value. Accessibility requires a registered local neighborhood/path geometry. Figure 2 must remain explicit that accessibility is not another universal line in the L-Phi plane.

### Status

LOW-MEDIUM RISK because the manuscript already states this correctly.

## Risk 6 — population transport is process specific

### Reviewer attack

"The fixation and occupancy results are artifacts of an exponential Moran process and symmetric rare mutation."

### Required SLK response

Do not universalize C8/C9/INV1. Their role is to demonstrate that adding a population process can both create new separations and impose new invariants.

The flagship contribution is the transport logic; the exact formulas are registered examples under declared process assumptions.

### Status

MEDIUM RISK. The claim ceiling already handles most of it.

## Risk 7 — no end-to-end empirical system

### Reviewer attack

"This is a theory assembled from abstractions without a biological system that estimates L, R, K, accessibility, invasion, fixation, and occupancy."

### Required SLK response

Do not pretend otherwise. Figure 3 should make the missing end-to-end validation a visible research program rather than a hidden weakness.

A complete G1-G9 system would be decisive but is not required for a pure-theory paper if the theorem and prior-art positioning are sufficiently sharp.

The manuscript should distinguish:

```text
formal contribution
empirical measurability
completed empirical validation
```

### Status

HIGH RISK for broad empirical claims; acceptable for a clearly theoretical Am Nat paper.

## Risk 8 — terminology may overstate novelty

Avoid unqualified phrases such as:

- "first theory of trait architecture"
- "general theory of specialization"
- "new theory of modularity"
- "universal evolutionary hierarchy"

Preferred wording:

- "integrated estimand hierarchy"
- "architecture-specific transport framework"
- "constructive split-and-invariant theorem"
- "measurement ladder connecting functional conflict to evolutionary realization"

## Submission-level novelty sentence

A defensible novelty sentence is:

> Existing theories explain why functional interference can favor specialization or modular organization and population-genetic theory distinguishes invasion, fixation, and stationary dynamics. SLK contributes a single architecture-specific estimand hierarchy linking an identified shared-coordinate conflict budget to recoverable architecture value and then to evolutionary realization, with explicit parameter witnesses for where adjacent criteria separate, an exact process-level invariant where two criteria re-align, and a gate-by-gate empirical claim ceiling.

## Required changes before submission

1. Promote `Phi=R-K` to the general identity everywhere; demote `R=sL` to a quadratic bridge.
2. Add a prior-art positioning paragraph in the Introduction naming modularity/evolvability and specialization/division-of-labor theory as antecedents rather than competitors to be displaced.
3. Add an operational definition of `K` and required metadata for empirical use.
4. Keep C8/C9/INV1 explicitly process-specific.
5. Do not imply end-to-end empirical validation.
6. Add a short Literature Cited section before submission.

## Audit verdict

```text
THEORY_SPINE:          STRONG
NOVELTY_IF_OVERCLAIMED: WEAK
NOVELTY_IF_FRAMED_AS_INTEGRATION+WITNESSES+INVARIANT: DEFENSIBLE
GENERALITY:            MODERATE; strongest through Phi=R-K, narrower for R=sL and Moran/Gibbs formulas
EMPIRICAL_CEILING:     CLEAR BUT LOW
AM_NAT_READINESS:      NOT YET; framing and K operationalization are the two main blockers
```
