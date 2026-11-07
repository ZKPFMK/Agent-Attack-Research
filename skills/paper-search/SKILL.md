---
name: paper-search
description: Search public literature on attacks, defenses and benchmarks for LLM agents and multi-agent systems. Use for P1 related work, every novelty check, and again within 7 days of submission.
---
# paper-search

Use multiple sources because this field changes faster than any single index. The search result is a lead;
the paper, venue and result must be checked against the public landing page before entering `refs.bib` or
LITERATURE.md.

## Procedure

1. Freeze the question and date window in LITERATURE.md. State the three surface terms (01 external interaction,
   02 internal cognition, 03 multi-agent collaboration), the attack goal, and the nearest known KB ids.
2. Search the user's KB first with `aa kb-search` or `kb_search`. A clear result means "not in this KB", never
   "novel". Record relevant neighbours and their access point, victim, metric and defense assumptions.
3. Run the public search (network may be unavailable):
   ```bash
   python3 skills/paper-search/scripts/paper_search.py \
     -q "multi-agent message tampering" -q "LLM agent collusion" \
     --since 2025-01-01 --source arxiv,openreview,dblp,s2 --json
   ```
   `--months 1` is useful for a pre-submission check. `--selftest` is offline and tests parsers only.
4. Search adversarial phrasings: mechanism (memory poisoning), entry point (tool output/MCP/web page), goal
   (tool misuse/privacy/false belief/availability), and system name (WebAgent/MAS/RAG). Search both English and
   Chinese where appropriate.
5. Deduplicate by normalised title, then open the public abstract/PDF. Do not infer a result from a title or a
   search snippet. Add a reading note for every true competitor.
6. Check the public version: ACL Anthology/venue page, OpenReview record, arXiv id and DOI. A preprint is prior
   art for positioning even when it is not peer reviewed; label its status.
7. Add the entry to `refs.bib`, run `bib-verify`, and add a matrix row with threat model, models/frameworks,
   defenses, metric definition, n and a page/table/figure pointer.
8. Write the novelty line:
   `YYYY-MM-DD | query | sources | window | hits reviewed | clear|overlap:<id>|taken:<id>`.
9. Re-run the chosen idea against the KB and public sources after the first pilot and within 7 days before P8.

## Failure modes

- "No search hit" is not a novelty proof: search aliases, the KB, citations and the last-month window.
- A paper's ASR is not comparable until success, judge, n, model snapshot and temperature match.
- Do not call a benchmark an attack, or a defense a competitor, without reading its threat model.
- Do not copy payloads or private/unpublished material into the repository.
- Network failure is `UNCHECKED`; it does not produce a clear novelty verdict.
