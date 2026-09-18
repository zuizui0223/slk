# SLK Am Nat reviewer-risk audit V8

## Current verdict

UTA1.8 removes the remaining dependence of deterministic invasion inference on the internal shape of the frequency-response curve.

Write

```text
Delta(p,E)=Phi(E)+H(p,E)
```

with endpoint ecological offsets

```text
h_R(E)=lim_{p->0}H(p,E)
h_D(E)=lim_{p->1}H(p,E).
```

Then invasion depends only on

```text
Phi+h_R
Phi+h_D.
```

The exact critical surfaces are

```text
Phi=-h_R
Phi=-h_D.
```

No linear, quadratic, symmetric, or pairwise-game assumption is needed for these deterministic endpoint criteria.

## What remains model dependent

The internal frequency-response parameterization determines mechanism interpretation, not the existence of the endpoint invasion criteria.

~~~text
canonical linear model
-> h_R=-eta, h_D=+eta

quadratic diagnostic
-> h_R=h0-eta+kappa
-> h_D=h0+eta+kappa

arbitrary H(p)
-> use endpoint offsets directly.
~~~

Thus two- and three-frequency experiments are optional for decomposing ecological feedback, whereas endpoint assays are the minimal invasion receipt.

## Environmental prediction in the general case

For

~~~text
Phi(E)=a(E-E_V),
~~~

with locally constant endpoint offsets,

~~~text
E_I-E_V=-h_R/a
E_R-E_V=-h_D/a.
~~~

Therefore

~~~text
E_I-E_R=(h_D-h_R)/a
(E_I+E_R)/2-E_V=-(h_R+h_D)/(2a).
~~~

The difference between endpoint ecological effects controls invasion-window spacing; their mean controls window displacement.

For smoothly varying endpoint effects,

~~~text
E_I-E_V
approximately
-h_R(E_V)/[Phi'(E_V)+h_R'(E_V)]

E_R-E_V
approximately
-h_D(E_V)/[Phi'(E_V)+h_D'(E_V)].
~~~

## Main reviewer risk now expected

The theoretical population-feedback risk has moved from model form to empirical endpoint estimation:

> Can rare-D and resident-D endpoint selection limits be estimated with acceptable extrapolation error and on a scale compatible with independently measured Phi?

This is directly testable and belongs to G5/G7 experimental design.

## Experimental response

A robust G7 design should separate two tasks.

### Task 1 — identify invasion

Estimate performance near the two endpoints and model the limits

~~~text
p -> 0
p -> 1.
~~~

This is sufficient for deterministic invasion criteria.

### Task 2 — interpret the ecological mechanism

Add interior frequencies:

~~~text
2 symmetric frequencies
-> canonical eta estimate

+ p=1/2
-> h0 and kappa diagnostic

additional frequencies
-> higher-order lack-of-fit assessment.
~~~

A complex interior shape therefore increases the experimental burden for mechanism interpretation but does not erase endpoint invasion inference.

## Important remaining boundary

UTA1.8 does not generalize the registered Moran fixation or rare-mutation occupancy results. A richer stochastic process must still be derived if one wants fixation or occupancy under arbitrary frequency-dependent ecology.

## Status

~~~text
THEORY_SPINE                         READY
UNIFIED_THRESHOLD_ATLAS              READY
ARBITRARY_SHAPE_ENDPOINT_INVASION    READY
ENVIRONMENTAL_ENDPOINT_DISPLACEMENT  READY
TWO_FREQUENCY_IDENTIFICATION         READY
THREE_FREQUENCY_CURVATURE_DIAGNOSTIC READY
FIXATION_OCCUPANCY_BOUNDARY          EXPLICIT
EMPIRICAL_CEILING                    THEORY_ONLY
MAIN_REVIEW_RISK                     ENDPOINT_LIMIT_ESTIMATION
PRIMARY_TARGET                       THE_AMERICAN_NATURALIST
~~~
