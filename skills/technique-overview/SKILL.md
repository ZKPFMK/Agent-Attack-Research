---
name: technique-overview
description: Use when writing the attack overview (a.k.a. "Our Approach" / "Key Insights") of an agent-attack paper. Recalls the closest prior attacks by mechanism and access, reduces the gap to numbered challenges, and answers each with a declarative, evidence-backed "Insight" plus one attack-pipeline figure, so a reviewer can restate why the attack works without reading the body.
---

# Attack overview (technique overview)

## Goal test

After reading only the abstract, introduction, threat model and overview, a reviewer
can: (a) restate the attack in two sentences, (b) say what the attacker controls and
what not, (c) say how it differs from the closest prior attack, (d) believe the
headline ASR is plausibly due to the attack and not to a weak victim or a lenient
judge. Ask `reviewer-sim` (generalist persona) to perform exactly this test.

## Procedure

1. **List the closest prior attacks** from `LITERATURE.md` and `KB-POSITION.md`
   (usually 2–3). For each: mechanism, access point, knowledge assumed, what it
   showed, and the one factual reason it does not cover our setting. Verify each
   against the original paper.
2. **Find the common trust assumption** the prior attacks and ours exploit (e.g.
   "agents treat peer messages as evidence", "tool descriptions are trusted context").
   If our attack does not share a mechanism-level story with them, say so and frame
   the paper as a new surface rather than an improvement.
3. **Reduce to challenges.** "Achieving <effect> under <threat model> requires: (C1)
   ... (C2) ...". Challenges must be concrete enough that an ablation can show each
   insight matters.
4. **One Insight per challenge.** Heading = declarative sentence stating the
   observation. Body: observation → pilot evidence (EVIDENCE row, held-out from the
   evaluation set) → how the attack uses it → when it fails.
5. **Figure.** An attack-pipeline overview (benign vs attacked flow with identical
   layout, attacker element tinted, insights labelled where they act). Ask
   `figure-artist` for it; caption = one sentence take-away.
6. **Putting it together** paragraph: the attack as a 3–5 step sketch consistent with
   the algorithm in the attack-design section.
7. **Optional scope extender.** One paragraph on applying the mechanism to a
   neighbouring surface or topology, marked "not evaluated" unless measured.
8. **Consistency check**: each insight ↔ an ablation row in the evaluation; the
   sketch ↔ the algorithm float; the capability list ↔ `THREAT-MODEL.md`.

## Style rules

- Describe prior attacks by mechanism and access, per paper; no tutorial headings
  ("Why X is needed").
- No anthropomorphism ("the agent trusts/wants"); state measured behaviour.
- No payload text; show structure with slots and `[REDACTED: ...]`.
- No numbers that the evaluation section does not contain; pilot numbers come from a
  held-out pilot set and have their own EVIDENCE rows.
- Keep limitations as short remarks at the end of the relevant insight.

## Output

`paper/sections/overview.tex` (or inside `intro.tex` / `attack.tex`), figure request in
`paper/figs/REQUESTS.md`.

Examples: `skills/paper-playbook/sections/05_technique_overview.md`,
`skills/paper-playbook/examples/toy_overview_and_related.md`.
