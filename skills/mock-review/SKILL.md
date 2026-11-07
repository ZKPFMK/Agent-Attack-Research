---
name: mock-review
description: Simulate venue-calibrated review of an LLM-agent attack paper with security, ML/NLP, implementation and ethics personas. Use before submission, after major revisions and before a rebuttal.
---
# mock-review

The review should try to break the paper. Reviewers read the paper plus CLAIMS.md, EVIDENCE.md, THREAT-MODEL.md,
ETHICS.md and LITERATURE.md; they do not accept a polished narrative as evidence.

## Personas

1. **Security expert skeptic:** Is the access point reachable? Is the attacker capability realistic? Does the result
   survive the strongest relevant defense and an adaptive attacker? What is the actual security consequence?
2. **ML/NLP generalist:** Can the mechanism be restated? Is the delta over the nearest KB/public work clear? Are
   tasks, model families, prompts, judges, n and uncertainty adequate? Are limitations honest?
3. **Implementer/reproducibility reviewer:** Can a clean checkout run with the stated snapshots, framework, seeds,
   cache and tools? Do raw transcripts support every table? Are costs and failures recorded?
4. **Ethics reviewer:** Are targets local/owned/sandboxed? Are payloads, credentials, personal data, model ToS and
   disclosure handled? Is the release decision justified?
5. **Desk-reject auditor:** title/abstract fit, anonymity, page limit, missing required sections, fabricated or
   unverified citations, undefined acronyms, unsupported numbers.

## Procedure

1. Freeze the version under review and the target venue/track. Do not review an outdated draft after claiming fixes.
2. Each persona writes CRITICAL/MAJOR/MINOR findings with file/section, concrete failure scenario, evidence or
   missing evidence, and an owner plus command to verify/fix.
3. Verify findings against raw logs and source files. Remove style preferences that do not affect correctness or
   acceptance; retain any plausible threat-model or metric failure until resolved.
4. Write REVIEWS.md with score/confidence, top three weaknesses, evidence ids, routed actions and a deadline.
5. A major finding is closed only by a changed claim, new logged experiment, verified citation, threat-model update,
   disclosure/release decision or explicit venue-based decision in DECISIONS.md.
6. Re-run `cra gate P8`, anonymisation and artifact smoke tests after fixes.

## Attack-paper checklist

- nearest KB/public attack and defense are explicitly compared;
- success is operational or judge validated (κ, precision/recall, fingerprint);
- naive, no-attack, benign utility and adaptive-defense controls exist;
- snapshots, seeds, temperature, framework/topology, n and CIs are visible;
- raw responses/cache are reproducible and redacted;
- no live target, credential, private research content or harmful release path is present;
- every surviving paper claim resolves to CLAIMS.md and every number to EVIDENCE.md.
