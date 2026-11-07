---
name: abstract-craft
description: Use when writing or tightening the abstract of an agent-attack paper (and its plain-text submission-form twin). Applies the three-part paradigm (gap in prior attacks, our attack under its threat model, results with scope/CI plus defenses and disclosure) with a sentence-level function table and an overclaim filter.
---

# Abstract craft

## Inputs

`CLAIMS.md` (survived/weakened claims), `EVIDENCE.md` (numbers with n and CI),
`THREAT-MODEL.md`, `ETHICS.md` (disclosure log), the contribution list
(`paper/sections/intro.tex`), target venue (for length norms, see
[venue-calibration](../venue-calibration/SKILL.md)).

## Procedure

1. **Write a one-line attack statement**: "An attacker who controls <access point>
   can make <victim> do <effect>, without <stronger access>." If this sentence cannot
   be written, the abstract is not ready; go back to the threat model.
2. **Fill the sentence-function table** below in `paper/ABSTRACT_PLAN.md` (Chinese or
   English bullet map is fine; discuss it with the human author before prose).
3. **Draft three blocks** (see `paper-playbook/sections/02_abstract.md`).
4. **Overclaim filter** (automatic pass, then manual):
   - forbidden: novel, groundbreaking, universal/all/any (unless a transfer table
     backs it), undetectable/stealthy (without a named detector and rate),
     real-world (for a sandbox), bypasses all defenses, significantly (without a
     number and test), first (unless `KB-POSITION.md` + a recent `paper-search` sweep
     support it; even then "to our knowledge, the first ... under <threat model>").
   - every number → EVIDENCE row id in a LaTeX comment `% EV:E12` or `\evid{E12}`;
     every rate has n and CI in the body.
   - every scope noun ("4 victim models", "three topologies", "120 tasks") → matches
     the setup table.
   - no vendor/product named as a target unless the disclosure log allows it.
5. **Consistency pass**: abstract ↔ contributions ↔ conclusion use the same numbers,
   the same order and the same attack name.
6. **Length**: ML/NLP venues: usually one paragraph, ~150–250 words (OpenReview/ARR
   forms may cap characters). Security venues: often ≤ ~250 words in the form;
   two to three short paragraphs are acceptable in the PDF. Check the CFP.
7. **Plain-text twin** `paper/abstract_plain.txt` for the submission form.

## Sentence-function table (6–10 sentences)

| # | function | notes |
|---|---|---|
| S1 | deployment context + implicit trust assumption | no citation needed |
| S2 | existing attacks, grouped by surface/access, venue'year | 1–2 representatives per group |
| S3 | gap | "However, ... requires <strong access> / has not been measured in MAS." |
| S4 | our attack: attacker, access point, effect | "We present X, in which ..." |
| S5–S6 | key mechanisms, one each | answer the challenges of the intro |
| S7 | knowledge/access qualifier | black-box, no weights, query budget |
| S8 | scope → headline ASR [CI] vs strongest baseline attack → utility/stealth | judge or programmatic check named |
| S9 | defenses incl. adaptive result | which hold, which fail |
| S10 | disclosure / release | only what `ETHICS.md` logs |

## Upgrading weak sentences

| weak | strong |
|---|---|
| "Our attack is highly effective." | "Across 4 victim models (n = 300 each), the final agent adopts the false claim in 41% of runs [CI 35–47], versus 9% for direct injection." [ill.] |
| "Our attack is stealthy." | "A perplexity detector and an instruction classifier flag 2% and 3% of attack messages at 1% FPR." [ill.] |
| "Existing defenses fail." | "Spotlighting and a monitor agent reduce ASR by at most 5 points; per-agent evidence retrieval reduces it to 6%." [ill.] |
| "We responsibly disclosed." | "We reported the issue to the framework maintainers on <date>; a fix is merged." (only if logged) |

## Headline-range hygiene

- A headline is a pooled rate with CI or a range across victims, never the best cell.
- Never mix models below a capability floor (e.g. that fail the benign task) into
  the ASR range; report them separately.
- If a baseline attack's number is reproduced rather than quoted, the abstract uses
  the reproduced number and the paper reports both.
- Results from different model snapshots are not pooled.

## Output

`paper/sections/abstract.tex`, `paper/abstract_plain.txt`, and a short diff note in
`paper/CHANGELOG.md`.

See toy examples: `skills/paper-playbook/examples/toy_abstracts.md`.
