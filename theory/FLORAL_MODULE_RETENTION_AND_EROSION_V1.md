# SLK supplementary ecology — pollen specialization can erode before mechanical support

## Biological question

When a flower has evolved two visibly different stamen classes, must loss of their reward-versus-pollen-export division eliminate the entire differentiated floral structure? **No universal evolutionary order follows from stamen dimorphism alone.** The anther and its supporting filament can have distinct ecological effects, so a lineage could retain mechanically useful filament geometry even as pollen-specialized anther tissue regresses. The possible opposite outcomes depend on the total reproductive fitness of physically accessible alternative architectures.

This is a **conditional evolutionary hypothesis and comparison**, not a new discovery that sterile stamens can be functional. Walker-Larsen & Harder (2000, 2001) already recognized and experimentally demonstrated secondary functions of staminodes, including visitor-access regulation and a lever promoting stigma contact in bee-pollinated *Penstemon*.

## Empirical starting point: a nested, physically feasible experiment

Fukano & Denda (2026) manipulated *Bredia hirsuta* stamens in Okinawa. Holding **short stamens present**, three accessible experimental configurations are directly comparable:

| Code | Short stamens | Long filament | Long anther | Visits; slips | Meaning |
|---|---|---|---|---|---|
| B | present | absent | absent | 39 visits; 12 slips on 8 flowers | short stamens only |
| D | present | present | absent | 31 visits; 0 slips on 6 flowers | filament support, without pollen-bearing long anthers |
| A | present | present | present | 33 visits; 0 slips on 7 flowers | complete dimorphic architecture |

**B versus D** isolates the **addition of the long filament with long anthers absent** in these interventions. It establishes a behavioral difference compatible with filament-dependent buzzing support and altered stigma-contact position: treatment B also recorded ventral stigma contact on 13/39 visits, while D recorded 0/31. It does not directly measure lifetime plant fitness, paternity, or heritable reduction of a long anther.

**A versus D** changes whether long anthers remain when filaments and short stamens are present. Both recorded zero slips, so long-anther tissue is **not required for the measured absence of slipping** under these conditions. This does not show that long anthers have no pollen-export benefit, because male fitness from long-anther pollen was not measured.

**C (long stamens intact, short stamens removed)** also recorded 0 slips in 26 visits on 8 flowers. Thus neither stamen class is established as mechanically indispensable for stable buzzing. **E (long filaments only)** received only 2 visits, including 1 slip; it cannot support a precise efficacy estimate. The six treatments do not form a complete factorial arrangement, and repeated visits to the same flowers must not be counted as independent plant fitness replicates.

### What B–D actually identifies, and what it does not

The behavioral support contrast B versus D can be meaningful even if the flowers are functionally unimorphic in *pollen-bearing anthers*. Hence the mechanical benefit of a long-stamen filament **cannot by itself be invoked as an adaptation maintaining long-anther pollen specialization**. A genetically or developmentally accessible intermediate flower with long supporting filaments but reduced long-anther tissue could retain the measured grip function.

The surgically emasculated D treatment is **not** evidence that this phenotype already occurs as a heritable, naturally established staminode-like state in *Bredia*. It is a functional counterfactual, subject to developmental feasibility and the total costs of maintaining each module.

## A minimal ecological model that respects those three nested phenotypes

At a fixed pollinator community `E`, define complete-cycle fitness of each viable floral architecture:

```text
S = short pollen-bearing stamens only            [treatment B analogue]
P = short stamens + long supportive filaments     [treatment D analogue]
D = short stamens + long filaments + long anthers  [treatment A analogue]

W_S(E), W_P(E), W_D(E) = male + female reproductive fitness
                         on a declared comparable scale.
h(E) = W_P(E) - W_S(E)      net retention value of the filament module
a(E) = W_D(E) - W_P(E)      incremental value of the pollen-bearing long anther.
```

This is a nested **ordered architectural comparison**, not an assumption that the biological modules combine additively: all costs, pollen competition and interactive effects are already inside the *conditional* finite differences `h(E)` and `a(E)`. No independent 'filament-without-any-stamen' or 'long-anther-without-filament' impossible phenotype is required.

If the only reachable alternatives are these three:

- `h>0, a>0`: `W_D > W_P > W_S`, so fully differentiated long anthers and filaments are favored among these candidates.
- `h>0, a<0`: `W_P > max(W_D,W_S)`, so **partial structural reduction** (anther tissue reduced but support retained) is favored over either extreme.
- `h<0, a<0`: `W_S > W_P > W_D`; the extra long-stamen modules lack net advantage.
- `h<0, a>0`: the direct `D` versus `S` comparison depends on `h+a`; no universal simple sequence follows.

The intermediate region `h>0, a<0` is especially important: a mechanically helpful floral module can be selectively maintained after its associated pollen-producing module becomes disadvantageous. This **does not mean original dimorphic anthers themselves remain under positive selection**. Nor does a behavioral stabilization measurement establish `h>0` on the lifetime fitness scale.

### Illustrative ecological ordering, not a measurement

Let `q in [0,1]` be the community fraction of pollinators that handle both anther classes indiscriminately (not an actual estimate for any listed species). Take dimensionless hypothetical payoffs

```text
W_S(q)=0
h(q)=W_P-W_S=0.9-1.1q
a(q)=W_D-W_P=0.9-1.6q.
```

The incremental long-anther contribution changes sign at `q_A=9/16=0.5625`, while the filament contribution changes sign later at `q_F=9/11≈0.81818`. Accordingly:

```text
q=0.00: W_D=1.8,   W_P=0.9,    W_S=0    => D highest
q=0.75: W_D=-0.225,W_P=0.075,  W_S=0    => P highest
q=1.00: W_D=-0.9,  W_P=-0.2,   W_S=0    => S highest.
```

This is a valid **conditional fitness-ranking witness** for an environment-driven `D > P > S` transition in the candidate optimum. No actual evolutionary trajectory, mutational access, demographic establishment, or adaptation rate is implied. Other payoff functions reverse the order of crossings or favor the full organ complex continuously.

## Critical counterexample: behavioral support is compatible with opposite evolutionary outcomes

Because B–D compares *visitation behavior*, two different complete-cycle fitness landscapes can reproduce exactly the same observed slipping contrast:

```text
Case 1: W_S=0, W_P=1.0, W_D=0.5  => supportive remnant P favored
Case 2: W_S=0, W_P=-0.2,W_D=0.5  => support has behavioral effect,
                                   yet its cost exceeds fitness gain;
                                   fully divided D favored.
```

The above are illustrative lifetime-fitness assignments, not estimates. Thus even a strong intervention on bee posture is **insufficient** to show that pollen-sterile supporting anatomy is selected for or would persist evolutionarily. Similarly, mechanically supporting a bee is not synonymous with increased pollen export or seed fitness.

## Repeated evolution, staminodes, and stringent novelty boundary

- Walker-Larsen J & Harder LD. 2000. **The evolution of staminodes in angiosperms: patterns of stamen reduction, loss, and functional re-invention.** *American Journal of Botany* 87:1367–1384. DOI **10.2307/2656866**. This already proposes that staminodes can acquire independent reproductive functions and persist when functional; it also explains why loss, reappearance and multiple roles can differ by lineage.
- Walker-Larsen J & Harder LD. 2001. **Vestigial organs as opportunities for functional innovation: the example of the Penstemon staminode.** *Evolution* 55:477–487. DOI **10.1111/j.0014-3820.2001.tb00782.x**. In *Penstemon ellipticus* the staminode affected visitor access and stigma contact; in *P. palmeri* it acted as a lever increasing pollen receipt; the studied hummingbird-pollinated species did not show the same measured function. This is direct prior art for **pollinator-dependent reuse and secondary loss of an anther-sterile organ**.
- Dellinger et al. 2021, DOI 10.1111/evo.14260, chiefly infer repeated **de novo** heteranthery under alternative pollination/reward conditions rather than documented retention of the original dimorphic pollen apparatus.
- Fukano & Denda 2026, DOI 10.1111/1442-1984.70070, provide a **within-species component-removal behavioral contrast**, not a historic transition from dimorphic fertile long anthers to staminodes.

These sources make it indefensible to advertise secondary floral functions, pollen-stamen sterilization, or function switching as discoveries of SLK. The still-interesting **falsifiable ecological application** is the predicted divergence in the *fitness consequences* of reducing long anther tissue versus losing long supporting filaments under a measured pollinator shift, conditional on ancestral architecture and available intermediates.

## What would reject the proposed partial-retention route?

Two treatments alone are not enough. Compare an **intact dimorphic flower** and a **long-anther-reduced, long-filament-retained flower** (both with functional short stamens) and a **short-only flower** at matched reproductive resource availability. Cross the treatments with different visitor communities. Measure (i) individual pollen fates by anther class, (ii) actual stigma contact, (iii) male and female total reproductive output, and (iv) the costs of expressing supporting tissue. Because removing long anthers also removes pollen rewards and male gametes, direct ablation does not automatically equal a whole-life fitness estimate of a developmentally reduced long-anther lineage; experimentally matched pollen quantity and sham manipulations are needed.

Evidence for the **specific** partial-retention selection hypothesis would require `h(E)>0` and `a(E)<0` on a common complete-cycle fitness scale, plus a heritable/accessibly developable P-like structure. Temporal or phylogenetic evidence is separately needed to claim the ancestral dimorphic architecture actually evolved toward P after pollinator turnover. If `a(E)>=0`, the intact long anther remains worthwhile; if `h(E)<=0`, the supportive remnant has no demonstrated net advantage; if suitable P mutants cannot arise, the predicted comparative advantage may never be realized.

**Biological conclusion:** a specialized organ system can be reduced *selectively by module*, so pollen-production and mechanical-support anatomy need not disappear together. This is a testable conditional evolutionary outcome grounded in a real component-removal design and extensive prior staminode biology, **not** an empirically observed SLK-specific evolutionary sequence.
