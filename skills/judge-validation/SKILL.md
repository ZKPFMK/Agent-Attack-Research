---
name: judge-validation
description: Validate an LLM judge or rule-based success detector against human labels before using it for ASR, utility or stealth. Use at P3, after changing the judge prompt/model, and whenever a reviewer questions the metric.
---
# judge-validation

A judge is part of the measurement instrument. Treat its prompt, model snapshot, temperature and parsing rule
like code: fingerprint them, validate them, and keep the labels.

## Procedure

1. Define the label before sampling: what exact behaviour counts as success, failure, refusal, partial success,
   utility loss or detection. Prefer deterministic tool-call/canary checks over semantic judging.
2. Draw a stratified sample across attack arms, models, tasks, defenses and expected outcomes. Preserve the raw
   transcript and a redacted human-label file; never let the judge see the gold label.
3. Have at least two human labels on a subset when feasible. Resolve disagreements with a documented rule. Keep
   `labels/<slug>/human.jsonl` and `labels/<slug>/judge.jsonl` with an item id and `label`.
4. Run:
   ```bash
   aa kappa labels/<slug>/human.jsonl labels/<slug>/judge.jsonl --field label --id id
   ```
   This reports accuracy, Cohen's κ, positive precision/recall/F1 and the confusion matrix. Record the judge
   fingerprint from `agentattack.judge.fingerprint`.
5. Use κ ≥ 0.70 as the pre-registered target. If it misses, revise the rubric or use human/rule labels; do not
   quietly change the threshold and keep the old ASR.
6. Check class imbalance and adversarial shortcuts: test benign controls, refusal language, exact canaries,
   tool-call traces, negation, quoted payloads and multilingual outputs.
7. Freeze the judge configuration before the main grid. Re-run validation after any model, temperature, system
   prompt, parsing or rubric change.
8. Report judge n, κ, precision/recall, fingerprint and whether each headline metric is judge-based or rule-based.

## Failure modes

- A fluent judge rewards the attack narrative instead of checking the victim action.
- One label per transcript hides disagreement and makes κ impossible to interpret.
- Validating only successful attacks creates spectrum bias.
- Calling judge disagreement a model failure without inspecting the transcript.
