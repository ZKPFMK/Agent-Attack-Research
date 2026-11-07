# 08 Threat model

Source of truth: `THREAT-MODEL.md` (owned by `threat-modeler`, checked with the
`threat-model` skill and `aa threat-check`). The paper section is a faithful,
compressed rendering of it; any difference is a bug.

## Structure (one subsection or a boxed paragraph list)

```
[system]          The victim system: agents, roles, topology, tools/memory, which LLMs,
                  which defenses are deployed by default.
[attacker goal]   What counts as success, stated as a checkable predicate (programmatic
                  check on environment state, or judge with a validated rubric).
[knowledge]       black-box / gray-box / white-box; what the attacker knows about prompts,
                  models, topology, other agents' identities.
[capabilities]    exactly what the attacker controls (one tool description; content of one
                  web page; one agent's outputs; write access to shared memory) and what
                  not (cannot modify system prompts, cannot see other agents' messages).
[access point]    where adversarial content enters, mapped to a taxonomy surface.
[constraints]     query budget, payload length, stealth requirements (e.g. must pass a named
                  detector, must keep benign utility within x points).
[victims]         which users/agents are harmed and how.
[out of scope]    what the paper does not claim (base-model jailbreaks, compromise of the
                  provider, physical access, social engineering of developers).
[realism]         a short argument with a concrete deployment scenario for why an attacker
                  plausibly has this access (third-party tool marketplace, open web, open
                  agent network), citing incidents or prior work where possible.
```

## Rules

- **Every capability used in §4 appears here; nothing here is unused.** Reviewers
  read §3 and §4 side by side.
- Variants (e.g. black-box vs gray-box) each get their own line and are evaluated
  separately; tables label which variant produced each row.
- The success criterion is the **same** one the experiments measure. If ASR is judged
  by an LLM, say so here and point to the judge validation (§5 / appendix).
- Separate the attack effect from base-model misbehaviour: state that the target
  behaviour is refused (or not produced) by each victim without the attack, and that
  this is measured (no-attack control row).
- Realism argument: avoid "an attacker could easily..."; give a deployment story with
  a citation or a public incident, and state the main assumption that, if false,
  invalidates the attack.
- For MAS papers, state how many agents the attacker controls, whether it knows the
  topology, and whether it can choose its position.

## Checklist

- [ ] Goal is a checkable predicate identical to the evaluation's success criterion.
- [ ] Knowledge level and capabilities explicit; each used in §4, each evaluated.
- [ ] Out-of-scope list present; base-model-jailbreak confound addressed.
- [ ] Realism paragraph with a concrete deployment scenario.
- [ ] Matches `THREAT-MODEL.md` (diff checked by `threat-modeler`).
