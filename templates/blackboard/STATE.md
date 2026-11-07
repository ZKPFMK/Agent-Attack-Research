# STATE — <project name>

> Owner: `pi-orchestrator`. Every agent reads this first; only the PI changes `phase`.

- **Phase:** P0 Scoping
- **kb:** <path to the knowledge base .md>
- **papers:** <path to the papers/ folder of the KB (optional)>
- **Target venue / deadline:** <venue> / <YYYY-MM-DD> (check current CFP, incl. ethics / open-science policy)
- **One-sentence thesis:** <attack X on system class Y achieves Z (metric) vs baseline B, under threat model TM-1>
- **API / compute budget:** <models, tokens or $, GPUs>
- **Last updated:** <YYYY-MM-DD> by <agent>

## Gate P0 (scoping)
<!-- `cra gate P0` / gate_check.py read the section whose heading contains "Gate P<k>".
     When the phase advances, add "## Gate P<k+1>" (keep old gate sections as the log).
     Waive an item only with a DECISIONS id: "- [~] ... WAIVED: <reason> (DECISIONS D-<n>)". -->
- [ ] thesis is one falsifiable sentence: target system class, attack goal, success metric and the baseline value
- [ ] venue + deadline set; current CFP read (incl. ethics / open-science policy)
- [ ] knowledge base path recorded (kb: line) and in-scope / out-of-scope list written
- [ ] compute + API budget set (models, tokens, $)
- [ ] ethics pre-screen: only owned or sandboxed targets, no real users / live third-party services
- [ ] kill criteria and kill date set

## Errata and rolling updates   (later agents read this first)

## Active tasks
| task | owner agent | input | expected output | status |
|---|---|---|---|---|

## Blockers / questions for the human
- ...
