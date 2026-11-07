# Local figure gallery -- index template

The harvested gallery (`figures/gallery/` by default, or any `--out` directory)
is **never committed**: the images belong to their authors.  Commit only notes
written in your own words, e.g. in `figures/PATTERNS.md` or in a project's
`paper/figs/NOTES.md`, using this template.

| # | pattern (see PATTERNS.md) | source (public paper id, fig.) | what works | what to avoid | template |
|---|---|---|---|---|---|
| 1 | A1 effectiveness bars | e.g. KB id / ACL / OpenReview Fig. 3 | controls, n and CI are visible | a bare ASR bar | p01 |

Regenerate the gallery:

    python3 figures/harvester/harvest.py CORPUS_DIR --out /tmp/agent_attack_figures
    python3 figures/harvester/gallery.py /tmp/agent_attack_figures   # open index.html
