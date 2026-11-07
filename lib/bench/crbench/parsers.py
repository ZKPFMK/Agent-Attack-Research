"""Regex-based, pluggable log-parser registry.

A *parser* turns raw tool output into a list of :class:`Record` objects with
normalised units (time -> seconds and memory/traffic -> bytes). Agent trial
JSONL also exposes success, utility, detection, token, query and cost metrics.

Shipped parsers (names used by ``crbench parse --parser NAME``):

``agent-jsonl``        Agent-harness JSONL with latency, outcome and budget fields.
``generic``            "time: 1.23 s", "Elapsed = 12 ms", "took 3.4sec", "RESULT name=... time=..."
``criterion``          Rust Criterion output: ``time: [1.1 ms 1.2 ms 1.3 ms]``
``gobench``            Go ``testing`` output: ``BenchmarkX-8  100  12345 ns/op``
``gbench``             Google Benchmark output: ``BM_X  123 ns  120 ns  1000``
``sat``                Solver-harness output: solve time plus SAT/UNSAT status
``gnu-time``           ``/usr/bin/time -v``: wall clock and maximum RSS

The registry intentionally contains no cryptography-specific parser. A research
project may register a local parser for a pinned benchmark, but the resulting
records must still be mapped to the Agent Attack evidence schema.

Register your own with :func:`register_parser` (see ``tests/test_parsers.py``).
"""
from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass
from typing import Callable, Iterable

TIME_UNITS = {
    "ns": 1e-9, "nanoseconds": 1e-9,
    "us": 1e-6, "µs": 1e-6, "μs": 1e-6, "microseconds": 1e-6,
    "ms": 1e-3, "milliseconds": 1e-3, "msec": 1e-3,
    "s": 1.0, "sec": 1.0, "secs": 1.0, "second": 1.0, "seconds": 1.0,
    "min": 60.0, "mins": 60.0, "minutes": 60.0,
    "h": 3600.0, "hours": 3600.0,
}
SIZE_UNITS = {
    "b": 1, "byte": 1, "bytes": 1,
    "kb": 1e3, "mb": 1e6, "gb": 1e9,
    "kib": 1024, "mib": 1024 ** 2, "gib": 1024 ** 3,
}
NUM = r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?"
TU = r"(?:ns|us|µs|μs|ms|msec|milliseconds|microseconds|nanoseconds|seconds|second|secs|sec|s|minutes|mins|min|hours|h)"


def to_seconds(value: float, unit: str) -> float:
    u = unit.strip()
    factor = TIME_UNITS.get(u, TIME_UNITS.get(u.lower()))
    if factor is None:
        raise ValueError(f"unknown time unit {unit!r}")
    return float(value) * factor


def to_bytes(value: float, unit: str) -> float:
    u = unit.strip().lower()
    if u not in SIZE_UNITS:
        raise ValueError(f"unknown size unit {unit!r}")
    return float(value) * SIZE_UNITS[u]


@dataclass
class Record:
    metric: str            # e.g. "time", "success", "tokens", "max_rss", "sat_status"
    value: float | str
    unit: str              # normalised unit: "s", "B", "bits", "" ...
    label: str = ""        # benchmark / attack / timer name if the log provides one
    line: int = 0          # 1-based line number in the source text
    raw: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


ParserFn = Callable[[str], list[Record]]


@dataclass
class Parser:
    name: str
    fn: ParserFn
    description: str = ""
    sniff: re.Pattern | None = None  # used by auto-detection


REGISTRY: dict[str, Parser] = {}


def register_parser(name: str, description: str = "", sniff: str | None = None):
    """Decorator: ``@register_parser("mytool", sniff=r"MyTool v\\d")``."""

    def deco(fn: ParserFn) -> ParserFn:
        REGISTRY[name] = Parser(name, fn, description, re.compile(sniff, re.M) if sniff else None)
        return fn

    return deco


def regex_parser(name: str, pattern: str, metric: str = "time", kind: str = "time",
                 description: str = "", sniff: str | None = None, flags=re.M | re.I) -> ParserFn:
    """Build and register a one-regex parser.

    ``pattern`` must have named groups ``value`` and ``unit`` (``unit`` optional ->
    seconds for time), and optionally ``label``.
    """
    rx = re.compile(pattern, flags)

    def fn(text: str) -> list[Record]:
        out = []
        for m in rx.finditer(text):
            gd = m.groupdict()
            v = float(gd["value"])
            unit = gd.get("unit") or ("s" if kind == "time" else "")
            if kind == "time":
                v, unit = to_seconds(v, unit), "s"
            elif kind == "size":
                v, unit = to_bytes(v, unit), "B"
            out.append(Record(metric, v, unit, (gd.get("label") or "").strip(),
                              text.count("\n", 0, m.start()) + 1, m.group(0).strip()))
        return out

    register_parser(name, description, sniff)(fn)
    return fn


def _lineno(text: str, pos: int) -> int:
    return text.count("\n", 0, pos) + 1


# ---------------------------------------------------------------- agent JSONL
_AGENT_KEYS = {
    "success": "success", "utility": "utility", "stealth": "stealth", "detected": "detected",
    "false_trigger": "false_trigger", "tokens": "tokens", "input_tokens": "input_tokens",
    "output_tokens": "output_tokens", "queries": "queries", "cost": "cost",
    "latency": "time", "latency_s": "time", "duration": "time", "duration_s": "time",
    "time": "time",
}
_AGENT_TIME_MS = {"latency_ms", "duration_ms", "time_ms"}


@register_parser("agent-jsonl", "Agent-harness JSONL: success/utility/detected, latency, tokens, queries and cost",
                 sniff=r'^\s*\{.*"(?:success|utility|detected|latency|tokens|queries|cost)"')
def parse_agent_jsonl(text: str) -> list[Record]:
    """Parse one JSON object per line, as emitted by ``agentattack.runner``.

    Unknown condition fields are deliberately ignored; they remain available in
    the raw JSONL and should be grouped with ``aa rate`` rather than flattened
    into a timing record.
    """
    out = []
    for ln, raw in enumerate(text.splitlines(), 1):
        if not raw.strip():
            continue
        try:
            obj = json.loads(raw)
        except json.JSONDecodeError:
            continue
        if not isinstance(obj, dict):
            continue
        label = str(obj.get("arm") or obj.get("attack") or obj.get("condition") or obj.get("task") or "")
        for key, metric in _AGENT_KEYS.items():
            if key not in obj or not isinstance(obj[key], (bool, int, float)):
                continue
            value = float(obj[key])
            unit = ""
            if metric == "time":
                unit = "s"
            out.append(Record(metric, value, unit, label, ln, raw.strip()))
        for key in _AGENT_TIME_MS:
            if isinstance(obj.get(key), (int, float)):
                out.append(Record("time", float(obj[key]) * 1e-3, "s", label, ln, raw.strip()))
        if isinstance(obj.get("status"), str):
            out.append(Record("status", obj["status"], "", label, ln, raw.strip()))
    return out


# ---------------------------------------------------------------- generic
_GENERIC = re.compile(
    rf"^(?P<label>[^\n:=]*?)\b(?:time|elapsed|took|duration|runtime|latency)\b\s*(?:\([^)]*\))?\s*[:=]?\s*(?P<value>{NUM})\s*(?P<unit>{TU})\b",
    re.I | re.M,
)
_RESULT_KV = re.compile(r"^RESULT\b(?P<body>.*)$", re.M)


@register_parser("generic", "time: X s / elapsed = X ms / took X sec; RESULT k=v lines")
def parse_generic(text: str) -> list[Record]:
    out = []
    for m in _GENERIC.finditer(text):
        out.append(Record("time", to_seconds(float(m["value"]), m["unit"]), "s",
                          m["label"].strip(" \t-:>"), _lineno(text, m.start()), m.group(0).strip()))
    for m in _RESULT_KV.finditer(text):
        kv = dict(re.findall(r"(\w+)=(\S+)", m["body"]))
        label = kv.pop("name", kv.pop("label", ""))
        for k, v in kv.items():
            tm = re.fullmatch(rf"({NUM})({TU})?", v)
            if not tm:
                if k in ("status", "check", "verdict"):
                    out.append(Record(k, v, "", label, _lineno(text, m.start()), m.group(0)))
                continue
            val, unit = float(tm.group(1)), tm.group(2)
            if unit:
                out.append(Record(k, to_seconds(val, unit), "s", label, _lineno(text, m.start()), m.group(0)))
            else:
                out.append(Record(k, val, "", label, _lineno(text, m.start()), m.group(0)))
    return out


# ---------------------------------------------------------------- criterion (Rust)
_CRIT = re.compile(
    rf"^(?P<label>\S[^\n]*?)?\s*\n?\s*time:\s+\[(?P<lo>{NUM})\s*(?P<ulo>\S+)\s+(?P<mid>{NUM})\s*(?P<umid>\S+)\s+(?P<hi>{NUM})\s*(?P<uhi>[^\]\s]+)\s*\]",
    re.M,
)


@register_parser("criterion", "Rust criterion: time: [lo mid hi]; reports mid (point estimate) plus lo/hi",
                 sniff=r"time:\s+\[")
def parse_criterion(text: str) -> list[Record]:
    out = []
    for m in _CRIT.finditer(text):
        label = (m["label"] or "").strip()
        ln = _lineno(text, m.start("lo"))
        out.append(Record("time", to_seconds(float(m["mid"]), m["umid"]), "s", label, ln, m.group(0).strip()))
        out.append(Record("time_lo", to_seconds(float(m["lo"]), m["ulo"]), "s", label, ln))
        out.append(Record("time_hi", to_seconds(float(m["hi"]), m["uhi"]), "s", label, ln))
    return out


# ---------------------------------------------------------------- go test -bench
_GOB = re.compile(rf"^(?P<label>Benchmark\S+?)(?:-\d+)?\s+(?P<iters>\d+)\s+(?P<value>{NUM})\s+ns/op(?P<rest>.*)$", re.M)


@register_parser("gobench", "go test -bench: BenchmarkX-8  N  T ns/op [B/op allocs/op]", sniff=r"^Benchmark\S+\s+\d+\s+\S+\s+ns/op")
def parse_gobench(text: str) -> list[Record]:
    out = []
    for m in _GOB.finditer(text):
        ln = _lineno(text, m.start())
        out.append(Record("time", float(m["value"]) * 1e-9, "s", m["label"], ln, m.group(0).strip()))
        bm = re.search(rf"({NUM})\s+B/op", m["rest"])
        if bm:
            out.append(Record("alloc", float(bm.group(1)), "B", m["label"], ln))
    return out


# ---------------------------------------------------------------- google benchmark
_GB = re.compile(rf"^(?P<label>BM_\S+|\S+/\S+)\s+(?P<wall>{NUM})\s+(?P<uw>ns|us|ms|s)\s+(?P<cpu>{NUM})\s+(?P<uc>ns|us|ms|s)\s+(?P<iters>\d+)", re.M)


@register_parser("gbench", "Google Benchmark console: name  Time unit  CPU unit  Iterations", sniff=r"^-{20,}\s*\n?Benchmark\s+Time\s+CPU")
def parse_gbench(text: str) -> list[Record]:
    out = []
    for m in _GB.finditer(text):
        ln = _lineno(text, m.start())
        out.append(Record("time", to_seconds(float(m["wall"]), m["uw"]), "s", m["label"], ln, m.group(0).strip()))
        out.append(Record("cpu_time", to_seconds(float(m["cpu"]), m["uc"]), "s", m["label"], ln))
    return out


# ---------------------------------------------------------------- solver status
_SAT_T = re.compile(
    rf"^c\s+(?:total process time since initialization|Total time(?: \(this thread\))?|process-time|total real time since initialization)\s*:?\s*(?P<value>{NUM})\s*(?P<unit>seconds|s)?",
    re.M | re.I,
)
_SAT_S = re.compile(r"^s\s+(SATISFIABLE|UNSATISFIABLE|UNKNOWN)\s*$", re.M)


@register_parser("sat", "Solver-harness output: 'c total process time ...' plus 's SATISFIABLE'", sniff=r"^s\s+(?:UN)?SATISFIABLE")
def parse_sat(text: str) -> list[Record]:
    out = [Record("time", float(m["value"]), "s", "solver", _lineno(text, m.start()), m.group(0).strip()) for m in _SAT_T.finditer(text)]
    for m in _SAT_S.finditer(text):
        out.append(Record("sat_status", m.group(1), "", "solver", _lineno(text, m.start()), m.group(0).strip()))
    return out


# ---------------------------------------------------------------- GNU time -v
_GT_W = re.compile(r"Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*(?P<value>[\d:.]+)")
_GT_M = re.compile(r"Maximum resident set size \(kbytes\):\s*(?P<value>\d+)")


@register_parser("gnu-time", "/usr/bin/time -v wall clock + max RSS", sniff=r"Maximum resident set size")
def parse_gnu_time(text: str) -> list[Record]:
    out = []
    for m in _GT_W.finditer(text):
        parts = [float(p) for p in m["value"].split(":")]
        secs = 0.0
        for p in parts:
            secs = secs * 60 + p
        out.append(Record("time", secs, "s", "wall", _lineno(text, m.start()), m.group(0).strip()))
    for m in _GT_M.finditer(text):
        out.append(Record("max_rss", float(m["value"]) * 1024, "B", "process", _lineno(text, m.start()), m.group(0).strip()))
    return out


# ---------------------------------------------------------------- dispatch
def detect(text: str) -> list[str]:
    """Return names of parsers whose sniff pattern matches ``text`` (most specific first)."""
    hits = [p.name for p in REGISTRY.values() if p.sniff is not None and p.sniff.search(text)]
    return hits or ["generic"]


def parse_text(text: str, parser: str | Iterable[str] = "auto") -> list[Record]:
    names = detect(text) if parser == "auto" else ([parser] if isinstance(parser, str) else list(parser))
    out: list[Record] = []
    for n in names:
        if n not in REGISTRY:
            raise KeyError(f"unknown parser {n!r}; known: {sorted(REGISTRY)}")
        out.extend(REGISTRY[n].fn(text))
    return out


def parse_file(path: str, parser: str = "auto") -> list[Record]:
    with open(path, encoding="utf-8", errors="replace") as f:
        return parse_text(f.read(), parser)


def values(records: Iterable[Record], metric: str = "time", label: str | None = None) -> list[float]:
    return [float(r.value) for r in records if r.metric == metric and (label is None or r.label == label)]


if __name__ == "__main__":
    demo = '{"arm":"proposed","task":"tool-routing","latency_ms":12.5,"success":true,"tokens":384,"queries":2}\n'
    for r in parse_text(demo, "agent-jsonl"):
        print(r)
