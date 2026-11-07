#!/usr/bin/env python3
"""A9 -- sensitivity curve across attack conditions.

Pattern: plot synthetic success or detection across rounds/budget conditions;
mark the preregistered primary cell and the point where the effect weakens.
The curve is an illustration, not a security bound.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def make(venue="lncs", outdir=ROOT / "examples"):
    rounds = np.arange(1, 17)
    naive = np.array([.08, .12, .17, .22, .28, .33, .37, .40, .43, .45, .47, .48, .49, .50, .50, .51])
    proposed = np.array([.12, .20, .29, .38, .47, .55, .62, .67, .71, .74, .76, .78, .79, .80, .80, .81])
    defended = np.array([.05, .07, .09, .12, .15, .18, .20, .21, .22, .22, .23, .23, .24, .24, .24, .25])
    threshold = 0.50
    fig, ax = P.figure(venue, width="full", aspect=0.42)
    ax.step(rounds, naive, where="mid", color=P.BASELINE_GREYS[0], marker="o", ms=3, label="naive injection")
    ax.step(rounds, proposed, where="mid", color=P.OURS, marker="o", ms=3, label="proposed attack")
    ax.step(rounds, defended, where="mid", color=P.ACCENT, marker="s", ms=3, linestyle="--", label="static defense")
    ax.axhline(threshold, color=P.INK_2, lw=0.8)
    ax.text(0.7, threshold + 0.02, "primary success threshold", fontsize="small", color=P.INK_2)
    first = int(rounds[np.argmax(proposed >= threshold)])
    ax.axvline(first, color=P.INK_MUTED, lw=0.6, linestyle=(0, (1, 1.5)))
    ax.annotate("primary budget", xy=(first, threshold), xytext=(first + 1, threshold - 0.12),
                arrowprops=dict(arrowstyle="->", lw=0.7, color=P.INK_MUTED), fontsize="small")
    ax.set_xlabel("message rounds")
    ax.set_ylabel("attack success rate")
    ax.set_xticks(rounds)
    ax.set_ylim(0, 0.9)
    ax.legend(loc="upper left", bbox_to_anchor=(0, 0.93))
    return P.save(fig, "p09_trail_bounds", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
