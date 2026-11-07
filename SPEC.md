# SPEC — build contract for agent-attack-research-agents

Every contributor (human or agent) building this repo follows this file.
It is the single source of truth for names, formats and hand-off contracts.

This repo is a fork of *crypto-research-agents*, re-targeted at **attacks on LLM agents and
LLM multi-agent systems (MAS)**: external-interaction attacks (prompt injection via web/tools/MCP,
GUI and visual manipulation, tool-selection hijacking, evidence poisoning), internal-cognition attacks
(backdoors, memory/RAG poisoning, reasoning hijacking, privacy extraction) and multi-agent-collaboration
attacks (infectious prompts, message tampering, collusion, malicious agents, manipulated-knowledge and
misinformation propagation). The falsify-first blackboard machinery is unchanged; the domain layer
(agents, skills, library, venues, case study) is new. The `cra` / `cra-mcp` / `crbench` tool names and
the `/cra-*` commands are kept for compatibility ("cra" = **c**laim-**r**igorous research **a**gents).

## 0. Hard rules (non-negotiable)

1. **No private research content.** Do NOT commit unpublished paper titles, submission numbers, author
   names, reviewer text, real experiment numbers, server addresses, API keys, e-mails or unpublished
   attack ideas from the maintainers' workspaces. Distil *methods* only. Examples use **toy /
   synthetic** systems. The user's own knowledge base (KB) of paper summaries stays **outside** the repo;
   tools reach it through `$CRA_KB` / `$CRA_PAPERS` or a `kb:` line in the project's `STATE.md`.
   A public paper may be named by title/venue/arXiv id. Before every push run `scripts/check_all.sh`
   and `scripts/privacy_scan.sh` (git-ignored deny-list `.privacy-denylist`).
2. **No copyrighted PDFs, no harvested figure images, no third-party source trees** in git.
   Baselines = MANIFEST entry (url, pinned commit, model snapshot, build/run recipe) + fetch script.
3. **Responsible research.** Attacks are run only against systems the project owns or sandboxed
   benchmark environments; never against live third-party services, real users or real accounts.
   Working payloads against deployed products are not committed; released artifacts go through the
   `ethics-disclosure` skill. Findings in deployed products trigger responsible disclosure before
   publication (logged in `ETHICS.md`).
4. Every piece of code ships with a test or a runnable `--selftest`. Python ≥ 3.10, stdlib-first
   (numpy/matplotlib optional). Tests never call a real LLM: they use `agentattack.llm.MockBackend`.
5. Bilingual: English for agents/skills/code/README; Chinese mirror docs in `docs/zh/`.

## 1. Repository layout

```
.claude-plugin/plugin.json   Claude Code plugin manifest
agents/<name>.md             12 subagent definitions (Claude Code format)
skills/<name>/SKILL.md       reusable skills (+ optional scripts/, references/)
commands/<name>.md           slash commands that kick off workflows
workflows/                   phase playbooks + Workflow-tool scripts (*.js)
lib/agentattack/             Python library for attack evaluation + MAS testbed (package `agentattack`, CLI `aa`)
lib/core/                    blackboard state layer + `cra` CLI (package `cra_core`)
lib/mcp/                     MCP server `cra-mcp` (package `cra_mcp`) + per-host installers + `cra-agent`
lib/studio/                  CRA Studio local GUI (package `cra_studio`); packaging/ builds the single executable
lib/bench/                   generic measurement + EVIDENCE ledger + audit-tex (package `crbench`)
figures/                     mplstyle, template scripts, harvester, gallery index
templates/                   blackboard, paper skeletons, MANIFEST/HANDOFF/rebuttal
references/                  attack taxonomy, reading lists, baseline/benchmark MANIFEST
case-study/                  toy end-to-end example (synthetic MAS, mock LLM) run through all phases
docs/                        BIGMAP, quickstart, integrations/; docs/zh/ Chinese mirror
AGENTS.md / CLAUDE.md        entry points for Codex-style agents / Claude Code
install.sh                   installs agents/skills/commands into a target project
```

## 2. The 12 agents (file = `agents/<id>.md`)

| id | role | owns blackboard file(s) |
|---|---|---|
| `pi-orchestrator` | phase gates, task dispatch, conflict arbitration | `STATE.md`, `DECISIONS.md` |
| `lit-scout` | arXiv/OpenReview/ACL/DBLP search, related-work matrix, reading notes, **bib verification** | `LITERATURE.md`, `refs.bib` |
| `kb-curator` | the user's attack knowledge base: "which paper already did X", taxonomy positioning, KB updates | `KB-POSITION.md` (+ proposes KB entries) |
| `idea-miner` | 8-step attack idea-mining loop | `IDEAS.md` |
| `threat-modeler` | threat model, attack formalisation, realism/access argument, harm assessment | `THREAT-MODEL.md`, `ETHICS.md` (harm plan) |
| `baseline-engineer` | fetch/pin/run prior attacks, defenses, benchmarks; model snapshots | `baselines/MANIFEST.md` |
| `experimenter` | evaluation protocol, ASR/utility/stealth/cost with CIs, judge validation, evidence ledger | `EVIDENCE.md`, `results/` |
| `falsifier` | red team on our own claims (judge artefacts, base-model jailbreak confound, defenses, novelty); veto | `CLAIMS.md` (verdict column) |
| `writer` | section-by-section writing via playbook | `paper/` |
| `figure-artist` | figures in house style, harvest figure patterns | `paper/figs/` |
| `reviewer-sim` | venue-calibrated mock review (security + ML/NLP venues) | `REVIEWS.md` |
| `submission-rebuttal` | checklist, anonymisation, ethics statement, disclosure, artifact, rebuttal, camera-ready | `SUBMISSION.md`, `ETHICS.md` (disclosure log) |

Agent file format (Claude Code subagent):

```markdown
---
name: <id>
description: <when the orchestrator should use it; 1-3 sentences, starts with a verb>
tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch   # least privilege
model: inherit
---
# <Title>
## Mission
## Inputs (blackboard files read)
## Outputs (blackboard files written, exact format)
## Procedure (numbered)
## Skills used (links to skills/<name>)
## Library used (lib modules)
## Hand-off contract (what "done" means; which agent is next)
## Failure modes & lessons (distilled, generic)
```

## 3. Skills (`skills/<name>/SKILL.md`)

| group | skills |
|---|---|
| literature & KB | `paper-search` (arXiv/DBLP/Semantic Scholar/OpenReview), `attack-kb` (query/extend the user's KB, taxonomy positioning), `lit-matrix`, `reading-notes`, `bib-verify` |
| ideas & design | `idea-mining-loop`, `threat-model`, `ethics-disclosure` |
| evaluation | `baseline-pin`, `eval-protocol` (replaces bench-protocol), `judge-validation`, `mas-testbed`, `adaptive-eval` (attacks vs defenses incl. adaptive attacker), `log-to-evidence` |
| gates | `falsify`, `phase-gate` |
| writing | `paper-playbook`, `abstract-craft`, `technique-overview`, `related-work-writing`, `experiments-writing`, `polish-writing`, `paper-figures`, `figure-harvest` |
| review & ship | `venue-calibration`, `mock-review`, `rebuttal`, `anonymize-check`, `artifact-pack`, `camera-ready` |

Retired legacy-domain skills: `eprint-search`, `sage-check`, `lean-bridge`, `param-estimation`, `textbook-index`. They are not part of the default Agent Attack workflow.

## 4. Blackboard (in the *user's research project*; templates in `templates/blackboard/`)

- `STATE.md` — phase (P0..P8), `kb:` path to the knowledge base, gate checklist, active tasks.
- `CLAIMS.md` — `ID | claim (falsifiable) | proposer | status {open,survived,refuted,weakened} | falsifier evidence | EVIDENCE refs`.
- `EVIDENCE.md` — `ID | value as printed | meaning | command | log path | code commit | machine / model snapshot | date | runs, statistic`.
  Rule: **no number enters the paper without an EVIDENCE row**; rates carry n and a 95% CI.
- `DECISIONS.md` — dated go/no-go decisions with rationale.
- `THREAT-MODEL.md` — attacker goal, knowledge, capabilities, access point, victim system, success
  criterion, stealth/constraints, out-of-scope; one section per attack variant.
- `KB-POSITION.md` — for each idea: nearest KB papers, taxonomy branch, the one-line delta.
- `ETHICS.md` — harm assessment, containment (sandbox, no live targets), release policy, disclosure log.
- `IDEAS.md`, `LITERATURE.md`, `REVIEWS.md`, `SUBMISSION.md`.

## 5. Phases (workflow)

P0 Scoping → P1 Literature & KB → P2 Ideation → P3 Threat model & attack design → P4 Baselines
→ P5 Experiments → P6 Falsification gate → P7 Writing + figures → P8 Review → submit → rebuttal → camera-ready.
Loops: P6 → P2/P3/P5. P8 review → P7/P5. Gate texts live in `lib/core/cra_core/phases.py`.

## 6. Library scope (`lib/agentattack`, package `agentattack`, CLI `aa`)

Stdlib only (numpy optional). Modules and public API:

- `metrics` — `wilson_ci(k, n, z=1.96)`, `Rate(k, n)` (`.p`, `.lo`, `.hi`, `.fmt()` → `"41.0% [35.2, 47.0] (n=300)"`),
  `rate(records, key="success")`, `rate_table(records, by, key)`, `bootstrap_ci(values, stat, B, seed)`,
  `mcnemar(b, c)` (exact two-sided p), `diff_ci(r1, r2)` (Newcombe hybrid score CI for p1−p2).
- `judge` — `cohen_kappa(a, b)`, `confusion(gold, pred)`, `agreement_report(gold, pred)` (accuracy, κ,
  precision/recall of the judge vs gold), `fingerprint(prompt, model, temperature)` (sha256 of the judge config).
- `threat_model` — `ThreatModel` dataclass (goal, target_system, access_point, knowledge ∈ {black-box,
  gray-box, white-box}, capabilities, constraints, success_criterion, victims, defenses, out_of_scope,
  surface), `validate()` → list of issues, `to_markdown()`, `from_dict()`; `SURFACES` taxonomy.
- `kb` — `parse_kb(md_path)` → list of `Paper` (key, title, zh_title, venue_year, category, summary, code, pdf);
  `scan_papers(papers_dir)` → ids per category folder; `search(papers, query, k)` ranked by token overlap.
- `llm` — `Backend` protocol `chat(messages, **kw) -> str`; `MockBackend(fn)`; `OpenAICompatible(base_url,
  model, api_key_env, temperature)` (urllib); `CachedBackend(inner, path)` (jsonl cache = provenance).
- `mas` — `Agent(name, system)`, topologies `chain/star/ring/complete/random_graph(n, p, seed)`,
  injections `MaliciousAgent`, `MessageTamper`, `MemoryPoison`; `Simulation(...).run()` → `Transcript`
  (jsonl-serialisable) with per-round belief probes; `adoption_curve(transcript)`.
- `runner` — `run_matrix(grid, trial_fn, seeds, out)` (resumable jsonl, one record per trial) and
  `env_record()` (python, platform, git commit, date, model/backend fields).
- `cli` — `aa kb-search`, `aa rate`, `aa kappa`, `aa threat-check`, `aa sim`, `aa selftest`.

## 7. Figures

`figures/style/crypto.mplstyle` (legacy filename retained for compatibility; content is the Agent Attack house style),
`figures/templates/*.py` produce PDF+PNG from synthetic data, and `figures/harvester/` builds a local, git-ignored
gallery from a local public-paper corpus.

## 8. Naming

kebab-case for agents/skills/commands; snake_case for Python modules. Paper ids in the KB follow
`<yy>_<venue>_<slug>` (e.g. `26_acl_lying_with_truths`); refer to them that way in every artefact.
