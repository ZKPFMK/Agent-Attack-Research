---
name: paper-figures
description: Produce publication-quality figures for a paper on attacks against LLM agents or multi-agent systems in the house style (venue column/full widths, Computer Modern or Times fonts, vector PDF, colour-blind-safe palette), starting from the templates in figures/. Covers attack-pipeline overviews, ASR-vs-defense bars with CI error bars, propagation/adoption curves over rounds, topology diagrams, model×attack heatmaps and results tables. Use when a paper needs a plot, a results table or a TikZ diagram, or when auditing figures before submission.
---
# paper-figures

Make every figure **at final size, in vector, from logged data, with a stated
take-away and visible uncertainty**. The toolkit lives in `figures/`: style sheets,
`palette.py`, matplotlib templates (`figures/templates/pNN_*.py`), TikZ templates
(`figures/templates/tikz/`) and `PATTERNS.md`. The templates were written for the
crypto version of this toolkit; the mapping below says which one to adapt for each
agent-attack figure type (use `figures/PATTERNS.md` codes if it has been updated).

## When to use
* Phase P7 (Writing + Figures): turning `results/` and EVIDENCE rows into figures.
* Phase P8 / camera-ready: re-rendering for a different venue class, or fixing
  reviewer complaints ("no error bars", "legend covers data", "unreadable in print").
* Any time a figure is drafted with default matplotlib settings.

## Procedure
1. **State the claim first.** Write the one sentence the figure must prove. It becomes
   the first sentence of the caption. If no claim exists, use a table or no figure.
2. **Pick the pattern** (figure type → template to adapt):

   | agent-attack figure | adapt | notes |
   |---|---|---|
   | Figure 1 motivating example / attack-pipeline overview (benign vs attacked flow) | `tikz/pipeline.tex` | identical layout for both flows; tint only the attacker element and the corrupted output |
   | Message flow between agents / tool calls over time | `tikz/protocol_flow.tex` | one lane per agent/tool; attacker messages dashed + tinted |
   | MAS topology diagram (chain/star/ring/complete, attacker position) | `tikz/pipeline.tex` (nodes + edges) | attacker node filled, victims outlined; same node order across panels |
   | ASR per attack or per defense with 95% CI error bars | `p01_speedup_bars.py` (+ `yerr`) | baseline attack in grey, ours in `P.OURS`; no-attack control as a reference line |
   | Propagation / adoption curve over rounds or hops | `p09_trail_bounds.py` (value vs round) or `p03_scaling_loglog.py` with linear axes | one line per topology/defense; shaded CI band; x = round/hop index |
   | Model × attack (or source → target transfer) heatmap | `p14_param_sweep_heatmap.py` / `p08_sbox_ddt_heatmap.py` | sequential single-hue map, cell annotations with the rate; outline the diagonal for transfer |
   | ASR vs utility (or stealth) trade-off across defenses/configs | `p05_pareto_tradeoff.py` | axes: utility (x) vs ASR (y); label points directly |
   | Cost breakdown (tokens/calls per stage) | `p02_breakdown_stacked.py` | never a pie |
   | ASR vs budget / payload length / #controlled agents | `p12_crossover_cost.py` or `p09_trail_bounds.py` | CI band; mark the budget used in the main table |
   | Seed-to-seed or snapshot-to-snapshot spread | `p15_bench_distribution.py` | shows that the gain is not noise |
   | Judge confusion matrix | `p08_sbox_ddt_heatmap.py` | 2×2 with counts, κ in the caption |
   | Main results table (ASR [CI], utility) | `p16_results_table.py` | best per column bold; controls first |

3. **Copy the template** into the project's `paper/figs/src/`. Replace the synthetic
   arrays with loaders that read `results/*.jsonl|csv`; compute rates and Wilson CIs
   with `agentattack.metrics` (`Rate(k, n).lo/.hi`). Never type numbers by hand.
4. **Size and font by venue.** Call `P.figure(venue, width="column"|"full"|fraction, aspect=...)`.
   * Built-in sheets: `lncs` (4.80 in), `acm` (3.33 / 7.00 in), `ieee` (3.50 / 7.16 in).
   * Other styles (ACL, NeurIPS/ICLR/ICML, USENIX): print `\the\columnwidth` and
     `\the\textwidth` in the venue style, convert pt → in (÷ 72.27), and pass a
     fraction of the closest sheet's full width; use `ieee`/`acm` for two-column and
     `lncs` (fraction > 1 allowed) for single-column styles.
   * In LaTeX, `\includegraphics[width=\columnwidth]` (or `\textwidth`) with no
     further scaling.
5. **Encode redundantly.**
   * Ours is `P.OURS` and baseline attacks/defenses use `P.baseline_style(i)`.
   * Every series gets a marker or dash in addition to its colour.
   * Categorical colours go in fixed order and never cycle past 8; the same model or
     defense keeps the same colour in every figure of the paper.
   * Sequential data uses one hue. Diverging data (e.g. ASR change vs no defense) is
     blue↔red with a grey midpoint at 0.
6. **Show uncertainty and n.** Error bars or bands are 95% CIs (say so in the caption,
   with n). Do not plot a rate without its CI; do not connect points from different
   model snapshots.
7. **Label directly.** End-of-line labels beat legends. Print values only on the bars
   that carry the claim. Percentages on a 0–100 axis unless the range is tiny (then
   say the axis is truncated).
8. **Redact.** No real payload text, usernames, API keys, URLs of live services or
   product screenshots in figures; synthetic transcripts only, with
   `[REDACTED: ...]` where needed.
9. **Render and inspect.** `python3 paper/figs/src/fig_x.py`, then open the PNG.
   Check label collisions, legends over data, greyscale readability
   (`pdftoppm -gray -r 150 fig.pdf /tmp/g`).
10. **Link to evidence.** Add the figure script path and the input data file to each
    EVIDENCE row whose number appears in the figure.
11. **Run the checklist** below and at the end of `figures/PATTERNS.md`.

## Checklist (quick)
- [ ] Vector PDF with fonts embedded (`pdffonts fig.pdf` shows no Type 3 fonts, unless usetex was used).
- [ ] Final size, and 7–8 pt text matching the caption font family.
- [ ] One y-axis, with units/definitions in both axis labels ("ASR (%)", "round").
- [ ] Every rate has a 95% CI bar/band; n stated in the caption.
- [ ] Ours is blue, baselines grey; same colour per model/defense across figures.
- [ ] Readable in greyscale and by colour-blind readers (`python3 figures/style/palette.py`).
- [ ] No pies, no 3-D, no rainbow colormaps, no coloured backgrounds, no in-axes titles duplicating the caption.
- [ ] Every number traces to EVIDENCE; synthetic/toy content labelled as such.
- [ ] Caption's first sentence is the take-away; defines ASR's success criterion or points to it.
- [ ] No payload text, identities, keys or live URLs in any figure.

## Tools
* `figures/style/palette.py`: `use`, `figure`, `size`, `line_style`, `baseline_style`, `direct_label`, `save`, `check_palette`.
* `figures/templates/run_all.py` renders every template (smoke test after style edits).
* `make -C figures/templates/tikz` builds the TikZ diagrams. `crypto-tikz.sty` (name
  kept for compatibility) can be `\usepackage`d in a paper.

## Anti-patterns seen in published agent-attack papers
* ASR bars with no error bars and no n, often from a single seed.
* A model × attack heatmap with a rainbow colormap and no cell values.
* Figure 1 as a cartoon with robot icons that does not show where the attacker sits.
* Benign and attacked flows drawn with different layouts, so the change is hard to see.
* Screenshots of real chat products with the payload readable.
* Propagation curves that pool different topologies or model snapshots in one line.
