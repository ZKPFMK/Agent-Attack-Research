# agentattack

Stdlib-first evaluation and contained testbed library for LLM-agent attack research. It provides:

- `metrics`: Wilson/bootstrap intervals, rates, McNemar and paired differences;
- `judge`: Cohen's kappa, confusion reports and judge fingerprints;
- `threat_model`: structured threat model and mechanical checks;
- `kb`: parse/search the user's Markdown knowledge base;
- `llm`: mock, OpenAI-compatible and cached backends;
- `mas`: explicit topologies, malicious agents, tampering, memory poisoning and transcripts;
- `runner`: interleaved, resumable JSONL trial grids;
- `aa`: `kb-search`, `rate`, `kappa`, `threat-check`, `sim`, `selftest`.

The mock backend and MAS testbed are synthetic teaching tools, not secure implementations or models of real
LLMs. Run attacks only against owned/local or sandboxed systems.
