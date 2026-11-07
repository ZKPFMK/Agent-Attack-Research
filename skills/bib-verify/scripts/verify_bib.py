#!/usr/bin/env python3
"""verify_bib.py -- check every BibTeX entry against arXiv / ACL Anthology / OpenReview / Crossref / DBLP.

Why: fabricated or garbled references (invented co-authors, placeholder
"Chen and others", wrong venue, a key pointing at a different paper) are a
research-integrity problem and an instant credibility loss with reviewers.
LLM-drafted bibliographies are especially prone to this.  This script is the
mechanical half of the `bib-verify` gate; the human/agent half is reading the
flagged entries.

Usage
-----
    python3 verify_bib.py refs.bib                       # Markdown report on stdout
                                                         # (stamped with "bib-sha256: <hash of refs.bib>"
                                                         #  so phase-gate can tell if the bib changed since)
    python3 verify_bib.py refs.bib --json report.json    # + machine-readable report
    python3 verify_bib.py refs.bib --offline             # static lint only
    python3 verify_bib.py refs.bib --only key1,key2      # re-check a few entries
    python3 verify_bib.py --selftest

Resolution order per entry (every id found is tried; the first VERIFIED wins)
-----------------------------------------------------------------------------
1. arXiv id (`eprint=` + `archiveprefix=arXiv`, `url=arxiv.org/abs|pdf/...`, `journal=`/`note=`
   "arXiv preprint arXiv:2406.13352", or DOI 10.48550/arXiv.<id>)  ->  arXiv API
   export.arxiv.org/api/query?id_list=<id>  (title, authors, v1 and latest-version years).
2. ACL Anthology id (`url=aclanthology.org/2024.acl-long.123`, or a 10.18653/v1/<id> DOI)
   ->  https://aclanthology.org/<id>.bib  (parsed with this file's BibTeX parser).
3. OpenReview id (`url=openreview.net/forum?id=...` or `pdf?id=...`)  ->  api2.openreview.net/notes?id=
   (API v2), falling back to api.openreview.net (v1).
4. Legacy IACR ePrint id (`eprint=YYYY/NNNN`, eprint.iacr.org URL, "ePrint Archive, Paper ...")  ->  OAI record
   (compatibility for older projects; not a default Agent Attack source).
5. `doi=`  ->  Crossref /works/<doi>, falling back to DataCite (Zenodo, LIPIcs, arXiv DOIs).
6. no id: title search -- DBLP (if reachable), Crossref bibliographic query, then the arXiv API
   title search (preprints are often missing from Crossref).

Each entry gets a status:
  VERIFIED     title similarity >= 0.90 and >= 1 author surname overlap (and year +-1 if given)
  MISMATCH     a record was found for the id/DOI but title or authors disagree
  WEAK         best title-search hit is similar but not conclusive (0.75..0.90) -> check by hand
  NOT_FOUND    nothing plausible found -> treat as fabricated until proven otherwise
  UNCHECKED    offline / service error
plus static LINT flags (placeholder authors, "and others" only, missing year/title,
`% UNVERIFIED` marker in the .bib, duplicate titles, ...).

Exit status: 0 if every entry is VERIFIED (lint warnings allowed), 1 if any entry
is MISMATCH/NOT_FOUND/WEAK/UNCHECKED, 3 on usage errors.  Use it as a gate.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import html
import json
import xml.etree.ElementTree as ET
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request

UA = "cra-bib-verify/0.2 (agent-attack research toolkit; low rate; mailto not set)"
ARXIV_API = "http://export.arxiv.org/api/query"
ACL_BIB = "https://aclanthology.org/{id}.bib"
OPENREVIEW_V2 = "https://api2.openreview.net/notes?id={id}"
OPENREVIEW_V1 = "https://api.openreview.net/notes?id={id}"
ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
ARXIV_NEW = re.compile(r"(?<![\d.])(\d{4}\.\d{4,5})(?:v\d+)?(?![\d])")
ARXIV_OLD = re.compile(r"\b([a-z\-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?\b")
ACL_ID = re.compile(r"(?:aclanthology\.org/|10\.18653/v1/)([A-Z]\d{2}-\d{4}|\d{4}\.[a-z0-9\-]+\.\d+)", re.I)
OPENREVIEW_ID = re.compile(r"openreview\.net/(?:forum|pdf)\?id=([A-Za-z0-9_\-]+)")
# Legacy compatibility for older blackboards; Agent Attack defaults use arXiv,
# ACL Anthology, OpenReview, Crossref/DataCite and DBLP instead.
EPRINT_OAI = ("https://eprint.iacr.org/oai?verb=GetRecord&identifier=oai:eprint.iacr.org:{id}"
              "&metadataPrefix=oai_dc")
CROSSREF = "https://api.crossref.org/works"
DATACITE = "https://api.datacite.org/dois"
DBLP = "https://dblp.org/search/publ/api"
EPRINT_ID = re.compile(r"(?:eprint\.iacr\.org/|ePrint Archive,?\s*(?:Paper|Report)?\s*|^)"
                       r"((?:19|20)\d{2})/(\d{1,5})\b", re.I)


# ------------------------------------------------------------- bib parsing ---

def parse_bib(text: str) -> list[dict]:
    """Small dependency-free BibTeX parser (handles nested braces and quotes).

    Returns dicts with keys: type, key, fields (lower-cased names), unverified_marker.
    A line `% UNVERIFIED` directly above an entry sets unverified_marker=True.
    """
    entries = []
    i, n = 0, len(text)
    while True:
        at = text.find("@", i)
        if at < 0:
            break
        m = re.match(r"@(\w+)\s*([{(])", text[at:])
        if not m:
            i = at + 1
            continue
        etype = m.group(1).lower()
        if etype in ("comment", "preamble", "string"):
            i = at + m.end()
            continue
        preceding = text[text.rfind("\n", 0, max(0, text.rfind("\n", 0, at))) + 1:at]
        marker = "UNVERIFIED" in preceding.upper()
        j = at + m.end()
        depth, k = 1, j
        while k < n and depth:
            c = text[k]
            if c in "{(":
                depth += 1
            elif c in "})":
                depth -= 1
            k += 1
        body = text[j:k - 1]
        key, _, rest = body.partition(",")
        fields = {}
        p = 0
        while p < len(rest):
            fm = re.match(r"\s*([\w\-:]+)\s*=\s*", rest[p:])
            if not fm:
                break
            name = fm.group(1).lower()
            p += fm.end()
            if p < len(rest) and rest[p] == "{":
                d, q = 1, p + 1
                while q < len(rest) and d:
                    d += {"{": 1, "}": -1}.get(rest[q], 0)
                    q += 1
                val = rest[p + 1:q - 1]
                p = q
            elif p < len(rest) and rest[p] == '"':
                q = p + 1
                while q < len(rest) and not (rest[q] == '"' and rest[q - 1] != "\\"):
                    q += 1
                val = rest[p + 1:q]
                p = q + 1
            else:
                vm = re.match(r"[^,]*", rest[p:])
                val = vm.group(0).strip()
                p += vm.end()
            fields[name] = re.sub(r"\s+", " ", val).strip()
            cm = re.match(r"\s*,", rest[p:])
            if cm:
                p += cm.end()
        entries.append({"type": etype, "key": key.strip(), "fields": fields,
                        "unverified_marker": marker})
        i = k
    return entries


# ----------------------------------------------------------- normalisation ---

_LATEX_ACCENT = re.compile(r"\\[`'^\"~=.uvHtcdbk]\s*\{?\s*([A-Za-z])\s*\}?")


def delatex(s: str) -> str:
    s = _LATEX_ACCENT.sub(r"\1", s or "")
    s = re.sub(r"\\(ss|o|O|l|L|aa|AA|ae|AE)\b", lambda m: {"ss": "ss", "o": "o", "O": "O", "l": "l",
                                                        "L": "L", "aa": "a", "AA": "A",
                                                        "ae": "ae", "AE": "AE"}[m.group(1)], s)
    s = re.sub(r"\$[^$]*\$", " ", s)            # math in titles
    s = re.sub(r"\\[a-zA-Z]+", " ", s)
    s = s.replace("{", "").replace("}", "").replace("~", " ")
    s = unicodedata.normalize("NFKD", html.unescape(s))
    return "".join(c for c in s if not unicodedata.combining(c))


def norm_title(s: str) -> str:
    s = delatex(s).lower()
    s = re.sub(r"[^a-z0-9 ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def title_sim(a: str, b: str) -> float:
    a, b = norm_title(a), norm_title(b)
    if not a or not b:
        return 0.0
    if a == b:
        return 1.0
    # tolerate a subtitle present on one side only
    if a.startswith(b) or b.startswith(a):
        short = min(len(a), len(b))
        if short >= 25:
            return 0.93
    return difflib.SequenceMatcher(None, a, b).ratio()


def surnames_from_bib(author_field: str) -> list[str]:
    out = []
    for a in re.split(r"\s+and\s+", delatex(author_field or "")):
        a = a.strip()
        if not a or a.lower() in ("others", "et al", "et al."):
            continue
        last = a.split(",")[0] if "," in a else a.split()[-1]
        out.append(norm_title(last).replace(" ", ""))
    return [x for x in out if x]


def surname_of(full: str) -> str:
    full = delatex(full).strip()
    if "," in full:
        return norm_title(full.split(",")[0]).replace(" ", "")
    return norm_title(full.split()[-1] if full.split() else "").replace(" ", "")


# ---------------------------------------------------------------- services ---

class Blocked(OSError):
    pass


def http_get(url: str, timeout: float = 25.0) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def fetch_eprint(eid: str) -> dict | None:
    """Resolve a legacy IACR ePrint entry when an older project still cites one."""
    xml = http_get(EPRINT_OAI.format(id=eid))
    if "<dc:title>" not in xml:
        return None
    title = html.unescape(re.search(r"<dc:title>(.*?)</dc:title>", xml, re.S).group(1)).strip()
    authors = [html.unescape(x).strip() for x in re.findall(r"<dc:creator>(.*?)</dc:creator>", xml, re.S)]
    date = re.search(r"<dc:date>(\d{4})", xml)
    return {"title": title, "authors": authors, "year": int(eid.split("/")[0]),
            "last_year": int(date.group(1)) if date else None, "source": f"ePrint {eid}"}


def parse_arxiv_atom(xml_text: str) -> list[dict]:
    """Records from an arXiv API Atom feed (id_list lookup or title search)."""
    out = []
    for e in ET.fromstring(xml_text).findall("a:entry", ATOM):
        title = re.sub(r"\s+", " ", e.findtext("a:title", "", ATOM) or "").strip()
        raw = (e.findtext("a:id", "", ATOM) or "").strip()
        m = re.search(r"arxiv\.org/abs/(.+?)(v\d+)?$", raw)
        if not m or title.lower() == "error":            # API errors come back as a pseudo-entry
            continue
        pub, upd = e.findtext("a:published", "", ATOM)[:4], e.findtext("a:updated", "", ATOM)[:4]
        out.append({"title": title, "id": m.group(1),
                    "authors": [(a.findtext("a:name", "", ATOM) or "").strip() for a in e.findall("a:author", ATOM)],
                    "year": int(pub) if pub.isdigit() else None,
                    "last_year": int(upd) if upd.isdigit() else None,
                    "venue": (e.findtext("arxiv:journal_ref", "", ATOM) or "").strip(),
                    "source": f"arXiv {m.group(1)}"})
    return out


def fetch_arxiv(aid: str) -> dict | None:
    recs = parse_arxiv_atom(http_get(f"{ARXIV_API}?{urllib.parse.urlencode({'id_list': aid, 'max_results': 1})}"))
    return recs[0] if recs else None


def search_arxiv_title(title: str) -> list[dict]:
    words = [w for w in re.findall(r"[A-Za-z0-9]+", delatex(title)) if len(w) > 2][:12]
    if not words:
        return []
    q = " AND ".join(f"ti:{w}" for w in words)
    return parse_arxiv_atom(http_get(f"{ARXIV_API}?{urllib.parse.urlencode({'search_query': q, 'max_results': 5})}"))


def record_from_bib(text: str, source: str) -> dict | None:
    es = parse_bib(text)
    if not es:
        return None
    f = es[0]["fields"]
    yr = f.get("year", "")[:4]
    return {"title": delatex(f.get("title", "")),
            "authors": [delatex(a).strip() for a in re.split(r"\s+and\s+", f.get("author", "")) if a.strip()],
            "year": int(yr) if yr.isdigit() else None, "venue": delatex(f.get("booktitle", f.get("journal", ""))),
            "source": source}


def fetch_acl(acl_id: str) -> dict | None:
    try:
        return record_from_bib(http_get(ACL_BIB.format(id=acl_id)), f"ACL Anthology {acl_id}")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def parse_openreview_note(raw: str, oid: str) -> dict | None:
    notes = json.loads(raw).get("notes") or []
    if not notes:
        return None
    n = notes[0]
    c = n.get("content") or {}
    val = lambda k: (c.get(k) or {}).get("value") if isinstance(c.get(k), dict) else c.get(k)  # v2 vs v1 shape
    ms = n.get("pdate") or n.get("odate") or n.get("cdate") or n.get("tcdate") or 0
    year = time.gmtime(ms / 1000).tm_year if ms else None
    au = val("authors") or []
    return {"title": (val("title") or "").strip(), "authors": au if isinstance(au, list) else [str(au)],
            "year": year, "venue": val("venue") or "", "source": f"OpenReview {oid}"}


def fetch_openreview(oid: str) -> dict | None:
    for url in (OPENREVIEW_V2, OPENREVIEW_V1):
        try:
            rec = parse_openreview_note(http_get(url.format(id=oid)), oid)
        except urllib.error.HTTPError as e:
            if e.code in (400, 403, 404):
                continue
            raise
        if rec and rec["title"]:
            return rec
    return None


def fetch_crossref_doi(doi: str) -> dict | None:
    """Crossref first; DataCite for DOIs Crossref does not know (Zenodo, LIPIcs, arXiv...)."""
    try:
        data = json.loads(http_get(f"{CROSSREF}/{urllib.parse.quote(doi)}"))
        return _crossref_item(data.get("message", {}))
    except urllib.error.HTTPError as e:
        if e.code != 404:
            raise
    try:
        data = json.loads(http_get(f"{DATACITE}/{urllib.parse.quote(doi)}"))
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise
    at = data.get("data", {}).get("attributes", {})
    names = []
    for c in at.get("creators", []):
        if c.get("givenName") or c.get("familyName"):
            names.append(f"{c.get('givenName', '')} {c.get('familyName', '')}".strip())
        else:
            nm = c.get("name", "")
            names.append(" ".join(reversed(nm.split(", "))) if ", " in nm else nm)
    return {"title": " ".join(t.get("title", "") for t in at.get("titles", [])[:1]),
            "authors": names, "year": at.get("publicationYear"),
            "venue": at.get("publisher", ""), "source": f"DataCite doi:{doi}"}


def _crossref_item(it: dict) -> dict:
    year = None
    for k in ("published-print", "published-online", "issued"):
        dp = (it.get(k) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            year = dp[0][0]
            break
    return {"title": " ".join(it.get("title") or []),
            "authors": [f"{a.get('given', '')} {a.get('family', '')}".strip() for a in it.get("author", [])],
            "year": year, "venue": " ".join(it.get("container-title") or []),
            "source": f"Crossref doi:{it.get('DOI', '')}"}


def search_crossref(title: str, author_hint: str) -> list[dict]:
    q = {"query.bibliographic": title, "rows": 5,
         "select": "title,author,DOI,issued,published-print,published-online,container-title"}
    if author_hint:
        q["query.author"] = author_hint
    data = json.loads(http_get(f"{CROSSREF}?{urllib.parse.urlencode(q)}"))
    return [_crossref_item(it) for it in data.get("message", {}).get("items", [])]


def search_dblp(title: str) -> list[dict]:
    raw = http_get(f"{DBLP}?{urllib.parse.urlencode({'q': title, 'format': 'json', 'h': 5})}")
    if raw.lstrip().startswith("<"):
        raise Blocked("DBLP bot challenge")
    out = []
    for h in json.loads(raw).get("result", {}).get("hits", {}).get("hit") or []:
        info = h.get("info", {})
        au = info.get("authors", {}).get("author", [])
        au = au if isinstance(au, list) else [au]
        out.append({"title": html.unescape(info.get("title", "")).rstrip("."),
                    "authors": [re.sub(r"\s+\d{4}$", "", a.get("text", "") if isinstance(a, dict) else str(a))
                                for a in au],
                    "year": int(info.get("year", 0) or 0) or None,
                    "venue": info.get("venue", "") if isinstance(info.get("venue"), str) else "",
                    "source": f"DBLP {info.get('key', '')}"})
    return out


# ---------------------------------------------------------------- checking ---

def find_arxiv_id(f: dict) -> str | None:
    is_arxiv = "arxiv" in f.get("archiveprefix", "").lower() or "arxiv" in f.get("eprinttype", "").lower()
    if f.get("eprint") and is_arxiv:
        m = ARXIV_NEW.search(f["eprint"]) or ARXIV_OLD.search(f["eprint"])
        if m:
            return m.group(1)
    doi = f.get("doi", "")
    m = re.search(r"10\.48550/arxiv\.(\S+)", doi, re.I)
    if m:
        return m.group(1)
    for k in ("url", "journal", "note", "howpublished", "booktitle", "publisher", "eprint"):
        v = f.get(k, "")
        if "arxiv" not in v.lower():
            continue
        m = ARXIV_NEW.search(v) or ARXIV_OLD.search(v)
        if m:
            return m.group(1)
    return None


def find_acl_id(f: dict) -> str | None:
    for k in ("url", "doi", "note", "howpublished"):
        m = ACL_ID.search(f.get(k, ""))
        if m:
            return m.group(1)
    return None


def find_openreview_id(f: dict) -> str | None:
    for k in ("url", "note", "howpublished", "pdf"):
        m = OPENREVIEW_ID.search(f.get(k, ""))
        if m:
            return m.group(1)
    return None


def find_eprint_id(f: dict) -> str | None:
    if find_arxiv_id(f) and not re.search(r"iacr|eprint\.iacr", " ".join(f.values()), re.I):
        return None                      # an arXiv "eprint = {2406.13352}" field is not an IACR id
    for k in ("eprint", "url", "howpublished", "note", "journal", "booktitle", "publisher"):
        v = f.get(k, "")
        m = EPRINT_ID.search(v) if k != "eprint" else re.search(r"((?:19|20)\d{2})/(\d{1,5})", v)
        if m:
            return f"{m.group(1)}/{int(m.group(2)):03d}"
    return None


def lint(e: dict) -> list[str]:
    f, flags = e["fields"], []
    au = f.get("author", "")
    if not f.get("title"):
        flags.append("missing title")
    if not au and e["type"] not in ("misc", "book", "manual", "online"):
        flags.append("missing author")
    if re.fullmatch(r"\s*\{?\s*\w+\s+and\s+others\s*\}?\s*", au or ""):
        flags.append("placeholder author list ('X and others' only)")
    if re.search(r"\b(anonymous|author\d|firstname|lastname|tbd|todo|xxx)\b", au, re.I):
        flags.append("placeholder author name")
    if not f.get("year") and not f.get("date"):
        flags.append("missing year")
    if re.search(r"\b(tbd|todo|xxx|\?\?)\b", " ".join(f.values()), re.I):
        flags.append("TODO/TBD text in entry")
    if e["unverified_marker"]:
        flags.append("marked % UNVERIFIED in source")
    return flags


def judge(entry: dict, rec: dict | None, how: str) -> tuple[str, float, str]:
    f = entry["fields"]
    if rec is None:
        return "NOT_FOUND", 0.0, f"no record via {how}"
    ts = title_sim(f.get("title", ""), rec["title"])
    bib_s = set(surnames_from_bib(f.get("author", "")))
    rec_s = {surname_of(a) for a in rec["authors"]}
    overlap = len(bib_s & rec_s)
    missing = sorted(bib_s - rec_s)
    year_ok = True
    if f.get("year", "").strip()[:4].isdigit() and rec.get("year"):
        y = int(f["year"].strip()[:4])
        years = {rec["year"], rec.get("last_year") or rec["year"]}
        year_ok = any(abs(y - yy) <= 1 for yy in years if yy)
    detail = (f"{rec['source']}: \"{rec['title'][:80]}\"; title_sim={ts:.2f}; "
              f"author overlap {overlap}/{len(bib_s) or '?'}")
    if missing and bib_s:
        detail += f"; bib surnames not in record: {', '.join(missing)}"
    if not year_ok:
        detail += f"; year {f.get('year')} vs {rec.get('year')}"
    if ts >= 0.90 and (overlap >= 1 or not bib_s) and not missing and year_ok:
        return "VERIFIED", ts, detail
    if ts >= 0.90 and overlap >= 1 and year_ok and len(missing) <= max(0, len(bib_s) // 4):
        return "VERIFIED", ts, detail + " (minor author-name variance)"
    if how.startswith("id"):
        return "MISMATCH", ts, detail
    if ts >= 0.75:
        return "WEAK", ts, detail
    return "NOT_FOUND", ts, detail


def check_entry(e: dict, offline: bool, state: dict) -> dict:
    f = e["fields"]
    res = {"key": e["key"], "type": e["type"], "title": delatex(f.get("title", ""))[:120],
           "lint": lint(e), "status": "UNCHECKED", "score": 0.0, "detail": ""}
    if offline:
        res["detail"] = "offline mode"
        return res
    try:
        ids = []
        if (aid := find_arxiv_id(f)):
            ids.append((f"id arXiv {aid}", lambda aid=aid: fetch_arxiv(aid)))
        if (acl := find_acl_id(f)):
            ids.append((f"id ACL {acl}", lambda acl=acl: fetch_acl(acl)))
        if (oid := find_openreview_id(f)):
            ids.append((f"id OpenReview {oid}", lambda oid=oid: fetch_openreview(oid)))
        if (eid := find_eprint_id(f)):
            ids.append((f"id ePrint {eid}", lambda eid=eid: fetch_eprint(eid)))
        if f.get("doi") and not re.search(r"10\.48550/arxiv", f["doi"], re.I):
            doi = re.sub(r"^https?://(dx\.)?doi\.org/", "", f["doi"].strip())
            ids.append((f"id doi {doi}", lambda doi=doi: fetch_crossref_doi(doi)))
        if ids:
            best = None
            for how, fetch in ids:
                r = judge(e, fetch(), how)
                if r[0] == "VERIFIED":
                    best = r
                    break
                if best is None or r[1] > best[1]:
                    best = r
                time.sleep(state.get("delay", 1.0) / 2)
            res["status"], res["score"], res["detail"] = best
            return res
        title = delatex(f.get("title", ""))
        if not title:
            res["status"], res["detail"] = "NOT_FOUND", "no title, no id"
            return res
        cands, used = [], []
        if not state.get("dblp_blocked"):
            try:
                cands += search_dblp(title)
                used.append("DBLP")
            except (Blocked, ValueError):
                state["dblp_blocked"] = True
        first = (surnames_from_bib(f.get("author", "")) or [""])[0]
        cands += search_crossref(title, first)
        used.append("Crossref")
        if not cands or max(title_sim(title, r["title"]) for r in cands) < 0.90:
            try:
                cands += search_arxiv_title(title)
                used.append("arXiv")
            except (urllib.error.URLError, OSError, ValueError, ET.ParseError):
                pass
        best = max(cands, key=lambda r: title_sim(title, r["title"]), default=None)
        res["status"], res["score"], res["detail"] = judge(e, best, "search " + "+".join(used))
    except (urllib.error.URLError, TimeoutError, OSError, ValueError, ET.ParseError) as exc:
        res["status"], res["detail"] = "UNCHECKED", f"service error: {exc}"
    finally:
        time.sleep(state.get("delay", 1.0))
    return res


def duplicate_titles(entries: list[dict]) -> dict[str, list[str]]:
    seen: dict[str, list[str]] = {}
    for e in entries:
        t = norm_title(e["fields"].get("title", ""))
        if t:
            seen.setdefault(t, []).append(e["key"])
    return {t: ks for t, ks in seen.items() if len(ks) > 1}


def bib_sha256(text: str) -> str:
    """Content hash of the .bib file, stamped into the report so gates can check freshness
    without relying on file mtimes (which git checkouts reset)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def render(results: list[dict], dups: dict, bib_sha: str | None = None) -> str:
    order = {"MISMATCH": 0, "NOT_FOUND": 1, "WEAK": 2, "UNCHECKED": 3, "VERIFIED": 4}
    counts: dict[str, int] = {}
    for r in results:
        counts[r["status"]] = counts.get(r["status"], 0) + 1
    lines = ["# bib-verify report", ""]
    if bib_sha:
        lines += [f"bib-sha256: {bib_sha}", ""]
    lines += ["Summary: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items(), key=lambda kv: order[kv[0]])),
             "", "| status | key | score | lint | detail |", "|---|---|---|---|---|"]
    for r in sorted(results, key=lambda r: (order[r["status"]], r["key"])):
        lines.append(f"| {r['status']} | `{r['key']}` | {r['score']:.2f} | {'; '.join(r['lint'])} | "
                     f"{r['detail'].replace('|', '/')} |")
    if dups:
        lines += ["", "## Duplicate titles", ""] + [f"- {', '.join(ks)}" for ks in dups.values()]
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- selftest ---

SELFTEST_BIB = r"""
@misc{agentdojo,
  author = {Edoardo Debenedetti and Jie Zhang and Mislav Balunovi{\'c} and Luca Beurer-Kellner and Marc Fischer and Florian Tram{\`e}r},
  title = {{AgentDojo}: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for {LLM} Agents},
  eprint = {2406.13352}, archivePrefix = {arXiv},
  year = 2024,
}
% UNVERIFIED
@article{fake,
  author = "Chen and others",
  title = {A Paper That Does Not Exist About Quantum Fuzzy Toy Agents},
  journal = {IEEE TIFS}, year = {2024}
}
@inproceedings{toyacl, author = {Alice Example}, title = {Toy}, booktitle = {ACL},
  url = {https://aclanthology.org/2099.acl-long.42/}, doi = {10.18653/v1/2099.acl-long.42}, year = {2099}}
@inproceedings{toyor, author = {Alice Example}, title = {Toy}, booktitle = {ICLR},
  url = {https://openreview.net/forum?id=AbC_d-1}, year = {2099}}
% Legacy compatibility fixture: ePrint is not a default Agent Attack source.
@misc{toyiacr, author = {Alice Example}, title = {Toy}, howpublished = {Cryptology ePrint Archive, Paper 2018/421}, year = {2018}}
@article{toyarxivjournal, author = {Alice Example}, title = {Toy}, journal = {arXiv preprint arXiv:2099.01234}, year = {2099}}
@misc{toyarxivdoi, author = {Alice Example}, title = {Toy}, doi = {10.48550/arXiv.2099.54321}, year = {2099}}
"""

SAMPLE_ARXIV = """<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
<entry><id>http://arxiv.org/abs/2099.01234v3</id><updated>2100-02-01T00:00:00Z</updated>
<published>2099-01-15T00:00:00Z</published><title>Toy Agents
 Believe Toy Rumours</title><author><name>Alice Example</name></author><author><name>Bob Example</name></author>
<arxiv:journal_ref>Toy Conf 2099</arxiv:journal_ref></entry></feed>"""
SAMPLE_ARXIV_ERR = """<feed xmlns="http://www.w3.org/2005/Atom"><entry><id>http://arxiv.org/api/errors#x</id>
<title>Error</title></entry></feed>"""
SAMPLE_ACL_BIB = """@inproceedings{example-2099-toy,
    title = "Toy Agents Believe Toy Rumours",
    author = "Example, Alice  and
      Example, Bob",
    booktitle = "Proceedings of the 137th Annual Meeting of the Toy Association",
    year = "2099",
    url = "https://aclanthology.org/2099.acl-long.42/",
}"""
SAMPLE_OR_V2 = json.dumps({"notes": [{"id": "AbC_d-1", "pdate": 4072550400000, "content": {
    "title": {"value": "Toy Agents Believe Toy Rumours"}, "authors": {"value": ["Alice Example", "Bob Example"]},
    "venue": {"value": "TOYCONF 2099 Poster"}}}]})
SAMPLE_OR_V1 = json.dumps({"notes": [{"id": "x", "cdate": 4072550400000, "content": {
    "title": "Toy Agents Believe Toy Rumours", "authors": ["Alice Example"]}}]})


def selftest(online: bool) -> int:
    es = {e["key"]: e for e in parse_bib(SELFTEST_BIB)}
    assert list(es)[:2] == ["agentdojo", "fake"], list(es)
    ad = es["agentdojo"]
    assert ad["fields"]["year"] == "2024" and not ad["unverified_marker"] and es["fake"]["unverified_marker"]
    # id extraction for every resolver
    assert find_arxiv_id(ad["fields"]) == "2406.13352" and find_eprint_id(ad["fields"]) is None
    assert find_arxiv_id(es["toyarxivjournal"]["fields"]) == "2099.01234"
    assert find_arxiv_id(es["toyarxivdoi"]["fields"]) == "2099.54321"
    assert find_acl_id(es["toyacl"]["fields"]) == "2099.acl-long.42" and find_arxiv_id(es["toyacl"]["fields"]) is None
    assert find_acl_id({"url": "https://aclanthology.org/P19-1001.pdf"}) == "P19-1001"
    assert find_openreview_id(es["toyor"]["fields"]) == "AbC_d-1"
    assert find_eprint_id(es["toyiacr"]["fields"]) == "2018/421" and find_arxiv_id(es["toyiacr"]["fields"]) is None
    assert surnames_from_bib(ad["fields"]["author"])[-1] == "tramer"
    assert "placeholder author list ('X and others' only)" in lint(es["fake"])
    assert title_sim("{AgentDojo}: A Dynamic", "AgentDojo: a dynamic") == 1.0
    # parsers on embedded sample responses
    rec = parse_arxiv_atom(SAMPLE_ARXIV)[0]
    assert rec["title"] == "Toy Agents Believe Toy Rumours" and rec["year"] == 2099 and rec["last_year"] == 2100
    assert rec["authors"] == ["Alice Example", "Bob Example"] and rec["id"] == "2099.01234", rec
    assert parse_arxiv_atom(SAMPLE_ARXIV_ERR) == []
    acl = record_from_bib(SAMPLE_ACL_BIB, "ACL Anthology 2099.acl-long.42")
    assert acl["title"] == "Toy Agents Believe Toy Rumours" and acl["year"] == 2099
    assert {surname_of(a) for a in acl["authors"]} == {"example"}, acl
    v2 = parse_openreview_note(SAMPLE_OR_V2, "AbC_d-1")
    v1 = parse_openreview_note(SAMPLE_OR_V1, "x")
    assert v2["year"] == v1["year"] == 2099 and v2["authors"][1] == "Bob Example" and v1["title"] == v2["title"]
    # judging
    toy = {"type": "misc", "key": "t", "unverified_marker": False,
           "fields": {"title": "Toy agents believe toy rumours", "author": "Alice Example and Bob Example", "year": "2100"}}
    assert judge(toy, rec, "id arXiv 2099.01234")[0] == "VERIFIED"           # year matches the latest version
    wrong = dict(toy, fields=dict(toy["fields"], author="Carol Other"))
    assert judge(wrong, rec, "id arXiv 2099.01234")[0] == "MISMATCH"
    assert judge(toy, None, "search")[0] == "NOT_FOUND"
    rep = render([{"status": "VERIFIED", "key": "k", "score": 1.0, "lint": [], "detail": "d"}], {}, bib_sha256("x"))
    assert f"bib-sha256: {bib_sha256('x')}" in rep and "| VERIFIED | `k` |" in rep
    print("selftest (offline part): OK")
    if online:
        st = {"delay": 3.0}
        r0, r1 = check_entry(ad, False, st), check_entry(es["fake"], False, st)
        print(f"  online: {r0['key']} -> {r0['status']} ({r0['detail'][:90]})")
        print(f"  online: {r1['key']} -> {r1['status']} ({r1['detail'][:90]})")
        if r0["status"] == "UNCHECKED":
            print("  network unavailable or rate-limited: online part skipped")
        else:
            assert r0["status"] == "VERIFIED", r0
            assert r1["status"] in ("NOT_FOUND", "WEAK", "UNCHECKED"), r1
            print("selftest (online part): OK")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("bib", nargs="?")
    ap.add_argument("--offline", action="store_true", help="static lint only, no network")
    ap.add_argument("--only", help="comma-separated keys to check")
    ap.add_argument("--json", help="write JSON report to this file")
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between network lookups")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--selftest-online", action="store_true", help="selftest incl. two live lookups")
    a = ap.parse_args(argv)
    if a.selftest or a.selftest_online:
        return selftest(a.selftest_online)
    if not a.bib:
        ap.print_usage()
        return 3
    with open(a.bib, encoding="utf-8") as fh:
        bib_text = fh.read()
    entries = parse_bib(bib_text)
    if a.only:
        keep = set(a.only.split(","))
        entries = [e for e in entries if e["key"] in keep]
    state = {"delay": 0.0 if a.offline else a.delay}
    results = []
    for idx, e in enumerate(entries, 1):
        r = check_entry(e, a.offline, state)
        results.append(r)
        print(f"[{idx}/{len(entries)}] {r['status']:9s} {r['key']}", file=sys.stderr)
    if state.get("dblp_blocked"):
        print("note: DBLP served a bot challenge; title searches used Crossref only", file=sys.stderr)
    dups = duplicate_titles(entries)
    # only a full run (no --only subset) may vouch for the whole file
    print(render(results, dups, None if a.only else bib_sha256(bib_text)))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as fh:
            json.dump({"results": results, "duplicates": dups}, fh, indent=2, ensure_ascii=False)
    bad = [r for r in results if r["status"] != "VERIFIED"]
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
