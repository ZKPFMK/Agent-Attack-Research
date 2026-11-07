# THREAT-MODEL — one section per attack variant (owner: `threat-modeler`)

> Machine-readable twin: `threat/<variant>.json` (fields of `agentattack.threat_model.ThreatModel`);
> check with `aa threat-check threat/<variant>.json`. Realism and capability statements the paper makes are
> registered in CLAIMS.md.

### TM-1 — <short name>   (claims: <C..>; surface: <01|02|03 ...>; status: draft | checked | frozen)
**Goal.** <observable attacker objective>
**Victim system.** <framework + topology + roles + memory/tools + models>
**Access point.** <the single channel where attacker-controlled bytes enter>
**Knowledge.** black-box | gray-box (<what is known>) | white-box
**Capabilities.** <per round / in total: messages, tokens, queries, edits>
**Constraints / stealth.** <detectors to evade, budgets, "each message individually true", ...>
**Success criterion.** <operational: rule / exact match / tool call observed / validated judge / belief probe; when measured>
**Defenses assumed.** <none | named defenses; does the attacker know them (adaptive)?>
**Out of scope.** <what we do not claim>
**Realism.** <why the access point is reachable without already holding what the attack grants; who holds it in practice>
**Formalisation.** <optional: optimisation objective or propagation model>
`aa threat-check` result: <ok | issues>, <date>
