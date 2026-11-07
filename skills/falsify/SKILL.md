---
name: falsify
description: Red-team protocol for trying to refute an LLM-agent or multi-agent attack claim before a reviewer does. Use at P6, before a number enters the paper, after a surprising result, and when a threat model or judge is questioned.
---
# falsify: break the attack claim before a reviewer does

## Principle

The job is to **refute** the claim, not confirm it. The proposer writes a falsifiable statement with its exact
victim, access point, quantifiers, budget, metric and kill switch. The falsifier runs real computations, re-labels,
controls or searches and reports actual outputs. "Could not refute" is a valid result only when the attempted checks
are listed.

## Input

A `CLAIMS.md` row in the form
`ID | claim | proposer | status | falsifier evidence | EVIDENCE refs`, normally with `status: open`, plus
`THREAT-MODEL.md`, `ETHICS.md`, raw `trials.jsonl`, judge labels, baseline manifest, KB position and cited sources.

## Attack order

1. **Definitions and scope.** Check that attacker goal, knowledge, capabilities, access point, victim, success
   rubric, stealth and out-of-scope are defined and identical in the paper, protocol and code. Reject circular
   access: a party that already controls the victim state does not need the proposed attack.
2. **Controls and confounds.** Add no-attack, naive injection and plain jailbreak at the same budget. Check whether
   the base model already produces the measured behaviour or whether the victim merely quotes a payload while
   refusing it. For MAS, check the stated topology, message route, memory writes and source roles.
3. **Judge artefact.** Blindly re-label a stratified transcript sample or use a second rubric/judge. Run `aa kappa`
   and report precision, recall, F1 and the judge fingerprint. Refusal-with-leak, partial adoption and later
   retraction must have pre-registered labels.
4. **Sensitivity.** Re-run the primary cell across model families/snapshots, temperature, seeds, paraphrases,
   framework versions, topology, defense settings and query/token budget. A one-cell result is weakened to that
   cell unless the claim says so.
5. **Raw recomputation.** Recompute every rate from JSONL with `aa rate`; check k/n, Wilson 95% CI, paired tests,
   excluded failures, timeout/refusal rules, multiple-comparison correction, utility, false-trigger, detection,
   latency, tokens, queries and cost. Do not trust a summary table.
6. **Defense and adaptive attacker.** Run the strongest applicable static defense and an attacker that knows the
   defense, or an adaptive defender for an evasion claim. Report utility under defense; a broken task is not a
   successful stealth attack.
7. **Realism and containment.** Confirm the access point is reachable without already granting the outcome and that
   the run used only an owned, local or sandbox target. Any live third-party target, real user, credential, private
   data, production page or public registry is a containment veto.
8. **Pre-emption.** Search the user's KB with `aa kb-search`, read `KB-POSITION.md`, and check recent public papers
   with `paper-search`. A known mechanism under a different name weakens or refutes a novelty claim.

Run at least one check at every step unless a clean refutation ends the campaign. Preserve counterexamples and
negative results under `falsify/<claim-id>/`.

## Verdict taxonomy

| verdict | meaning | required evidence |
|---|---|---|
| `survived` | every applicable attack above was attempted and none succeeded | commands, outputs, raw paths and searches |
| `weakened` | true only for a narrower model, budget, cell, metric or novelty statement | replacement claim plus the forcing evidence |
| `refuted` | counterexample, recomputation contradiction, judge artefact, containment violation or prior art | minimal reproducible evidence or verified citation |

Write the verdict in `CLAIMS.md`, append material changes to `STATE.md` errata, and notify `pi-orchestrator`. Keep
refuted rows so future projects do not repeat them. Only survived or weakened rows can be used by `writer`.

## Output example

```markdown
| C7 | On local MAS T, attack A raises adoption over naive injection at equal query budget | idea-miner | weakened | adaptive defense removes the gain on model snapshot S2; replacement: "...without adaptive defense on S1" | E14 |
```

## Parallel rounds

Give each sub-agent a disjoint claim group, required first-line verdict (`REFUTED`, `SURVIVED` or `UNVERIFIABLE`),
a kill switch and a do-not-do list. A final falsifier reads all outputs, recomputes disputed cells and adjudicates
conflicts. Never let the proposer be the only falsifier.

## Related skills

`judge-validation`, `adaptive-eval`, `eval-protocol`, `baseline-pin`, `threat-model`, `attack-kb`, `paper-search`,
`log-to-evidence`.
