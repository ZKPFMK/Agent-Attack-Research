"""crbench -- a small, dependency-light measurement harness + EVIDENCE ledger.

In agent-attack projects, success rates come from ``aa rate`` (lib/agentattack); crbench is used for
the EVIDENCE ledger, ``audit-tex``, and timing/latency/overhead measurements of attacks and defenses.

Modules
-------
stats      median / IQR / bootstrap CI / speedup-with-CI
runner     interleaved A/B/... subprocess runner with warm-up and repeats
envcapture machine / compiler / git / env-var snapshot
lock       advisory file lock so two benches never overlap
parsers    agent JSONL and common benchmark/resource log parsers
tables     Markdown and LaTeX (booktabs) table generation with EVIDENCE footnotes
evidence   EVIDENCE.md ledger reader/writer and the ``audit-tex`` checker
cli        ``crbench`` command-line entry point

Design rule: every number that reaches a paper must be traceable to a log file
through an EVIDENCE.md row.  ``crbench audit-tex`` enforces this mechanically.
"""

__version__ = "0.1.0"

from .stats import Summary, bootstrap_ci, iqr, median, speedup, summarize  # noqa: F401
from .parsers import REGISTRY, parse_text, register_parser  # noqa: F401
