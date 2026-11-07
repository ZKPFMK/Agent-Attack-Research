#!/usr/bin/env python3
"""A8 -- task by model or defense heatmap.

Pattern: rows are tasks and columns are victim conditions; values are synthetic
rates, missing cells are masked, and readable cells carry their value. Replace
the matrix with logged rates and put n/CI in the table or caption.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np
from matplotlib.colors import ListedColormap, BoundaryNorm


def make(venue="lncs", outdir=ROOT / "examples"):
    tasks = ["Browse", "Retrieve", "Plan", "Tool use", "Memory"]
    conditions = ["small / no defense", "small / filter", "large / no defense", "large / filter"]
    rates = np.array([
        [34, 18, 49, 27],
        [41, 22, 57, 31],
        [29, 16, 44, 24],
        [37, 20, 52, 28],
        [48, 25, 63, 35],
    ], dtype=float)
    rates[2, 3] = np.nan
    mask = np.ma.masked_invalid(rates)
    fig, ax = P.figure(venue, width=0.72 if venue == "lncs" else "column", aspect=0.92)
    cmap = ListedColormap(["#ffffff", P.SEQ_BLUE[2], P.SEQ_BLUE[5], P.SEQ_BLUE[8], P.SEQ_BLUE[11]])
    cmap.set_bad(P.NEUTRAL_MID)
    norm = BoundaryNorm([0, 10, 30, 50, 70, 100], cmap.N)
    im = ax.imshow(mask, cmap=cmap, norm=norm, aspect="auto")
    for i in range(len(tasks)):
        for j in range(len(conditions)):
            value = rates[i, j]
            if np.isfinite(value):
                ax.text(j, i, f"{value:.0f}%", ha="center", va="center", fontsize=7,
                        color="white" if value >= 50 else P.INK)
            else:
                ax.text(j, i, "n/a", ha="center", va="center", fontsize=7, color=P.INK_MUTED)
    ax.set_xticks(range(len(conditions)), ["small\nclean", "small\nfilter", "large\nclean", "large\nfilter"], fontsize=6)
    ax.set_yticks(range(len(tasks)), tasks, fontsize=7)
    ax.set_xlabel("victim model and defense")
    ax.set_ylabel("task")
    ax.xaxis.set_label_position("top")
    ax.xaxis.tick_top()
    ax.grid(False)
    ax.set_xticks(np.arange(-.5, len(conditions)), minor=True)
    ax.set_yticks(np.arange(-.5, len(tasks)), minor=True)
    ax.grid(which="minor", color=P.GRID, lw=0.3)
    ax.tick_params(which="both", length=0)
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title("synthetic ASR; replace with logged k/n and 95% CI", fontsize="small", color=P.INK_2,
                 loc="left", pad=2, y=-0.12)
    return P.save(fig, "p08_sbox_ddt_heatmap", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
