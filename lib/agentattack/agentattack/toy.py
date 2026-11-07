"""TOY: rule-based stand-in agents for tests, demos and the case study.  Not a model of any real LLM.

``rumor_mock`` reacts to lines of the form ``CLAIM: <text> [source: <label>]`` in its context:

* a claim seen from m distinct lines is believed with probability 1 - (1 - g)^m, where g is the
  gullibility, reduced to 0.3 g when the claim carries ``[source: unverified]`` (a provenance label);
* the "coin" is a hash of (seed, agent system prompt, claim lines), so runs are exactly reproducible;
* a believer relays the claim; an agent whose system prompt contains "summar" relays it *without*
  the source label (the toy version of provenance loss under summarisation);
* to a ``PROBE:`` it answers ``YES ...`` if it believes, else ``NO ...``.
"""
from __future__ import annotations

import hashlib
import re

from .llm import MockBackend

CLAIM = re.compile(r"CLAIM:\s*(.+?)\s*(\[source:\s*([^\]]+)\])?\s*$", re.M)


def _coin(*parts: str) -> float:
    h = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()
    return int(h[:12], 16) / float(16 ** 12)


def rumor_mock(gullibility: float = 0.5, seed: int = 0, name: str = "mock-rumor") -> MockBackend:
    def fn(messages):
        system = messages[0]["content"] if messages and messages[0]["role"] == "system" else ""
        user = messages[-1]["content"]
        claims = CLAIM.findall(user)
        believe, text = False, ""
        if claims:
            text = claims[0][0]
            labelled = any(src.strip().lower() == "unverified" for _, _, src in claims)
            g = gullibility * (0.3 if labelled else 1.0)
            p = 1 - (1 - g) ** len(claims)
            believe = _coin(str(seed), system, "|".join(c[0] + c[2] for c in claims)) < p
        if "PROBE:" in user:
            return f"YES, I believe {text}." if believe else "NO, I have no reliable evidence."
        if believe:
            if "summar" in system.lower():
                return f"Summary of what I heard: CLAIM: {text}"
            src = next((c[2] for c in claims if c[2]), "")
            return f"CLAIM: {text}" + (f" [source: {src.strip()}]" if src else "")
        return "Working on the task; nothing new to report."

    return MockBackend(fn, name=name)
