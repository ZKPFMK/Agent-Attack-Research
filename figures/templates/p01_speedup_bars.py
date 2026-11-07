#!/usr/bin/env python3
"""A1 -- effectiveness bars with a clean-control reference line.

Pattern: grouped synthetic bars for attack success by task. Controls and the
proposed mechanism use redundant encodings; replace arrays with logged trials
and Wilson intervals before publication.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def make(venue="lncs", outdir=ROOT / "examples"):
    tasks = ["Browse", "Retrieve", "Plan", "Tool use", "Memory"]
    rng = np.random.default_rng(1)
    naive = np.array([0.18, 0.24, 0.21, 0.16, 0.28])
    proposed = np.array([0.34, 0.48, 0.43, 0.31, 0.57]) + rng.normal(0, 0.006, 5)
    clean_false_trigger = 0.04
    fig, ax = P.figure(venue, width="full", aspect=0.42)
    x = np.arange(len(tasks))
    w = 0.36
    ax.bar(x - w / 2, naive, w * 0.94, color=P.BASELINE_GREYS[2], label="Naive injection")
    bars = ax.bar(x + w / 2, proposed, w * 0.94, color=P.OURS, label="Proposed attack")
    ax.axhline(clean_false_trigger, color=P.INK_2, lw=0.8, zorder=3)
    ax.text(len(tasks) - 0.4, clean_false_trigger + 0.012, "Clean false-trigger", va="bottom", ha="right",
            color=P.INK_2, fontsize="small")
    for b, v in zip(bars, proposed):
        ax.text(b.get_x() + b.get_width() / 2, v, f"{100 * v:.0f}%", ha="center", va="bottom",
                fontsize="small", color=P.INK)
    ax.set_title(f"mean proposed ASR: {100 * proposed.mean():.1f}%", loc="left", fontsize="small",
                 color=P.INK_2)
    ax.set_xticks(x, tasks)
    ax.set_ylabel("attack success rate")
    ax.set_ylim(0, proposed.max() * 1.22)
    ax.set_xlim(-0.6, len(tasks) + 0.15)
    ax.tick_params(axis="x", length=0)
    ax.legend(loc="upper left", ncols=2)
    return P.save(fig, "p01_speedup_bars", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
