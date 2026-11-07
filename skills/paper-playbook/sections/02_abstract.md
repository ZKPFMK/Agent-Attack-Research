# 02 Abstract — the three-part paradigm

Full procedure and more examples: [abstract-craft](../../abstract-craft/SKILL.md).

## Three paragraphs (or three blocks of one paragraph), one job each

| ¶ | job | sentences |
|---|---|---|
| ① Gap | deployment context of the agents/MAS → the trust assumption they make → existing attacks grouped by surface (1–2 representatives each, venue'year) → what remains unexplored or unrealistic | 3–5 |
| ② Our attack | "We present X, an attack in which <attacker with access A> <does B> so that <victim C>" → one sentence per key insight/component → threat-model qualifier (black-box, no weights, query budget) | 3–6 |
| ③ Results | scoping sentence (frameworks, models, benchmarks, n, judge) → headline ASR with CI or range vs the strongest baseline attack → utility/stealth/cost → defenses (incl. adaptive) → disclosure/artifact sentence | 3–5 |

ML/NLP venues usually want one paragraph of ~150–250 words; security venues tolerate
two to three short paragraphs. Check the submission form's limit.

## Sentence rules

1. Sentence one states the deployment context and needs no citation.
2. Group prior attacks by **surface or mechanism**, not by chronology.
3. End ¶① with the gap: "However, existing attacks assume <strong access> / target
   single agents / are blocked by <defense>."
4. ¶② sentence one states attacker, access point and effect in one clause.
5. State the **knowledge/access** qualifier explicitly ("without access to model
   weights or other agents' prompts"); it is the realism argument in miniature.
6. ¶③ scoping first: "Across N victim models in M frameworks (n = … tasks each, judge
   validated against human labels, κ = …)". Then the headline.
7. A headline rate is a range or a value with a CI, and names the baseline attack it
   beats. Never "up to 100%" from one cell of a large grid without the median.
8. Defense sentence: which defenses were evaluated, whether an adaptive variant was
   tried, what remains effective. Do not claim "bypasses all defenses".
9. Close with disclosure ("We disclosed the findings to the affected vendors") only if
   true and logged in `ETHICS.md`, and the artifact/release policy.

## Forbidden in abstracts

- "Universal", "all", "any" without matching evidence; "real-world" for a simulated
  sandbox; "undetectable" (say which detector, which rate).
- ASR without the success criterion (judge or programmatic check) being defined in
  the paper.
- Numbers from a different grid than the tables (e.g. a cherry-picked model).
- Product or vendor names in an attack context before disclosure is complete.
- Working harmful strings or payload text.

## Plain-text form for submission systems

Prepare `paper/abstract_plain.txt`: no `\cite`, write `>=` and `x`, no LaTeX macros;
never copy from the PDF. Diff it against the LaTeX abstract before submitting
(OpenReview and ARR forms may have their own character limits).

## Checklist

- [ ] ¶① ends with the gap; prior attacks grouped by surface with venue'year.
- [ ] ¶② states attacker, access, effect, and the knowledge qualifier.
- [ ] ¶③ starts with a scope sentence; every number has an EVIDENCE row and a CI/n.
- [ ] Defense and disclosure sentences match §6 and `ETHICS.md`.
- [ ] No overclaiming adjectives; no payload text.
