# agent-attack-research-agents — instructions for Claude Code

This repository is a toolkit, not a research result. A research project is initialized separately with
`/cra-init <dir>` (see `docs/QUICKSTART.md`). It is designed for attacks on LLM agents and multi-agent systems,
using the user's 01/02/03 attack taxonomy and 04–09 defense/framework/benchmark context.

When working in a research project:

1. Read `STATE.md` first. `pi-orchestrator` owns phase changes.
2. Hand work between agents only through blackboard files and raw result logs.
3. A statement enters `paper/` only if its `CLAIMS.md` status is `survived` or `weakened` with the weakened wording.
4. A number enters `paper/` only if it has an `EVIDENCE.md` row; rates include n and a CI. Run `crbench audit-tex`.
5. A citation stays only if `bib-verify` confirms it. Search the user's KB before claiming novelty.
6. Attack experiments use owned/local or sandboxed targets only. Never test live third-party services, real users,
   credentials, production pages or public registries. Record harm and containment in `ETHICS.md`.
7. Keep working payloads, private/unpublished paper material and secrets out of git. Use synthetic/redacted data.
8. Prefer `lib/agentattack` and `lib/bench` over ad-hoc scripts; throw-away scripts go under `falsify/<claim-id>/`
   or `results/<experiment>/`.

When working on this repository, follow `SPEC.md`. The `cra`/`cra-mcp` names are kept for compatibility.
