---
name: related-work-writing
description: Use when writing or auditing the Related Work section of an agent-attack paper. Organises prior attacks by attack surface and attacker access rather than chronology, builds the comparison table with an "Ours" row, separates attacks, benchmarks and defenses, writes the "Our work" delta paragraph, and checks every characterisation of prior work against its source.
---

# Related-work writing

## Inputs

`LITERATURE.md` (related-work matrix from `lit-scout`), `KB-POSITION.md` (taxonomy
branch and nearest KB papers from `kb-curator`), `refs.bib` (verified by
`bib-verify`), `THREAT-MODEL.md`, the contribution list.

## Procedure

1. **Choose axes.** From the matrix pick the axes along which reviewers judge novelty:
   attack surface/access point (external content and web, tools and MCP, GUI/visual,
   memory/RAG, training/backdoor, inter-agent messages, participating agent) and
   attacker capability (knowledge level, number of controlled components, query
   budget). Secondary columns: MAS vs single agent, multi-hop propagation, stealth
   evaluated, adaptive defense evaluated, real framework vs simulation.
2. **Place each work.** For each work record: surface, access, what it injects, what
   it showed (with its own scope: models, judge, benchmark), limitations it states
   itself, venue'year, KB id. Verify against the original (page/section noted in
   `LITERATURE.md`). Where later papers paraphrase an earlier attack, compare with
   the earlier paper's own threat model and evaluation.
3. **Build the table** (`templates/paper/sections/related_table.tex` style): one row per
   closest attack, last row `\textbf{Ours}`, caption defines all marks and states
   that marks follow each paper's own evaluation.
4. **Write the paragraphs**: lead-in (2–3 sentences) → one paragraph per surface
   (one sentence per work, shared limitation last) → benchmarks and evaluation
   frameworks → defenses (forward pointer to the defenses section) →
   `\textbf{Our work.}` (3–4 sentences with the one-line delta) → concurrent work.
5. **Tone filter**: remove "unfortunately", "fail", "naive", "unrealistic",
   "trivial"; replace with factual scope ("... assumes white-box access to the
   victim", "... evaluates a single agent", "... does not report utility under
   attack").
6. **Self-citation check**: own prior work in third person, critiqued like others.
7. **Coverage check** with `lit-scout`/`paper-search`: arXiv, OpenReview and ACL
   Anthology for the last 6–12 months (the field moves fast); any close concurrent
   work gets a labelled paragraph; record the sweep date in `LITERATURE.md`.
8. **Bib hygiene**: published versions over preprints when they exist (ACL Anthology,
   PMLR, NeurIPS proceedings, USENIX/ACM/IEEE DOIs); arXiv entries with id and
   version; braces around acronyms (`{LLM}`, `{MCP}`). Verification itself is owned by
   `bib-verify`.

## Placement in the paper

- ML/NLP venues: usually §2 after the introduction (or before the conclusion).
- Security venues: often a separate section near the end; keep a short positioning
  paragraph in the introduction anyway, since many reviewers decide novelty there.
- SoK papers: the related work *is* the paper; organise by the taxonomy.

## Anti-patterns

- A chronological list of summaries without a thesis.
- Quoting another paper's ASR without its scope (model, judge, benchmark), or
  comparing ASRs across papers as if like-for-like.
- Mixing defenses and benchmarks into the attack paragraphs.
- Omitting the closest prior attack because it is inconvenient (reviewers will name
  it); check the KB branch neighbours explicitly.
- A table whose "Ours" row claims a property the evaluation does not show.

## Output

`paper/sections/related.tex` (or inside `background.tex`), table in
`related_table.tex`, verification notes appended to `LITERATURE.md`.
