# 10 Evaluation

Full procedure, table rules and fairness statements:
[experiments-writing](../../experiments-writing/SKILL.md). Protocols upstream:
`eval-protocol`, `judge-validation`, `mas-testbed`, `adaptive-eval`.

## Structure

```
[opening]        Research questions RQ1..RQk (effectiveness, utility/stealth, ablation,
                 transferability, defenses), each answered in one subsection. Artifact
                 footnote (anonymous during review).
[setup]
  victims        Table: framework (version/commit) × model (provider snapshot id or
                 open-weight revision) × role; default defenses on/off.
  benchmarks     tasks/environments (public benchmark + version, or synthetic set with
                 its construction), number of tasks, how attack goals are paired with tasks.
  baselines      prior attacks (pinned in baselines/MANIFEST.md), each run in our harness
                 with its recommended configuration; "no attack" and "direct request" rows.
  metrics        ASR (success criterion of §3), utility (benign task success with and
                 without attack), stealth (detector / judge / human flag rate), cost.
                 Each rate with n and 95% CI (Wilson); paired comparisons with McNemar or
                 a CI on the difference.
  judge          if an LLM judges success: model snapshot, prompt (appendix), temperature,
                 agreement with human labels (accuracy, κ, n) — `judge-validation`.
  runs           temperature, seeds, attempts per task, total trials, date range of API
                 calls, cached responses (provenance).
[main results]   Table: rows = attacks (baselines + ours), columns = victims; cells = ASR
                 [CI]; plus utility column. Three bold-headed claims, scope first.
[ablations]      each component removed; budget/length sweeps; position of the attacker in
                 the topology; number of controlled agents.
[transferability] payload optimised on surrogate / model A, evaluated on B..Z; across
                 frameworks; across topologies or task domains.
[case study]     one redacted, synthetic end-to-end trace (appendix if long).
[limitations]    where ASR is low and why; variance across seeds/dates.
```

## Number discipline (summary)

1. Single data source (EVIDENCE rows → jsonl/csv → tables); no hand-typed numbers.
2. Scope sentence before every range (models, frameworks, n, judge).
3. Every rate: n and 95% CI; no CI-free "up to" claims.
4. No-attack and direct-request controls in the main table (base-model confound).
5. Baselines run in the same harness, same victims, same budget; reproduced vs
   reported numbers both given when a reported number is quoted.
6. Utility under attack is reported next to ASR (an attack that breaks the task is
   detectable).
7. Judge validated; programmatic success checks preferred where possible.
8. Model snapshots and API dates recorded; results from different snapshots are not
   pooled.
9. The ablation is the strongest evidence; include it in the body.
10. Cost (queries/tokens/$ with price date) disclosed for attacker and for defenses.

## Checklist

- [ ] RQs stated; each answered by a subsection with a bold claim.
- [ ] Setup table with framework versions and model snapshot ids.
- [ ] Metrics defined; every rate with n and CI; judge validation summarised in body.
- [ ] Controls (no attack, direct request) and strongest baseline attacks present.
- [ ] Ablation and transferability in the body.
- [ ] Every table cell traceable to an EVIDENCE row.
