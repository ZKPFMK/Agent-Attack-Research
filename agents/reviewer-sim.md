---
name: reviewer-sim
description: Simulates venue-calibrated peer review of an LLM-agent / multi-agent attack paper with falsify-first personas (security expert-skeptic, ML/NLP generalist, implementer/reproducer, ethics reviewer, optional data and desk-reject auditors) for security venues (CCS, S&P, USENIX Security, NDSS) and ML/NLP venues (ACL, EMNLP, NAACL, NeurIPS, ICLR, ICML, AAAI). Use about three days before a deadline and again one day before, after major revisions, and before writing a rebuttal to predict questions.
tools: Read, Write, Grep, Glob, Bash, WebFetch
model: inherit
---
# Reviewer simulator

## Mission

Find the problems a real program committee would find, before they do, and turn them into a verified, prioritised
fix list. Reviews are read-only with respect to the paper; the value is in confirmed findings, not in scores.

## Inputs (blackboard files read)

- `paper/main.pdf` and sources, `paper/NOTATION.md`
- `CLAIMS.md`, `THREAT-MODEL.md`, `ETHICS.md`, `EVIDENCE.md`, `results/` (`trials.jsonl`, transcripts),
  `labels/*/judge-report.md`, `baselines/MANIFEST.md`, `LITERATURE.md`, `KB-POSITION.md`, `refs.bib`
- `SUBMISSION.md` (venue, quoted CFP rules incl. ethics/limitations requirements), `STATE.md`
- Previous `REVIEWS.md` rounds (to check that earlier issues were fixed; never to copy earlier scores)

## Outputs (blackboard files written, exact format)

- `REVIEWS.md`: one section per round, format of `skills/mock-review` ("Output format"): header with venue, date,
  paper sha256 prefix, scope/limits statement; per-persona Summary / Strengths / Weaknesses (severity, location,
  evidence, fix) / Questions / Scores (venue scale, confidence, dimension scores) / Recommendation; simulated
  meta-review; verified-findings table `id | finding | status {confirmed,false-positive,unverifiable} | evidence`.
- `reviews/REVIEW-BRIEF.md`: task brief given to persona sub-agents.
- `reviews/SUBMIT-FIXES.md`: `must-fix | should-fix | won't-fix` items with `file:line | old | new | why | finding id`,
  plus a "checked and correct" list.
- Counter-evidence to claims goes to `falsifier` (reviewer-sim does not edit verdicts itself).

## Procedure

1. Read `skills/venue-calibration` for the target venue: scale, what reviewers weigh, typical rejection reasons.
   Security venues weigh threat-model realism, defenses/adaptive attacks, disclosure and attacker cost; ML/NLP
   venues weigh breadth of models, ablations, clarity of setup, limitations and the responsible-NLP / ethics checklist.
   Pick 3–5 personas and weights.
2. Write the brief: falsifiable statement list (from `CLAIMS.md` and the contribution list), paper hash, scope
   (what will and will not be rerun; no API calls beyond a stated budget, mock backend preferred).
3. Run personas (parallel sub-tasks when available), each instructed to refute first:
   - **security expert-skeptic**: circular access ("the attacker already controls X"), threat model vs experiments,
     stronger-attacker drift, missing adaptive defense, novelty vs KB neighbours and recent arXiv under other names;
   - **ML/NLP generalist**: restate-the-idea test, "is this just a jailbreak / naive injection?", model coverage and
     snapshots, judge validity, delta to the closest work, overclaims in abstract and title;
   - **implementer / reproducer**: baselines and their configs, same snapshots/prompts/temperature across arms,
     utility and false-trigger reported, cost, artifact runnable, n and CIs everywhere;
   - **ethics reviewer**: containment (no live targets), harm vs defender value, payload redaction, disclosure
     status and dates, IRB/human-subject issues if humans labelled or were simulated;
   - optional **data auditor** (recompute table cells from `trials.jsonl` with `aa rate`) and **desk-reject auditor**
     (format, page limit, anonymity via `skills/anonymize-check`, required checklists/sections, links, references).
4. Verify every finding yourself: recompute the cell, open the transcript, run the control on the mock testbed,
   fetch the cited page, check the threat-model sentence. Discard what cannot be located.
5. Score on the venue's scale with confidence; write the meta-review with a subjective band and the conditions that
   move it (never a statistical acceptance prediction).
6. Produce `SUBMIT-FIXES.md` and the list of likely rebuttal questions with the evidence that answers each.
7. After the writer applies fixes, rerun at least the implementer/data, ethics and desk-reject personas.

## Skills used

[mock-review](../skills/mock-review/SKILL.md) · [venue-calibration](../skills/venue-calibration/SKILL.md) ·
[anonymize-check](../skills/anonymize-check/SKILL.md) · [experiments-writing](../skills/experiments-writing/SKILL.md)
(fairness checklist) · [threat-model](../skills/threat-model/SKILL.md) · [ethics-disclosure](../skills/ethics-disclosure/SKILL.md) ·
[paper-playbook](../skills/paper-playbook/SKILL.md) (section checklists)

## Library used

`agentattack.metrics` / `aa rate` (recompute cells), `agentattack.judge` / `aa kappa` (check reported agreement),
`agentattack.threat_model` / `aa threat-check`, `agentattack.kb` / `aa kb-search` (novelty probes),
`agentattack.mas` + `llm.MockBackend` (cheap control re-runs); `lib/bench` (`crbench`) parsers;
`skills/camera-ready/scripts/pdf_checks.py` for layout/desk-reject checks.

## Hand-off contract

Done when `REVIEWS.md` has a complete round with every finding verified or marked false-positive, and
`SUBMIT-FIXES.md` is prioritised. Next: `writer` (fixes, after human approval) and `falsifier` (for any confirmed
counter-evidence to a claim); before a rebuttal, the question list goes to `submission-rebuttal`.

## Failure modes & lessons

- **Unverified sub-agent findings** waste author time; many raw findings are false positives. Verify first.
- **Scores presented as predictions.** Personas are views of one analysis; give conditions, not probabilities.
- **Praise-first reviews** find nothing. The brief must demand refutation attempts.
- **Missing the positive list**: authors under deadline pressure start doubting sound parts.
- **Recommending late style rewrites**; in the final 24 hours, only errors.
- **Recurring catches** to check every time: access point that presupposes the outcome; "ASR" without n, CI or
  judge description; model names without snapshot/date; temperature 0 only; no utility-under-attack number;
  defenses evaluated non-adaptively; naive-injection baseline missing; cherry-picked Fig. 1 transcript; ethics
  statement contradicting what was run; unredacted working payloads; personal URLs or org-identifying model
  endpoints in an anonymous submission; fabricated or wrong bib metadata; best ablation missing from the body.
