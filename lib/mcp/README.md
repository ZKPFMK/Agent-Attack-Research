# cra-mcp

MCP server for the agent-attack-research-agents blackboard. It exposes typed claim/evidence/gate tools plus KB
search, public paper search, structured threat checks and rate/CI summaries. It works with Claude Code, Codex,
Cline, Gemini CLI, Cursor, VS Code, ChatGPT and other MCP hosts.

```bash
pip install -e lib/core -e lib/agentattack -e lib/mcp
cra-mcp --project /path/to/project --profile core
cra-mcp install --host codex --project /path/to/project
```

Call `cra_resume` first in each session. Tools never contact live attack targets and never publish project files.
