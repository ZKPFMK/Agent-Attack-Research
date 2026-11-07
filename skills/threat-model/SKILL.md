---
name: threat-model
description: Make an agent-attack threat model precise, reachable and reproducible before designing the attack. Use in P0/P3 and whenever the access point, victim state, or defense assumptions change.
---
# threat-model

A threat model is an operational contract. It says what the attacker can reach, what the victim contains,
and exactly what counts as success. It is not a story about a powerful attacker.

## Required fields

`ThreatModel` JSON has exactly: `goal`, `target_system`, `access_point`, `knowledge` (black-box/gray-box/white-box),
`capabilities`, `constraints`, `success_criterion`, `victims`, `defenses`, `out_of_scope`, `surface`.
Write the human version in THREAT-MODEL.md and check the JSON:

```bash
aa threat-check threat/<variant>.json --md
```

## Procedure

1. Name the victim system, version or model snapshot, framework, topology, roles, tools, memory and data flow.
2. Identify the single attacker-controlled entry point: a page/tool result, MCP metadata, one participating agent,
   a normal memory write path, an image/UI element, a training corpus item, or a message edge.
3. Separate knowledge from capability. Black-box may know only public behaviour; gray-box may know prompts,
   topology or model family; white-box must justify access to weights/gradients. Do not grant a capability merely
   because it makes the attack easier.
4. State the objective as an observable output: a specified tool call, a leaked canary, a false-belief probe,
   a denial outcome, or a rubric label. Define who labels it and when.
5. Quantify constraints: controlled agents/messages/queries, token or dollar budget, payload length, stealth,
   latency, and whether the attacker knows the defense. State `none` explicitly where appropriate.
6. Run the reachability test: could an attacker reach this entry point without already possessing the access or
   effect the attack claims to obtain? A vector-store write is not a query-only memory attack; a system-prompt
   edit is not prompt injection.
7. List benign tasks and utility controls. A successful attack that breaks all normal behaviour is a denial result,
   not a stealthy integrity result.
8. List defenses and evaluate both static and adaptive settings when the attacker can observe them.
9. Write harm/containment in ETHICS.md before running real model calls. Use only owned/local or sandbox targets.
10. Register each realism and capability claim as `open` in CLAIMS.md; falsifier attacks it before P3 closes.

## Common mistakes

- Mixing attack success, capability exposure, and vulnerability rate.
- Reporting ASR without n, CI, judge definition or a benign false-trigger control.
- Calling a public paper's attack "black-box" while using hidden system prompts or privileged state.
- Omitting model snapshot, temperature, framework version, topology or memory reset policy.
- Treating a topology change as a new attack mechanism without explaining the mechanism.
