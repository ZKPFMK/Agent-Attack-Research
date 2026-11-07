# 07 Background

## Job

Fix terminology and recall exactly the system background the later sections use: the
agent/MAS model, the frameworks and protocols attacked, and the prior mechanisms the
attack builds on. Nothing more: standard LLM material that is not referenced later is
cited, not explained.

## Structure

```
2.1 LLM agents             one paragraph: the agent loop (observe → reason → act/tool call →
                           observe), context window contents (system prompt, user task, tool
                           outputs, memory/RAG), in the paper's notation
2.2 Multi-agent systems    roles, message passing, topology (chain/star/ring/complete/random),
                           orchestration (planner, debate, voting), what is shared (memory,
                           blackboard, tools)
2.3 The attacked surface   e.g. tool registries and MCP descriptions; web/DOM content;
                           memory write paths; inter-agent message channel
2.4 Frameworks/benchmarks  the concrete frameworks and benchmarks used later, with version
                           or commit, one sentence each
2.5 Notation               compact table (symbol/term | meaning), 6–12 rows
```

Security venues often merge 2.1–2.3 into a short "Background" and put related work at
the end; ML/NLP venues often put related work here as §2 and background inline.

## Rules

- Formalise only what later sections use: if the attack is defined over a message
  graph G = (V, E) with per-round messages m_i^t, define exactly that; avoid heavy
  formalism that no theorem or algorithm needs.
- Name framework versions/commits and model snapshots once, here or in the setup
  table, and refer to them consistently.
- A defense that the attack must bypass is described here or in §6, not both.
- If a reviewer is likely unfamiliar with the surface (e.g. MCP, accessibility trees,
  agent memory stores), keep one paragraph of intuition; reviewers outside the niche
  flag "background too brief".
- Diagrams of the benign system belong here only if Figure 1 does not already show
  them; reuse the same layout as the attack figure.

## Checklist

- [ ] Every term in the notation table is used in ≥ 2 later sections.
- [ ] The threat model (§3) and the attack algorithm (§4) can be stated with what §2
      defines.
- [ ] Frameworks/benchmarks named with version/commit; models with snapshot ids.
- [ ] No material that no later section uses.
