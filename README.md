# agent-attack-research-agents

**A falsify-first multi-agent research system for attacks on LLM agents and LLM multi-agent systems** — from
knowledge-base positioning and threat modelling through controlled evaluation, red-teaming, paper writing,
responsible disclosure and camera-ready packaging. It is available as Claude Code agents/skills/commands, an MCP
server (`cra-mcp`) for Codex, Cline, Gemini CLI, Cursor, VS Code and other MCP hosts, a stdlib-first Python
library (`agentattack`) and a local CRA Studio UI.

The repository is a fork of a crypto-paper workflow. The blackboard discipline is retained; the domain layer now
covers the user's three attack folders:

- **01 external interaction:** web/content/evidence injection, role and chat boundaries, GUI/visual attacks,
  tool/MCP metadata and selection, toolchain consequences and cost;
- **02 internal cognition:** backdoors, reasoning hijacking, memory/RAG and multimodal memory poisoning, privacy
  extraction and availability attacks;
- **03 multi-agent collaboration:** infectious prompts, message tampering, hidden/malicious agents, collusion,
  distributed/compositional prompts, manipulated knowledge/misinformation, control-flow hijacking and blocking.

Defense, framework, benchmark and misinformation neighbours from folders 04–09 are used as baselines and context.
The user's distilled KB and paper PDFs stay outside this repository; set `CRA_KB` or put `kb: /path/to/file.md` in
an initialized research project's `STATE.md`.

## Why this workflow

Attack papers often fail because the access point is circular, "success" is a judge artefact, the naive injection
was never measured, benign utility is missing, the strongest defense is absent, or a result cannot be reproduced
from a model snapshot and raw transcript. This toolkit makes those failures visible:

- every attack-facing claim enters `CLAIMS.md` and is attacked by `falsifier` before prose;
- every rate carries n and a Wilson 95% interval, and every printed number has an `EVIDENCE.md` row;
- every judge is validated against human labels and fingerprinted;
- every idea is positioned against the user's KB before investment;
- every experiment records models, snapshots, temperature, seeds, framework, topology, cache and cost;
- every artifact obeys sandbox, redaction and responsible-disclosure rules.

## What is inside

| path | purpose |
|---|---|
| `agents/` | 12 roles: pi-orchestrator, lit-scout, kb-curator, idea-miner, threat-modeler, baseline-engineer, experimenter, falsifier, writer, figure-artist, reviewer-sim, submission-rebuttal |
| `skills/` | paper-search, attack-kb, threat-model, ethics-disclosure, eval-protocol, judge-validation, mas-testbed, adaptive-eval, falsify, baseline-pin, writing, review and release procedures |
| `commands/` | `/cra-init`, `/cra-status`, `/cra-phase`, `/cra-lit`, `/cra-ideas`, `/cra-falsify`, `/cra-bench`, `/cra-write`, `/cra-figure`, `/cra-review`, `/cra-rebuttal`, `/cra-submit` |
| `lib/agentattack/` | ASR/utility/stealth metrics, Wilson/bootstrap CIs, McNemar, judge κ and fingerprinting, threat-model schema, KB parser/search, mock/OpenAI-compatible/cached backends, MAS testbed, resumable trial runner and `aa` CLI |
| `lib/core/` | blackboard tables, claim/evidence invariants, phase gates, event log and `cra` CLI |
| `lib/mcp/` | `cra-mcp`: typed blackboard tools plus KB search, threat checks, rate CIs, paper search and host installers |
| `lib/bench/` | `crbench`: raw-log parsing, latency/resource measurement, environment capture, evidence ledger and `audit-tex` |
| `templates/` | attack-paper blackboard and neutral article paper skeleton |
| `case-study/` | synthetic five-agent provenance-relay example; no live models or services |
| `figures/` | attack-pipeline, topology, ASR/CI, propagation and model×attack figure patterns |

## Install

```bash
git clone <this repo> ~/agent-attack-research-agents
cd ~/agent-attack-research-agents
python3 -m pip install -e lib/core -e lib/agentattack -e lib/mcp -e lib/bench
./install.sh /path/to/my-agent-attack-project       # or ./install.sh --user
scripts/check_all.sh --quick
```

To initialize a project:

```bash
cra init ~/papers/my-agent-attack
cd ~/papers/my-agent-attack
export CRA_KB=/absolute/path/to/Agent安全论文知识库.md
cra status
```

In Claude Code, use `/cra-init .`, then `/cra-phase P1`, `/cra-ideas "<attack bottleneck>"`,
`/cra-falsify` and `/cra-status`. Outside Claude Code, install `cra-mcp` for the host and call `cra_resume`
first in each session. See `docs/QUICKSTART.md` and `docs/integrations/README.md`.

The domain library's offline demo is:

```bash
aa selftest
cd case-study/toy-agent-attack
PYTHONPATH=../../lib/agentattack python3 code/run_experiment.py
PYTHONPATH=../../lib/agentattack python3 code/check_claim.py
```

## Scope and safety

The attack testbed is for authorized security research, defensive evaluation and synthetic education. It never
contacts live third-party agents, real users, public registries or production pages. Working payloads, credentials,
personal data and private research content do not belong in git. Transferable findings require a disclosure entry
and a human-approved release decision. Toy backends are not models of real LLM behaviour.

## License

MIT
