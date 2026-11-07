---
name: adaptive-eval
description: Evaluate an agent attack against defenses when the attacker knows the defense, as well as in the static setting. Use in P4/P5 for any claim about robustness, stealth or mitigation.
---
# adaptive-eval

A defense result is not meaningful if the attacker was frozen while the defense was visible. Separate the static
and adaptive conditions, keep the same task/seed grid, and state what the attacker knows.

## Procedure

1. Choose defenses from the relevant 04/05/06 folders or public benchmark baselines. Pin their code/config,
   model snapshot, detector threshold, system prompt and version in `baselines/MANIFEST.md`.
2. Define three arms where applicable: no defense, defense with the original attack, defense with an adaptive
   attack trained/tuned against that defense. The adaptive budget must be disclosed.
3. Freeze the task, seed, model, topology, temperature and trial count. Interleave all arms by seed; do not tune
   on the evaluation tasks.
4. Measure attack success, benign utility, false-trigger rate, detection/stealth, latency, tokens and query cost.
   Use Wilson CIs for rates and paired McNemar when the same tasks are paired.
5. For an adaptive attacker, disclose the observation: detector output, rejection reason, public system prompt,
   prior transcripts, tool schema, or only the final answer. Do not claim white-box adaptation from black-box data.
6. Report the defense's coverage boundary. A defense can lower ASR while degrading benign utility or moving the
   attack to a different surface; retain that result.
7. Keep failed adaptive attempts and budget limits. They are evidence about the chosen threat model, not proof of
   universal robustness.
8. Put every printed number in EVIDENCE.md with the raw trials log and a code/model/judge fingerprint.

## Kill switches

The robustness claim dies if an adaptive attack restores the baseline ASR within the pre-registered tolerance,
if the defense's utility loss exceeds the stated bound, or if the attack only works with access the threat model
excluded. Re-scope rather than hide the result.
