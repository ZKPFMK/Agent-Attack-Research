---
name: paper-playbook
description: Use when drafting or restructuring a paper on attacks against LLM agents or LLM multi-agent systems (security venues such as CCS/S&P/USENIX/NDSS or ML/NLP venues such as ACL/EMNLP/NeurIPS/ICLR). Gives the overall skeleton, page budget, and the rhetorical moves of every section from title to appendix (threat model, attack design, evaluation, defenses, ethics), with good/bad toy examples.
---

# Paper Playbook — structure and rhetorical moves for agent-attack papers

The playbook fixes the **form** of a paper; the content is always rewritten for the
new paper. Templates here are structures, not wording to copy.

## Six principles (read first)

1. **Every number has one source.** Abstract, intro, body, tables and appendix quote
   the same value from the same row of `EVIDENCE.md`. No number enters the paper
   without an EVIDENCE row (SPEC §4); every rate carries n and a 95% CI. Numbers are
   generated or grep-checked (`\evid{E<n>}` tags), never retyped from memory.
2. **Write falsifiable claims first, then try to break them.** Each contribution is
   first written as one sentence in `CLAIMS.md`; the `falsifier` and `reviewer-sim`
   agents attack it (judge artefacts, base-model jailbreak confound, adaptive
   defenses, novelty vs the KB) before the prose is polished. Prose cites the row with
   `\claimref{C<n>}`; only `survived`/`weakened` rows may be cited.
3. **The threat model is the contract.** Every attack result is valid only inside the
   threat model of `THREAT-MODEL.md`. The paper never claims more access, less
   knowledge or broader victims than were actually evaluated.
4. **Form is fixed, wording is new.** Reuse the skeleton and the moves, never the
   sentences of a previous paper.
5. **The body carries the weight; the appendix only supplements.** No claim in the
   body may depend solely on an appendix (judge validation *summary* and the key
   ablation stay in the body).
6. **Harm-aware writing.** Working payloads against deployed products are not
   printed; harmful strings are redacted consistently (`ETHICS.md` release policy, the
   `ethics-disclosure` skill). Disclosure status is stated, not implied.

## Section files

| file | section |
|---|---|
| `sections/00_overall_structure.md` | skeleton, page budget per venue family, layout hard rules, terminology freeze |
| `sections/01_title.md` | title patterns and anti-patterns |
| `sections/02_abstract.md` | three-part paradigm (gap → attack → results/defenses/disclosure) |
| `sections/03_introduction.md` | motivating attack example (Figure 1) → gap → challenges → our attack |
| `sections/04_contributions.md` | lead-in + ordered bullets; wording rules |
| `sections/05_technique_overview.md` | key insights behind the attack, one per challenge |
| `sections/06_related_work.md` | organise by attack surface/axis, comparison table with an "Ours" row |
| `sections/07_background.md` | agent/MAS model, notation, the frameworks and protocols attacked |
| `sections/08_threat_model.md` | attacker goal, knowledge, capabilities, access point, victims, success criterion, out of scope |
| `sections/09_attack_design.md` | attack pipeline, components, algorithm, payload construction (redacted), cost |
| `sections/10_evaluation.md` | setup (victims/models/frameworks/benchmarks), metrics with n and CIs, results, ablations, transferability |
| `sections/11_defenses.md` | existing defenses, adaptive attacker, possible mitigations |
| `sections/12_discussion_ethics.md` | limitations, broader impact, ethics considerations & responsible disclosure |
| `sections/13_conclusion.md` | two-to-three sentence conclusion |
| `sections/14_appendix.md` | prompts (harmful parts redacted), judge prompt + validation, extra results |
| `examples/toy_abstracts.md` | good/bad abstracts for three toy papers |
| `examples/toy_intro_and_contributions.md` | toy Figure-1 example, intro opening + contribution list, good vs bad |
| `examples/toy_overview_and_related.md` | toy insights, related-work table, threat-model box |

Toy papers used throughout (all systems are **synthetic** and every number is
**invented and illustrative**, marked `[ill.]`):

- **T1 (MAS propagation):** "RelayRumor" — a toy rumor-relay attack on a 5-agent
  chain: one compromised relay agent rewrites a true claim into a plausible false one
  and measures whether the last agent adopts it.
- **T2 (tool injection):** a toy tool-description poisoning attack on a sandboxed
  email-assistant agent with a mock tool registry.
- **T3 (memory poisoning):** a toy query-only memory-injection attack on a RAG agent
  with a synthetic knowledge base.

## Workflow (used by the `writer` agent)

1. Freeze terminology and the attack's one-word name (`00_overall_structure.md`);
   copy the threat model from `THREAT-MODEL.md`.
2. Write `CLAIMS.md` rows for each contribution; get falsifier verdicts.
3. Draft in this order: threat model → contributions → attack design → evaluation →
   defenses → overview → related work → introduction (with Figure 1) → ethics →
   abstract → title → conclusion. (The abstract is written last because it
   summarises the other sections.)
4. After each section, run the section's checklist (end of each file).
5. Hand to `reviewer-sim`; iterate; hand to `submission-rebuttal`.

## Related skills

- [abstract-craft](../abstract-craft/SKILL.md), [technique-overview](../technique-overview/SKILL.md),
  [related-work-writing](../related-work-writing/SKILL.md),
  [experiments-writing](../experiments-writing/SKILL.md),
  [venue-calibration](../venue-calibration/SKILL.md), [polish-writing](../polish-writing/SKILL.md)
- Upstream: `threat-model`, `ethics-disclosure`, `eval-protocol`, `judge-validation`,
  `adaptive-eval` (their outputs are what this playbook turns into prose).
- LaTeX skeleton: `templates/paper/`.
