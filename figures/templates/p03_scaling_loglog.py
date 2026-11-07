#!/usr/bin/env python3
"""A3 -- scaling curve with measured points and guide lines.

Pattern: trial count or token cost versus agents, rounds or task size on log
axes. Replace synthetic curves with results and state the tested regime; a guide
line is descriptive, not a universal bound.
"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "style"))
import palette as P
import numpy as np
from matplotlib.ticker import FixedLocator, FuncFormatter


def make(venue="lncs", outdir=ROOT / "examples"):
    rng = np.random.default_rng(3)
    log_agents = np.arange(2, 11)
    agents = 2.0 ** log_agents
    local = 2e-3 * agents * np.log2(agents) * (1 + rng.normal(0, 0.04, agents.size)) + 0.01
    global_ = 6e-5 * agents ** 2 * (1 + rng.normal(0, 0.04, agents.size)) + 0.01
    fig, ax = P.figure(venue, width="column" if venue != "lncs" else 0.62, aspect=0.75)
    for i, (values, name) in enumerate([(global_, "all-to-all relay"), (local, "local relay")]):
        color = P.BASELINE_GREYS[0] if i == 0 else P.OURS
        ax.loglog(agents, values, color=color, marker=P.MARKERS[i], linestyle="-", base=2)
        P.direct_label(ax, agents[-1], values[-1], name, dx=5)
    for guide, label in [(lambda a: a * np.log2(a), r"$O(a\log a)$"),
                         (lambda a: a ** 2, r"$O(a^2)$")]:
        g = guide(agents) / guide(agents[0]) * local[0]
        ax.loglog(agents, g, color=P.INK_MUTED, lw=0.6, linestyle=(0, (4, 2)), base=2, zorder=1)
        ax.annotate(label, (agents[-3], g[-3]), xytext=(4, -6), textcoords="offset points",
                    color=P.INK_MUTED, fontsize="small", ha="left", va="top")
    ax.xaxis.set_major_locator(FixedLocator(agents[::2]))
    ax.xaxis.set_major_formatter(FuncFormatter(lambda v, _: rf"$2^{{{int(round(np.log2(v)))}}}$"))
    ax.set_xlabel("number of agents")
    ax.set_ylabel("latency (s)")
    ax.set_xlim(agents[0] / 1.3, agents[-1] * 6)
    ax.grid(axis="both", which="major")
    return P.save(fig, "p03_scaling_loglog", outdir)


if __name__ == "__main__":
    P.cli(make, __doc__)
