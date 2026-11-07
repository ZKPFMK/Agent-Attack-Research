# Agent-attack taxonomy

The user's paper folders are organised around three attack surfaces. The taxonomy is deliberately orthogonal:
entry point, attacker capability, victim state, mechanism, outcome and defense assumptions must be recorded
separately.

1. **01 external interaction:** attacker-controlled web/content/evidence, role/chat serialization, GUI/visual
   environment, tool/MCP metadata and choice, cross-tool consequences, resource cost.
2. **02 internal cognition:** training/backdoor, reasoning/constraint hijack, memory/RAG and multimodal memory,
   privacy/knowledge-file extraction, availability/fault amplification.
3. **03 collaboration:** infection/replication, message tampering, hidden/malicious agents, collusion/covert
   channels, distributed/compositional triggers, manipulated knowledge/misinformation, code/control-flow abuse,
   recursive blocking.

Defense folders 04–06, framework folder 07, benchmark folder 08 and false-information/trust folder 09 provide
comparison axes. A changed topology, additional agent, longer prompt or composition of known attacks is a new
setting only when it creates a new mechanism, capability or measurable trade-off. See
`skills/attack-kb/references/taxonomy.md` for representative public ids from the user's KB.
