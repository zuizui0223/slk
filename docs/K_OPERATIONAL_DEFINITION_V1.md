# Operational definition of architecture cost K

## General definition

SLK defines architecture cost `K` as the **net optimized fitness debit attributable to using the differentiated architecture rather than its matched pre-cost comparison**, expressed on the same fitness scale and time horizon as recoverable benefit `R`.

The general architecture margin is therefore

```text
Phi = R - K.
```

`K` is not assumed to be one universal physiological quantity. It is a comparison-specific estimand.

## What may contribute to K

Depending on the biological system, admissible channels can include additional:

- developmental production cost;
- maintenance or energetic cost;
- regulatory burden;
- material/tissue cost;
- coordination or cross-talk cost not already included in `R`;
- demographic cost expressed on the registered fitness scale.

A channel must not be counted twice. If residual coupling or cross-talk is already included inside the optimized recovery model defining `R`, it cannot also be charged again in `K`.

## Required empirical receipt

Any empirical estimate or bound on `K` must declare:

```text
shared comparison state
differentiated comparison state
fitness scale
time horizon
included cost channels
excluded cost channels
how benefit terms were prevented from leaking into K
point estimate / interval / bound
uncertainty model
```

## Preferred experimental definition

Where possible, compare a matched differentiated architecture against the corresponding pre-cost counterfactual while holding the recovered functional benefit fixed or separately modeled. Operationally,

```text
K = fitness(pre-cost differentiated comparison)
    - fitness(realized differentiated architecture)
```

on a loss scale, or the sign-equivalent debit on the chosen fitness scale.

If the pre-cost counterfactual cannot be directly constructed, `K` may be partially identified by bounds, but the resulting `Phi` must inherit those bounds.

## Identification warning

Observed total fitness difference between shared and differentiated phenotypes is

```text
Delta_arch = R - K,
```

not `K` alone. Endpoint comparison therefore identifies the net margin but does not automatically decompose benefit and architecture cost.

## Generality boundary

The theory does not require every application to separate `R` and `K` if only the sign of `Phi` is needed. Direct matched-worldline comparison can classify architecture value. Separate `R` and `K` become necessary when the biological interpretation specifically concerns recovery efficiency or architecture cost.
