# CRA Studio

CRA Studio is a local workbench for agent-attack research projects: blackboard ledgers, phase gates, files and an
OpenAI-compatible local model endpoint. It does not run attacks against live third-party services.

```bash
pip install -e lib/core -e lib/agentattack -e lib/bench -e lib/mcp -e lib/studio
cra-studio
pyinstaller packaging/cra-studio.spec --noconfirm
```

Guide: [docs/studio.md](../../docs/studio.md) · Chinese: [docs/zh/studio.md](../../docs/zh/studio.md)
