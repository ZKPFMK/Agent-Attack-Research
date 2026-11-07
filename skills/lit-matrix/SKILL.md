---
name: lit-matrix
description: Build and lint the related-work matrix (work, venue/year, setting, technique, threat model / mechanism, concrete numbers + source, code available?, our delta) and the novelty-check log in LITERATURE.md. Use in P1, whenever a new baseline appears, and before writing the related-work section.
---

# lit-matrix

The matrix is the single place where "who did what, under which parameters, with which numbers" lives.
Writers copy from it; the falsifier attacks it; baselines are chosen from it.

## Format (in `LITERATURE.md`)

```markdown
## Related-work matrix
| work | venue/year | surface (01/02/03) | threat model (access, knowledge) | technique | victim models/frameworks | defenses evaluated | reported numbers + source | code? | our delta |
|---|---|---|---|---|---|---|---|---|---|
| [@agentpoison] AgentPoison | NeurIPS 2024 | 02 memory/RAG | query-only, black-box | retrieval-triggered poisoning | model/framework, task set | detector? | ASR, judge, n, Fig. 4 | yes/no | ours ... |
```

Column rules: `work` is a verified BibTeX key and public id; `surface` is 01 external, 02 internal or 03
collaboration; `threat model` states access and knowledge; `technique` is the mechanism in <=12 words; victim
models/frameworks includes exact snapshots/versions; defenses says what was actually tested; every reported number
has a table/figure/section pointer and metric definition; code is `yes <url>`, `no` or `unknown`; `our delta` is
explicit and can be `none`. Do not compare ASR values with different success criteria or judges as though they
share a denominator.

## Procedure

1. Seed from `references/reading-lists/<area>.md`, then expand with `paper-search` (last 12 months first).
2. One row per *result* (a paper with two incomparable results gets two rows).
3. Fill numbers only from the paper's tables/figures; if the paper's parameters differ from ours, note it in
   *setting* instead of "normalising" silently.
4. Mark the 2–4 rows that are the real competitors (**bold** the work cell); `baseline-engineer` pins those.
5. Lint: `python3 skills/lit-matrix/scripts/lit_matrix.py LITERATURE.md --bib refs.bib`.
6. `python3 skills/lit-matrix/scripts/lit_matrix.py --template` prints an empty skeleton.

## Reading the matrix for gaps

Sort by *setting*, then look for (a) settings with no row (application gap — weakest kind of novelty, must be
argued), (b) a technique used in one setting but not the neighbouring one (transfer), (c) a parameter every row
fixes to the same value (a "hidden fixed parameter" — hand to `idea-miner`), (d) threat model / mechanism that nobody has a
lower bound for.
