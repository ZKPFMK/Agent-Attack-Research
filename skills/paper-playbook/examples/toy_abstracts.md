# Toy abstracts — good vs bad

All three papers and systems are **invented and synthetic**. Every number is
**illustrative only** and marked `[ill.]`; none comes from a real measurement.
Citations like [A24] are placeholders.

---

## T1 — RelayRumor: a rumor-relay attack on a 5-agent chain (MAS propagation)

### Bad

> Multi-agent systems are a very important and novel technology. In this paper we
> propose a novel and powerful attack that breaks all multi-agent systems. Our
> attack achieves up to 100% [ill.] attack success rate on GPT and is
> undetectable. Code is at https://github.com/<real-username>/relayrumor.

What is wrong: no deployment context or gap; "novel", "all", "undetectable" with no
evidence; "up to 100%" is one cell, no n, no CI, no success criterion, no baseline;
a vendor named as target; the link de-anonymises the submission.

### Good

> LLM agents are increasingly chained so that each agent summarises and forwards the
> findings of the previous one, implicitly treating a peer's message as a faithful
> report of evidence. Existing multi-agent attacks either compromise the orchestrator
> [A24] (ACL'24) or spread self-replicating instructions [B25] that instruction
> detectors flag. Whether a single participant, without access to other agents'
> prompts, can steer a chain's conclusion has not been measured.
>
> We present RelayRumor, an attack in which one relay agent rewrites a true claim
> into a plausible false one, anchors it to a true but irrelevant source, and hedges
> it so that it survives paraphrasing by downstream agents. The attacker sees only
> its own input and controls only its own output.
>
> In a synthetic five-agent fact-checking chain with 4 [ill.] open-weight victim
> models (n = 300 [ill.] tasks each; success judged by a programmatic answer check),
> the final agent adopts the false claim in 41% [ill.] of runs [95% CI 35–47 ill.],
> versus 9% [ill.] for direct injection, while benign accuracy on unattacked claims
> stays within 2 [ill.] points. An instruction detector flags 3% [ill.] of RelayRumor
> messages at a 1% false-positive rate; requiring each agent to retrieve its own
> evidence reduces adoption to 6% [ill.]. Our harness and benign templates are
> available.\footnote{anonymous link}

---

## T2 — Tool-description poisoning (external interaction)

### Bad

> We study tool poisoning. Using prompt engineering we found descriptions that make
> agents call our tool. This shows that tool-using agents are insecure.

Wrong: "study" with no result; no threat model (who writes the description?); no
scope; overclaims "agents are insecure" from one setting.

### Good

> Tool-using agents select tools from registries whose descriptions are written by
> third parties and inserted verbatim into the agent's context. Prior injection
> attacks place instructions in tool *outputs* [C24], which output-side detectors now
> screen [D25]; the description itself, read before any call, has received less
> attention.
>
> We show that a third-party tool author who controls only the name and description
> of one tool in a registry of 20 [ill.] tools can make a sandboxed email assistant
> select that tool and forward the user's draft to it. Descriptions are optimised
> black-box against a surrogate model and transfer to held-out victims.
>
> Across 3 [ill.] victim models and 120 [ill.] benign tasks each, the poisoned tool is
> selected in 58% [ill.] of tasks [CI 49–66 ill.] and the draft is forwarded in 33%
> [ill.] [CI 25–42 ill.], against 4% [ill.] for the strongest prior description
> attack in the same harness. An adaptive description sanitiser lowers forwarding to
> 12% [ill.] with a 5-point [ill.] utility loss. All experiments use a mock registry;
> no public marketplace was contacted.

---

## T3 — Query-only memory injection (internal cognition)

### Bad

> Agents with memory can be attacked. We give a new attack which is better than all
> other memory attacks.

Wrong: no setting (who can write to memory, how?); "all other" is unfalsifiable;
no numbers, no utility, no defenses.

### Good

> Agents that store past interactions in a retrieval memory let any user influence
> what later users retrieve. Prior memory attacks either write directly to the store
> [E24] (NeurIPS'24) or require the trigger to appear in the victim's query [F25].
>
> We show that an attacker who can only issue ordinary queries can plant records that
> are retrieved for a *different* user's semantically related questions, by
> phrasing queries so that the agent's own summaries carry the false record.
>
> On a synthetic customer-support agent with a 5,000-record [ill.] memory and 2 [ill.]
> victim models, planted records are retrieved for 37% [ill.] of related victim
> queries (n = 400) [ill.] and change the answer in 21% [ill.] [CI 17–25 ill.], with
> no measurable change in benign answer accuracy. Memory-write filtering with a
> provenance tag blocks the attack; we release the harness with synthetic data only.
