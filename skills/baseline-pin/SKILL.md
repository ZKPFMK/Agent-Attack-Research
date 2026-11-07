---
name: baseline-pin
description: Identify the strongest fair attack, defense or benchmark baseline, pin its exact revision, build the local adapter, verify behaviour and record the recipe in baselines/MANIFEST.md. Use in P4 before comparisons and whenever fairness is questioned.
---
# baseline-pin

A baseline is a measured comparison under the same task, victim, budget and reporting rules. A paper's chosen
baseline is evidence about what it compared, not proof that it is the strongest fair comparator.

## 1. Choose the baseline before fetching it

Start from `LITERATURE.md`, `KB-POSITION.md` and the defense rows in the user's KB. Classify each candidate:

- attack baseline: no attack, naive injection, the closest public mechanism and the proposed attack's ablations;
- defense baseline: the strongest applicable static defense and an adaptive defender when the claim concerns evasion;
- system baseline: the same task with the same model/framework and the attack surface disabled;
- benchmark baseline: a public harness or task suite that defines the workload and success rubric.

Write `baseline = X because ...; rejected Y because ...` in `DECISIONS.md`. Record mismatches instead of silently
forcing an incomparable system into a table. A different topology, model family or memory policy is a separate
condition unless the paper explicitly studies that factor.

## 2. Fetch and pin

```bash
references/baselines/fetch.sh "$PROJECT/baselines" <name>   # when a public fetch recipe exists
# record the full revision in baselines/PINNED.tsv and MANIFEST.md
```

Pin a full commit or immutable release digest. Record the public URL, licence, framework version, model snapshot
identifier, prompt/configuration hash and any patch hash. Do not commit third-party source trees, model weights,
credentials, private transcripts or working payloads. A baseline that cannot be fetched offline after the initial
setup must say so in its `REPRO.md`.

## 3. Build the local adapter

Record copy-pasteable commands, Python version, package lock or hashes, environment variables required at runtime,
framework/topology configuration and the exact command used to produce the raw result. Keep each configuration in a
separate directory and record a clean-cache or cache-warm policy. `crbench stale` is useful for compiled adapters;
for a model-backed run, record the model snapshot and response-cache path instead of relying on a mutable alias.

The adapter must expose the same task IDs and success rubric as the proposed attack. It must log messages, memory
writes, tool calls, detector decisions, tokens, queries, latency and failures in the same schema as `trials.jsonl`.
A mock/local adapter is the default for development; network calls and hosted models require the project's approved
containment and budget.

## 4. Verify before measuring

- [ ] the baseline's own smoke tests pass;
- [ ] task inputs and expected benign outputs are correct;
- [ ] the same model snapshot, temperature, decoding, framework, topology, task set and seed policy can be used on
      both arms;
- [ ] no-attack, naive-injection and proposed/ablation arms differ only in the preregistered factor;
- [ ] defenses are configured as their authors specify, and the adaptive attacker observes exactly the information
      allowed by the threat model;
- [ ] success labels agree with the frozen rubric and the validated judge; failures, refusals and timeouts are kept;
- [ ] the access point is reachable without granting the attacker the outcome being measured;
- [ ] API keys, private data and live third-party targets are absent from commands, logs and artifacts.

Print the runtime configuration and compare it with the source paper's setting. If a configuration is infeasible,
record the boundary and exact error, and make the harness emit `FAILED (<reason>)` rather than hiding the failure.

## 5. MANIFEST row

```markdown
| name | role | public url | revision/digest | framework + version | model/snapshot | task/config hash | build/run recipe | command | parser | fairness notes |
|---|---|---|---|---|---|---|---|---|---|---|
| naive-injection | attack control | local synthetic | repo:0123456789abcdef | local harness 0.1 | mock-rumor/seeded | tasks:abc123 | `pip install -e ...` | `aa sim config.json` | `aa rate` | same tasks, seeds and rubric as proposed arm |
```

Add a practical reproduction priority list and a `known differences` section. Every row must state whether it is
measured locally, reproduced from a public artifact, or retained only as a qualitative comparison.

## 6. Fairness sign-off

- [ ] same tasks, task order policy, seeds and stopping rule;
- [ ] same model family and snapshot, or a separate clearly labelled cross-model comparison;
- [ ] same temperature, tool permissions, memory/RAG state, context budget and framework/topology;
- [ ] same success rubric, judge fingerprint and human-label validation;
- [ ] same attack/query/token budget and detector observation;
- [ ] same defense configuration, with adaptive knowledge stated;
- [ ] same machine/session policy, cache policy and interleaving;
- [ ] every cited number re-measured locally or marked `reported` and never mixed into a computed ratio;
- [ ] benign utility, false-trigger rate, stealth and cost are reported alongside effectiveness;
- [ ] containment and release decisions are recorded in `ETHICS.md`.

## Hand-off

The row is complete, the fairness checklist is signed or has a written exception, the adapter's smoke run is logged,
and a reference result exists under `results/` with an EVIDENCE row. Next: `experimenter`; notify `falsifier` if the
baseline changes a claim's denominator or scope.
