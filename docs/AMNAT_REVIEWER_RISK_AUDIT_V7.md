# SLK Am Nat reviewer-risk audit V7

## Current verdict

The main reviewer risk identified in V6 was adequacy of the linear canonical frequency map. UTA1.7 converts that assumption into an explicit three-frequency model check and supplies a local quadratic repair for invasion inference.

The registered hierarchy now has two population-feedback layers:

~~~text
minimal canonical pair:
Delta(p)=Phi+eta(2p-1)

quadratic diagnostic extension:
Delta(p)=Phi+h0+eta x+kappa x^2,
x=2p-1.
~~~

The canonical pair is the nested special case

~~~text
h0=0,
kappa=0.
~~~

## What a three-frequency experiment identifies

With independent architecture value Phi from G5 and frequencies

~~~text
p_-=1/2-q,
p_0=1/2,
p_+=1/2+q,
~~~

one obtains

~~~text
h0=Delta_0-Phi
eta=(Delta_+-Delta_-)/(4q)
kappa=(Delta_++Delta_--2Delta_0)/(8q^2).
~~~

Thus canonical-map adequacy is directly testable.

## Generalized invasion consequences

With curvature retained,

~~~text
rare D invasion:
Phi>eta-kappa-h0

resistance to rare S:
Phi>-eta-kappa-h0.
~~~

Along Phi(E)=a(E-E_V),

~~~text
E_I-E_V=(eta-kappa-h0)/a
E_R-E_V=-(eta+kappa+h0)/a.
~~~

Therefore

~~~text
E_I-E_R=2eta/a
~~~

while

~~~text
(E_I+E_R)/2-E_V=-(h0+kappa)/a.
~~~

This gives a clean biological decomposition:

- eta controls the spacing of reciprocal invasion thresholds;
- h0+kappa shifts the center of the invasion window relative to intrinsic architecture value.

Nonlinearity therefore has an interpretable ecological signature rather than merely producing a failed goodness-of-fit test.

## Important boundary

UTA1.7 repairs invasion inference only.

Once h0 or kappa is nonzero, the registered pairwise-game Moran fixation formula and symmetric rare-mutation occupancy invariant are not automatically valid. They require a separate stochastic derivation for the richer frequency-dependent model.

The manuscript must preserve this boundary.

## Main reviewer risk now expected

> Is a quadratic local frequency approximation sufficient when real ecological feedback is strongly nonlinear, asymmetric, or state dependent?

This is a narrower and more productive risk than the previous linearity concern.

The response is prospective:

1. measure at least three frequencies to test the canonical map;
2. use additional frequencies to test the quadratic approximation;
3. if higher-order structure remains, estimate the empirical frequency-response surface directly;
4. use the observed endpoint signs for invasion inference;
5. do not transport canonical fixation/occupancy formulas into an unregistered richer model.

## Current strongest empirical design

~~~text
G1-G5:
identify conflict and independently estimate Phi

G7:
measure Delta(p) at symmetric frequencies
-> 2 frequencies: canonical Phi/eta estimate
-> + p=1/2: identify h0 and kappa
-> extra frequencies: lack-of-fit test

across environments E:
recover Phi(E), eta(E), h0(E), kappa(E)
-> locate architecture-value and invasion crossings
-> test threshold displacement.
~~~

## Status

~~~text
THEORY_SPINE                         READY
UNIFIED_THRESHOLD_ATLAS              READY
ECOLOGICAL_THRESHOLD_DISPLACEMENT    READY
VARYING_FEEDBACK_GENERALIZATION      READY
TWO_FREQUENCY_IDENTIFICATION         READY
THREE_FREQUENCY_CURVATURE_DIAGNOSTIC READY
GENERALIZED_INVASION_SURFACES        READY
FIXATION_OCCUPANCY_BOUNDARY          EXPLICIT
EMPIRICAL_CEILING                    THEORY_ONLY
MAIN_REVIEW_RISK                     HIGHER_ORDER_FREQUENCY_RESPONSE_ADEQUACY
PRIMARY_TARGET                       THE_AMERICAN_NATURALIST
~~~
