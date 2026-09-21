# SLK Am Nat reviewer-risk audit V9

## Current verdict

UTA1.9 converts the remaining endpoint-limit problem into a finite-frequency certification problem.

The invasion layer no longer requires exact p=0 or p=1 treatments. Instead it uses finite frequencies plus an explicit local smoothness receipt.

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

> How are the local smoothness bounds M_R or C_R justified empirically?

This is now the principal model-validation task.

A defensible design should:

1. use multiple near-endpoint frequencies rather than one extrapolation pair alone;
2. fit local slopes/curvature and inspect lack of fit;
3. choose conservative smoothness bounds before endpoint classification;
4. validate the bound on held-out near-endpoint frequencies where feasible;
5. report unresolved whenever the certified interval overlaps zero.

The theory does not claim that finite data can prove a global derivative bound without assumptions. It states exactly which local regularity assumption is needed for a certified endpoint statement.

## Practical implication

The old risk was conceptual:

> invasion depends on an experimentally unattainable limit.

The new risk is ordinary experimental design:

> how fine must the frequency grid be, and how conservative must the local smoothness envelope be, to certify the endpoint sign?

That is a much narrower and testable problem.

## Status

~~~text
THEORY_SPINE                         READY
ARBITRARY_SHAPE_ENDPOINT_INVASION    READY
FINITE_FREQUENCY_ENDPOINT_BOUNDS     READY
SAMPLING_PLUS_APPROXIMATION_INTERVAL READY
ENVIRONMENTAL_THRESHOLD_ERROR_BOUND  READY
EMPIRICAL_CEILING                    THEORY_ONLY
MAIN_REVIEW_RISK                     LOCAL_SMOOTHNESS_BOUND_VALIDATION
PRIMARY_TARGET                       THE_AMERICAN_NATURALIST
~~~
