---
name: figure-harvest
description: Harvest figures from a local corpus of public agent-security / multi-agent papers (PDF), classify them by type, score their quality, and browse them in a local HTML contact sheet to learn which figure patterns work (attack-pipeline overviews, ASR bars, propagation curves, topology diagrams, heatmaps). Use before designing figures for a new paper or when extending figures/PATTERNS.md. Output is local-only (copyright).
---
# figure-harvest

Learn figure patterns from the papers closest to yours: related attacks, same-venue
papers, benchmark papers and the baseline papers. The distilled lessons go into
words. The harvested images are never committed.

## When to use
* At the start of P7 (Writing + Figures), on the related-work PDFs gathered in P1
  (the user's KB corpus via `$CRA_PAPERS`, or arXiv/OpenReview/ACL Anthology downloads).
* When the target venue or sub-field has conventions you do not know yet.
  Examples: prompt-injection papers lead with a Figure 1 showing the injected
  content inside a tool output or web page; MAS papers use topology diagrams and
  per-round propagation curves; benchmark papers use model × attack heatmaps and
  ASR–utility scatter plots; GUI-agent papers use annotated screenshots.
* When extending `figures/PATTERNS.md` with a new pattern.

## Procedure
1. **Assemble the corpus.** Use a directory of *public* PDFs. Exclude your own drafts,
   anything under embargo or review, and anything not public:
   ```bash
   python3 figures/harvester/harvest.py "$CRA_PAPERS" \
       --out /tmp/fig_gallery --exclude drafts --exclude ours --exclude '.zip' \
       --jobs 8 --timeout 90 --max-pages 60
   ```
   * `--exclude` takes a substring glob, or `re:REGEX` for a regular expression.
   * Directories are searched recursively (a KB laid out as one folder per category
     and paper id works directly).
   * Duplicate PDFs are skipped, detected by hash or by first-page text.
2. **Browse.** Run `python3 figures/harvester/gallery.py /tmp/fig_gallery` and open
   `index.html`. The page groups figures by type and sorts them by quality. It has a
   type filter and a minimum-quality slider.
3. **Inspect the best 10–20** for your planned figure types. The classifier's types
   map to agent-attack figures roughly as: `agent-architecture` → Figure 1 /
   attack overview; `message-flow` → agent message flows; `topology-graph` → network
   layouts; `plot-bar` → ASR/defense bars; `plot-line` → propagation/adoption curves;
   `heatmap-matrix` → model × attack grids; `table-like` → results tables. For each
   figure, note in words:
   * what makes it readable (where is the attacker shown? is benign vs attacked flow
     comparable?)
   * which encodings it uses (colour for attacker, dashes for injected messages)
   * how it handles uncertainty (CIs? seeds? n?), baselines and controls
   * how it handles harmful content (redaction, synthetic examples)
   * what you would not copy
4. **Distil.** Update the project's `paper/figs/NOTES.md`, or `figures/PATTERNS.md`
   if the pattern is new (coordinate with the `figure-artist` owner of `figures/`).
   Follow `figures/gallery_index.template.md`:
   * pattern name
   * public paper (title + venue/year or arXiv id) and figure number ("see e.g."),
     KB id if the paper is in the user's KB
   * what works
   * pitfalls
   * the template that implements it (create one if missing: synthetic data, plus a
     PDF+PNG in `figures/examples/`)
5. **Discard.** Delete the gallery, or keep it outside the repository.
   Never `git add` a harvested PNG; never quote harvested payload text.

## How it works (so you can trust or tune it)
* **Captions.** A text block counts as a caption if its first line matches
  `Fig.|Figure|图 <n>` followed by punctuation, or starts with a bold label.
  Running-text mentions such as "Fig. 3 shows…" are rejected.
* **Clip.** The clip is seeded with drawings or images that lie within 40 pt above
  the caption (then below, as a fallback). It then grows through vertically adjacent
  graphics with gaps under 14 pt. Growth stops at paragraphs of running text and at
  other captions. Nearby label text is absorbed, and the clip is padded by 4 pt.
  Text-only figures (e.g. prompt boxes, unframed algorithms) fall back to the band
  between the preceding paragraph and the caption.
* **Statistics:** path item counts, horizontal and vertical ticks (an axis needs
  both), arrowheads, grid detection, vector and rendered-pixel colour counts,
  whitespace fraction, words per square inch, effective raster dpi.
* **Type:** the classifier combines caption-keyword scores with statistic rules. Its
  vocabulary covers agent-paper captions such as "attack success rate", "propagation",
  "topology", "message flow" and "defense"; output types are `message-flow`,
  `agent-architecture`, `state-machine`, `topology-graph`, `plot-*`,
  `heatmap-matrix`, `table-like`, `pseudocode-box` and `other`. It still relies on
  heuristics, so check the type filter rather than trusting it.
* **Quality:** the score starts at 50. Vector content: +20. Rasters: from +15 down to
  −15, depending on dpi. Colours: +10 for 2–7 colours, −10 for more than 14.
  Whitespace: +10 for 45–90%. Very small crops and very dense text are penalised.
  Screenshot-heavy GUI-agent figures score low on purpose; judge them by hand.
* **Robustness:** each PDF runs in a forked process with a timeout, and per-page
  exceptions are recorded without stopping the run. `--selftest` builds a synthetic
  PDF and checks the full pipeline.

## Known limitations
* Classification is heuristic rather than a scientific labeler; plots whose text was
  converted to outlines and raster-only figures rely heavily on caption keywords.
* Prompt/transcript boxes are often classified as `pseudocode-box` or `other`.
* Multi-panel figures that sit side by side with separate captions can merge into
  one crop.
* Two-column layouts (ACL, ACM, IEEE, USENIX) sometimes pull in the neighbouring
  column's graphics. Check the crops.
