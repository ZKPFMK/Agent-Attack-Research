# 09 Attack design

## Shape of the attack section

```
[opening]      One paragraph: the attack in one sentence, its stages, and pointer to the
               overview figure.
[overview fig] Attack pipeline: benign flow vs attacked flow, identical layout; numbered
               stages that match the subsection order.
[stage k]      One subsection per stage/component:
                 goal of the stage → mechanism → design choice and the evidence for it
                 (pilot/ablation EVIDENCE row) → what the attacker needs (link to §3).
[algorithm]    Algorithm float: name — one-line purpose; Input/Output with types
               (victim pipeline, access point, budget); comments; then walk through key
               lines in prose.
[payload]      Structure of the adversarial content (template slots, optimisation target),
               shown with harmful parts redacted; full templates in the appendix, also
               redacted where they would be directly reusable against deployed systems.
[cost]         Attacker cost in one currency used everywhere (queries, tokens, $ at a
               stated price date, wall-clock).
[variants]     Black-box / gray-box / adaptive variants, each clearly labelled.
[remarks]      What is NOT claimed; when the attack does not apply.
```

## Rules distilled from review rounds

- **Every design choice needs evidence**, not "we chose": "we compared three rewrite
  strategies on the pilot set (Table 9) and keep the one with highest ASR at equal
  stealth".
- **Optimisation is honest about its oracle.** If the attack optimises against a
  surrogate model or a judge, say which, and evaluate on held-out victims and an
  independent success check; otherwise reviewers suspect overfitting to the judge.
- **No hidden human in the loop.** If prompts were hand-crafted or iterated
  manually, say how many iterations, on which data, and that the evaluation set was
  held out.
- **Same capability set as §3.** An algorithm line that reads another agent's message
  or the system prompt contradicts a black-box threat model.
- **Generality by family, not instance.** Present the attack as a template with slots
  (`<carrier>`, `<trigger>`, `<goal>`) plus the instantiation used; this defends
  against "a single prompt that works on one model".
- **Determinism and seeds.** State temperature, sampling, number of attack attempts
  per task, and whether success means "any of k attempts" (report k).
- **Redaction rule.** Payloads that would work verbatim against a deployed, unpatched
  system are not printed; show structure with `[REDACTED: <category>]`, and describe
  release gating (§8, `ethics-disclosure`).

## Checklist

- [ ] Overview figure stages = subsection order = algorithm lines.
- [ ] Each design choice backed by a pilot/ablation EVIDENCE row.
- [ ] Algorithm uses only capabilities from §3; optimisation oracle named.
- [ ] Attempts per task (k), temperature and seeds stated.
- [ ] Payloads redacted per `ETHICS.md`; cost in one currency.
