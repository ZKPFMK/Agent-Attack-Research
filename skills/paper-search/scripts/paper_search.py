#!/usr/bin/env python3
"""paper_search.py -- search arXiv, DBLP, Semantic Scholar (and optionally OpenReview) from the CLI.

Stdlib only.  Built for novelty checks on attacks against LLM agents / multi-agent systems
("has anyone injected X through Y in the last 30 days?") and for seeding the related-work matrix.

Examples
--------
    # novelty check: arXiv + DBLP + Semantic Scholar, last 30 days
    python3 paper_search.py "memory poisoning" "multi-agent" --months 1

    # several phrasings of one idea = several queries (union, de-duplicated by normalised title)
    python3 paper_search.py -q "tool description poisoning MCP" -q "malicious tool metadata agent" --since 2025-06-01

    # one source, JSON for scripting; arXiv category filter
    python3 paper_search.py "prompt infection" --source arxiv --categories cs.CR,cs.CL,cs.MA --json

    # OpenReview (ICLR/NeurIPS/COLM submissions) is opt-in
    python3 paper_search.py "agent backdoor" --source arxiv,openreview

    python3 paper_search.py --selftest          # offline: parsers tested on embedded sample responses

Positional words form ONE query (joined by spaces); use -q/--query repeatedly for several queries.

Sources
-------
* arXiv API      http://export.arxiv.org/api/query?search_query=...  (Atom XML; submittedDate window
                 pushed into the query and re-checked client-side; sorted newest first)
* DBLP           https://dblp.org/search/publ/api?q=...&format=json  (published versions + venues;
                 may answer with an HTML bot challenge -> reported, other sources still used)
* Semantic Scholar https://api.semanticscholar.org/graph/v1/paper/search  (venue, arXiv id, date;
                 rate-limited without a key: set $S2_API_KEY to send x-api-key)
* OpenReview     https://api2.openreview.net/notes/search?term=...  (opt-in; venue string per note)

Date window: --since YYYY-MM-DD or --months N.  arXiv / S2 / OpenReview filter by date; DBLP only
has a year, so DBLP hits are kept if year >= since.year (coarser -- say so in the novelty log).

Exit status: 0 = at least one source answered (possibly zero hits), 2 = NO source answered
(offline / blocked: novelty check NOT performed), 3 = usage error.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

UA = "cra-paper-search/0.2 (agent-attack research toolkit; literature novelty check; low rate)"
ARXIV = "http://export.arxiv.org/api/query"
DBLP = "https://dblp.org/search/publ/api"
S2 = "https://api.semanticscholar.org/graph/v1/paper/search"
OPENREVIEW = "https://api2.openreview.net/notes/search"
ALL_SOURCES = ("arxiv", "dblp", "s2", "openreview")
DEFAULT_SOURCES = ("arxiv", "dblp", "s2")
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}


class Blocked(OSError):
    """Service answered with a bot challenge / rate limit instead of data."""


RETRIES = 1          # extra attempts after an HTTP 429 / 503 (set by --retries)
BACKOFF = 5.0        # seconds before the first retry, doubled each time


def http_get(url: str, headers: dict | None = None, timeout: float = 25.0) -> str:
    h = {"User-Agent": UA}
    h.update(headers or {})
    req = urllib.request.Request(url, headers=h)
    for attempt in range(RETRIES + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            if e.code not in (429, 503):
                raise
            if attempt == RETRIES:
                raise Blocked(f"HTTP {e.code} rate limit from {urllib.parse.urlsplit(url).netloc}") from e
            time.sleep(BACKOFF * 2 ** attempt)
    raise AssertionError("unreachable")


def norm_title(s: str) -> str:
    s = html.unescape(s or "").lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


# ------------------------------------------------------------------- arXiv ---

def arxiv_query_string(query: str, since: dt.date | None, categories: list[str]) -> str:
    """Plain words -> AND of all: terms; text containing ':' is passed through as raw arXiv syntax."""
    if ":" in query:
        q = query
    else:
        words = [w for w in re.findall(r'"[^"]+"|\S+', query) if w]
        q = " AND ".join(f"all:{w}" for w in words)
    if categories:
        q = f"({q}) AND ({' OR '.join('cat:' + c for c in categories)})"
    if since:
        q += f" AND submittedDate:[{since:%Y%m%d}0000 TO {dt.date.today():%Y%m%d}2359]"
    return q


def parse_arxiv_atom(xml_text: str) -> list[dict]:
    root = ET.fromstring(xml_text)
    out = []
    for e in root.findall("a:entry", ATOM):
        raw_id = (e.findtext("a:id", "", ATOM) or "").strip()
        m = re.search(r"arxiv\.org/abs/([^\s]+?)(v\d+)?$", raw_id)
        aid = m.group(1) if m else raw_id
        title = re.sub(r"\s+", " ", e.findtext("a:title", "", ATOM) or "").strip()
        if not aid or title.lower() == "error":       # the API reports errors as a pseudo-entry
            continue
        pub = (e.findtext("a:published", "", ATOM) or "")[:10]
        cats = [c.get("term", "") for c in e.findall("a:category", ATOM)]
        out.append({
            "source": "arxiv", "id": f"arXiv:{aid}", "url": f"https://arxiv.org/abs/{aid}",
            "title": title,
            "authors": ", ".join((a.findtext("a:name", "", ATOM) or "").strip() for a in e.findall("a:author", ATOM)),
            "year": int(pub[:4]) if pub[:4].isdigit() else 0, "date": pub,
            "venue": (e.findtext("arxiv:journal_ref", "", ATOM) or "").strip() or "arXiv " + (cats[0] if cats else ""),
            "doi": (e.findtext("arxiv:doi", "", ATOM) or "").strip(),
            "abstract": re.sub(r"\s+", " ", e.findtext("a:summary", "", ATOM) or "").strip()[:400],
        })
    return out


def arxiv_search(query: str, since: dt.date | None, n: int, categories: list[str]) -> list[dict]:
    params = {"search_query": arxiv_query_string(query, since, categories), "start": 0, "max_results": n,
              "sortBy": "submittedDate", "sortOrder": "descending"}
    return parse_arxiv_atom(http_get(f"{ARXIV}?{urllib.parse.urlencode(params)}"))


# -------------------------------------------------------------------- DBLP ---

def parse_dblp(raw: str) -> list[dict]:
    if raw.lstrip().startswith("<"):
        raise Blocked("DBLP returned HTML (bot challenge / rate limit)")
    out = []
    for h in (json.loads(raw).get("result", {}).get("hits", {}).get("hit") or []):
        info = h.get("info", {})
        au = info.get("authors", {}).get("author", [])
        au = au if isinstance(au, list) else [au]
        ee = info.get("ee", "")
        venue = info.get("venue", "")
        out.append({
            "source": "dblp", "id": info.get("key", ""),
            "url": ee if isinstance(ee, str) else (ee or [""])[0],
            "title": html.unescape(info.get("title", "")).rstrip("."),
            "authors": ", ".join(re.sub(r"\s+\d{4}$", "", a.get("text", "") if isinstance(a, dict) else str(a))
                                 for a in au),
            "year": int(info.get("year", 0) or 0), "date": "",
            "venue": venue if isinstance(venue, str) else ", ".join(venue),
            "doi": info.get("doi", ""), "abstract": "",
        })
    return out


def dblp_search(query: str, n: int) -> list[dict]:
    return parse_dblp(http_get(f"{DBLP}?{urllib.parse.urlencode({'q': query, 'format': 'json', 'h': n})}"))


# -------------------------------------------------------- Semantic Scholar ---

S2_FIELDS = "title,authors,year,venue,externalIds,publicationDate,url,abstract"


def parse_s2(raw: str) -> list[dict]:
    out = []
    for p in json.loads(raw).get("data") or []:
        ext = p.get("externalIds") or {}
        if ext.get("ArXiv"):
            pid, url = f"arXiv:{ext['ArXiv']}", f"https://arxiv.org/abs/{ext['ArXiv']}"
        else:
            pid, url = f"S2:{p.get('paperId', '')}", p.get("url", "")
        out.append({
            "source": "s2", "id": pid, "url": url, "title": (p.get("title") or "").strip(),
            "authors": ", ".join(a.get("name", "") for a in p.get("authors") or []),
            "year": int(p.get("year") or 0), "date": p.get("publicationDate") or "",
            "venue": p.get("venue") or "", "doi": ext.get("DOI", ""),
            "acl": ext.get("ACL", ""), "abstract": (p.get("abstract") or "")[:400],
        })
    return out


def s2_search(query: str, since: dt.date | None, n: int) -> list[dict]:
    params = {"query": query, "limit": min(n, 100), "fields": S2_FIELDS}
    if since:
        params["publicationDateOrYear"] = f"{since.isoformat()}:"
    key = os.environ.get("S2_API_KEY")
    return parse_s2(http_get(f"{S2}?{urllib.parse.urlencode(params)}", {"x-api-key": key} if key else None))


# --------------------------------------------------------------- OpenReview ---

def _orv(content: dict, k: str):
    v = content.get(k)
    return v.get("value") if isinstance(v, dict) else v


def parse_openreview(raw: str) -> list[dict]:
    out = []
    for note in json.loads(raw).get("notes") or []:
        c = note.get("content") or {}
        ms = note.get("pdate") or note.get("cdate") or 0
        d = dt.datetime.fromtimestamp(ms / 1000, dt.timezone.utc).date().isoformat() if ms else ""
        au = _orv(c, "authors") or []
        out.append({
            "source": "openreview", "id": f"OpenReview:{note.get('forum') or note.get('id', '')}",
            "url": f"https://openreview.net/forum?id={note.get('forum') or note.get('id', '')}",
            "title": (_orv(c, "title") or "").strip(), "authors": ", ".join(au if isinstance(au, list) else [str(au)]),
            "year": int(d[:4]) if d else 0, "date": d, "venue": _orv(c, "venue") or "", "doi": "",
            "abstract": (_orv(c, "abstract") or "")[:400],
        })
    return out


def openreview_search(query: str, n: int) -> list[dict]:
    params = {"term": query, "type": "terms", "content": "all", "source": "forum", "limit": n}
    return parse_openreview(http_get(f"{OPENREVIEW}?{urllib.parse.urlencode(params)}"))


# -------------------------------------------------------------------- core ---

def in_window(r: dict, since: dt.date | None) -> bool:
    if not since:
        return True
    if r.get("date"):
        try:
            return dt.date.fromisoformat(r["date"][:10]) >= since
        except ValueError:
            pass
    return not r.get("year") or r["year"] >= since.year


def merge(rows: list[dict]) -> list[dict]:
    """De-duplicate by normalised title; keep the first row, record the other sources/ids on it."""
    by_title: dict[str, dict] = {}
    for r in rows:
        k = norm_title(r["title"])
        if not k:
            continue
        if k in by_title:
            first = by_title[k]
            first.setdefault("also", []).append(f"{r['source']}:{r['id']}")
            if not first.get("venue") or first["venue"].startswith("arXiv"):
                if r.get("venue") and not r["venue"].startswith("arXiv"):
                    first["venue"] = r["venue"]
        else:
            by_title[k] = r
    return sorted(by_title.values(), key=lambda r: (r.get("date") or str(r.get("year") or "")), reverse=True)


def run(queries: list[str], sources: list[str], since: dt.date | None, n: int, categories: list[str],
        delay: float = 1.0) -> tuple[list[dict], dict]:
    status: dict[str, str] = {}
    rows: list[dict] = []
    for q in queries:
        for src in sources:
            fn = {"arxiv": lambda: arxiv_search(q, since, n, categories),
                  "dblp": lambda: dblp_search(q, n),
                  "s2": lambda: s2_search(q, since, n),
                  "openreview": lambda: openreview_search(q, n)}[src]
            try:
                res = fn()
                status[src] = "ok" if status.get(src) in (None, "ok") else status[src] + "+ok"
            except (urllib.error.URLError, TimeoutError, OSError, ValueError, ET.ParseError) as exc:
                status.setdefault(src, f"failed: {exc}")
                print(f"[offline?] {src} query {q!r} failed: {exc}", file=sys.stderr)
                continue
            finally:
                time.sleep(delay)          # arXiv asks for >= 3 s between bursts; keep everything polite
            for r in res:
                if in_window(r, since):
                    r["query"] = q
                    rows.append(r)
    return merge(rows), status


def render_md(rows: list[dict]) -> str:
    lines = ["| src | id | date/year | title | authors | venue |", "|---|---|---|---|---|---|"]
    for r in rows:
        also = f" (+{len(r['also'])})" if r.get("also") else ""
        lines.append(f"| {r['source']}{also} | [{r['id']}]({r['url']}) | {r.get('date') or r['year']} | "
                     f"{r['title'].replace('|', '/')} | {r['authors'][:60]} | {r.get('venue', '')} |")
    return "\n".join(lines)


# ---------------------------------------------------------------- selftest ---

SAMPLE_ARXIV = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>http://arxiv.org/abs/2099.01234v2</id>
    <published>2099-01-15T10:00:00Z</published>
    <title>Toy Agents Believe
      Toy Rumours</title>
    <summary>We study a synthetic chain of toy agents.</summary>
    <author><name>Alice Example</name></author><author><name>Bob Example</name></author>
    <arxiv:doi>10.0000/toy.1</arxiv:doi>
    <category term="cs.CR"/><category term="cs.MA"/>
  </entry>
  <entry>
    <id>http://arxiv.org/abs/2098.00007v1</id>
    <published>2098-03-01T00:00:00Z</published>
    <title>An Older Toy Paper</title><summary>x</summary>
    <author><name>Carol Example</name></author>
    <arxiv:journal_ref>Toy Conf 2098</arxiv:journal_ref>
  </entry>
</feed>"""

SAMPLE_DBLP = json.dumps({"result": {"hits": {"hit": [{"info": {
    "key": "conf/toy/ExampleE99", "title": "Toy Agents Believe Toy Rumours.", "year": "2099",
    "venue": "TOYCONF", "ee": "https://doi.org/10.0000/toy.1", "doi": "10.0000/toy.1",
    "authors": {"author": [{"text": "Alice Example 0001"}, {"text": "Bob Example"}]}}}]}}})

SAMPLE_S2 = json.dumps({"total": 2, "data": [
    {"paperId": "abc", "title": "Toy Agents Believe Toy Rumours", "year": 2099, "venue": "Toy Conf",
     "publicationDate": "2099-01-15", "externalIds": {"ArXiv": "2099.01234", "DOI": "10.0000/toy.1"},
     "authors": [{"name": "Alice Example"}], "url": "https://www.semanticscholar.org/paper/abc", "abstract": None},
    {"paperId": "def", "title": "Another Toy", "year": 2097, "venue": "", "publicationDate": None,
     "externalIds": {"ACL": "2097.toy-main.1"}, "authors": [], "url": "https://s2/def"}]})

SAMPLE_OPENREVIEW = json.dumps({"notes": [{"id": "n1", "forum": "f1", "pdate": 4072550400000,
    "content": {"title": {"value": "Toy Agents Believe Toy Rumours"}, "authors": {"value": ["Alice Example"]},
                "venue": {"value": "TOYCONF 2099 Poster"}}}]})


def selftest() -> int:
    a = parse_arxiv_atom(SAMPLE_ARXIV)
    assert [r["id"] for r in a] == ["arXiv:2099.01234", "arXiv:2098.00007"], a
    assert a[0]["title"] == "Toy Agents Believe Toy Rumours" and a[0]["date"] == "2099-01-15", a[0]
    assert a[0]["authors"] == "Alice Example, Bob Example" and a[0]["doi"] == "10.0000/toy.1"
    assert a[0]["venue"] == "arXiv cs.CR" and a[1]["venue"] == "Toy Conf 2098"
    q = arxiv_query_string('memory "multi agent"', dt.date(2099, 1, 1), ["cs.CR"])
    assert q.startswith('(all:memory AND all:"multi agent") AND (cat:cs.CR) AND submittedDate:[209901010000'), q
    assert arxiv_query_string("ti:toy AND au:example", None, []) == "ti:toy AND au:example"
    d = parse_dblp(SAMPLE_DBLP)
    assert d[0]["title"] == "Toy Agents Believe Toy Rumours" and d[0]["authors"] == "Alice Example, Bob Example"
    try:
        parse_dblp("<html>challenge</html>")
        raise AssertionError("bot page not detected")
    except Blocked:
        pass
    s = parse_s2(SAMPLE_S2)
    assert s[0]["id"] == "arXiv:2099.01234" and s[1]["id"] == "S2:def" and s[1]["acl"] == "2097.toy-main.1", s
    o = parse_openreview(SAMPLE_OPENREVIEW)
    assert o[0]["id"] == "OpenReview:f1" and o[0]["venue"].startswith("TOYCONF") and o[0]["year"] == 2099, o
    since = dt.date(2099, 1, 10)
    kept = [r for r in a + d + s + o if in_window(r, since)]
    assert {r["source"] for r in kept} == {"arxiv", "dblp", "s2", "openreview"}
    assert not any(r["id"] == "arXiv:2098.00007" for r in kept)
    m = merge(kept)
    assert len(m) == 1 and len(m[0]["also"]) == 3 and m[0]["venue"] == "TOYCONF", m
    assert "| arxiv (+3) |" in render_md(m)
    print("selftest: OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("words", nargs="*", help="words of one query")
    ap.add_argument("-q", "--query", action="append", default=[], help="a query phrasing (repeatable)")
    ap.add_argument("--source", default=",".join(DEFAULT_SOURCES),
                    help=f"comma list from {','.join(ALL_SOURCES)} (default {','.join(DEFAULT_SOURCES)})")
    ap.add_argument("--since", help="only papers dated on/after YYYY-MM-DD")
    ap.add_argument("--months", type=float, help="only papers from the last N months")
    ap.add_argument("-n", "--max", type=int, default=25, help="hits per source per query (default 25)")
    ap.add_argument("--categories", default="", help="arXiv categories, e.g. cs.CR,cs.CL,cs.AI,cs.LG,cs.MA")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests (default 1)")
    ap.add_argument("--retries", type=int, default=1, help="retries after HTTP 429/503, with backoff (default 1)")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    global RETRIES
    RETRIES = max(0, a.retries)
    queries = a.query + ([" ".join(a.words)] if a.words else [])
    if not queries:
        ap.print_usage(sys.stderr)
        print("error: give a query (or --selftest)", file=sys.stderr)
        return 3
    sources = [s.strip() for s in a.source.split(",") if s.strip()]
    bad = [s for s in sources if s not in ALL_SOURCES]
    if bad:
        print(f"error: unknown source(s) {bad}; choose from {ALL_SOURCES}", file=sys.stderr)
        return 3
    since = dt.date.fromisoformat(a.since) if a.since else (
        dt.date.today() - dt.timedelta(days=int(a.months * 30.44)) if a.months else None)
    cats = [c.strip() for c in a.categories.split(",") if c.strip()]
    rows, status = run(queries, sources, since, a.max, cats, a.delay)
    if not any(v.startswith("ok") or v.endswith("+ok") for v in status.values()):
        print("ERROR: no source answered (offline/blocked). Novelty check NOT performed.", file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"queries": queries, "since": since.isoformat() if since else None,
                          "date": dt.date.today().isoformat(), "sources": status, "n": len(rows),
                          "results": rows}, indent=2, ensure_ascii=False))
    else:
        print(f"<!-- queries={queries} since={since} sources={status} hits={len(rows)} date={dt.date.today()} -->")
        print(render_md(rows) if rows else "_no hits_")
    return 0


if __name__ == "__main__":
    sys.exit(main())
