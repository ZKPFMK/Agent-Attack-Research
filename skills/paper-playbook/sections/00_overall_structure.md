# 00 Overall structure, page budget, layout rules

## Default skeleton (attack paper)

Shares are of the body; scale to the venue's limit. Security venues (two-column,
~13 pp. body in recent years) and ML/NLP venues (~8–9 pp. main text in recent years)
differ a lot; always check the current CFP for the limit and for what counts toward
it (see `skills/venue-calibration`).

| § | title | share of body | job |
|---|---|---|---|
| — | Abstract | page 1 | gap → our attack → results (ASR with scope) + defenses + disclosure |
| 1 | Introduction | ~12% | motivating attack example (Figure 1), gap, challenges, our attack, contributions |
| 1.x | Contributions | (inside §1) | lead-in + 3–4 ordered bullets |
| 2 | Background & related work | ~10% | agent/MAS model, frameworks attacked, related attacks by surface, comparison table |
| 3 | Threat model | ~6% | goal, knowledge, capabilities, access point, victims, success criterion, out of scope |
| 4 | Attack design | ~22% | overview figure; key insights; components; algorithm; payload construction (redacted); cost |
| 5 | Evaluation | ~30% | setup, metrics (ASR/utility/stealth/cost, n, CI), main results, ablations, transferability, case study |
| 6 | Defenses | ~8% | existing defenses incl. adaptive attacker; possible mitigations |
| 7 | Discussion & limitations | ~4% | scope of validity, failure cases, what is not claimed |
| 8 | Ethics considerations & responsible disclosure | ~3% (or the venue's mandated section) | harm, containment, disclosure, release policy |
| 9 | Conclusion | ≤ 0.3 page | two to three sentences |
| A– | Appendix | per CFP | prompts (redacted), judge prompt + validation, per-model tables, cost details |

Variants:

- **Security venues (CCS/S&P/USENIX/NDSS):** threat model is an early, standalone
  section; related work often sits near the end; an ethics section (and for some, an
  open-science section) is expected; evaluation must show real-framework realism
  and an adaptive-defense discussion.
- **ML/NLP venues (ACL/EMNLP/NAACL via ARR, NeurIPS, ICLR, ICML, COLM):** related work
  usually after the introduction; a *Limitations* section (ARR: mandatory, outside the
  page limit in recent cycles) and an *Ethics statement*; a responsible-NLP or
  NeurIPS checklist; more emphasis on many models, benchmarks and ablations.
- **Benchmark/measurement papers:** replace "Attack design" with "Benchmark
  construction" and keep threat model + judge validation; see the
  `benchmark-paper-template` skill if installed.
- **SoK papers:** taxonomy + systematised comparison table replace §4–5.

## Page discipline

Legal ways to save space, in order of preference:

1. Tighten floats: algorithms `\footnotesize`, tables `\small`/`\scriptsize` with
   `\arraystretch` 0.88–0.92, `\tabcolsep` 2.5–3pt.
2. Move per-model breakdowns, full prompts and judge validation details to the
   appendix; keep the summary row and the CI in the body.
3. Merge Figure 1 and the attack-overview figure if they show the same pipeline.
4. Remove footnote URLs duplicated elsewhere.
5. Only then cut sentences — cut adjectives before content, never cut a number's
   scope sentence (models, n, judge).

**Forbidden (desk-reject risk):** changing margins (`geometry`), font size, line
spacing, removing or altering the venue style's anonymity/line numbers, putting
required sections (Limitations at ARR) inside the page limit when they must be
after it or vice versa. Overprinting after a negative `\vspace` before a float is
a classic trap; scan with the camera-ready overlap checker.

## Terminology and naming freeze (before writing, grep after writing)

Keep `paper/NOTATION.md` (term/symbol, meaning, first defined in §):

- One name per role: *attacker*, *victim agent*, *benign agent*, *user*,
  *orchestrator*, *tool*, *environment*. Do not alternate "malicious agent" /
  "adversarial agent" / "compromised agent" unless they denote different capabilities.
- One name per metric: **ASR** (attack success rate, defined by the success
  criterion of §3), **utility** (benign task success under attack / without attack),
  **stealth** (e.g. detection rate by a named detector, or human/judge flag rate),
  **cost** (tokens, API calls, wall-clock, $ at a stated price date).
- One name for the attack (one word or acronym) used in title, headings, figure
  captions, contributions and tables.
- Model names exactly as the provider's snapshot id at first use (e.g. a dated API
  snapshot or an open-weight checkpoint revision), short name afterwards; the mapping
  table goes to the setup section.

## Global style rules

- Avoid em/en dashes as sentence punctuation; use commas, colons or separate
  sentences. (Ranges like `2--3` are fine.)
- Statement-style paragraph headings ("A single relay suffices to flip the chain's
  verdict."), not "Why X is needed".
- Never write "the model believes/wants"; write what was measured ("the victim
  outputs the false claim in 41% [ill.] of runs").
- Harmful content: describe the *category* and *mechanism*; print payloads only in
  redacted form; never print working exploits for unpatched deployed systems.
- The first pages (title, abstract, introduction with Figure 1) must summarise
  attack, threat model and headline result without the body.

## Checklist

- [ ] Section shares roughly match the budget; the required sections (limitations,
      ethics, checklist) are placed as the CFP requires.
- [ ] No layout-changing package; venue style options correct (anonymous/review).
- [ ] Terminology table frozen; variant names grep to zero.
- [ ] Attack name identical in title, headings, captions, contributions, tables.
