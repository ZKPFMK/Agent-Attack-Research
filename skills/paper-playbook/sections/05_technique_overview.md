# 05 Attack overview (key insights)

Either a subsection at the end of the introduction ("Our approach in a nutshell") or
the first subsection of the attack-design section, ≈ 0.5–1 page. Many reviewers read
only the introduction, this overview, the threat model and the main results table, so
it must let a reader restate *why the attack works* **without reading §4 in full**.
Full procedure: [technique-overview](../../technique-overview/SKILL.md).

## Structure

```
[recall]           One paragraph: the victim pipeline in the notation of §2 (agents, message
                   flow, tools, memory) and the attacker's single access point (from §3).
[prior routes]     One bold-headed paragraph per closest prior attack: what it injects,
                   where, what it assumes; ends with the factual reason it does not solve
                   our setting (blocked by a defense, needs stronger access, single hop).
[challenges]       "Achieving <effect> under <threat model> therefore requires answering:
                   (C1) ... (C2) ... (C3) ..." (same numbering as the introduction).
[figure]           Attack-pipeline overview: benign flow vs attacked flow, attacker element
                   tinted, each insight labelled where it acts. Caption = take-away.
[Insight 1]        Bold heading = a complete declarative sentence ("Agents defer to peers
                   that cite evidence they cannot check."). Observation → evidence from a
                   pilot (EVIDENCE row) → how the attack uses it.
[Insight 2..k]     Same format, one per challenge.
[putting together] The attack as one short algorithm sketch, literally consistent with §4.
```

## Rules

- Insights must be **measured observations or mechanistic arguments**, not slogans:
  each insight cites a pilot measurement (`\evid{E<n>}`) or a controlled ablation.
- Insight headings are sentences, not noun phrases. Bad: "Evidence anchoring." Good:
  "Agents accept a claim when it is attached to a true but irrelevant citation."
- Describe prior attacks by mechanism and access, at the level of the pipeline; do not
  repeat the related-work comparison.
- Do not anthropomorphise ("the agent wants"); describe inputs, outputs and measured
  rates.
- No payload text; describe the payload's *structure* (e.g. "a true citation, a
  hedged rewrite, a request to forward").
- Late in the process, fix only obvious errors in the overview; do not restyle it.

## Toy skeleton (T1, RelayRumor; illustrative)

> **Recall.** Agents a_1..a_5 form a chain; a_i receives m_{i-1}, consults its own
> evidence, and forwards m_i. The attacker controls a_2's output only (§3).
> **Prior routes.** Self-replicating prompts [..] require every hop to execute an
> instruction and are flagged by instruction detectors; orchestrator compromise [..]
> assumes control of the planner.
> **Challenges.** (C1) a_3..a_5 re-check claims; (C2) the rewrite must survive two
> paraphrasing hops.
> **Insight 1: Downstream agents rarely re-check a claim that cites a true source.**
> In a pilot, adding a true but irrelevant citation reduced re-check rate from 62% to
> 18% [ill.] (E3).
> **Insight 2: Hedged claims survive paraphrase better than assertive ones.** ...

## Checklist

- [ ] Each closest prior attack recalled with its access assumption and its gap.
- [ ] Challenges numbered as in §1; each insight answers one.
- [ ] Insight headings are declarative sentences backed by a pilot or ablation row.
- [ ] Figure caption states the take-away; attacker element is the only tinted part.
- [ ] Algorithm sketch consistent with §4.
