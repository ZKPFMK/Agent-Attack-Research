---
name: experiments-writing
description: Use when turning attack/defense evaluation results into the evaluation section of an agent-attack paper. Enforces that every printed number traces to an EVIDENCE.md row with n and a 95% CI, prescribes table designs (setup, main ASR/utility results, ablation, transferability, defenses, judge validation), fair-comparison statements, and boundary/limitation statements.
---

# Experiments writing

## Iron rule

**Every number printed in the paper (text, table, figure, caption, footnote,
abstract) has an `EVIDENCE.md` row**: `ID | value as printed | meaning | command |
log path | code commit | machine / model snapshot | date | runs, statistic`. Rates
carry n and a 95% CI (Wilson, via `agentattack.metrics`). Tables are generated from
the jsonl/csv behind those rows (e.g. with the `crbench` table generator), not typed.
Put `\evid{E<n>}` (or `% EV:<ID>`) next to hand-placed numbers so `crbench audit-tex`
can cross-check them, and `\claimref{C<n>}` after each claim sentence.

## Procedure

1. **Freeze the data.** Ask `experimenter` for the final result files and the
   EVIDENCE rows. Anything run after the freeze requires a new row and a note in
   `DECISIONS.md`. Results from different model snapshots or API dates are not pooled.
2. **Decide the scope sentence** for every range ("across 4 victim models in 2
   frameworks, n = 300 tasks per cell, success by programmatic check").
3. **Write the section** following `paper-playbook/sections/10_evaluation.md`
   (and `11_defenses.md` for the defense results).
4. **Generate tables** (below). Mark the best cell per column (bold); captions
   define every abbreviation, the success criterion and n.
5. **Write the fairness statements** (below) that apply.
6. **Write boundary/limitation remarks** (below).
7. **Cross-check script**: `crbench audit-tex paper/main.tex EVIDENCE.md` (lib/bench),
   or extract every number from the PDF text (`pdftotext -layout`) and match it to
   EVIDENCE rows; unmatched numbers are errors unless they are setup constants or
   citations. Record the result in `SUBMISSION.md`.

## Table set

| table | contents | notes |
|---|---|---|
| Setup | framework + version/commit; model + snapshot id / revision; role; default defenses; benchmark + version; #tasks | one place for all pinning |
| Main results | rows = attacks (no attack, direct request, prior attacks, ours); columns = victims; cells = ASR [95% CI]; utility column | `n` in the caption; controls first |
| Utility / stealth | benign task success with/without attack; detector TPR at fixed FPR; length/perplexity stats | an attack that breaks the task is detectable |
| Ablation | each component removed; position of attacker; #controlled agents; budget | strongest evidence that each insight matters |
| Transferability | source (surrogate) → target models/frameworks/topologies matrix | heatmap or table; held-out targets marked |
| Defenses | defense × (ASR, utility) non-adaptive and adaptive | defense configs pinned |
| Judge validation | judge snapshot, n labelled, accuracy, κ, precision/recall of "success" | summary in body, details in appendix |
| Cost | tokens, calls, $ (price date), wall-clock per successful attack | attacker and defense overhead |

Layout: `\small`/`\scriptsize`, `\arraystretch` ≈ 0.92; table captions above
tables, figure captions below figures; CIs as `41.0 [35.2, 47.0]` or `41.0±5.9`
(state which).

## Fair-comparison statements (use the ones that apply)

- **Same harness:** "All attacks run in our harness on the same victims, tasks,
  temperature and attempt budget; baseline prompts follow the authors' released
  templates (commit in Table 2)."
- **Reproduced vs reported:** "Rerunning [X]'s released code yields 28% [ill.] on
  our setup versus 45% reported on theirs; we compare against the reproduced number
  and report both."
- **Cross-paper caution:** "ASRs from different papers use different victims,
  judges and success criteria and are not directly comparable; we mark quoted
  numbers with ◇."
- **Base-model confound:** "Without the attack, each victim produces the target
  behaviour in ≤ 1% [ill.] of tasks (no-attack row) and refuses the direct request in
  ≥ 95% [ill.]; the gain is therefore due to the attack, not a weakly aligned model."
- **Judge:** "Success is judged by <snapshot> with the prompt in Appendix B; on 200
  [ill.] human-labelled transcripts it agrees with the majority label in 94% [ill.]
  (κ = 0.86 [ill.])."
- **Snapshot/date:** "All API calls were made between <date> and <date> against the
  snapshot ids in Table 2; responses are cached in the artifact."
- **Statistical test:** "Differences between paired attacks are tested with an
  exact McNemar test on the same tasks; we report p-values without multiple-comparison
  correction unless stated."

## Boundary / limitation statements

- Exclusions: "Model D fails the benign task in 60% [ill.] of runs without attack; we
  report it separately and exclude it from pooled ranges."
- Where we lose: "In complete-graph topologies, majority voting reduces ASR to 7%
  [ill.]; RelayRumor relies on sequential dependence."
- Variance: "ASR varies by up to 6 points [ill.] across three seeds; we report the
  pooled rate with its CI."
- Synthetic vs real: "Tasks are synthetic; we make no claim about deployment rates."
- Cost: "Optimisation uses 1,200 [ill.] surrogate queries per payload."

## Measurement hygiene to report (and to follow)

- Fixed seeds and temperature; attempts per task (report pass@k only with k stated).
- All arms evaluated on the same task set in the same period; cached responses
  (`CachedBackend`) as provenance.
- Never mix runs from different snapshots or harness commits in one comparison; if an
  earlier number is not reproducible, retract it explicitly.
- Programmatic success checks preferred; LLM judges validated (`judge-validation`).

## Output

`paper/sections/evaluation.tex` (and `defenses.tex`), generated tables in
`paper/tables/`, the cross-check report in `SUBMISSION.md`.
