# Quickstart

## Install

```bash
python3 -m pip install -e lib/core -e lib/agentattack -e lib/mcp -e lib/bench
./install.sh ~/papers/my-agent-attack
cd ~/papers/my-agent-attack
export CRA_KB=/absolute/path/to/Agent安全论文知识库.md
claude
```

Optional: install `cra-studio` for the local UI, `latexmk` for papers, and a local/OpenAI-compatible model
endpoint for approved experiments. The toy testbed and all self-tests are offline.

## A typical run

| step | command | result |
|---|---|---|
| 1 | `/cra-init .` | blackboard, threat/labels/results dirs and article skeleton |
| 2 | `/cra-lit "memory poisoning in multi-agent systems"` | KB/public search, literature matrix, verified references |
| 3 | `/cra-ideas "<attack bottleneck>"` | Gate A/B ideas, naive controls, KB position and open claims |
| 4 | `/cra-phase P3` | threat model, realism, pilot and judge validation |
| 5 | `/cra-phase P4` then `/cra-bench "<attack vs defense grid>"` | pinned baselines, interleaved trials, CIs and evidence |
| 6 | `/cra-falsify` | attack success/judge/base-model/defense/novelty/ethics red team |
| 7 | `/cra-write intro` and `/cra-figure "ASR vs defense"` | evidence-linked paper and figures |
| 8 | `/cra-review "CCS"` then `/cra-submit` | venue review, anonymisation, artifact and release gate |

At any point use `/cra-status`. Outside Claude Code install `cra-mcp` and call `cra_resume` first.

## Offline demo

```bash
aa selftest
cd case-study/toy-agent-attack
PYTHONPATH=../../lib/agentattack python3 code/run_experiment.py
PYTHONPATH=../../lib/agentattack python3 code/check_claim.py
```

The example uses only a deterministic mock backend and synthetic text. It is not a vulnerability result.
