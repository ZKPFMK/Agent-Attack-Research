# Toy introduction and contribution list — good vs bad

Invented paper T1 ("RelayRumor", a toy rumor-relay attack on a synthetic 5-agent
chain). Numbers are **illustrative** `[ill.]`. The system is **toy**: mock agents in
the `agentattack.mas` testbed with a synthetic claim set.

## Figure 1 (motivating example), described

```
benign:    user task ──► a1 (retriever) ──► a2 (relay) ──► a3 ──► a4 ──► a5 (verdict: TRUE)
attacked:  user task ──► a1 (retriever) ──► [a2 relay, attacker-controlled] ──► a3 ──► a4 ──► a5 (verdict: FALSE)
                                             rewrites claim c → c'
                                             + true but irrelevant citation
                                             + hedge ("reportedly")
```

Caption (good): "One relay that rewrites a single claim and anchors it to a true
source makes the final agent report the false claim; no other agent's prompt or
memory is modified. Toy system; claim text synthetic."

Caption (bad): "Overview of our attack." (no take-away, no scope, no toy label).

## Contribution list

### Bad

```latex
\subsection{Contributions}
\begin{itemize}
\item We study multi-agent misinformation and propose a novel attack.
\item Our attack achieves up to 100\% ASR, although it does not work on model D.
\item We investigate many defenses.
\item We release everything, including working payloads for commercial assistants.
\end{itemize}
```

Problems: "study/investigate/novel"; concession inside contributions; "up to 100%"
without scope, n or CI; no section pointers; releasing working payloads against
deployed products contradicts responsible release.

### Good

```latex
\subsection{Contributions}
Inspired by the observation that agents rarely re-check a claim that cites a true
source, we show that a single relay can steer the conclusion of a sequential agent
pipeline without access to any other agent. Our main contributions are:

\begin{itemize}
\item \textbf{A relay-level threat to agent pipelines.} We identify peer messages
  that carry citations as an attack surface distinct from tool outputs and
  orchestrator prompts, and formalise an attacker that controls one relay's output
  only (\Cref{sec:threat}).\claimref{C1}
\item \textbf{RelayRumor.} We design a three-stage rewrite (claim substitution,
  evidence anchoring, hedging) that survives downstream paraphrasing; unlike
  self-replicating prompt attacks, it contains no instruction for other agents to
  execute (\Cref{sec:attack}).\claimref{C2}
\item \textbf{Evaluation.} Across 4 [ill.] victim models and three topologies, the
  final agent adopts the false claim in 41\% [ill.]\evid{E7} of runs (95\% CI
  35--47, $n=300$), versus 9\% [ill.]\evid{E8} for direct injection, with benign
  accuracy within 2 points [ill.]\evid{E9} (\Cref{tab:main}).\claimref{C3}
\item \textbf{Defenses.} An instruction detector flags 3\% [ill.]\evid{E12} of attack
  messages at 1\% FPR; per-agent evidence retrieval lowers adoption to 6\%
  [ill.]\evid{E13} at a 3-point utility cost, which we recommend as a design rule
  (\Cref{sec:defense}).\claimref{C4}
\end{itemize}
```

## Opening paragraph

### Bad

> Multi-agent systems are a hot topic. Many papers have been written. They are not
> secure. In this paper we attack them.

### Good (structure only; wording illustrative)

> LLM agents are increasingly composed into pipelines in which each agent consumes
> and summarises the output of another [..]. Such pipelines rely on an implicit
> assumption: a peer's message is a faithful report of the evidence it cites.
> Figure 1 shows a synthetic five-agent fact-checking chain in which one relay
> rewrites a single claim and the final agent reports it as true. Prior multi-agent
> attacks either control the orchestrator [..] or spread instructions that each hop
> must execute [..], which instruction detectors increasingly catch [..]. Whether an
> attacker who controls only one participant's output, and sees no other agent's
> prompt, can steer the pipeline has not been measured. This is hard for two reasons:
> (C1) downstream agents can re-check claims against their own evidence, and (C2) the
> rewrite must survive further paraphrasing hops.
