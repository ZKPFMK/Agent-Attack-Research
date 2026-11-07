# 03 Introduction — motivating example, gap, challenges, our attack

Target: about 1–1.5 pages (two-column) before the contributions. It must read as if
written by someone who knows both the agent ecosystem and the attack literature.

## Move sequence

```
[context]      One sentence on how agents / MAS are deployed for this task (tools, web,
               memory, delegation, debate); cite 2–3 representative systems/frameworks.
[trust]        The implicit trust assumption that makes the system work
               (agents trust tool outputs / peer messages / retrieved memory / UI).
[Figure 1]     A concrete, synthetic motivating example of the attack: the benign task,
               where the attacker sits, what the victim does wrong. Referenced here.
[prior]        Existing attacks on this surface in one sentence each group, citing the
               line at once (e.g. indirect prompt injection; MAS infection; memory
               poisoning).
[gap]          What they leave open, as a factual limitation: strong access (white-box,
               control of the orchestrator), single-agent scope, detectable payloads,
               blocked by a now-standard defense, not evaluated on real frameworks.
[question]     "Can an attacker with only <access> cause <effect> in <victim class>?"
[challenges]   2–3 numbered challenges that make the question hard (e.g. C1: benign
               agents re-verify claims; C2: payloads must survive paraphrase across hops;
               C3: no feedback from the final agent).
[our attack]   One paragraph: the attack, how each challenge is met by one insight
               (same numbering), and the threat-model qualifier.
[results]      2–3 sentences with the headline numbers (scope first), defenses, disclosure.
[contribs]     The contribution list (file 04).
```

## Figure 1 (motivating example)

- Synthetic and harmless in the paper; real-system screenshots only after disclosure
  and with identifying details removed.
- Shows benign flow and attacked flow side by side with **identical layout**; tint
  only the attacker-controlled element and the corrupted output.
- Caption's first sentence is the take-away ("A single relay that rewrites one claim
  makes the final agent report a false conclusion; no agent's prompt is modified.").
- Harmful payload text appears as `[REDACTED: instruction to exfiltrate contacts]`,
  not verbatim.

## Rules

- Citation density: 2–4 citations in the first paragraph; cite each prior-attack line
  as a block instead of one citation per sentence.
- Arguments for "existing attacks are insufficient" come in three strengths. Weak:
  "existing attacks are not effective" (never alone). Medium: "attack A succeeds but
  assumes access the attacker rarely has". Strong: "existing attacks target a surface
  that defense D now closes; the surface we use is not covered by D". Use strong.
- Realism first: say *who* the attacker is in deployment terms (a third-party tool
  provider, a web page author, one participant in an open agent network, a user who
  can write to shared memory).
- A "what this paper is not" sentence defuses scope objections ("We do not jailbreak
  the base model: every victim refuses the target behaviour when asked directly; see
  §5.x").
- Use the standard transitions (temporal, contrastive, causal); do not stack three
  connectives in a row.
- Own prior work is cited in the third person.

## Toy example (T1, RelayRumor; numbers illustrative)

> LLM agents are increasingly composed into pipelines in which each agent summarises
> and forwards the work of the previous one [..]. These pipelines rely on an implicit
> assumption: an agent treats a peer's message as a faithful report of evidence.
> Figure 1 shows what happens when one relay in a five-agent fact-checking chain
> rewrites a single claim [...]. Prior multi-agent attacks either compromise the
> orchestrator [..] or inject self-replicating prompts that keyword filters catch [..].
> Can one relay, with no access to other agents' prompts, flip the chain's verdict?
> This is hard because (C1) downstream agents re-check claims against their own
> evidence, and (C2) the rewrite must survive two further paraphrasing hops. [...]
> Across 4 [ill.] victim models, the final agent adopts the false claim in 41% [ill.]
> of runs [95% CI 35–47, n = 300], versus 9% [ill.] for direct injection.

## Checklist

- [ ] Figure 1 referenced in the first page; synthetic; redacted; identical layout.
- [ ] Gap stated as a factual limitation of named prior attacks.
- [ ] Challenges numbered; each answered by one insight with the same number.
- [ ] Threat-model qualifier and "not a base-model jailbreak" sentence present.
- [ ] Headline numbers with scope and CI, identical to the abstract.
