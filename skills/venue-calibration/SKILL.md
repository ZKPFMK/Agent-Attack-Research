---
name: venue-calibration
description: Choose and calibrate a target venue for an LLM-agent attack paper, then adapt claims, evaluation, ethics and artifact to its current rules. Use at P0, before mock review and before submission.
---
# venue-calibration

This is orientation only. Always read the current CFP, author kit, ethics/responsible-research policy and artifact
policy before committing to a format or deadline. Page limits, rebuttals and review workflows change.

## Venue families

| family | examples | reviewers usually test |
|---|---|---|
| security | ACM CCS, IEEE S&P, USENIX Security, NDSS, PoPETs | reachable threat model, real security consequence, adaptive defenses, responsible disclosure, reproducibility |
| ML/NLP | ACL/EMNLP/NAACL (often ARR), NeurIPS, ICLR, ICML, COLM, AAAI | mechanism and novelty, model/task coverage, metrics and judge validity, ablations, limitations, responsible NLP |
| systems/tooling | relevant systems or HCI venue | deployment setting, overhead, failure boundaries, user/agent impact and artifact |

Do not assume that a security venue accepts an attack merely because ASR is high, or that an ML venue accepts a
benchmark without a mechanism and a defensible research question.

## Procedure

1. Record venue, track, current CFP URL/date, page limit, anonymity, supplementary/artifact rules, ethics form,
   disclosure policy and whether preprints are allowed in STATE.md and SUBMISSION.md.
2. Calibrate the claim: security papers need a reachable attacker and consequence; ML/NLP papers need a mechanism,
   controls, model/task evidence and limitations. Put the largest evidence in the body.
3. Check the target's expected baselines: public attack suites, defense baselines, local model snapshots and
   framework versions. Do not compare an API model's ASR to an open model's ASR without explaining the setting.
4. Include a threat-model section, judge validation, benign utility, adaptive defense evaluation and ethics/release
   decision regardless of venue; omit only with a logged, venue-specific reason.
5. Run a venue-calibrated mock review with security skeptic, ML/NLP generalist, implementer, ethics reviewer and
   desk-reject auditor. Route each finding to an owner.
6. Re-check page counts and current forms at P8. The venue's current instructions win over this skill.

## Common rejection reasons

Circular access, success defined only by an LLM judge, no naive injection/no-attack control, one model or one
framework, missing adaptive defense, no benign utility, unverifiable citations, unredacted harmful artifacts,
overclaiming "first/universal/robust", or numbers without n/CI/raw logs.
