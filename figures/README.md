# figures/ — Agent Attack house style, templates and local harvester

```text
style/        compatibility base style + venue sheets, palette.py (sizes, colour, CVD check)
templates/    p01..p16 synthetic figure templates + run_all.py
templates/tikz/  message flow, agent pipeline, topology and evidence diagrams
examples/     rendered outputs of templates (generated; synthetic only)
harvester/    harvest.py (public-paper PDFs -> local crops + index), gallery.py
PATTERNS.md   pattern catalog in words: use, anatomy, pitfalls, template
tests/        pytest smoke tests
gallery/      default harvest output; gitignored and never committed
```

Requirements: Python >= 3.10 with numpy and matplotlib. The harvester also needs PyMuPDF
(`pip install pymupdf`). TikZ templates and the table preview need TeX Live (`latexmk`, `pdflatex`, `tikz-cd`,
`booktabs`) and `pdftoppm`.

## 1. Use the house style

```python
import sys; sys.path.insert(0, "figures/style")
import palette as P

fig, ax = P.figure("acm", width="full", aspect=0.45)
ax.plot(rounds, adoption, **P.line_style(0), label="proposed")
ax.plot(rounds, baseline, **P.baseline_style(0), label="naive control")
P.save(fig, "fig_propagation", outdir="paper/figs")
```

Make figures at their final venue width and include them without extra scaling. Rates and counts should be loaded
from `results/` or generated tables, with every printed number linked to an EVIDENCE row. Use redundant encodings:
colour plus marker/dash, and printed values plus colour in heatmaps. The palette is checked for contrast under
simulated protan and deutan vision; run `python3 figures/style/palette.py` after changing it.

The file `style/crypto.mplstyle` is a compatibility filename retained for existing scripts. Its contents and the
palette are domain-neutral and intended for agent-attack evaluation figures.

| venue sheet | column width | full width |
|---|---:|---:|
| `acm` | 3.33 in | 7.00 in |
| `ieee` | 3.50 in | 7.16 in |
| `lncs` | 4.80 in | 4.80 in |

## 2. Figure patterns

| id | pattern | typical use |
|---|---|---|
| A1 | attack-flow bars | ASR/utility/detection by attack arm or defense |
| A2 | stage breakdown | prompt, routing, tool, memory and response costs |
| A3 | scaling curve | agents, rounds, context or task size; show measured points |
| A4 | threat-model plane | attacker knowledge × access or capability × stealth budget |
| A5 | utility/effectiveness Pareto plot | effectiveness versus benign utility or detection |
| A6 | propagation waterfall | belief/message states over rounds, with defenses marked |
| A7 | state/provenance layout | source labels, memory writes and message transformations |
| A8 | rubric heatmap | task × attack, model × surface or defense × attack |
| A9 | mechanism sensitivity | judge, temperature, topology or payload placement controls |
| A10 | failure distribution | latency, tokens, queries, costs or refusal/failure modes |
| A11 | error/ablation curve | proposed mechanism versus controls across a controlled sweep |
| A12 | budget crossover | success, cost or detection as the query/token budget changes |
| A13 | message/memory matrix | which agents receive, retain or transform a signal |
| A14 | configuration sweep | two discrete knobs with infeasible cells visibly marked |
| A15 | interleaved trial distributions | repeated runs with median, IQR, n and bootstrap interval |
| A16 | evidence-linked results table | main comparison with units, direction and evidence IDs |

The numbered Python files keep their historical names so existing project scripts continue to run. Treat their arrays
as synthetic placeholders: replace them with loaders for `trials.jsonl`, and rename axis labels to the actual
surface, task and metric before using them in a paper.

```bash
python3 figures/templates/run_all.py --venue acm
make -C figures/templates/tikz
```

## 3. Local figure harvester

Use only public PDFs supplied through `$CRA_PAPERS` or another explicitly permitted local directory. Keep the gallery
outside the repository and use it for design study, not as evidence or a source of copied artwork.

```bash
python3 figures/harvester/harvest.py "$CRA_PAPERS" \
    --out /tmp/agent_attack_figures --exclude drafts --exclude ours --exclude '.zip' \
    --jobs 8 --timeout 90 --max-pages 60
python3 figures/harvester/gallery.py /tmp/agent_attack_figures
python3 figures/harvester/harvest.py --selftest
```

The harvester detects captions, clips nearby vector/raster content, records drawing and whitespace statistics, and
classifies figures as bars, lines, scaling, tables, message flow, architecture, state machines, heatmaps, topology
or pseudocode. The classifier is heuristic; inspect the best crops by hand. Do not harvest private/review PDFs, real
user data or working attack payloads. Do not commit harvested images; record lessons in words in `PATTERNS.md` or a
project's `paper/figs/NOTES.md`, citing public identifiers.

## 4. Quality checklist

1. Final-size vector PDF and a readable PNG preview exist.
2. Every plotted number maps to a trial record and an EVIDENCE ID; every rate shows n and a CI.
3. The caption's first sentence states the single take-away and labels synthetic/toy data.
4. Controls and defenses use the same axes and scale as the proposed attack.
5. The threat-model diagram marks the sole access point and does not draw capabilities the attacker lacks.
6. Transcripts and payloads are redacted according to `ETHICS.md`.
7. The figure survives grayscale conversion, font inspection and a clean regeneration from the logged data.

```bash
python3 -m pytest figures/tests -q
pdftoppm -gray paper/figs/figure.pdf /tmp/figure-gray
pdffonts paper/figs/figure.pdf
```
