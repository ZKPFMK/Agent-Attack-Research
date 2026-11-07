#!/usr/bin/env python3
"""lit_matrix.py -- lint the related-work matrix and novelty-check log in LITERATURE.md
(attacks on LLM agents / multi-agent systems).

    python3 lit_matrix.py LITERATURE.md [--bib refs.bib] [--max-novelty-age 30]
    python3 lit_matrix.py --template          # print an empty matrix + log skeleton
    python3 lit_matrix.py --selftest

Matrix columns (order fixed, header row must match case-insensitively):
  work | venue/year | surface/branch | threat model | victims (models, frameworks) | defenses evaluated |
  reported numbers + source | code? | our delta

Row rules
  * work: a bib key `[@key]` / `\\cite{key}`, an arXiv id (2405.12345 / arXiv:2405.12345), or a KB id
    `<yy>_<venue>_<slug>` in backticks (e.g. `24_neurips_agentpoison`)
  * surface/branch: starts with external-interaction | internal-cognition | multi-agent-collaboration
    (attack rows) or defense | benchmark | framework | survey (other rows); "/branch" optional
  * threat model: names the attacker knowledge (black-box | gray-box | white-box | no-box) or "n/a"
    for benchmark/survey rows; access point in the same cell is encouraged
  * victims: non-empty (models AND agent framework/topology; "n/a" only for survey rows)
  * defenses evaluated: non-empty; write "none" explicitly if the paper evaluated none
  * reported numbers + source: empty, "n/a", or numbers WITH a source pointer
    (Tab./Table/Fig./Sec./§/p./"measured" + EVIDENCE id E<n>/"reported in")
  * code?: yes <url> | no | unknown
  * our delta: non-empty ("none" is an honest answer and a red flag for the PI)
With --bib: every bib key used in the matrix must exist in refs.bib.

Novelty log: a section "## Novelty checks" with lines
  - YYYY-MM-DD | query: "..." | sources: arxiv,dblp,s2,kb | window: 30d | hits reviewed: N | verdict: clear|overlap:<id>|taken:<id>
The newest entry must be at most --max-novelty-age days old (default 30), must include arxiv in its
sources, must not say "taken"; a missing "kb" source is a warning (check the user's KB too).
Exit 1 on any error (warnings alone exit 0).
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys

COLUMNS = ["work", "venue/year", "surface/branch", "threat model", "victims (models, frameworks)",
           "defenses evaluated", "reported numbers + source", "code?", "our delta"]
SURFACE_TOPS = ("external-interaction", "internal-cognition", "multi-agent-collaboration",
                "defense", "benchmark", "framework", "survey")
SOURCE_PTR = re.compile(r"(tab\.?|table|fig\.?|figure|sec\.?|§|p\.\s?\d|thm\.?|measured|reported in|\bE\d+\b)", re.I)
KEY_PAT = re.compile(r"\[@([\w:\-./]+)\]|\\cite[pt]?\{([^}]+)\}")
ARXIV_PAT = re.compile(r"\b(?:arxiv:)?\d{4}\.\d{4,5}(?:v\d+)?\b", re.I)
KB_ID_PAT = re.compile(r"`\d{2}_[a-z0-9_\-]+(?:\([a-z0-9\-]+\))?_[a-z0-9_]+`", re.I)
KNOWLEDGE = re.compile(r"\b(black|gray|grey|white|no)[- ]box\b|^n/a\b", re.I)

TEMPLATE = """## Related-work matrix

| work | venue/year | surface/branch | threat model | victims (models, frameworks) | defenses evaluated | reported numbers + source | code? | our delta |
|---|---|---|---|---|---|---|---|---|
| [@Key24] Short name `24_venue_slug` | VENUE 2024 | internal-cognition/memory-RAG poisoning | black-box; writes k records into the retrieval store | 2 model families; 3 agent apps | 2 (perplexity filter, paraphrase) | ASR 80% at k=5 (Tab. 2) | yes https://... | what we add; "none" = red flag |

## Novelty checks

- 2099-01-01 | query: "..." | sources: arxiv,dblp,s2,kb | window: 30d | hits reviewed: 0 | verdict: clear
"""


def parse_matrix(text: str):
    lines = text.splitlines()
    for i, l in enumerate(lines):
        if l.strip().startswith("|"):
            hdr = [h.strip().lower() for h in l.strip().strip("|").split("|")]
            if hdr[:1] == ["work"]:
                rows = []
                for r in lines[i + 2:]:
                    if not r.strip().startswith("|"):
                        break
                    cells = [c.strip() for c in r.strip().strip("|").split("|")]
                    rows.append(cells + [""] * (len(hdr) - len(cells)))
                return hdr, rows
    return None, []


def bib_keys(path: str) -> set[str]:
    with open(path, encoding="utf-8") as fh:
        return set(re.findall(r"@\w+\s*[{(]\s*([^,\s]+)\s*,", fh.read()))


def lint(text: str, bib: set[str] | None, max_age: int, today: dt.date) -> list[str]:
    errs = []
    hdr, rows = parse_matrix(text)
    if hdr is None:
        return ["no related-work matrix found (header must start with '| work |')"]
    if hdr != COLUMNS:
        errs.append(f"matrix header {hdr} != expected {COLUMNS}")
    if not rows:
        errs.append("matrix has no rows")
    for n, c in enumerate(rows, 1):
        c = dict(zip(COLUMNS, c))
        tag = f"row {n} ({c['work'][:30]})"
        keys = [k for m in KEY_PAT.finditer(c["work"]) for k in (m.group(1) or m.group(2)).split(",")]
        if not keys and not ARXIV_PAT.search(c["work"]) and not KB_ID_PAT.search(c["work"]):
            errs.append(f"{tag}: no bib key, arXiv id or KB id")
        if bib is not None:
            for k in keys:
                if k.strip() not in bib:
                    errs.append(f"{tag}: key '{k.strip()}' not in refs.bib")
        surf = c["surface/branch"].strip().lower()
        top = surf.split("/")[0].strip()
        if top not in SURFACE_TOPS:
            errs.append(f"{tag}: surface/branch must start with one of {', '.join(SURFACE_TOPS)}")
        if not KNOWLEDGE.search(c["threat model"].strip()):
            errs.append(f"{tag}: threat model must name attacker knowledge (black/gray/white/no-box) or be n/a")
        elif c["threat model"].strip().lower().startswith("n/a") and top not in ("benchmark", "survey", "framework"):
            errs.append(f"{tag}: threat model n/a is only allowed for benchmark/survey/framework rows")
        if not c["victims (models, frameworks)"]:
            errs.append(f"{tag}: empty victims (which models and which agent framework/topology?)")
        if not c["defenses evaluated"]:
            errs.append(f"{tag}: empty 'defenses evaluated' (write 'none' if the paper evaluated none)")
        num = c["reported numbers + source"]
        if num and num.lower() not in ("n/a", "-", "none") and re.search(r"\d", num) and not SOURCE_PTR.search(num):
            errs.append(f"{tag}: numbers without a source pointer: '{num}'")
        if not re.match(r"^(yes\b.*https?://\S+|no\b|unknown\b)", c["code?"], re.I):
            errs.append(f"{tag}: code? must be 'yes <url>', 'no' or 'unknown'")
        if not c["our delta"]:
            errs.append(f"{tag}: empty 'our delta'")
        elif c["our delta"].lower().startswith("none"):
            errs.append(f"{tag}: WARNING our delta = none (overlap; tell the PI)")
    m = re.search(r"^##\s*Novelty checks\s*$(.*?)(?=^##\s|\Z)", text, re.M | re.S)
    if not m:
        errs.append("no '## Novelty checks' section")
    else:
        entries = re.findall(r"^-\s*(\d{4}-\d{2}-\d{2})\s*\|(.*)$", m.group(1), re.M)
        if not entries:
            errs.append("novelty log is empty")
        else:
            newest = max(entries, key=lambda e: e[0])
            age = (today - dt.date.fromisoformat(newest[0])).days
            if age > max_age:
                errs.append(f"newest novelty check is {age} days old (> {max_age}); re-run paper_search.py")
            if re.search(r"verdict:\s*taken", newest[1], re.I):
                errs.append(f"newest novelty check says TAKEN: {newest[1].strip()}")
            src = re.search(r"sources:\s*([^|]*)", newest[1], re.I)
            srcs = {s.strip().lower() for s in (src.group(1).split(",") if src else [])}
            if "arxiv" not in srcs:
                errs.append("newest novelty check does not list arxiv among its sources")
            if "kb" not in srcs:
                errs.append("novelty: WARNING newest check does not list kb (search the user's KB with attack-kb)")
    return errs


def is_warning(x: str) -> bool:
    return "WARNING" in x


def selftest() -> int:
    good = TEMPLATE.replace("2099-01-01", "2000-01-10")
    e = lint(good, {"Key24"}, 30, dt.date(2000, 1, 20))
    assert e == [], e
    bad = (good.replace("(Tab. 2)", "").replace("yes https://...", "maybe")
           .replace("internal-cognition/", "cognition/").replace("black-box;", "attacker;")
           .replace("2 (perplexity filter, paraphrase)", "").replace(",kb", ""))
    e = lint(bad, {"Other"}, 30, dt.date(2000, 3, 1))
    for frag in ("source pointer", "code?", "not in refs.bib", "days old", "surface/branch", "knowledge",
                 "defenses evaluated", "kb"):
        assert any(frag in x for x in e), (frag, e)
    assert [x for x in e if is_warning(x)] == [x for x in e if "WARNING" in x]
    kb_only = good.replace("[@Key24] Short name ", "")
    assert lint(kb_only, None, 30, dt.date(2000, 1, 20)) == []
    arx = good.replace("[@Key24] Short name `24_venue_slug`", "arXiv:2405.12345")
    assert lint(arx, None, 30, dt.date(2000, 1, 20)) == []
    nab = good.replace("internal-cognition/memory-RAG poisoning", "benchmark").replace("black-box;", "n/a;")
    assert lint(nab, None, 30, dt.date(2000, 1, 20)) == []
    nax = good.replace("black-box;", "n/a;")
    assert any("only allowed" in x for x in lint(nax, None, 30, dt.date(2000, 1, 20)))
    noarx = good.replace("arxiv,dblp,s2,kb", "dblp,kb")
    assert any("arxiv" in x for x in lint(noarx, None, 30, dt.date(2000, 1, 20)))
    print("selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("literature", nargs="?")
    ap.add_argument("--bib")
    ap.add_argument("--max-novelty-age", type=int, default=30)
    ap.add_argument("--template", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if a.template:
        print(TEMPLATE)
        return 0
    if not a.literature:
        ap.error("give LITERATURE.md")
    with open(a.literature, encoding="utf-8") as fh:
        text = fh.read()
    errs = lint(text, bib_keys(a.bib) if a.bib else None, a.max_novelty_age, dt.date.today())
    for x in errs:
        print(("WARN  " if is_warning(x) else "ERROR ") + x)
    hard = [x for x in errs if not is_warning(x)]
    print("lit-matrix:", "OK" if not hard else f"{len(hard)} error(s)")
    return 1 if hard else 0


if __name__ == "__main__":
    sys.exit(main())
