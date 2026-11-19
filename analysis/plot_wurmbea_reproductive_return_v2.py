#!/usr/bin/env python3
"""Plot checked published-summary indices; matplotlib is only needed to render."""
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / "results/wurmbea_reproductive_return_v2.json").read_text())
comp = data["comparisons"]
plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 11,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, axes = plt.subplots(1, 2, figsize=(12.2, 5.9), gridspec_kw={"width_ratios": [1.3, 1]})
fig.subplots_adjust(left=.075, right=.98, bottom=.29, top=.79, wspace=.31)
labels = ["Seed\nnumber", "+ Germination", "+ Survival\n(second season)", "+ Corm mass\n(growth proxy)"]
x = range(4)
for key, label, color in [("Fo_over_Mo", "Open pollination", "#147D80"),
                          ("Fc_over_Mc", "Hand cross-pollination", "#8650A0")]:
    vals = comp[key]["stage_ratios"]
    axes[0].plot(x, vals, marker="o", lw=2.5, ms=7, color=color, label=label)
    for i, y in enumerate(vals):
        axes[0].annotate(f"{y:.2f}", (i, y), xytext=(0, 10), textcoords="offset points",
                         ha="center", color=color, weight="bold", fontsize=10)
axes[0].axhline(1, color="#8F969D", lw=1, ls="--")
axes[0].set_ylim(.65, 4.2)
axes[0].set_ylabel("Female / fruiting-male index")
axes[0].set_title("A   Female advantage depends on pollination", loc="left", fontsize=12, pad=16)
axes[0].legend(loc="upper left", frameon=False, fontsize=10)
vals = [v * 100 for v in comp["Ms_over_Mc"]["stage_ratios"]]
axes[1].plot(x, vals, marker="o", lw=2.5, ms=7, color="#BC633F")
for i, y in enumerate(vals):
    axes[1].annotate(f"{y:.1f}%", (i, y), xytext=(0, 11), textcoords="offset points",
                     ha="center", color="#A44F30", weight="bold", fontsize=10)
axes[1].set_ylim(0, 65)
axes[1].set_ylabel("Self / cross-pollinated fruiting-male index (%)")
axes[1].set_title("B   Losses accumulate after self-pollination", loc="left", fontsize=12, pad=16)
for ax in axes:
    ax.set_xticks(list(x), labels, fontsize=9)
    ax.set_xlim(-.14, 3.14)
    ax.grid(axis="y", color="#E8EBEE", lw=.8)
    ax.set_axisbelow(True)
fig.text(.075, .945, "Female function must translate into surviving offspring", fontsize=19, weight="bold")
fig.text(.075, .89, "Wurmbea dioica  |  Recalculation of published treatment means", fontsize=12, color="#52606C")
fig.text(.075, .13, "Descriptive ratios of products of treatment means; family subsets differ among stages.", fontsize=10, color="#52606C")
fig.text(.075, .09, "Corm mass is a growth proxy. No new confidence intervals or lifetime fitness estimates.", fontsize=10, color="#52606C")
fig.text(.075, .045, "Source: Ramsey, Vaughton & Peakall (2006), Table 2. DOI: 10.1111/j.1420-9101.2006.01129.x", fontsize=9, color="#52606C")
fig.savefig(ROOT / "results/wurmbea_reproductive_return_stages_v2.png", dpi=180,
            facecolor="white", bbox_inches="tight", pad_inches=.18)
plt.close(fig)
