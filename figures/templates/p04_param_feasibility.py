#!/usr/bin/env python3
"""A4 -- threat-model capability map.

Pattern: attacker query budget on the x-axis and a detector threshold on the
y-axis. Shade the tested region and label out-of-scope cells. Replace every
boundary with preregistered, evidence-linked conditions before publication.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def attack_score(budget, adaptive=False):
    score = 0.20 + 0.66 * (1.0 - np.exp(-budget / (34.0 if adaptive else 25.0)))
    return score + (0.05 * np.log1p(budget) / np.log(65.0) if adaptive else 0.0)


def make(venue="lncs", outdir=ROOT / "examples"):
    budget = np.linspace(0, 64, 200)
    threshold = 0.58 + 0.08 * np.sin(budget / 18.0)
    fixed = attack_score(budget)
    adaptive = attack_score(budget, adaptive=True)
    fig, ax = P.figure(venue, width="full", aspect=0.45)
    ax.fill_between(budget, threshold, 1.0, where=adaptive >= threshold, color=P.FEASIBLE,
                    lw=0, alpha=0.75, label="effect observed")
    ax.fill_between(budget, 0.0, threshold, color=P.NEUTRAL_MID, lw=0, alpha=0.8,
                    label="below detector threshold")
    ax.plot(budget, fixed, color=P.BASELINE_GREYS[0], lw=0.9, label="fixed attacker")
    ax.plot(budget, adaptive, color=P.OURS_DARK, lw=1.0, label="adaptive attacker")
    ax.plot(budget, threshold, color=P.CATEGORICAL[7], lw=0.9, linestyle="--", label="detector threshold")
    primary = 32.0
    primary_score = float(np.interp(primary, budget, adaptive))
    ax.plot([primary], [primary_score], marker="*", ms=9, color=P.ACCENT, mec="white", mew=0.6, zorder=5)
    ax.annotate("primary pilot", (primary, primary_score), xytext=(8, -3), textcoords="offset points",
                ha="left", va="top", fontsize="small")
    ax.text(3, 0.12, "below threshold", color=P.INK_MUTED, fontsize="small", style="italic")
    ax.text(42, 0.90, "effect region", color=P.INK_MUTED, fontsize="small", style="italic")
    ax.set_xlabel("attacker query budget")
    ax.set_ylabel("attack score / detector threshold")
    ax.set_xlim(0, 64)
    ax.set_ylim(0, 1.02)
    ax.legend(loc="lower right", fontsize="small", ncols=2)
    return P.save(fig, "p04_param_feasibility", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
