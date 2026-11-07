"""Rates with honest uncertainty: attack success rate (ASR), utility, false-trigger rate, stealth.

Every rate printed in a paper should carry n and a 95% interval.  ``Rate.fmt()`` produces the
canonical string that goes into EVIDENCE.md, e.g. ``"41.0% [35.6, 46.6] (n=300)"``.
"""
from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Callable, Iterable, Sequence


def wilson_ci(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score interval for a binomial proportion k/n (well-behaved at 0, n and small n)."""
    if n <= 0:
        return (0.0, 1.0)
    if not 0 <= k <= n:
        raise ValueError(f"need 0 <= k <= n, got k={k}, n={n}")
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (max(0.0, centre - half), min(1.0, centre + half))


@dataclass(frozen=True)
class Rate:
    k: int
    n: int
    z: float = 1.96

    @property
    def p(self) -> float:
        return self.k / self.n if self.n else float("nan")

    @property
    def lo(self) -> float:
        return wilson_ci(self.k, self.n, self.z)[0]

    @property
    def hi(self) -> float:
        return wilson_ci(self.k, self.n, self.z)[1]

    def fmt(self, digits: int = 1) -> str:
        if not self.n:
            return "n/a (n=0)"
        f = f"{{:.{digits}f}}"
        return f"{f.format(100 * self.p)}% [{f.format(100 * self.lo)}, {f.format(100 * self.hi)}] (n={self.n})"

    def as_dict(self) -> dict:
        return {"k": self.k, "n": self.n, "p": self.p, "lo": self.lo, "hi": self.hi, "fmt": self.fmt()}


def _truthy(v) -> bool:
    if isinstance(v, str):
        return v.strip().lower() in ("1", "true", "yes", "y", "success", "succeeded")
    return bool(v)


def rate(records: Iterable[dict], key: str = "success") -> Rate:
    """Rate of truthy ``record[key]`` over records that have the key (missing = not counted)."""
    vals = [_truthy(r[key]) for r in records if key in r and r[key] is not None]
    return Rate(sum(vals), len(vals))


def rate_table(records: Sequence[dict], by: Sequence[str], key: str = "success") -> list[dict]:
    """Group records by the fields in ``by`` and compute a Rate per group (sorted by group key)."""
    groups: dict[tuple, list[dict]] = {}
    for r in records:
        groups.setdefault(tuple(str(r.get(b, "")) for b in by), []).append(r)
    out = []
    for g in sorted(groups):
        rt = rate(groups[g], key)
        out.append({**dict(zip(by, g)), "rate": rt})
    return out


def bootstrap_ci(values: Sequence[float], stat: Callable[[Sequence[float]], float] | None = None,
                 B: int = 2000, seed: int = 0, alpha: float = 0.05) -> tuple[float, float, float]:
    """Percentile bootstrap: returns (estimate, lo, hi).  Default statistic = mean."""
    if not values:
        raise ValueError("bootstrap_ci needs at least one value")
    stat = stat or (lambda xs: sum(xs) / len(xs))
    rng = random.Random(seed)
    n = len(values)
    reps = sorted(stat([values[rng.randrange(n)] for _ in range(n)]) for _ in range(B))
    lo = reps[int(math.floor(alpha / 2 * (B - 1)))]
    hi = reps[int(math.ceil((1 - alpha / 2) * (B - 1)))]
    return stat(values), lo, hi


def mcnemar(b: int, c: int) -> float:
    """Exact two-sided McNemar p-value for paired binary outcomes.

    b = #pairs where only arm A succeeded, c = #pairs where only arm B succeeded (same tasks/seeds).
    """
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n
    return min(1.0, 2 * tail)


def paired_counts(a: Sequence[bool], b: Sequence[bool]) -> tuple[int, int]:
    """(only-a, only-b) discordant counts for paired outcomes, for :func:`mcnemar`."""
    if len(a) != len(b):
        raise ValueError("paired outcomes must have equal length")
    return (sum(1 for x, y in zip(a, b) if x and not y), sum(1 for x, y in zip(a, b) if y and not x))


def diff_ci(r1: Rate, r2: Rate, z: float = 1.96) -> tuple[float, float, float]:
    """Newcombe hybrid-score interval for p1 - p2 (independent samples). Returns (diff, lo, hi)."""
    l1, u1 = wilson_ci(r1.k, r1.n, z)
    l2, u2 = wilson_ci(r2.k, r2.n, z)
    d = r1.p - r2.p
    lo = d - math.sqrt((r1.p - l1) ** 2 + (u2 - r2.p) ** 2)
    hi = d + math.sqrt((u1 - r1.p) ** 2 + (r2.p - l2) ** 2)
    return d, max(-1.0, lo), min(1.0, hi)


def n_for_halfwidth(halfwidth: float, p: float = 0.5, z: float = 1.96) -> int:
    """Trials per cell so that a normal-approximation 95% CI has at most this half-width."""
    if not 0 < halfwidth < 1:
        raise ValueError("halfwidth must be in (0, 1)")
    return math.ceil(z * z * p * (1 - p) / halfwidth ** 2)
