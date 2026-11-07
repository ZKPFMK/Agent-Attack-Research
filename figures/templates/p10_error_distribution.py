#!/usr/bin/env python3
"""A10 -- trial latency/token distribution with a tail threshold.

Pattern: histogram of a synthetic evaluation metric on a log y-axis, with a
policy threshold and sample count. Replace the samples with raw trial records;
do not infer a rare-event rate from a short tail.
"""
import sys, pathlib, math
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def make(venue="lncs", outdir=ROOT / "examples"):
    rng = np.random.default_rng(11)
    sample_count = 20_000
    latency = rng.lognormal(mean=4.2, sigma=0.42, size=sample_count)
    threshold = float(np.percentile(latency, 95))
    tail = float(np.mean(latency > threshold))
    fig, ax = P.figure(venue, width="full", aspect=0.42)
    bins = np.linspace(0, 180, 61)
    hist, edges = np.histogram(latency, bins)
    centers = (edges[:-1] + edges[1:]) / 2
    ax.bar(centers, hist / sample_count, width=edges[1] - edges[0], color=P.SEQ_BLUE[4], lw=0,
           label=f"empirical (N={sample_count:,})")
    for marker, label in [(threshold, "95th percentile")]:
        ax.axvline(marker, color=P.CATEGORICAL[7], lw=0.9, label=label)
    ax.text(threshold - 2, 1e-2, f"tail = {100 * tail:.1f}%", ha="right", fontsize="small")
    ax.set_yscale("log")
    ax.set_ylim(1e-5, 0.2)
    ax.set_xlabel("trial latency (ms)")
    ax.set_ylabel("frequency")
    ax.legend(loc="upper right")
    return P.save(fig, "p10_error_distribution", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
