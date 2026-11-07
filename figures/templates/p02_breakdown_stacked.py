#!/usr/bin/env python3
"""A2 -- evaluation-stage breakdown as horizontal stacked bars.

Pattern: one row per clean, control or attack arm, with identical prompt,
routing, tool and memory stages. Replace synthetic values with evidence-linked
logs before publication.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def make(venue="lncs", outdir=ROOT / "examples"):
    stages = ["Prompt", "Routing", "Tool call", "Memory"]
    methods = ["Clean", "Naive injection", "Proposed attack"]
    t = np.array([[0.5, 1.8, 4.6, 1.3],
                  [0.5, 2.0, 4.9, 1.5],
                  [0.5, 2.8, 6.8, 2.4]])     # seconds, synthetic
    fig, ax = P.figure(venue, width="full", aspect=0.30)
    y = np.arange(len(methods))[::-1]
    left = np.zeros(len(methods))
    for j, stage in enumerate(stages):
        ax.barh(y, t[:, j], left=left, height=0.62, color=P.CATEGORICAL[j], label=stage,
                edgecolor="white", linewidth=0.8, hatch=P.HATCHES[j] if j == 3 else None)
        left += t[:, j]
    for yi, total in zip(y, left):
        ax.text(total + 0.2, yi, f"{total:.1f} s", va="center", fontsize="small")
    ratio = left[0] / left[-1]
    ax.annotate("", xy=(left[-1], y[-1] - 0.42), xytext=(left[0], y[-1] - 0.42),
                arrowprops=dict(arrowstyle="<->", color=P.INK_2, lw=0.7, shrinkA=0, shrinkB=0))
    ax.text((left[0] + left[-1]) / 2, y[-1] - 0.5, f"{ratio:.2f}" + r"$\times$ clean latency",
            ha="center", va="top", fontsize="small", color=P.INK)
    ax.set_yticks(y, methods)
    ax.set_xlabel("evaluation latency (s)")
    ax.set_xlim(0, left.max() * 1.12)
    ax.set_ylim(y[-1] - 0.95, y[0] + 0.5)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", visible=True)
    ax.tick_params(axis="y", length=0)
    ax.legend(ncols=4, loc="lower left", bbox_to_anchor=(0, 1.0), fontsize="small")
    return P.save(fig, "p02_breakdown_stacked", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
