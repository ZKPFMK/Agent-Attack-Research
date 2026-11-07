---
name: eval-protocol
description: Pre-register and run fair evaluations of attacks and defenses for LLM agents and multi-agent systems. Covers interleaved trial grids, Wilson/bootstrap uncertainty, judge validation, utility, stealth, cost, model snapshots and cached raw responses before numbers enter EVIDENCE.md.
---
# eval-protocol

An attack evaluation is a measurement campaign, not a single ASR. Freeze the protocol before the main run;
keep the raw trial record and enough controls to distinguish an attack mechanism from an easy task, a weak judge,
or a model-version accident.

## Pre-registration

Write `results/<date>-<slug>/PROTOCOL.md` with:

- attack, access point, target system and success criterion from THREAT-MODEL.md;
- task set, benign controls, model families and exact snapshot/API dates;
- framework/tool/memory/topology versions, system prompts, temperature, max tokens, seed policy;
- arms: no attack, naive injection, proposed attack, relevant defense, adaptive attack against defense;
- n per cell (use `agentattack.metrics.n_for_halfwidth`, with the conservative p=.5 default);
- primary ASR, benign utility, false-trigger rate, stealth/detection, latency, tokens, queries and cost;
- judge/rule, human validation sample, κ target, judge fingerprint and stopping/multiple-comparison rule;
- redaction, cache path, environment fields and the pre-registered kill criteria.

## Run rules

1. Use `agentattack.runner.run_matrix` so trial records are resumable and seed-major interleaved. Each line must
   include arm, model snapshot, framework, defense, task id, seed, temperature, success, utility, detected,
   tokens, queries, cost, judge fingerprint and transcript/cache path where applicable.
2. Reset memory and external state between trials unless persistence is the independent variable. Never let an
   attack tune on evaluation tasks or leak a prior transcript into a control.
3. Run the same task/seed pairs for paired arms. Keep failures, timeouts and refusals as records with a reason;
   do not silently remove hard cases.
4. Use `Rate(k,n)`/Wilson 95% CIs for rates and bootstrap CIs for continuous metrics. For paired binary outcomes,
   report McNemar's p-value and discordant counts. Never print a rate without n.
5. Validate semantic judges with `skills/judge-validation`; prefer exact tool/canary checks where possible.
6. Measure benign utility with and without the attack. A method that succeeds by destroying all useful behaviour
   is an availability result and must be labelled that way.
7. Evaluate static and adaptive defenses. Report the attacker observation and budget; do not call a black-box
   adaptive search white-box.
8. Use `aa rate results/.../trials.jsonl --by model,defense --key success --md --log ...` and put its output,
   raw JSONL, environment, code commit and model snapshot in EVIDENCE.md.
9. Re-run a minimum of three independent seeds for smoke tests; the final n comes from the protocol, not from
   whichever trials happened to finish.

## Required report table

| arm | model/snapshot | framework/topology | defense | ASR [95% CI], n | utility [CI] | false-trigger | detected/stealth | tokens/queries/$ |
|---|---|---|---|---|---|---|---|---|

## Red flags

One model, one task, one seed, no naive baseline, judge-only success, pooled topologies, mixed snapshots,
missing benign utility, or an adaptive defense tested only against a frozen payload. File a negative result rather
than expanding the claim after seeing the outcomes.
