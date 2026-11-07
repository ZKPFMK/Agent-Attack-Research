"""``aa`` -- command-line front end of agentattack.

  aa kb-search "memory poisoning via query only" [--kb PATH] [-k 5] [--json]
  aa kb-list [--kb PATH] [--papers DIR]                  list KB entries (and folder ids without a KB entry)
  aa rate trials.jsonl --by model,defense [--key success] [--md] [--log out.log]
  aa kappa gold.jsonl pred.jsonl [--field label] [--id id] [--positive true]
  aa threat-check THREAT-MODEL.json [--md]
  aa sim config.json --out transcript.jsonl              run a MAS propagation simulation, print adoption curve
  aa selftest                                            offline end-to-end check (mock backend only)
"""
from __future__ import annotations

import argparse
import json
import os
import sys

from . import __version__, judge, kb, mas, metrics
from .runner import load_records
from .threat_model import ThreatModel


def _need_kb(a) -> str:
    p = kb.resolve_kb(a.kb, a.project)
    if not p:
        raise SystemExit("no knowledge base found: pass --kb PATH, set CRA_KB, or add 'kb: <path>' to STATE.md")
    return p


def _cmd_kb_search(a) -> int:
    papers = kb.parse_kb(_need_kb(a))
    hits = kb.search(papers, " ".join(a.query), a.k)
    if a.json:
        print(json.dumps([{"score": s, "key": p.key, "title": p.title or p.heading, "venue_year": p.venue_year,
                           "category": p.category, "pdf": p.pdf, "code": p.code} for s, p in hits],
                         ensure_ascii=False, indent=1))
        return 0
    if not hits:
        print("no match (try other words, Chinese or English)")
    for s, p in hits:
        print(f"{s:.2f}  {p.short()}\n      {p.category}")
    return 0


def _cmd_kb_list(a) -> int:
    papers = kb.parse_kb(_need_kb(a))
    keys = {p.key for p in papers}
    for p in papers:
        print(p.short())
    print(f"# {len(papers)} KB entries")
    if a.papers:
        missing = [(c, i) for c, ids in kb.scan_papers(a.papers).items() for i in ids if i not in keys]
        for c, i in missing:
            print(f"NO-KB-ENTRY  {c}/{i}")
        print(f"# {len(missing)} paper folders without a KB entry")
    return 0


def _rate_rows(recs, by, key):
    if not by:
        return [{"rate": metrics.rate(recs, key)}]
    return metrics.rate_table(recs, by, key)


def _cmd_rate(a) -> int:
    recs = load_records(a.trials)
    by = [b for b in (a.by or "").split(",") if b]
    rows = _rate_rows(recs, by, a.key)
    lines = []
    if a.md:
        lines.append("| " + " | ".join(by + [a.key, "k/n", "95% CI (Wilson)"]) + " |")
        lines.append("|" + "---|" * (len(by) + 3))
        for r in rows:
            rt = r["rate"]
            lines.append("| " + " | ".join([str(r[b]) for b in by] + [f"{100 * rt.p:.1f}%", f"{rt.k}/{rt.n}",
                                                                     f"[{100 * rt.lo:.1f}, {100 * rt.hi:.1f}]"]) + " |")
    else:
        for r in rows:
            label = ", ".join(f"{b}={r[b]}" for b in by) or "all"
            lines.append(f"{label}: {a.key} = {r['rate'].fmt()}")
    out = "\n".join(lines)
    print(out)
    if a.log:
        os.makedirs(os.path.dirname(os.path.abspath(a.log)), exist_ok=True)
        with open(a.log, "w", encoding="utf-8") as fh:
            fh.write(f"# aa rate {a.trials} --by {a.by or ''} --key {a.key}  (agentattack {__version__})\n{out}\n")
    return 0


def _labels(path, field, idf):
    return {str(r[idf]) if idf else str(i): r[field] for i, r in enumerate(load_records(path))}


def _norm(v):
    return str(v).strip().lower()


def _cmd_kappa(a) -> int:
    g, p = _labels(a.gold, a.field, a.id), _labels(a.pred, a.field, a.id)
    common = sorted(set(g) & set(p))
    if not common:
        raise SystemExit("no common items between gold and pred (check --id)")
    rep = judge.agreement_report([_norm(g[i]) for i in common], [_norm(p[i]) for i in common], positive=_norm(a.positive))
    if len(common) < max(len(g), len(p)):
        rep["unmatched"] = max(len(g), len(p)) - len(common)
    print(json.dumps(rep, indent=1))
    if rep["kappa"] < a.min_kappa:
        print(f"WARN kappa {rep['kappa']:.3f} < {a.min_kappa}: do not report ASR from this judge yet", file=sys.stderr)
        return 1
    return 0


def _cmd_threat(a) -> int:
    tm = ThreatModel.load(a.path)
    issues = tm.validate()
    if a.md:
        print(tm.to_markdown())
    for i in issues:
        print(f"ISSUE  {i}")
    print("threat model OK" if not issues else f"{len(issues)} issue(s)")
    return 1 if issues else 0


def _cmd_sim(a) -> int:
    with open(a.config, encoding="utf-8") as fh:
        cfg = json.load(fh)
    tr = mas.from_config(cfg).run()
    tr.dump(a.out)
    curve = mas.adoption_curve(tr)
    print(json.dumps({"adoption_per_round": [round(x, 4) for x in curve], "final": mas.final_adopters(tr),
                      "transcript": a.out}, ensure_ascii=False, indent=1))
    return 0


def selftest() -> int:
    import tempfile

    from .toy import rumor_mock

    assert metrics.Rate(0, 10).lo == 0.0 and metrics.Rate(10, 10).hi == 1.0
    assert abs(metrics.wilson_ci(50, 100)[0] - 0.4038) < 1e-3
    assert judge.cohen_kappa([1, 1, 0, 0], [1, 1, 0, 0]) == 1.0
    sample = ("## Toy Attack\n**全名：**Toy Attack on Agents。  \n**年份与会议：**2099，ToyConf。  \n"
              "**分类：**多智能体协作安全、记忆投毒。  \n**论文标识：**`99_toy_attack`。\n\n"
              "A toy summary about memory poisoning in multi-agent chats.\n\n**原文：**[本地 PDF](../x.pdf)。\n")
    ps = kb.parse_kb_text(sample)
    assert ps[0].key == "99_toy_attack" and kb.search(ps, "memory poisoning")[0][1].key == "99_toy_attack"
    names = [f"a{i}" for i in range(5)]
    sim = mas.Simulation([mas.Agent(n, "You relay facts.") for n in names], mas.chain(names), rumor_mock(0.9, 1),
                         rounds=4, task="toy", probe="Is the bridge closed?", adopt=mas.make_adopt({"startswith": "YES"}),
                         injections=[mas.MaliciousAgent("a0", "CLAIM: the bridge is closed [source: forum]")])
    tr = sim.run()
    with tempfile.TemporaryDirectory() as d:
        tr.dump(os.path.join(d, "t.jsonl"))
        assert mas.adoption_curve(mas.Transcript.load(os.path.join(d, "t.jsonl"))) == mas.adoption_curve(tr)
    print("agentattack selftest ok")
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="aa", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--version", action="version", version=__version__)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name, fn in (("kb-search", _cmd_kb_search), ("kb-list", _cmd_kb_list)):
        s = sub.add_parser(name)
        if name == "kb-search":
            s.add_argument("query", nargs="+")
            s.add_argument("-k", type=int, default=5)
            s.add_argument("--json", action="store_true")
        else:
            s.add_argument("--papers", help="papers/ root with category folders, to find ids without a KB entry")
        s.add_argument("--kb")
        s.add_argument("--project", default=".")
        s.set_defaults(fn=fn)
    r = sub.add_parser("rate", help="success rate with Wilson 95%% CI from a trials jsonl")
    r.add_argument("trials")
    r.add_argument("--by", default="")
    r.add_argument("--key", default="success")
    r.add_argument("--md", action="store_true")
    r.add_argument("--log", help="also write the table to this log (cite it in EVIDENCE.md)")
    r.set_defaults(fn=_cmd_rate)
    k = sub.add_parser("kappa", help="judge vs gold labels: kappa, precision, recall")
    k.add_argument("gold")
    k.add_argument("pred")
    k.add_argument("--field", default="label")
    k.add_argument("--id", default="id", help="item id field ('' = line order)")
    k.add_argument("--positive", default="true")
    k.add_argument("--min-kappa", type=float, default=0.7)
    k.set_defaults(fn=_cmd_kappa)
    t = sub.add_parser("threat-check", help="validate a threat-model JSON")
    t.add_argument("path")
    t.add_argument("--md", action="store_true")
    t.set_defaults(fn=_cmd_threat)
    s = sub.add_parser("sim", help="run a multi-agent propagation simulation from a JSON config")
    s.add_argument("config")
    s.add_argument("--out", required=True)
    s.set_defaults(fn=_cmd_sim)
    sub.add_parser("selftest").set_defaults(fn=lambda a: selftest())
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
