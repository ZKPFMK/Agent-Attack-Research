#!/usr/bin/env python3
"""toy_mining_demo.py -- the 8-step attack idea-mining loop on a fully synthetic multi-agent system.

    python3 toy_mining_demo.py              # full run (400 seeds per cell), prints every step
    python3 toy_mining_demo.py --seeds 100  # faster
    python3 toy_mining_demo.py --json out.json
    python3 toy_mining_demo.py --selftest   # asserts the qualitative findings (offline, stdlib, ~1 s)

NOTHING here is an LLM or a real system.  The "agents" are a few lines of rule-based arithmetic
(a bounded-confidence opinion-dynamics model, a classic from the social-simulation literature);
the "false claim" is an abstract proposition F with no content.  The point is the *method*:

  0 probe target       ASR of a naive injection (max-confidence claim at the chain head) at the sink agent
  1 cheap probes       two directions; one dies immediately (head injection never reaches the sink)
  Gate A               habit-fixed assumption: "state the false claim with maximal confidence"
  3 systematic search  sweep injection position k (smooth -> honest 'no anomaly') and claimed strength s
  Gate B               anomaly: a *weaker* claim beats the maximal one by a wide, significant margin
  5 root cause         ablate the victim's update rule term by term -> the bounded-confidence filter
  6 control            shifted priors separate 'P: distance to the receiver's belief' from the naive
                       'extreme claims look implausible'; removing the filter removes the anomaly
  7 validation         a second, structurally different agent family (stochastic voter-copy agents)
  8 generalise         other chain lengths / horizons + the limitation (no filter -> no effect)

Statistics are self-contained (Wilson CI, exact McNemar on paired seeds); in a real project use
`agentattack.metrics` and `aa rate` instead.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys

THRESH = 6          # an agent "believes F" when its confidence (0..10) is >= THRESH
NO_FILTER = 99      # eps large enough to disable bounded confidence


# ----------------------------------------------------------------- toy MAS ---

def simulate(n=8, rounds=6, k=0, s=10, eps=6, w=0.7, noise=0.1, prior=(1, 2, 3), family="avg", seed=0):
    """Chain 0 -> 1 -> ... -> n-1.  Each round agent i reads the belief of agent i-1 (previous round);
    the attacker additionally sends a message with confidence s to agent k every round.
    Families
      avg    : accept message m iff |m - own| <= eps, then own = round(w*m + (1-w)*own)
      voter  : accept message m iff |m - own| <= eps, then copy it (own = m) with probability 1/2
    Returns the list of final confidences."""
    r = random.Random(seed)
    b = [r.choice(prior) for _ in range(n)]
    for _ in range(rounds):
        new = b[:]
        for i in range(n):
            msgs = ([b[i - 1]] if i > 0 else []) + ([s] if i == k else [])
            for m in msgs:
                if abs(m - new[i]) > eps:
                    continue                       # bounded confidence: too-distant messages ignored
                if family == "avg":
                    new[i] = round(w * m + (1 - w) * new[i])
                elif r.random() < 0.5:
                    new[i] = m
            if r.random() < noise:
                new[i] = min(10, max(0, new[i] + r.choice((-1, 1))))
        b = new
    return b


def trials(seeds, **kw):
    """Binary success per seed: does the sink agent (decision maker) believe F at the end?"""
    return [simulate(seed=x, **kw)[-1] >= THRESH for x in range(seeds)]


# -------------------------------------------------------------- statistics ---

def wilson(k, n, z=1.96):
    if n == 0:
        return 0.0, 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, c - h), min(1.0, c + h)


def fmt(xs):
    p, lo, hi = wilson(sum(xs), len(xs))
    return f"{100 * p:5.1f}% [{100 * lo:4.1f}, {100 * hi:5.1f}] (n={len(xs)})"


def mcnemar(a, b):
    """Exact two-sided McNemar p for paired binary outcomes a, b (same seeds)."""
    n10 = sum(x and not y for x, y in zip(a, b))
    n01 = sum(y and not x for x, y in zip(a, b))
    m = n10 + n01
    if m == 0:
        return n10, n01, 1.0
    tail = sum(math.comb(m, i) for i in range(0, min(n10, n01) + 1)) / 2 ** m
    return n10, n01, min(1.0, 2 * tail)


# -------------------------------------------------------------------- loop ---

def mine(seeds=400, verbose=True):
    say = print if verbose else (lambda *a, **k: None)
    out = {}
    base = dict(n=8, rounds=6, eps=6)

    say("Pre-gate 0  access point: messages into ONE chain agent; success: sink agent's belief probe says F;"
        " payload: abstract proposition F (benign surrogate, nothing harmful to redact)")
    say("\n== Step 0  probe target: naive injection (k=0 head, s=10 max confidence)")
    naive = trials(seeds, k=0, s=10, **base)
    out["naive"] = sum(naive) / seeds
    say(f"   ASR(sink) = {fmt(naive)}")

    say("\n== Step 1  cheap probes")
    head_any = max(sum(trials(seeds // 4, k=0, s=s, **base)) for s in range(5, 11))
    out["head_any"] = head_any
    say(f"   direction 'better wording at the head': best over s=5..10 -> {head_any}/{seeds // 4} successes "
        "-> DEAD (the claim never travels 7 hops in 6 rounds: a propagation-horizon limit, recorded as negative)")
    say("   direction 'move the injection point': kept for Step 3")

    say("\n== Gate A  habit-fixed assumption: the payload states F with MAXIMAL confidence (s=10)."
        " Freed parameters: injection position k and claimed strength s")

    say("\n== Step 3  systematic search (k x s grid, sink ASR in %)")
    grid = {(k, s): trials(seeds, k=k, s=s, **base) for k in range(8) for s in range(5, 11)}
    say("   s\\k " + " ".join(f"{k:>5d}" for k in range(8)))
    for s in range(5, 11):
        say(f"   {s:>3d} " + " ".join(f"{100 * sum(grid[k, s]) / seeds:5.1f}" for k in range(8)))
    pos_curve = [sum(grid[k, 10]) for k in range(8)]
    out["position_monotone"] = all(a <= b for a, b in zip(pos_curve, pos_curve[1:]))
    say(f"   position sweep at s=10: monotone in k = {out['position_monotone']} -> smooth trend, NO anomaly")

    say("\n== Gate B  look for the outlier, not the best value (strength sweep at k=5)")
    sweep = {s: grid[5, s] for s in range(5, 11)}
    best = max(sweep, key=lambda s: sum(sweep[s]))
    b10, n01, p = mcnemar(sweep[best], sweep[10])
    out.update(best_s=best, p_best_vs_max=p, asr_best=sum(sweep[best]) / seeds, asr_max=sum(sweep[10]) / seeds)
    say(f"   best s={best}: {fmt(sweep[best])}   s=10: {fmt(sweep[10])}")
    say(f"   paired McNemar (same seeds) s={best} vs s=10: {b10} vs {n01} discordant, p={p:.2g}")
    say("   ANOMALY: a weaker false claim spreads further than the maximal one (non-monotone in s)")

    say("\n== Step 5  mechanistic root cause: ablate the victim's update rule one term at a time")
    abl = {"full rule": dict(eps=6), "no bounded-confidence filter": dict(eps=NO_FILTER),
           "no noise": dict(eps=6, noise=0.0), "w=0.5 instead of 0.7": dict(eps=6, w=0.5)}
    out["ablation"] = {}
    for name, kw in abl.items():
        kw = {**base, **kw}
        r_best = trials(seeds, k=5, s=best, **kw)
        r_max = trials(seeds, k=5, s=10, **kw)
        gap = (sum(r_best) - sum(r_max)) / seeds
        out["ablation"][name] = gap
        say(f"   {name:<30s} ASR(s={best}) - ASR(s=10) = {100 * gap:+6.1f} pp")
    say("   -> only removing the filter kills the gap.  Hypothesis P: a message is used iff "
        "|claimed - receiver's belief| <= eps, so s=10 is ignored by receivers with belief < 10-eps")

    say("\n== Step 6  control experiment (never skip)")
    say("   naive explanation N: 'agents distrust extreme claims' (absolute level)  -> s=10 fails for ANY prior")
    say("   property P: distance to the receiver's belief                          -> s=10 works if priors rise")
    hi = dict(base, prior=(4, 5, 6))
    c_max = trials(seeds, k=5, s=10, **hi)
    c_lowprior = sweep[10]
    out["control_shifted_prior_asr_max"] = sum(c_max) / seeds
    say(f"   priors {{4,5,6}}, s=10: {fmt(c_max)}  vs priors {{1,2,3}}: {fmt(c_lowprior)}"
        f"  -> {'P survives, N refuted' if sum(c_max) > sum(c_lowprior) + seeds // 5 else 'P NOT supported, back to 5'}")
    nf = {s: trials(seeds, k=5, s=s, **dict(base, eps=NO_FILTER)) for s in range(5, 11)}
    out["control_nofilter_best"] = max(nf, key=lambda s: (sum(nf[s]), s))
    say(f"   filter removed: best s = {out['control_nofilter_best']} (anomaly vanishes: max strength is best again)")

    say("\n== Step 7  validation on a second, structurally different family (stochastic voter-copy agents)")
    med = {s: trials(seeds, k=5, s=s, family="voter", **base) for s in range(5, 11)}
    mbest = max(med, key=lambda s: sum(med[s]))
    _, _, mp = mcnemar(med[mbest], med[10])
    out.update(voter_best_s=mbest, voter_p=mp)
    say(f"   family=voter: best s={mbest} {fmt(med[mbest])}  s=10 {fmt(med[10])}  McNemar p={mp:.2g}")
    say("   (in a real project: >= 2 model families AND >= 2 agent frameworks, see eval-protocol)")

    say("\n== Step 8  generalise + limitation")
    out["generalise"] = {}
    for n, rounds, k in ((6, 5, 3), (8, 6, 5), (12, 10, 9)):
        g = dict(n=n, rounds=rounds, eps=6)
        rb = trials(seeds, k=k, s=best, **g)
        rm = trials(seeds, k=k, s=10, **g)
        out["generalise"][f"n={n}"] = (sum(rb) - sum(rm)) / seeds
        say(f"   chain n={n:<2d} rounds={rounds:<2d} k={k}: ASR(s={best}) {fmt(rb)}  ASR(s=10) {fmt(rm)}")
    say("   claim (falsifiable): against bounded-confidence relays, the most effective claimed strength is the"
        " largest value within eps of the receivers' beliefs, not the maximum.")
    say("   limitation: no distance filter -> no effect (Step 6); head injection is horizon-limited (Step 1).")
    return out


def selftest() -> int:
    o = mine(seeds=200, verbose=False)
    assert o["naive"] < 0.05 and o["head_any"] == 0, o            # naive baseline and dead direction
    assert o["position_monotone"], o                               # honest 'no anomaly' sweep
    assert o["best_s"] < 10 and o["asr_best"] - o["asr_max"] > 0.3 and o["p_best_vs_max"] < 1e-6, o
    assert o["ablation"]["no bounded-confidence filter"] < 0 < o["ablation"]["no noise"], o
    assert o["control_shifted_prior_asr_max"] > o["asr_max"] + 0.2, o
    assert o["control_nofilter_best"] == 10, o
    assert o["voter_best_s"] < 10 and o["voter_p"] < 0.01, o
    assert all(v > 0.1 for v in o["generalise"].values()), o
    assert wilson(0, 10)[1] == 0.0 and abs(wilson(5, 10)[0] - 0.5) < 1e-12
    assert mcnemar([1, 1, 0], [0, 0, 0])[:2] == (2, 0)
    print("selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--seeds", type=int, default=400)
    ap.add_argument("--json", help="write the summary dict to this file")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    out = mine(a.seeds)
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump(out, fh, indent=2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
