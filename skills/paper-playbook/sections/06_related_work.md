# 06 Related Work

Full procedure: [related-work-writing](../../related-work-writing/SKILL.md).

## Organise by surface/axis, not by time

Place prior work along the axes reviewers use to judge attack novelty, typically
(a) **attack surface / access point** (user prompt, external content and web,
tool descriptions and MCP servers, GUI/visual input, memory and RAG, training data,
inter-agent messages, a participating agent) and (b) **attacker capability /
knowledge** (white-box, gray-box, black-box; query budget; number of controlled
components). The KB taxonomy (`KB-POSITION.md`) gives the branch for each work. A
comparison table places each work in its cell; the "Ours" row occupies the cell no
one else does, and the table's other columns check the properties that matter
(multi-agent? propagation across hops? stealth evaluated? adaptive defense
evaluated? real framework?).

## Structure (≈ 1 page two-column)

```
[lead-in, 2-3 sentences]  Attacks on LLM agents can be organised by where adversarial content
                          enters and what the attacker controls [survey refs]. Table 1 places
                          prior attacks closest to ours.
[Table 1]                 rows: prior attacks (+ venue'year), last row \textbf{Ours}; columns:
                          surface | access/knowledge | MAS? | multi-hop? | stealth eval |
                          adaptive-defense eval | framework(s); caption defines all marks.
[¶ surface A]             one sentence per work: what it injects, where, under what access,
                          what it shows; last sentence states what all of them share.
[¶ surface B]             same.
[¶ defenses]              defenses relevant to our setting (detectors, prompt hardening,
                          isolation/privilege separation, monitor agents), labelled as such;
                          forward pointer to §6 where they are evaluated.
[¶ Our work]              3-4 sentences: the cell we occupy and the one-line delta to the
                          closest prior attack (identical to contribution 2).
[¶ concurrent]            "Concurrent work." for works within ~3 months of the deadline.
```

## Rules

- Judge prior work only by **factual scope**: "assumes white-box access to the
  victim", "evaluates a single agent", "does not report utility under attack". Never
  "naive", "fail", "unrealistic" as an adjective (show the access assumption instead).
- Every characterisation (ASR, setting, access) is checked against the **original
  paper**, not a survey or a later paraphrase; record page/section in `LITERATURE.md`.
- If you quote another paper's ASR, quote its scope (models, judge, benchmark) too, or
  do not quote it. Cross-paper ASR comparisons are rarely like-for-like; prefer
  running the baseline yourself (`baseline-pin`).
- Benchmarks (e.g. AgentDojo, NeurIPS'24 Datasets & Benchmarks) and defenses are cited
  in their own paragraphs, not mixed with attacks.
- Your own earlier papers appear in the third person and receive the same factual
  critique.
- Name papers in prose by first author or system name; use the KB id
  (`<yy>_<venue>_<slug>`) in internal notes only.

## Checklist

- [ ] Organised by surface/capability; Table 1 with an "Ours" row.
- [ ] Each characterisation verified against the source paper (noted in LITERATURE.md).
- [ ] Defenses and benchmarks in separate paragraphs.
- [ ] "Our work" delta identical to contribution 2 and the table caption.
- [ ] No evaluative adjectives about others.
