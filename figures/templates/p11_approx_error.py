#!/usr/bin/env python3
"""A11 -- judge agreement or rubric-threshold error curve.

Pattern: top panel shows reference human labels and judge scores; bottom panel
shows agreement and kappa as the rubric threshold changes. Report kappa,
precision, recall and F1 from the labelled sample alongside the figure.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np


def kappa(gold, pred):
    gold = np.asarray(gold, dtype=int)
    pred = np.asarray(pred, dtype=int)
    po = float(np.mean(gold == pred))
    pg = np.bincount(gold, minlength=2) / len(gold)
    pp = np.bincount(pred, minlength=2) / len(pred)
    pe = float(np.dot(pg, pp))
    return (po - pe) / (1.0 - pe) if pe < 1.0 else 1.0


def make(venue="lncs", outdir=ROOT / "examples"):
    rng = np.random.default_rng(13)
    count = 40
    ids = np.arange(count)
    judge_score = np.clip(np.linspace(0.03, 0.97, count) + rng.normal(0, 0.09, count), 0, 1)
    human = (np.linspace(0.03, 0.97, count) > 0.56).astype(int)
    thresholds = np.linspace(0.15, 0.85, 29)
    agreement, kappas = [], []
    for threshold in thresholds:
        pred = (judge_score >= threshold).astype(int)
        agreement.append(np.mean(pred == human))
        kappas.append(kappa(human, pred))
    default = 0.55
    default_pred = (judge_score >= default).astype(int)
    fig, (a1, a2) = P.figure(venue, width="full", aspect=0.62, nrows=2, sharex=False,
                             gridspec_kw={"height_ratios": [1, 1.6]})
    a1.scatter(ids, human, s=14, color=P.BASELINE_GREYS[0], label="human label", zorder=3)
    a1.scatter(ids, judge_score, s=10, color=P.OURS, label="judge score", zorder=2)
    a1.axhline(default, color=P.INK_MUTED, lw=0.7, linestyle="--")
    a1.set_ylim(-0.08, 1.08)
    a1.set_ylabel("label / score")
    a1.set_title(f"default agreement = {100 * np.mean(default_pred == human):.1f}%",
                 loc="left", fontsize="small", color=P.INK_2)
    a1.legend(loc="upper left", ncols=2, fontsize="small")
    a2.plot(thresholds, agreement, color=P.OURS, lw=1.0, label="accuracy")
    a2.plot(thresholds, kappas, color=P.ACCENT, lw=1.0, linestyle="--", label="Cohen's kappa")
    a2.axvline(default, color=P.INK_MUTED, lw=0.7)
    a2.axhline(0.7, color=P.INK_2, lw=0.7, linestyle=(0, (3, 2)))
    a2.text(default + 0.015, 0.71, "$\\kappa=0.7$ review threshold", fontsize="small", color=P.INK_2)
    a2.set_xlabel("positive-label threshold")
    a2.set_ylabel("agreement")
    a2.set_xlim(0.1, 0.9)
    a2.set_ylim(0, 1.02)
    a2.legend(loc="lower left")
    return P.save(fig, "p11_approx_error", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
