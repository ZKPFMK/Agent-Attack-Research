---
name: reading-notes
description: Write structured, dated, falsifiable reading notes for an agent-attack, defense or benchmark paper. Capture its threat model, mechanism, evaluation and limitations before it enters the literature matrix or KB positioning.
---
# reading-notes

Notes are the compressed layer later agents read before reopening a PDF. They must be useful for comparison and
honest about what was and was not read. A note records the paper's conditions, not a stronger interpretation that
would make our idea look newer or more effective.

## File and naming

Use `notes/papers/<kb-id-or-year-shortname>.md`. If the paper is in the user's KB, prefer its public id, for
example `notes/papers/26_acl_lying_with_truths.md`. Keep one file per paper and append a dated section on re-reads.
Do not copy a private/unpublished paper or a long passage into the repository.

## Template

```markdown
---
key: paper_key                 # bib key; must pass bib-verify
kb_id: 26_acl_lying_with_truths | none
source: ACL Anthology / OpenReview / arXiv / DOI / local-public-pdf
read: 2099-01-31 (sections 1-4, 6; appendix skipped)
reader: lit-scout
---
## One-line contribution
## Surface and access point
01 external interaction | 02 internal cognition | 03 multi-agent collaboration
access: <where attacker content or state enters>
## Threat model
attacker knowledge: black-box | gray-box | white-box
capabilities: <queries, message edits, memory writes, tool/MCP publication, compromised peer, ...>
victim: <models/snapshots, framework, topology, tools, memory/RAG>
out of scope: <explicit exclusions>
## Attack or defense mechanism
<five concise lines: what is changed, where it propagates, and which assumption is used>
## Operational success criterion
<what counts as success, who labels it, threshold, and when it is measured>
## Claims (numbered and falsifiable)
C1. ... (Sec./Fig./Tab./p.)
## Evaluation and concrete numbers
| value | metric definition | model/framework | n/seeds | source pointer |
|---|---|---|---|---|
## Defenses and adaptive setting
<defenses evaluated, configuration, attacker knowledge of the defense, utility impact>
## Hidden assumptions and fixed choices
<temperature, prompt, topology, memory policy, detector access, task filtering, excluded failures>
## Weak points / reviewer attacks
## Open problems and limitations
<paraphrase plus page/section pointer; quote only short phrases when necessary>
## Relevance to this project
compare | reuse | mine | ignore — why
nearest KB ids: <ids>
our possible delta: <one testable difference, or pre-empted>
artifact/code: <public URL, revision, licence, or none>
```

## Rules

- Every number carries a page/table/figure/section pointer and its metric definition.
- Distinguish what the paper proves, measures, reports from prior work, or conjectures.
- Record the exact read scope. An abstract skim is not a full read.
- Use the same 01/02/03 surface and access-point vocabulary as `attack-kb` and `THREAT-MODEL.md`.
- Record model snapshot, temperature, framework, topology, judge and sample count whenever the source provides them;
  write `not reported` when it does not.
- If a note disagrees with another note, add an erratum to the project blackboard and tell `pi-orchestrator`.
- Keep negative notes. A paper that does not transfer to the proposed setting can still prevent repeated work.
- Never turn “not in the user's KB” into a novelty claim; `lit-scout` must check public literature separately.
