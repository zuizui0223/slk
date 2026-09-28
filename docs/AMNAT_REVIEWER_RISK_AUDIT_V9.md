# SLK Am Nat reviewer-risk audit V9

## Current verdict

UTA1.9 converts the endpoint-limit problem into a finite-frequency certification problem, but the numerical device is not itself a novelty claim. The two-scale cancellation at `epsilon` and `2epsilon` is Richardson-type extrapolation with classical prior art in Richardson & Gaunt (1927).

The invasion layer therefore uses an established extrapolation idea for a specific biological purpose: finite rare-frequency measurements, an explicit local smoothness receipt, combined approximation/sampling uncertainty, and a three-way invasion / non-invasion / unresolved decision.

## First-order certificate

Near rare D,

```text
|Delta(p)-Delta_R| <= M_R p.
```

At p=epsilon,

```text
Delta_R
in
[Delta(epsilon)-M_R epsilon,
 Delta(epsilon)+M_R epsilon].
```

A positive lower bound certifies invasion; a negative upper bound certifies non-invasion.

## Second-order certificate

If

```text
|Delta''(p)| <= C_R
```

on [0,2epsilon], then

```text
Delta_R_hat
=
2Delta(epsilon)-Delta(2epsilon)
```

satisfies

```text
|Delta_R_hat-Delta_R|
<=
C_R epsilon^2.
```

Thus two finite rare-frequency treatments improve the deterministic endpoint approximation from order epsilon to order epsilon^2.

The same design applies near p=1.

## Sampling uncertainty

If measured effects have intervals

```text
Delta(epsilon) in [L1,U1]
Delta(2epsilon) in [L2,U2],
```

then the certified endpoint interval is

```text
[
2L1-U2-C_R epsilon^2,
2U1-L2+C_R epsilon^2
].
```

Therefore the invasion claim is explicitly three-way:

```text
lower > 0  -> invasion certified
upper < 0  -> non-invasion certified
otherwise  -> unresolved.
```

The framework never turns an unresolved endpoint into a biological negative.

## Environmental threshold precision

For local environmental slope a=dPhi/dE,

```text
endpoint fitness error B
-> threshold-position error <= B/|a|.
```

Under the two-point curvature certificate,

```text
|E_I_hat-E_I|
<=
C_R epsilon^2/|a|.
```

This gives a direct frequency-resolution criterion for ecological-gradient experiments.

## Main reviewer risk now expected

> If the component algebra, invasion definition, extrapolation device, and fixation/occupancy process are established, what biological work is done by the integrated SLK transport?

This is now the principal conceptual-review task. Bowers et al. (2005) already owns the idea of placing a trade-off curve and resident-mutant invasion boundaries in one evolutionary geometry, so SLK must not sell value-to-invasion geometry itself as new. The strongest residual answer is UTA1.10-UTA1.11: persistent integration is observationally non-identifying, but a fixed upstream comparison plus the measured sign sequence separates negative architecture value, local release barriers, and rare-establishment barriers; if all three early signs are positive, those explanations are explicitly excluded rather than differentiation being declared inevitable. When estimates are uncertain, marginal intervals define a conservative box-compatible outer state set rather than forcing a midpoint label; genuinely nested boxes can only eliminate states, while exact joint compatibility would require the joint feasible region. G1-G9 specifies what must be measured before each localization is licensed. The argument does not depend on priority claims for the component mathematics, trade-off/invasion geometry, or statistical partial-identification theory.

A secondary model-validation question remains:

> How are the local smoothness bounds M_R or C_R justified empirically?

A defensible design should:

1. use multiple near-endpoint frequencies rather than one extrapolation pair alone;
2. fit local slopes/curvature and inspect lack of fit;
3. choose conservative smoothness bounds before endpoint classification;
4. validate the bound on held-out near-endpoint frequencies where feasible;
5. report unresolved whenever the certified interval overlaps zero.

The theory does not claim that finite data can prove a global derivative bound without assumptions. It states exactly which local regularity assumption is needed for a certified endpoint statement.

## Practical implication

The endpoint-limit objection is now an ordinary experimental-design problem:

> how fine must the frequency grid be, and how conservative must the local smoothness envelope be, to certify the endpoint sign?

But that repair should not be sold as new numerical mathematics. The biological payoff is diagnostic and exclusionary: identical persistent integration can arise at different decision layers, and the transport either localizes the first failing sign or rules out the first three registered failure explanations when all early signs are positive. Mechanism attribution still requires separate causal evidence.

## Status

~~~text
THEORY_SPINE                         READY
ARBITRARY_SHAPE_ENDPOINT_INVASION    READY
FINITE_FREQUENCY_ENDPOINT_BOUNDS     READY
SAMPLING_PLUS_APPROXIMATION_INTERVAL READY
ENVIRONMENTAL_THRESHOLD_ERROR_BOUND  READY
EMPIRICAL_CEILING                    THEORY_ONLY
NUMERICAL_METHOD_NOVELTY             NOT_CLAIMED
MAIN_REVIEW_RISK                     UTA1_10_11_DIAGNOSTIC_BIOLOGICAL_PAYOFF
SECONDARY_REVIEW_RISK                LOCAL_SMOOTHNESS_BOUND_VALIDATION
PRIMARY_TARGET                       THE_AMERICAN_NATURALIST
~~~
