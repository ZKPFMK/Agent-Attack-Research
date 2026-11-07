"""Read the user's attack knowledge base (KB) and answer "which paper already did X?".

The KB is a Markdown file kept OUTSIDE this repo (path from ``$CRA_KB``, ``--kb`` or the ``kb:`` line
in a project's STATE.md).  Expected entry format (labels may use a full-width colon)::

    ## Lying with Truths
    **全名：**Lying with Truths: ...
    **中文名：**用真相说谎 ...                       (optional)
    **年份与会议：**2026，ACL ...                     (any label starting with 年份)
    **分类：**多智能体协作安全、...
    **论文标识：**`26_acl_lying_with_truths`。
    <one-paragraph summary>
    **代码：** <url>                                   (optional; any label starting with 代码)
    **原文：**[本地 PDF](../papers/03_.../x.pdf)。

Sections without a ``论文标识`` / id line are kept only if they have a summary (keyed by heading).
English labels (Title/Venue/Category/ID/Code/PDF) are accepted too.
"""
from __future__ import annotations

import os
import re
from dataclasses import dataclass, field

LABEL = re.compile(r"^\*\*([^*]+?)[：:]\s*\*\*\s*(.*)$")
LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
FIELD_OF = [
    ("title", ("全名", "title", "full name")),
    ("zh_title", ("中文名",)),
    ("venue_year", ("年份", "venue", "year")),
    ("category", ("分类", "category")),
    ("key", ("论文标识", "id", "key")),
    ("code", ("代码", "code")),
    ("pdf", ("原文", "pdf")),
]


@dataclass
class Paper:
    key: str
    heading: str
    title: str = ""
    zh_title: str = ""
    venue_year: str = ""
    category: str = ""
    summary: str = ""
    code: str = ""
    pdf: str = ""
    extra: dict = field(default_factory=dict)

    def short(self) -> str:
        return f"{self.key} — {self.title or self.heading} ({self.venue_year.split('。')[0]})"


def _clean(v: str) -> str:
    return v.strip().rstrip("。.").strip().strip("`").strip()


def _field_for(label: str) -> str | None:
    lab = label.strip().lower()
    for name, prefixes in FIELD_OF:
        if any(lab.startswith(p) for p in prefixes):
            return name
    return None


def parse_kb_text(text: str) -> list[Paper]:
    papers: list[Paper] = []
    cur: Paper | None = None
    body: list[str] = []
    in_code = False

    def flush():
        if cur is not None:
            cur.summary = "\n".join(p for p in "\n".join(body).split("\n\n") if p.strip()).strip()
            if cur.key or cur.title or (cur.summary and len(cur.summary) > 80 and cur.extra):
                papers.append(cur)

    for raw in text.splitlines():
        line = raw.rstrip()
        if line.lstrip().startswith("```"):
            in_code = not in_code
            continue
        if in_code:
            continue
        if line.startswith("## ") and not line.startswith("### "):
            flush()
            head = line[3:].strip()
            cur, body = Paper(key="", heading=head), []
            continue
        if cur is None:
            continue
        m = LABEL.match(line.strip())
        if m:
            label, val = m.group(1), m.group(2).strip()
            name = _field_for(label)
            if name in ("code", "pdf"):
                links = LINK.findall(val) or re.findall(r"<([^>]+)>", val)
                val = links[0] if links else _clean(val)
                setattr(cur, name, val)
            elif name:
                setattr(cur, name, _clean(val))
            else:
                cur.extra[label.strip()] = _clean(val)
            continue
        if line.startswith("#"):
            continue
        body.append(line)
    flush()
    for p in papers:
        if not p.key:
            p.key = re.sub(r"\W+", "_", p.heading.lower()).strip("_")
    return papers


def parse_kb(path: str) -> list[Paper]:
    with open(path, encoding="utf-8") as fh:
        return parse_kb_text(fh.read())


def scan_papers(papers_dir: str) -> dict[str, list[str]]:
    """Category folder (e.g. ``03_攻击_多智能体协作``) -> sorted paper ids (sub-folder names)."""
    out: dict[str, list[str]] = {}
    for cat in sorted(os.listdir(papers_dir)):
        d = os.path.join(papers_dir, cat)
        if os.path.isdir(d) and not cat.startswith("."):
            out[cat] = sorted(x for x in os.listdir(d) if os.path.isdir(os.path.join(d, x)) and not x.startswith("."))
    return out


_CJK = re.compile(r"[㐀-鿿]+")
_WORD = re.compile(r"[a-z0-9][a-z0-9\-]+")
_STOP = {"the", "and", "for", "with", "of", "in", "on", "to", "via", "an", "is", "by", "llm", "agent", "agents"}


def tokens(text: str) -> set[str]:
    """ASCII words (len >= 2, minus stop words) + CJK character bigrams."""
    t = text.lower()
    out = {w for w in _WORD.findall(t) if w not in _STOP}
    for run in _CJK.findall(t):
        out |= {run[i:i + 2] for i in range(len(run) - 1)} if len(run) > 1 else {run}
    return out


def search(papers: list[Paper], query: str, k: int = 5) -> list[tuple[float, Paper]]:
    """Rank papers by IDF-weighted token overlap; matches in key/title/category count double.  Score in [0, 1]."""
    import math

    q = tokens(query)
    if not q or not papers:
        return []
    docs = []
    for p in papers:
        head = tokens(" ".join([p.key.replace("_", " "), p.title, p.zh_title, p.heading, p.category]))
        docs.append((p, head, head | tokens(p.summary)))
    n = len(docs)

    def hit(t: str, toks: set[str]) -> bool:  # ASCII query words also match as prefixes ("mcp" ~ "mcptox")
        return t in toks or (t.isascii() and len(t) >= 3 and any(x.startswith(t) for x in toks))

    idf = {t: math.log((n + 1) / (1 + sum(1 for _, _, d in docs if hit(t, d)))) + 1.0 for t in q}
    total = 3 * sum(idf.values())
    scored = []
    for p, head, full in docs:
        s = (2 * sum(idf[t] for t in q if hit(t, head)) + sum(idf[t] for t in q if hit(t, full))) / total
        if s > 0:
            scored.append((round(s, 3), p))
    scored.sort(key=lambda x: (-x[0], x[1].key))
    return scored[:k]


def kb_path_from_state(project: str) -> str | None:
    """Return the ``kb:`` path from a project's STATE.md (relative paths resolved against the project)."""
    sp = os.path.join(project, "STATE.md")
    if not os.path.exists(sp):
        return None
    with open(sp, encoding="utf-8") as fh:
        m = re.search(r"^\s*[-*]?\s*\**kb\**\s*:\**\s*(\S.*?)\s*$", fh.read(), re.M | re.I)
    if not m or m.group(1).startswith("<"):
        return None
    p = os.path.expanduser(m.group(1).strip("`"))
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(project, p))


def resolve_kb(explicit: str | None = None, project: str = ".") -> str | None:
    for c in (explicit, os.environ.get("CRA_KB"), kb_path_from_state(project)):
        if c and os.path.exists(c):
            return c
    return None
