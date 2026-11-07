# Use from any platform

`cra-mcp` exposes the same blackboard pipeline to MCP hosts. Install the Python packages and configure a
project-local server; the server does not upload project files or contact attack targets.

```bash
python3 -m pip install -e lib/core -e lib/agentattack -e lib/mcp
cra-mcp install --host <codex|cline|gemini|cursor|vscode|chatgpt|...> --project /abs/project
```

At the start of every session call `cra_resume`. Adopt a role with `role_card`, read procedures with
`skill_guide`, and change ledgers through `claim_register`, `claim_verdict`, `evidence_add`, `decision_log`,
`gate_tick` and `phase_advance`. The full profile adds `kb_search`, `paper_search`, `rate_ci` and `threat_check`.
See `COMPATIBILITY.md` and the host-specific files for config shapes.
