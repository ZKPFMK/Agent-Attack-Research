"""Run an experiment grid trial-by-trial into a resumable jsonl file, with environment provenance.

    def trial(cond: dict, seed: int) -> dict:      # must return at least {"success": bool}
        ...
    run_matrix({"model": ["m1", "m2"], "defense": ["none", "spotlight"]}, trial, seeds=range(50),
               out="results/main/trials.jsonl")

Each output line = condition fields + seed + trial result + ``_key``.  Re-running skips finished keys,
so a crashed or rate-limited run can simply be restarted.  ``aa rate trials.jsonl --by model,defense``
turns it into an ASR table with Wilson CIs.
"""
from __future__ import annotations

import itertools
import json
import os
import platform
import subprocess
import sys
import time
from typing import Callable, Iterable


def env_record(**extra) -> dict:
    def git(*args):
        try:
            return subprocess.run(["git", *args], capture_output=True, text=True, timeout=10).stdout.strip()
        except (OSError, subprocess.SubprocessError):
            return ""
    return {"python": sys.version.split()[0], "platform": platform.platform(), "host": platform.node(),
            "git_commit": git("rev-parse", "--short", "HEAD"), "git_dirty": bool(git("status", "--porcelain")),
            "date": time.strftime("%Y-%m-%d"), **extra}


def grid(spec: dict[str, Iterable]) -> list[dict]:
    keys = list(spec)
    return [dict(zip(keys, vals)) for vals in itertools.product(*(list(spec[k]) for k in keys))]


def _key(cond: dict, seed: int) -> str:
    return json.dumps({**cond, "seed": seed}, sort_keys=True, ensure_ascii=False)


def run_matrix(spec: dict[str, Iterable], trial_fn: Callable[[dict, int], dict], seeds: Iterable[int], out: str,
               env: dict | None = None, interleave: bool = True) -> dict:
    """Execute every (condition, seed) once.  ``interleave`` runs seed-major so that drift over time
    (API changes, rate limiting) hits all conditions equally instead of one condition block."""
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    done = set()
    if os.path.exists(out):
        with open(out, encoding="utf-8") as fh:
            for line in fh:
                if line.strip():
                    rec = json.loads(line)
                    if "_key" in rec:
                        done.add(rec["_key"])
    meta_path = out + ".env.json"
    if not os.path.exists(meta_path):
        with open(meta_path, "w", encoding="utf-8") as fh:
            json.dump(env or env_record(), fh, indent=1)
    conds, seeds = grid(spec), list(seeds)
    order = [(c, s) for s in seeds for c in conds] if interleave else [(c, s) for c in conds for s in seeds]
    ran = skipped = 0
    with open(out, "a", encoding="utf-8") as fh:
        for c, s in order:
            k = _key(c, s)
            if k in done:
                skipped += 1
                continue
            res = trial_fn(dict(c), s)
            fh.write(json.dumps({**c, "seed": s, **res, "_key": k}, ensure_ascii=False) + "\n")
            fh.flush()
            ran += 1
    return {"ran": ran, "skipped": skipped, "total": len(order), "out": out}


def load_records(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as fh:
        return [json.loads(l) for l in fh if l.strip()]
