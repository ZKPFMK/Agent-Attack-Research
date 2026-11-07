---
name: log-to-evidence
description: Turn agent-attack trial logs into EVIDENCE.md rows and generated LaTeX/Markdown tables so every reported rate, utility, detection or cost traces to a command, raw record, revision and environment. Use after every evaluation campaign and before each paper build.
---
# log-to-evidence

**No number enters the paper without an EVIDENCE row.** Each row records the value as printed, its metric meaning,
exact command, raw log or JSONL path, code revision, environment/model snapshot, date and statistic. Rates include
`k/n` and a 95% Wilson interval. Derived values get a separate row with `derived: <formula over IDs>`.

## Procedure

1. **Preserve raw records.** Keep `results/<date>-<slug>/PROTOCOL.md`, `trials.jsonl`, `cache.jsonl` and `env.json`.
   Every trial retains arm, task id, seed, model/snapshot, framework/topology, defense, temperature, success,
   utility, detected, tokens, queries, cost, judge fingerprint and transcript path. Do not overwrite a run that later
   disagrees with a summary.
2. **Recompute from JSONL.** Use the project library and the same filter used by the protocol:
   ```bash
   aa rate results/2026-01-01-rumor/trials.jsonl \
      --by arm,model,defense --key success --md
   ```
   Inspect the filtered records and failure policy before copying a value. Keep any recomputation script under the
   project `scripts/` or `falsify/<claim-id>/` so it can run again.
3. **Choose the printed form.** State the metric definition, rounding rule, denominator and whether failures,
   refusals and timeouts are counted. Use one rule across abstract, tables, captions and appendix. Do not call a toy
   mock-backend output a real-model result.
4. **Add an evidence row.** Use `crbench evidence add` with the raw JSONL and the exact command. For example:
   ```bash
   crbench evidence add EVIDENCE.md --printed '41.0% [35.2, 47.0] (n=300; k=123)' \
     --meaning 'ASR for proposed arm; success rubric R2' \
     --command 'aa rate results/2026-01-01-rumor/trials.jsonl --by arm --key success --md' \
     --log results/2026-01-01-rumor/trials.jsonl --runs '123/300; Wilson 95% CI' --target .
   crbench evidence add EVIDENCE.md --printed '−8.4 pp' \
     --meaning 'utility difference under attack versus clean' \
     --command 'derived: E7 - E8' --log -
   ```
   `--commit auto` records the code revision and dirty state; `--machine auto` records a host hash. Include model
   snapshot and judge fingerprint in the meaning or environment field.
5. **Generate tables from the same records.** Keep evidence IDs beside cells or comments:
   ```bash
   crbench table results/2026-01-01-rumor/trials.jsonl --latex \
      --evidence proposed=E7 naive=E8 utility=E9
   ```
   In LaTeX use `\evid{E7}` or a `% EV:E7` comment so the audit can connect the number to the ledger.
6. **Audit before every build.**
   ```bash
   crbench evidence check EVIDENCE.md --root .
   crbench audit-tex paper/main.tex EVIDENCE.md
   ```
   Fix every `untraced` and `mismatch`. Use an ignore marker only for definitions, years or counts that are clearly
   not empirical claims, and record the reason beside it.

## Synthetic row examples

```markdown
| ID | value as printed | meaning | command | log path | code/model | date | statistic |
|---|---|---|---|---|---|---|---|
| E1 | 41.0% [35.2, 47.0] (n=300; k=123) | proposed ASR, rubric R2 | `aa rate ... --by arm` | `results/2026-01-01-rumor/trials.jsonl` | `abc123; model-snapshot-x` | 2026-01-01 | Wilson 95% |
| E2 | 18.0% [14.0, 22.9] (n=300; k=54) | naive-injection ASR | `aa rate ... --by arm` | same JSONL | `abc123; model-snapshot-x` | 2026-01-01 | Wilson 95% |
| E3 | +23.0 pp | proposed minus naive | `derived: E1 - E2` | `-` | `-` | 2026-01-01 | paired/bootstrap CI |
| E4 | 7.0% (n=300; k=21) | detector rate under proposed arm | `aa rate ... --key detected` | same JSONL | `abc123; detector-y` | 2026-01-01 | Wilson 95% |
| E5 | withdrawn | later rerun changed the denominator; see E6 | `recompute.py` | `results/...` | `...` | 2026-01-02 | reason recorded |
```

## Pitfalls

- **Mixed configurations:** one row must come from one model/framework/topology/defense configuration. Do not combine
  the best cells from different sweeps into one headline.
- **Unpaired denominators:** if arms do not share task ids and seeds, label the comparison unpaired and use the right
  interval/test.
- **Rates without n or CI:** the percentage alone is not evidence.
- **Judge drift:** a changed rubric/model/temperature creates a new judge fingerprint and a new evidence row.
- **Hidden failures:** keep timeouts, refusals, parse errors and excluded trials visible with their counting rule.
- **Negative results:** failed defenses, false triggers, utility loss and boundary conditions are evidence too.
- **Toy leakage:** results from `MockBackend` or `aa sim` are labelled synthetic and cannot support a claim about a
  real model or deployed product.
