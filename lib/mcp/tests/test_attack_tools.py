"""The agent-attack domain tools: kb_search, rate_ci, threat_check (in-process, no network)."""
import json

import pytest

pytest.importorskip("agentattack")

from cra_core.toolkit import init_project  # noqa: E402
from cra_mcp.tools import Context, build_tools  # noqa: E402

KB = """## AgentPoison
**全名：**AgentPoison: Poisoning Memory or Knowledge Bases。
**年份与会议：**2024，NeurIPS。
**分类：**内部认知攻击、长期记忆投毒。
**论文标识：**`24_neurips_agentpoison`。

Backdoor triggers retrieve poisoned memory entries.
"""


@pytest.fixture()
def tools(tmp_path):
    init_project(str(tmp_path))
    (tmp_path / "kb.md").write_text(KB, encoding="utf-8")
    state = (tmp_path / "STATE.md").read_text(encoding="utf-8")
    (tmp_path / "STATE.md").write_text(state.replace("<path to the knowledge base .md>", "kb.md"), encoding="utf-8")
    return tmp_path, {t.name: t.fn for t in build_tools(Context(str(tmp_path)))}


def test_kb_search(tools):
    root, T = tools
    r = T["kb_search"]("memory poisoning", kb_path=str(root / "kb.md"))
    assert r["ok"] and r["data"][0]["key"] == "24_neurips_agentpoison"
    assert T["kb_search"]("memory poisoning")["ok"]  # via the kb: line in STATE.md


def test_rate_ci(tools):
    root, T = tools
    (root / "results").mkdir(exist_ok=True)
    (root / "results" / "t.jsonl").write_text("\n".join(json.dumps({"m": m, "success": s})
                                                       for m, s in [("a", 1), ("a", 0), ("b", 1), ("b", 1)]))
    r = T["rate_ci"]("results/t.jsonl", by="m")
    assert r["ok"] and [(x["m"], x["k"], x["n"]) for x in r["data"]] == [("a", 1, 2), ("b", 2, 2)]
    assert not T["rate_ci"]("results/none.jsonl")["ok"]


def test_threat_check(tools):
    root, T = tools
    (root / "tm.json").write_text(json.dumps({"goal": "g", "surface": "moon"}))
    r = T["threat_check"]("tm.json")
    assert not r["ok"] and any("surface" in v for v in r["violations"])
