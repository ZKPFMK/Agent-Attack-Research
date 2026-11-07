---
name: idea-mining-loop
description: Run the eight-step attack-idea loop: probe, free a fixed threat-model assumption, search systematically, find an anomaly against a naive baseline, identify the mechanism, run controls, validate on real local systems, and generalise with a limitation.
---
# idea-mining-loop

An idea is a mechanism that survives controls, not a stack of familiar payloads. Use this loop when the attack
bottleneck is measurable and intuition has stalled. Keep negative branches in IDEAS.md.

## Pre-gate

Write: `surface/branch = ...; access point = ...; object changed = ...; success metric = ...; naive baseline = ...`.
Reject circular threat models: an attacker who can edit system prompts or write the vector store already has the
claimed effect. State the defender value and containment before running model calls.

## Eight steps

0. **Probe.** Build a tiny synthetic/local test and record a baseline with n, task set and rule.
1. **Cheap probes.** Try 3–5 independent mechanisms in <=30 minutes each; kill those that cannot beat the naive
   baseline or require excluded access.
2. **Free an assumption (Gate A).** Ask what neighbouring papers fix by convention: source labels, message order,
   topology, role names, memory write timing, tool metadata, payload length, detector visibility, or attacker budget.
3. **Search and sweep.** Expose exactly one parameter and sweep wider than intuition; write one JSONL trial per
   seed with `agentattack.runner.run_matrix`.
4. **Find an anomaly (Gate B).** Compare against no-attack and naive injection. A smooth increase is not a mechanism.
   Look for a disproportionate change, transfer gap, phase transition or defense trade-off.
5. **Mechanistic root cause.** Explain the change in terms of context construction, provenance, routing, memory,
   tool choice, reasoning or feedback. Phrase a falsifiable `anomaly iff mechanism M` hypothesis.
6. **Control experiment.** Match the surface feature while removing M, and add M without the surface feature. If the
   anomaly remains, the proposed cause is incomplete.
7. **Real-system validation.** Port to at least two model families or local frameworks, with no-attack/naive/control,
   interleaved seeds, cached responses, validated judge and ASR/utility/stealth/cost.
8. **Generalise and bound the claim.** Vary task/topology/defense/attacker budget, state the transfer boundary and
   lower/upper limitation. "Works on one benchmark" is the honest endpoint when that is all the evidence supports.

## Examples

- 01: vary whether tool metadata is ranked by name, description or capability; control with semantically matched
  benign metadata and measure malicious tool selection plus benign task utility.
- 02: vary query-only memory injection timing; control with the same text that is never retrieved; measure canary
  recall and unrelated-task utility.
- 03: vary provenance labels during a toy chain relay; control with identical content and independent sources;
  measure adoption per round and the effect of a monitor agent.

## Kill switches

Kill or weaken the idea if the naive injection matches it, the effect vanishes under a benign utility control, the
access is circular, a judge cannot reach κ=0.7, an adaptive defense restores the control, or the nearest KB paper
has the same mechanism and threat model. Do not call a topology/configuration change novel by itself.

## Outputs

Update IDEAS.md with status, Gate A/B, root cause, control, KB-POSITION reference and kill switch; register every
paper-facing claim as `open` in CLAIMS.md; put scripts under `scripts/` and trials under `results/`.
