# CRA Studio

CRA Studio is a local GUI for the agent-attack blackboard. It shows project files, claims, evidence, gate status
and next actions, and can talk to an OpenAI-compatible endpoint configured by the user. Model calls are not made
by the UI unless the user configures an approved endpoint; attack runs remain subject to ETHICS.md.

```bash
pip install -e lib/core -e lib/agentattack -e lib/bench -e lib/mcp -e lib/studio
cra-studio
```

The packaged executable can also serve the local `cra-mcp` server. Build it with the existing
`packaging/cra-studio.spec`; do not include API keys, private KB files or raw harmful payloads in a package.
