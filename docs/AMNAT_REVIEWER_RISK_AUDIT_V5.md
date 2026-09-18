# SLK Am Nat reviewer-risk audit V5

## Current verdict

The main conceptual risk after V4 was that the ecological threshold-displacement result might look tied to an overly simple constant-feedback environmental slice.

That risk is reduced by UTA1.4b. SLK now separates two ecological effects:

1. feedback **level** at the architecture-value crossing, which displaces invasion from value;
2. feedback **slope** along the environment, which amplifies, compresses, shifts, or can remove the invasion crossing in the focal direction.

## Exact affine co-varying prediction

Let

~~~text
Phi(E)=a(E-E_V)
eta(E)=eta_0+b(E-E_V).
~~~

Then

~~~text
E_I-E_V=eta_0/(a-b)
E_R-E_V=-eta_0/(a+b).
~~~

For |b|<a,

~~~text
|E_I-E_R|=2a|eta_0|/(a^2-b^2)
(E_I+E_R)/2-E_V=eta_0 b/(a^2-b^2).
~~~

Thus ecology predicts both the width and the location of the transition zone.

For eta_0>0 and 0<b<a, coordination feedback strengthens along the same environmental direction as intrinsic architecture value, delaying rare invasion more strongly than the constant-feedback prediction. If b approaches a, establishment is pushed far away. In the affine model, b>=a means increasing E from E_V never produces rare-D invasion.

## Smooth-system interpretation

For smooth non-affine functions,

~~~text
E_I-E_V
approximately
eta(E_V)/[Phi'(E_V)-eta'(E_V)].
~~~

This is explicitly a local first-order statement, not a universal exact formula.

The ecological prediction is therefore not "environments are linear." It is:

> realized differentiation depends on the relative environmental slopes of intrinsic architecture value and ecological frequency feedback.

## Remaining reviewer risk

The principal open question is now empirical identifiability rather than mathematical generality:

> Can empirical studies estimate Phi(E), eta(E), and their local slopes on compatible scales well enough to test the predicted displacement?

That is a productive risk because it maps directly onto the G1-G9 measurement programme.

## Strongest reader-facing ecological message

~~~text
stronger conflict
does not necessarily mean
more differentiation

and

a more favorable environment for differentiation
does not necessarily mean
an environment where differentiation can establish from rarity.
~~~

Which mismatch occurs is predicted by recoverability, architecture cost, release geometry, and frequency feedback.

## Status

~~~text
THEORY_SPINE                         READY
UNIFIED_THRESHOLD_ATLAS              READY
CROSS_LEVEL_COMPATIBILITY            READY
CONSTANT_FEEDBACK_DISPLACEMENT       READY
VARYING_FEEDBACK_GENERALIZATION      READY
CONFLICT_DIFFERENTIATION_DISCORDANCE READY
EMPIRICAL_CEILING                    THEORY_ONLY
MAIN_REVIEW_RISK                     EMPIRICAL_IDENTIFIABILITY_OF_PHI_AND_ETA
PRIMARY_TARGET                       THE_AMERICAN_NATURALIST
~~~
