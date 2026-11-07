# 13 Conclusion

Two to three sentences, no new information, at most a third of a page.

## Template

> We showed that <attacker with access A> can <effect> in <victim class> by
> <mechanism in one clause>, reaching <headline ASR with scope> against
> <strongest baseline attack>. <Defense finding: which defenses hold/fail, adaptive
> result.> [Optional] <One concrete direction for defenses or open problem.>

## Rules

- Same numbers, scope and wording as the abstract. No claim the abstract lacks.
- End with a defender-oriented sentence where possible (what system designers should
  change); it strengthens the ethics argument.
- If pages are tight, the optional sentence goes first.
- Do not "summarise the sections" ("In Section 3 we ...").
- No alarmist closing ("this threatens all deployed agents").

## Toy (T1, illustrative)

> We showed that one rewriting relay, without access to other agents' prompts, makes
> the final agent of a five-agent chain adopt a false claim in 41% [ill.] of runs
> (n = 300) [ill.], versus 9% [ill.] for direct injection. Requiring each agent to
> retrieve its own evidence reduces this to 6% [ill.] at a 3-point [ill.] utility
> cost, which suggests evidence provenance, not message filtering, as the defense to
> pursue.
