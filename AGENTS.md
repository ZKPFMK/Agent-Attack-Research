# agent-attack-research-agents — instructions for Codex and generic agents

This repo is a falsify-first toolkit for research on attacks against LLM agents and multi-agent systems. Research
happens in a separate project initialized with `/cra-init <dir>`.

Read `STATE.md` before working in a project; use blackboard files for hand-offs; register claims before developing
or writing them; make the falsifier attack open claims; trace every paper number to EVIDENCE.md; verify references;
position ideas against the KB; and use only owned/local or sandboxed targets. Nothing leaves the machine without
explicit human approval. Do not commit live-target payloads, secrets, personal data, private research content or
copyrighted PDFs. See `SPEC.md` for names, schemas, phases and the `agentattack` API.

Outside Claude Code, use `cra-mcp`: call `cra_resume` first, then use typed ledger tools. The Python CLI `aa`
provides `kb-search`, `kb-list`, `rate`, `kappa`, `threat-check`, `sim` and `selftest`.
