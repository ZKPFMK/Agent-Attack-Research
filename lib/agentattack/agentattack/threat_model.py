"""A machine-checkable threat model for an attack on an LLM agent / multi-agent system.

The blackboard file THREAT-MODEL.md is written for humans; this dataclass is the structured twin
(``aa threat-check tm.json``) so that missing fields and common realism gaps are caught early.
"""
from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field, fields

KNOWLEDGE = ("black-box", "gray-box", "white-box")

# Attack surfaces (top level) and branches, following the user's KB folder layout 01/02/03.
SURFACES: dict[str, list[str]] = {
    "external-interaction": [
        "web/content injection", "tool/MCP description & metadata", "tool selection & retrieval",
        "evidence/search poisoning", "chat-template & role confusion", "GUI/visual/pop-up",
        "toolchain consequence & cost",
    ],
    "internal-cognition": [
        "training backdoor", "memory/RAG poisoning", "reasoning hijack", "privacy & knowledge-file extraction",
        "availability/fault amplification",
    ],
    "multi-agent-collaboration": [
        "infectious/self-replicating prompt", "message tampering / man-in-the-middle", "malicious or hidden-intent agent",
        "collusion & covert channel", "manipulated knowledge / misinformation propagation", "control-flow hijack & code execution",
        "compositional / distributed prompt", "blocking & denial of collaboration",
    ],
}

REQUIRED = ("goal", "target_system", "access_point", "knowledge", "capabilities", "success_criterion", "surface")


@dataclass
class ThreatModel:
    goal: str = ""                     # what the attacker wants the victim system to do / believe / leak
    target_system: str = ""            # the victim system (framework, topology, tools, memory)
    access_point: str = ""             # where attacker-controlled bytes enter (web page, tool output, one agent, memory ...)
    knowledge: str = ""                # black-box | gray-box | white-box (+ what exactly is known)
    capabilities: list[str] = field(default_factory=list)   # what the attacker can do (and how often/how much)
    constraints: list[str] = field(default_factory=list)    # stealth, budget, no model weights, query limits ...
    success_criterion: str = ""        # operational, judge-checkable definition of success
    victims: list[str] = field(default_factory=list)        # models / agents evaluated as victims
    defenses: list[str] = field(default_factory=list)       # defenses assumed deployed (and whether attacker knows them)
    out_of_scope: list[str] = field(default_factory=list)
    surface: str = ""                  # key of SURFACES, optionally "surface/branch"

    def validate(self) -> list[str]:
        """Return human-readable issues (empty = passes the mechanical checks)."""
        issues = []
        for f in REQUIRED:
            v = getattr(self, f)
            if not v or (isinstance(v, list) and not any(str(x).strip() for x in v)):
                issues.append(f"missing: {f}")
        k = self.knowledge.split()[0].strip(",;:").lower() if self.knowledge.strip() else ""
        if self.knowledge and k not in KNOWLEDGE:
            issues.append(f"knowledge should start with one of {', '.join(KNOWLEDGE)} (got {self.knowledge!r})")
        top = self.surface.split("/")[0].strip()
        if self.surface and top not in SURFACES:
            issues.append(f"surface {top!r} not in {', '.join(SURFACES)}")
        sc = self.success_criterion.lower()
        if self.success_criterion and not any(w in sc for w in ("judge", "match", "exact", "contains", "call", "rule",
                                                                  "label", "executes", "outputs", "adopt", "probe")):
            issues.append("success_criterion should be operational (how is success checked: rule, exact match, "
                          "tool call observed, validated judge, belief probe ...)")
        if not self.out_of_scope:
            issues.append("out_of_scope is empty: state what the attacker cannot do (e.g. modify weights, "
                          "control the user, read other agents' private channels)")
        if not self.constraints:
            issues.append("constraints is empty: state stealth/budget/query limits or say 'none' explicitly")
        if not self.defenses:
            issues.append("defenses is empty: name the defenses evaluated (or 'none deployed' + why realistic)")
        if k == "white-box" and not any("weight" in c.lower() or "gradient" in c.lower() for c in self.capabilities):
            issues.append("white-box knowledge but no capability uses weights/gradients: is gray-box enough?")
        return issues

    def to_markdown(self, title: str = "Threat model") -> str:
        def lst(xs):
            return "".join(f"\n  - {x}" for x in xs) if xs else " —"
        return (f"## {title}\n"
                f"- **Surface:** {self.surface}\n- **Attacker goal:** {self.goal}\n"
                f"- **Target system:** {self.target_system}\n- **Access point:** {self.access_point}\n"
                f"- **Knowledge:** {self.knowledge}\n- **Capabilities:**{lst(self.capabilities)}\n"
                f"- **Constraints / stealth:**{lst(self.constraints)}\n"
                f"- **Success criterion:** {self.success_criterion}\n- **Victims:**{lst(self.victims)}\n"
                f"- **Defenses considered:**{lst(self.defenses)}\n- **Out of scope:**{lst(self.out_of_scope)}\n")

    @classmethod
    def from_dict(cls, d: dict) -> "ThreatModel":
        names = {f.name for f in fields(cls)}
        unknown = set(d) - names
        if unknown:
            raise ValueError(f"unknown threat-model fields: {', '.join(sorted(unknown))}")
        return cls(**d)

    @classmethod
    def load(cls, path: str) -> "ThreatModel":
        with open(path, encoding="utf-8") as fh:
            return cls.from_dict(json.load(fh))

    def to_dict(self) -> dict:
        return asdict(self)
