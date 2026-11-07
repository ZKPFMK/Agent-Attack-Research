#!/usr/bin/env python3
"""A12 -- budget crossover: where effectiveness changes with attack budget.

Pattern: synthetic curves over message/query budget, a crossover region marker
and measured points overlaid to show calibration. The threshold is local to the
protocol and is not a universal claim.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def make(venue="lncs", outdir=ROOT / "examples"):
    budget = np.linspace(2, 64, 400)
    fixed_cost = 1.6 * budget + 5
    adaptive_cost = 8.5 * np.sqrt(budget) + 8
    crossover = budget[np.argmin(np.abs(fixed_cost - adaptive_cost))]
    fig, ax = P.figure(venue, width="full", aspect=0.42)
    ax.axvspan(budget[0], crossover, color=P.SEQ_ORANGE[0], lw=0, alpha=0.6)
    ax.axvspan(crossover, budget[-1], color=P.SEQ_BLUE[0], lw=0, alpha=0.6)
    ax.plot(budget, fixed_cost, color=P.ACCENT, label="fixed prompt")
    ax.plot(budget, adaptive_cost, color=P.OURS, linestyle="--", label="adaptive prompt")
    rng = np.random.default_rng(5)
    measured = np.array([4, 8, 16, 32, 48, 64])
    ax.plot(measured, 8.5 * np.sqrt(measured) + 8 + rng.normal(0, 1.0, measured.size), "o",
            color=P.OURS, ms=3.5, mec="white", mew=0.5, label="adaptive measured")
    ax.axvline(crossover, color=P.INK_2, lw=0.6)
    ax.text(crossover, ax.get_ylim()[1] * 0.97, f" crossover $b\\approx{crossover:.0f}$", va="top",
            fontsize="small")
    ax.text((budget[0] + crossover) / 2, 10, "fixed cheaper", ha="center", fontsize="small", color=P.INK_2)
    ax.text((crossover + budget[-1]) / 2, 10, "adaptive cheaper", ha="center", fontsize="small", color=P.INK_2)
    ax.set_xlabel("query budget")
    ax.set_ylabel("evaluation cost (s)")
    ax.set_xlim(budget[0], budget[-1])
    ax.set_ylim(0, 150)
    ax.legend(loc="upper left", bbox_to_anchor=(0.0, 0.9))
    return P.save(fig, "p12_crossover_cost", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
