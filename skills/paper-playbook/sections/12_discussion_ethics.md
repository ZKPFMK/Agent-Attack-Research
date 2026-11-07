# 12 Discussion, limitations, ethics and responsible disclosure

Two parts. Many venues mandate them in a specific form and place (ARR: a
"Limitations" section; NeurIPS/ICLR/ICML: ethics/impact statements or checklist items;
USENIX Security and other security venues: ethics considerations and, in recent
years, open-science sections). Quote the CFP rule into `SUBMISSION.md` and follow it.

## A. Discussion and limitations

```
[scope]          What the results establish and under which threat model, models, frameworks
                 and dates (API models drift; results are for the stated snapshots).
[failure cases]  Where the attack does not work (model, topology, defense) and the measured
                 reason if known.
[assumptions]    The assumption that, if false, invalidates the attack (from §3 realism).
[judge/metric]   Residual measurement risk: judge error rate, synthetic tasks vs real use.
[generality]     What would need to change for other frameworks/surfaces; marked as
                 conjecture unless measured.
```

- Limitations are specific and measured where possible ("ASR drops to 6% [ill.] when
  the final agent retrieves its own evidence"), not ritual ("more models could be
  tested").
- Nothing here contradicts the abstract; if it does, the abstract is wrong.

## B. Ethics considerations and responsible disclosure

Source of truth: `ETHICS.md` (harm assessment, containment, release policy,
disclosure log), produced with the `ethics-disclosure` skill.

```
[harm]           Who could be harmed if the attack were used, and how severe.
[containment]    All experiments ran on systems we own or sandboxed benchmarks; no live
                 third-party services, no real users/accounts; synthetic personal data.
[human subjects] If humans labelled data or judged stealth: IRB/ethics-board status, pay,
                 consent, exposure to harmful content and how it was limited.
[disclosure]     Vendors/maintainers contacted, date, response, embargo; only claims that
                 are logged in ETHICS.md ("we disclosed to X on <date>; X acknowledged").
[release]        What is released (code, harness, benign templates) and what is withheld
                 or gated (working payloads, optimised triggers) and why.
[benefit]        Why publishing helps defenders (concrete defense insight from §6).
```

- Never claim disclosure that has not happened; "we will disclose" is a promise the
  camera-ready must keep.
- Do not name a vendor as vulnerable before its disclosure window ends unless the
  vendor agreed.
- Use the venue's ethics wording (e.g. "Ethics Considerations") and length rules.

## Checklist

- [ ] Limitations specific, measured where possible, consistent with the abstract.
- [ ] Containment statement true for every experiment (checked against `ETHICS.md`).
- [ ] Disclosure statement matches the disclosure log; dates present.
- [ ] Release/withholding policy stated; artifact gating consistent with it.
- [ ] Section names/placement follow the CFP.
