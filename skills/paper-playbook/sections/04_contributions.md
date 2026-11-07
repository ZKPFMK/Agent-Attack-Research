# 04 Our Contributions

About a third of a page: a lead-in sentence and three or four bullets (or bold-titled
paragraphs).

## Lead-in template

> Inspired by <observation about the trust assumption>, we show that <attacker with
> access A> can <effect> in <victim class>. Our main contributions are:

## Fixed order: problem/surface → attack → evaluation → defenses/insight

1. `\textbf{A new attack surface / threat.}` The trust assumption, why it is
   exploitable, and the threat model in one sentence (`\Cref{sec:threat}`).
2. `\textbf{<Name>, an attack that <does X>.}` Its components (one clause per key
   insight), the access it needs, and what distinguishes it from the closest prior
   attack in one factual clause (`\Cref{sec:attack}`).
3. `\textbf{Systematic evaluation.}` Scope (frameworks, models, benchmarks, topologies,
   n) and the two most recognisable numbers with CI, against the strongest baseline
   attack; utility and stealth in one clause (`\Cref{sec:eval}`, `\Cref{tab:main}`).
4. `\textbf{Defenses and lessons.}` Which defenses were tested, the adaptive-attacker
   result, the mitigation that helps and its utility cost; disclosure/artifact if
   relevant (`\Cref{sec:defense}`).

Variants:

- **Benchmark papers:** benchmark → evaluation findings → analysis → tooling/release.
- **Measurement papers:** phenomenon → controlled measurement → causal analysis →
  implications for defenses.
- **One discovery, everything derived:** "Our main finding is that <phenomenon>, on
  which all other results build." Strong when the phenomenon is surprising and robust.

## Wording rules

- Each bullet: verb + deliverable + section pointer; 2–4 sentences.
- **Numbers only in bullets 3 and 4**, each with an EVIDENCE row and an n/CI in the
  body; put `\evid{E<n>}` after each and `\claimref{C<n>}` at the end of each bullet.
- **No concessions** inside contributions; limitations go to §7.
- Strong verbs in order of force: show / demonstrate (with evidence) > identify /
  characterise > design / propose > evaluate / measure. Avoid "study", "investigate",
  "explore", "try to".
- "First" only if the KB position (`KB-POSITION.md`) and a recent `paper-search` sweep
  support it; prefer "to our knowledge, the first ... under <threat model>".
- The one-line delta to the closest prior attack must be **identical in substance** in
  bullet 2, the related-work "Our work" paragraph and the comparison-table caption.

## Pre-flight

Before prose: each bullet exists as a row in `CLAIMS.md` with status `survived` or
`weakened` (then the bullet uses the weakened wording). Typical weakened forms:
"on 3 of 4 [ill.] victim models", "in the chain and star topologies (not complete
graphs)", "against the evaluated defenses (an adaptive variant of D2 reduces ASR to
…)".

See `examples/toy_intro_and_contributions.md` for good/bad toy bullets.

## Checklist

- [ ] 3–4 bullets in surface → attack → evaluation → defenses order.
- [ ] Numbers only in bullets 3–4, each with `\evid`; each bullet with `\claimref`.
- [ ] Every bullet has a CLAIMS row that survived falsification.
- [ ] Delta-to-closest-attack sentence consistent in three places.
