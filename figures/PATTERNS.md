# Figure pattern catalog for Agent Attack papers

This catalog describes figure structures in words. It does not reproduce harvested artwork or payload text. Sources are
public papers identified by a KB id, ACL Anthology id, OpenReview id, arXiv id or DOI; inspect the source locally and
record the exact figure number in the project's `paper/figs/NOTES.md`.

The local harvester is a design aid. Its crops are copyright material, stay outside git and never become evidence for
our results. Every synthetic template in this repository is labelled synthetic and must be regenerated from project
results before it enters a paper.

## Design rules

- One figure answers one question. Put the take-away in the first sentence of the caption.
- Draw the access point, victim state and defense boundary explicitly. A diagram must not grant the attacker a
  capability that `THREAT-MODEL.md` withholds.
- Rates show `k/n` and a 95% interval. Tables and captions name the model snapshot, task set and judge when relevant.
- Use colour plus a marker, line style, hatch or printed value. Figures must work in grayscale and for common colour
  vision deficiencies.
- Load data from `results/` or an evidence-linked table. Do not type headline values into a plotting script.
- Show controls: clean/no attack, naive injection, proposed mechanism, defenses and adaptive attacker where the claim
  requires them.
- Redact working payloads and private transcripts according to `ETHICS.md`; `[payload truncated]` is a valid label.

The compatibility filenames `style/crypto.mplstyle` and `templates/tikz/crypto-tikz.sty` are retained for existing
imports. Their contents are the domain-neutral Agent Attack house style.

## A1 — Effectiveness bars with uncertainty — `p01_speedup_bars.py`

Use for ASR, utility loss, detector rate or false-trigger rate across a small number of arms. Put the clean and naive
controls beside the proposed arm, use Wilson intervals as whiskers, print `k/n` in the caption or cells, and state
whether higher or lower is better. Avoid a single saturated bar labelled “ours” with no denominator.

## A2 — Pipeline or cost breakdown — `p02_breakdown_stacked.py`

Use when the mechanism has stages such as source retrieval, message routing, memory write, tool selection and final
response. Keep the same stage order in each row and show totals. Separate input tokens, output tokens, queries,
latency and estimated cost when they have different meanings; do not hide an expensive stage in one aggregate bar.

## A3 — Scaling or propagation curve — `p03_scaling_loglog.py`

Use for rounds, number of agents, context length, task count or attack budget. Show measured points, seed bands and
control curves. A log axis is justified by the range, not by aesthetics. Label the regime and report where the trend
breaks; a fitted line is not a mechanism or a bound.

## A4 — Threat-model capability map — `p04_param_feasibility.py`

Use a two-dimensional map such as attacker knowledge × access point or message budget × detector strength. Shade only
regions tested by the protocol, mark the selected cells, and label cells outside scope. Never call a synthetic boundary
a security limit; describe it as a design or evaluation boundary.

## A5 — Effectiveness/utility/stealth trade-off — `p05_pareto_tradeoff.py`

Use when an attack or defense trades ASR against benign utility, detection, latency or cost. Pareto points should come
from the same task/model configuration. State the direction of improvement on both axes and annotate only a few points.
A Pareto front is descriptive; it does not prove that an unmeasured point is dominated.

## A6 — Round-by-round state waterfall — `p06_noise_waterfall.py`

Use to show how a message, belief or memory state changes through rounds. Mark the injection, summarisation, detector
and retraction steps with distinct symbols. A rising “adoption” segment must not be mistaken for evidence of a real
system unless it is generated from logged trials; mock propagation is labelled toy.

## A7 — Provenance/state layout — `p07_modulus_layout.py`

Use for source-label preservation, message tampering, memory poisoning or tool-output transformation. Rows represent
states such as received, transformed and stored; segments represent content, provenance and metadata. Put the
attacker-controlled portion in the warning colour and show what the defender can inspect. A diagram of an example is
not a success-rate result.

## A8 — Task/model/defense heatmap — `p08_sbox_ddt_heatmap.py`

Use for a matrix of ASR, utility or detection. Print values and denominators in cells when readable; otherwise include
a keyed table. Mask missing or out-of-scope cells with hatching rather than assigning them a zero. Keep one colour
scale across panels and put the scale direction in the label.

## A9 — Sensitivity and ablation curve — `p09_trail_bounds.py`

Use for temperature, judge rubric, topology, memory policy, payload placement, corroboration count or defense budget.
Keep the proposed change isolated and include the naive control. Distinguish a confidence interval from a range over
conditions; annotate the condition where the mechanism stops working.

## A10 — Failure and cost distribution — `p10_error_distribution.py`

Use for latency, tokens, queries, estimated cost, refusal, timeout or parse-failure distributions. Show the sample
count and the failure-counting policy. Tail claims need enough observations or an explicit limitation; do not infer a
rare-event probability from a handful of trials.

## A11 — Metric error or judge agreement — `p11_approx_error.py`

Use for judge-versus-human disagreement, rubric threshold sweeps or detector calibration. Show the reference labels,
judge output and the operational threshold. Report kappa, precision, recall and F1 in the caption or table. A smooth
curve does not replace a stratified human-labelled sample.

## A12 — Budget crossover — `p12_crossover_cost.py`

Use when attack success, detection or cost changes regime as query/token/message budget grows. Overlay measured cells on
any analytic or toy expectation and mark the crossover as an observed region, not a universal threshold. Keep budget
definitions identical across arms.

## A13 — Message or memory matrix — `p13_sparsity_pattern.py`

Use a small multiple matrix to show which agent receives, forwards, stores or transforms a signal. Rows are agents or
memory stores and columns are rounds/channels. Use a single accent for attacker-controlled transitions and neutral
fills for absent edges. The matrix explains a mechanism; the transcript and evidence ledger support the quantitative
claim.

## A14 — Two-factor configuration sweep — `p14_param_sweep_heatmap.py`

Use for topology × corroboration, payload location × format, defense strength × budget or model × framework. Mark
infeasible cells, report the sweep range and highlight the pre-registered primary cell. Do not select the most
favourable cell after seeing results without recording the decision.

## A15 — Interleaved trial distributions — `p15_bench_distribution.py`

Use for latency, token count or cost comparisons where run order and variance matter. Plot individual runs, median and
IQR, and a paired/bootstrap interval. State warm-up, interleaving, cache and machine policy. For effectiveness rates,
use the rate/CI plot pattern instead of converting Bernoulli trials into fake timing points.

## A16 — Evidence-linked results table — `p16_results_table.py`

Use for the main comparison when there are fewer than roughly 30 values. Headers name the metric, direction, model,
framework and defense. Bold only the best value under the stated direction; explain missing cells. Add evidence IDs in
comments or a companion column while keeping the printed table readable.

## Diagram patterns

### D1 Message flow — `tikz/protocol_flow.tex`

Columns are attacker/content source, router or tool, victim agents and defender. Horizontal arrows show the actual
message path; dashed arrows show observations or probes. Put the single access point and the success state in the
caption.

### D2 Agent pipeline — `tikz/pipeline.tex`

Use left-to-right boxes for retrieval, planning, tool call, memory write and response. Tint the changed stage and keep
all other stages neutral. Reuse the same layout for clean, attacked and defended variants so the difference is visible.

### D3 Topology and propagation — `tikz/spn_round.tex`

Adapt the compatibility template to a chain, ring, star or arbitrary graph. Mark compromised nodes, directed edges,
round boundaries and retractions. The topology shown must match the simulator configuration and `THREAT-MODEL.md`.

### D4 Evidence/claim diagram — `tikz/commutative_diagram.tex`

Use a small graph from claim to protocol, raw trial records, judge labels and EVIDENCE rows. This helps reviewers see
which number supports which statement; it is not a substitute for the raw files.

### D5 State transformation or provenance diagram — `tikz/lattice_basis.tex`

Use boxes and arrows to show source labels, transformations and stored memory. Keep payload text abstract or redacted.
Use a legend for attacker-controlled, defender-controlled and observed data.

## Checklist before `paper/figs/`

1. The claim is `survived` or `weakened`; the caption uses weakened wording where required.
2. The generator reads logged data and names all EVIDENCE IDs.
3. Rates include n and CI; non-rate uncertainty has its method and sample count.
4. Model snapshot, framework, topology, temperature and defense are visible or defined in the caption.
5. The figure is final-size, vector, grayscale-readable and free of clipped labels.
6. Synthetic/mock content is labelled and never presented as a deployed vulnerability.
7. No working payload, credential, personal data or private transcript appears.
