# Figure 1 — unified critical-surface transport

## Caption

**Figure 1. One architecture comparison crosses different evolutionary thresholds.** SLK transports the same declared architecture comparison from identified shared-coordinate conflict through endpoint architecture value, small-step selective accessibility, frequency-dependent invasion, finite-population fixation, and symmetric rare-mutation occupancy. Each added mechanism introduces its own critical surface: sufficiently small release switches at k=k_local; global endpoint value at Phi=0, equivalently k=k_global; rare invasion at Phi=eta; resistance to reverse invasion at Phi=-eta; reciprocal fixation ordering at Phi=0; and absolute fixation advantage over neutrality at 3Phi=eta under weak selection. Under the registered exponential-Moran process with connected symmetric rare mutation, reciprocal fixation ordering and monomorphic occupancy re-align exactly on the same Phi=0 surface. The left panel shows that all five flagship non-implications can be constructed inside one convex recovery family, R(d)=d+d^2 and K(d)=kd, by varying only k and eta. The arrows are estimand handoffs, not logical implications.

## Reader-facing message

~~~text
identified conflict
      |
      v
global endpoint value            Phi=0
      |
      v
small-step accessibility         k=k_local
      |
      v
rare invasion                    Phi=+/-eta
      |
      v
finite-population fixation       Phi=0; 3Phi=eta under weak selection
      |
      v
rare-mutation occupancy          Phi=0
~~~

The figure is a **critical-surface transport map**, not a claim that every stage has a different threshold.

## Exact re-alignment

For the registered canonical pair and exponential-Moran / symmetric rare-mutation process,

~~~text
rho_D/rho_S = exp[beta(N-2)Phi]
Pi_D/Pi_S   = exp[beta(N-2)Phi]
~~~

so

~~~text
global endpoint D>S
iff
reciprocal fixation favors D
iff
symmetric rare-mutation occupancy favors D
iff
Phi>0.
~~~

This shared surface is conditional on the declared equal-diagonal-feedback canonical mapping, fixation process, and mutation assumptions.

## One-family witness system

Use

~~~text
d in [0,1]
R(d)=d+d^2
K(d)=k d
k_local=1
k_global=2
Phi=2-k.
~~~

Then varying only k and eta yields all five registered separations:

1. conflict without positive endpoint value;
2. positive endpoint value without sufficiently small selectively uphill release;
3. positive value plus small-step accessibility without rare invasion;
4. rare invasion without reciprocal fixation superiority;
5. absolute fixation advantage over neutrality without greater symmetric rare-mutation occupancy.

The explicit parameter values remain registered in theory/UNIFIED_THRESHOLD_ATLAS_V1.md and theory/NON_EQUIVALENCE_THEOREM_V1.md.

## Scope

The figure does not depict continuous-architecture branching, edgewise topology, spatial migration, or temporal Floquet dynamics. Those remain PAYOFF extensions outside the SLK flagship. The local-accessibility surface refers specifically to sufficiently small selectively uphill steps along the declared release path and does not imply absolute historical unreachability.
