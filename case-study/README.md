# case-study — end-to-end toy agent-attack project

This is a **synthetic teaching example**, not a security result. It shows the P0–P8 blackboard workflow for a
03 multi-agent collaboration question: does removing a provenance label during a relay make a toy victim more
likely to adopt an injected false claim? The backend is deterministic rule code, not an LLM; no real service,
user, payload or paper number is involved.

- [`WALKTHROUGH.md`](WALKTHROUGH.md): phase-by-phase flow and exact commands.
- [`toy-relay/`](toy-agent-attack/): project files, generated trials and an article skeleton.

Run from the repository root:

```bash
python3 -m venv /tmp/cra-venv
/tmp/cra-venv/bin/pip install -e lib/core -e lib/bench -e lib/mcp -e lib/agentattack
cd case-study/toy-agent-attack
PYTHONPATH=../../lib/agentattack python3 code/run_experiment.py
PYTHONPATH=../../lib/agentattack python3 code/check_claim.py
```
