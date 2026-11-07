# WALKTHROUGH — toy-agent-attack

This project is deliberately small: a five-agent chain, a deterministic mock backend and a synthetic bridge
closure claim. One malicious first agent sends the claim. The control varies only whether a summarising relay
preserves the source label. The output illustrates adoption curves, Wilson intervals, raw JSONL provenance and a
falsifier script; it does not estimate a real model's vulnerability.

## Reproduce

```bash
cd case-study/toy-agent-attack
PYTHONPATH=../../lib/agentattack python3 code/run_experiment.py
PYTHONPATH=../../lib/agentattack python3 code/check_claim.py
python3 ../../skills/phase-gate/scripts/gate_check.py --project . --phase P6
```

The experiment uses `agentattack.mas.Simulation`, `toy.rumor_mock`, `runner.run_matrix` and `aa rate`. No network
call is made. `results/trials.jsonl` is resumable; `results/rate.log` is the generated table cited by E1.

## Phase mapping

- **P0:** STATE.md declares the falsifiable adoption question, sandbox, budget and kill switch.
- **P1:** LITERATURE.md/KB-POSITION.md show how to compare the idea with the user's 03 collaboration KB branch;
  the toy project does not claim novelty.
- **P2:** IDEAS.md records the fixed assumption (provenance survives summarisation), naive baseline and controls.
- **P3:** THREAT-MODEL.md and `threat/toy.json` pass `aa threat-check`; ETHICS.md says synthetic/local only.
- **P4/P5:** `baselines/MANIFEST.md`, `code/run_experiment.py`, raw trials and EVIDENCE.md define the protocol.
- **P6:** `code/check_claim.py` attempts the claim against the no-label control and keeps its output under falsify/.
- **P7/P8:** paper/ is a placeholder article source; the full project would add figures, review, anonymisation and
  release decisions before anything leaves the machine.
