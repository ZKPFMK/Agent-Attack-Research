# crbench

Measurement and provenance harness for agent-attack research. Use `agentattack.runner` and `aa rate` for trial
success/utility/stealth rates with Wilson intervals; use `crbench` for latency/resource logs, agent-harness JSONL
parsing, environment capture, tables, EVIDENCE.md operations and `audit-tex`. The parser registry keeps common
benchmark formats and local resource logs; it has no cryptography-specific parser.

```bash
pip install -e lib/bench
crbench evidence check EVIDENCE.md --root .
crbench audit-tex paper/main.tex EVIDENCE.md
```
