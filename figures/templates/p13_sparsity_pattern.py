#!/usr/bin/env python3
"""A13 -- message and memory provenance matrix.

Pattern: small multiples of equal-size panels for agent/round conditions; filled
cells are observed state or message edges, and labels identify the condition.
Use it to explain propagation or memory changes; values are synthetic here.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch


def state_matrix(size, injected=(), retained=()):
    matrix = np.zeros((size, size), dtype=int)
    for src, dst in ((i, i + 1) for i in range(size - 1)):
        matrix[src, dst] = 1
    for src, dst in injected:
        matrix[src, dst] = 2
    for src, dst in retained:
        matrix[src, dst] = 3
    return matrix


def make(venue="lncs", outdir=ROOT / "examples"):
    size = 6
    panels = [
        state_matrix(size),
        state_matrix(size, injected=((0, 1), (2, 3))),
        state_matrix(size, injected=((0, 1), (2, 3)), retained=((1, 2), (3, 4))),
    ]
    names = ["clean", "injected", "defense retains provenance"]
    fig, axs = P.figure(venue, width="full", aspect=0.31, ncols=3)
    cmap = ListedColormap(["white", P.OURS_DARK, P.ACCENT, P.SEQ_BLUE[8]])
    for ax, matrix, name in zip(axs, panels, names):
        ax.imshow(matrix, cmap=cmap, vmin=0, vmax=3, interpolation="nearest")
        ax.set_xticks(np.arange(-.5, size), minor=True)
        ax.set_yticks(np.arange(-.5, size), minor=True)
        ax.grid(which="minor", color=P.GRID, lw=0.25)
        ax.grid(which="major", visible=False)
        ax.tick_params(which="both", length=0, labelbottom=False, labelleft=False)
        for sp in ax.spines.values():
            sp.set_visible(True)
            sp.set_color(P.INK_2)
            sp.set_linewidth(0.5)
        ax.set_xlabel(name, fontsize="small")
    legend = [Patch(facecolor=P.OURS_DARK, label="ordinary handoff"),
              Patch(facecolor=P.ACCENT, label="injected message"),
              Patch(facecolor=P.SEQ_BLUE[8], label="retained provenance")]
    fig.legend(handles=legend, loc="lower center", ncol=3, frameon=False, fontsize="small")
    return P.save(fig, "p13_sparsity_pattern", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
