# Phases P0–P8 — agent-attack research pipeline

Each phase has an owner, explicit files and a mechanical gate. `pi-orchestrator` alone advances `STATE.md`.

| Phase | owner | output | gate |
|---|---|---|---|
| P0 Scoping | pi-orchestrator | STATE.md, ETHICS.md | falsifiable goal/metric/baseline; venue/CFP; KB path; budget; sandbox and kill criteria |
| P1 Literature & KB | lit-scout, kb-curator | LITERATURE.md, KB-POSITION.md, refs.bib, notes | true competitors + defense neighbours; KB/public novelty check <=30 days; bib clean |
| P2 Ideation | idea-miner, kb-curator | IDEAS.md, open CLAIMS | Gate A/B; one-line KB delta; naive baseline and kill criterion |
| P3 Threat model & attack design | threat-modeler | THREAT-MODEL.md, threat/*.json, ETHICS.md | `aa threat-check`; reachable access; pilot across >=2 model families/frameworks; judge κ target |
| P4 Baselines | baseline-engineer | baselines/MANIFEST.md | prior attack/defense/benchmark pinned; model snapshots/configs recorded; headline reproduction or discrepancy |
| P5 Experiments | experimenter | results/, EVIDENCE.md | preregistered grid; interleaved seeds; ASR/utility/false-trigger/stealth/cost; raw cache; adaptive defense |
| P6 Falsification | falsifier | CLAIMS verdicts | no open claims; confounds/naive/judge/defense/novelty attacks tried; PI decision logged |
| P7 Writing + figures | writer, figure-artist | paper/ | claims/numbers traced; threat model/ethics; figures from logs; audit-tex |
| P8 Review → submit | reviewer-sim, submission-rebuttal | REVIEWS.md, SUBMISSION.md, ETHICS.md | mock review; bib/anonymisation/artifact; disclosure and release gate; human approval |

P6 loops to P2/P3/P5; P8 loops to P5/P7. The attack taxonomy is `01 external`, `02 internal`, `03 collaboration`;
defense and benchmark neighbours are in the user's sibling folders 04–09.

Workflow scripts: `lit-sweep.js`, `idea-tournament.js`, `falsify-round.js`, `mock-review-panel.js`.
Without Workflow support, dispatch the corresponding agent definitions one at a time through the blackboard.
