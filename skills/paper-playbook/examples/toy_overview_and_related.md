# Toy attack overview, threat-model box and related-work table

Invented papers; all systems synthetic; all numbers and citations illustrative.

## Related-work table (T1, RelayRumor)

```latex
\begin{table}[t]
\centering\small
\caption{Attacks closest to RelayRumor. Access: what the attacker controls.
\checkmark: evaluated; --: not evaluated. Adaptive: evaluated against a defender
that knows the attack. Marks follow each paper's own evaluation, not our reruns.}
\label{tab:related}
\renewcommand{\arraystretch}{0.92}\setlength{\tabcolsep}{3pt}
\begin{tabular}{llcccc}
\toprule
Attack & Access & MAS & Multi-hop & Stealth eval & Adaptive def. \\
\midrule
[A24] & orchestrator prompt     & \checkmark & --         & --         & -- \\
[B25] & one agent, instruction  & \checkmark & \checkmark & --         & -- \\
[G25] & message channel (MitM)  & \checkmark & \checkmark & \checkmark & -- \\
\midrule
\textbf{Ours} & one relay's output only & \checkmark & \checkmark & \checkmark & \checkmark \\
\bottomrule
\end{tabular}
\end{table}
```

Rules shown: caption defines every mark and its source; "Access" column states the
assumption reviewers care about; the "Ours" row matches contribution 2 and the
threat model.

## Threat-model box (T1)

```latex
\noindent\fbox{\parbox{0.96\linewidth}{\small
\textbf{Goal.} The final agent outputs verdict FALSE for a true claim $c$
(programmatic check against the gold label).
\textbf{Knowledge.} Black-box: the attacker sees only $m_1$ (its input); it does not
know other agents' prompts or models.
\textbf{Capability.} Replaces its own output $m_2$; one attempt per task.
\textbf{Constraints.} $|m_2'| \le 1.2\,|m_2|$; benign accuracy on other claims
within 3 points.
\textbf{Out of scope.} Orchestrator compromise; base-model jailbreaks; real users.}}
```

## Contrasting-mechanism bullets (related work, T2)

> Prior attacks on tool-using agents differ in *when* adversarial content is read:
> - **Output-side injection** places instructions in what a tool *returns* [C24];
>   it requires the agent to call the tool first and is screened by output detectors.
> - **Description-side poisoning** places content in what the agent reads *before*
>   choosing a tool [H25]; prior work evaluates selection, not the downstream data flow.

## Bad vs good insight headings

| bad | good |
|---|---|
| "Evidence anchoring" | "Agents rarely re-check a claim that cites a true source." |
| "Why hedging helps" | "Hedged claims survive paraphrase; assertive ones get corrected." |
| "Tool selection" | "Agents rank tools by description overlap with the task, not by provenance." |
| "Our memory trick" | "The agent's own summaries launder attacker queries into trusted records." |

## Tiny pilot example (T1)

> On a pilot set of 50 [ill.] synthetic claims (held out from evaluation), a3 re-checked
> the relayed claim in 31 of 50 [ill.] runs without a citation and in 9 of 50 [ill.]
> runs with a true but irrelevant citation (E3).

Every number in such an example must be recomputable from logged transcripts by a
script listed in `EVIDENCE.md` (e.g. one that calls
`agentattack.metrics.rate_table(records, by="citation", key="rechecked")`).
