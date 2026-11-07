---
name: attack-kb
description: Position an LLM-agent attack against the user's distilled knowledge base and the 01/02/03 taxonomy, then record the nearest papers and one testable delta. Use before investing in an idea, after a pilot changes the threat model, and at every novelty gate.
---
# attack-kb

The KB is a curated map, not a novelty oracle. Its summaries are evidence for positioning; the public paper
is the source for exact numbers and claims. Never edit the user's KB directly. Propose additions under
`kb/proposed/` and let the user approve them.

## Taxonomy

- **01 external interaction:** web/content and evidence inputs; chat-template/role boundaries; GUI/visual
  surfaces; tool/MCP metadata and selection; toolchain consequences and resource cost.
- **02 internal cognition:** training/backdoor triggers; reasoning and constraint hijacking; memory/RAG and
  multimodal memory poisoning; privacy/knowledge-file extraction; availability and malfunction amplification.
- **03 multi-agent collaboration:** infectious prompts; message tampering; malicious or hidden-intent agents;
  collusion/covert channels; distributed/compositional prompts; manipulated knowledge and misinformation;
  code/control-flow hijacking; blocking and collaboration denial.

Defense neighbours live in folders 04/05/06 and benchmark/framework neighbours in 07/08/09. Keep the axes
separate: entry point, attacker capability, victim state, success criterion, topology, and defense knowledge.

## Procedure

1. Resolve the KB from `--kb`, `$CRA_KB`, or the `kb:` line in STATE.md. Check its SHA-256 and date.
2. Search exact mechanism, aliases, access point, goal, and victim setting:
   `aa kb-search "query" -k 10`.
3. Read the top 5–10 entries. For each, record whether access point, victim, success criterion and defense
   assumptions are the same. A shared technique name alone is not pre-emption.
4. Place the idea on exactly one primary branch (01/02/03) and optionally one secondary branch. State why.
5. Write a `KB-POSITION.md` section with a ranked table and a one-line, testable delta. Do not say "first"
   unless the public search also supports it.
6. Include the nearest defense papers (04–06) and explain whether they cover the same access point.
7. If a paper is missing from the KB, write `kb/proposed/<yy>_<venue>_<slug>.md` in the established format:
   full title, Chinese title if known, year/venue, category, id, one paragraph ordered what → mechanism → scale
   → findings → differences, then code/data and public source. Do not add a title or number from memory.
8. Hand the position to the falsifier. The kill switch is: a KB/public paper with the same access point,
   victim state, goal and mechanism, or a pilot that only reproduces a known attack.

## Required distinction

"More agents", a different graph, a longer prompt, or stacking two known payloads is a configuration unless
it changes the threat model or exposes a new mechanism. Record the distinction explicitly.
