"""Adapter recipes: how to benchmark each public baseline with crbench.

These are *recipes*, not vendored code.  Each entry tells you which parser to use
and a typical command template (run from the baseline's build directory, see
``references/baselines/MANIFEST.md`` (benchmarks, prior attacks, defenses) for fetch/pin/build).  ``{target}`` and
``{threads}`` are placeholders you fill in.

Fairness reminders printed by ``crbench adapters NAME`` come from the manifest's
fairness checklist: same parameters, same thread count, same compiler and flags,
same machine, interleaved rounds.
"""
from __future__ import annotations

ADAPTERS: dict[str, dict] = {
    "agent-harness": {"parser": "generic", "cmd": "python run_trials.py --cond {target}",
                      "notes": "Your own trial runner (agentattack.runner.run_matrix). Success rates come from `aa rate`; "
                               "use crbench only for wall-clock/latency. Record model snapshot id, temperature, seed."},
    "defense-overhead": {"parser": "generic", "cmd": "python measure_overhead.py --defense {target}",
                         "notes": "Latency/token overhead of a defense: same tasks, same model snapshot, interleaved arms, "
                                  "report median + IQR per task and end-to-end."},
    "agentdojo-style": {"parser": "generic", "cmd": "python -m <benchmark>.scripts.benchmark --model {target}",
                        "notes": "Pin the benchmark commit and the suite version in baselines/MANIFEST.md; record utility "
                                 "with and without attack, and the attack/defense names exactly as the benchmark spells them."},
    "local-llm-server": {"parser": "generic", "cmd": "python bench_requests.py --base-url http://127.0.0.1:8000/v1 --model {target}",
                         "notes": "vLLM/Ollama/llama.cpp server: record server version, quantisation, max context, GPU, "
                                  "and keep threads/batching identical across arms."},
    "gnu-time": {"parser": "gnu-time", "cmd": "/usr/bin/time -v {target}", "notes": "Peak memory (max RSS)."},
}


def describe(name: str) -> str:
    a = ADAPTERS[name]
    return f"{name}: parser={a['parser']}\n  cmd:   {a['cmd']}\n  notes: {a['notes']}"


if __name__ == "__main__":
    for n in ADAPTERS:
        assert ADAPTERS[n]["parser"]
        print(describe(n))
