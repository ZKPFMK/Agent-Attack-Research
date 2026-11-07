# 01 Title

The title is the first positioning statement. Decide it together with the abstract's
second paragraph and the threat model: all three must name the same attack, surface
and victim class.

## Patterns that work

| pattern | shape | toy example (invented) |
|---|---|---|
| Name + mechanism | "<Name>: <mechanism> against <victim class>" | "RelayRumor: Steering Multi-Agent Chains with a Single Rewriting Relay" |
| Surface + effect | "<Effect> via <surface> in <system>" | "Hijacking Tool Selection via Poisoned Tool Descriptions in LLM Agents" |
| Phenomenon as claim | "<System> <verb> <phenomenon>" | "Benign Agents Amplify Planted Errors in Sequential Pipelines" |
| Question (measurement only) | "Do/Can <agents> <property>?" | "Can a Single Agent Corrupt a Debate?" (only if the paper measures, not attacks) |
| Benchmark | "<Name>: A Benchmark for <attack class> in <systems>" | "ToyRelayBench: A Benchmark for Message Tampering in Agent Pipelines" |

## Rules

1. **Name the mechanism and the surface, not the model.** "Attacking GPT-x" ages in
   months and reads as a jailbreak report; "via poisoned tool descriptions" names a
   reusable attack surface.
2. **Fit on two lines in the venue's title font.** If one word spills, rephrase.
3. **Scope words must be earned.** "Universal", "transferable", "black-box",
   "stealthy", "practical" each require a dedicated experiment (cross-model transfer,
   no gradient/weights access, a detector evaluation, a real framework or sandboxed
   deployment). Otherwise reviewers attack the word.
4. **Avoid:** "novel", "towards", "breaking all", alarmist verbs ("destroy"), real
   product or company names as targets unless disclosure is complete and the venue's
   ethics guidance allows it, acronyms unknown to a general security/NLP reader,
   titles longer than ~15 words.
5. A playful name is fine if it is short, searchable and not already used by a prior
   attack (check the KB and `paper-search`).

## Process

Produce 5–8 candidates in `paper/TITLES.md`, each with a one-line rationale and the
risk a reviewer might see ("'universal' not backed by transfer table"). The human
author chooses.

## Bad → better (toy)

- Bad: "A Novel and Highly Effective Universal Attack That Breaks All LLM-Based
  Multi-Agent Systems" (no mechanism, "universal" unearned, "all").
- Better: "RelayRumor: Steering Multi-Agent Chains with a Single Rewriting Relay".
