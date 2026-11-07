# 11 Defenses

Reviewers at security venues expect an attack paper to evaluate the attack against
**existing defenses** and against a defender who knows the attack (**adaptive**
evaluation), and to discuss **mitigations**. Protocol: `adaptive-eval`.

## Structure

```
[opening]        Which defense classes are relevant to the threat model and why others are
                 not (one sentence each).
[existing]       One row per defense (pinned in baselines/MANIFEST.md): detection (input/
                 output classifiers, perplexity/known-answer detection), prompt-level
                 (spotlighting/delimiters, instruction hierarchy prompts, sandwiching),
                 system-level (privilege separation, tool allow-lists, isolation of
                 untrusted content, monitor/supervisor agents, voting/consensus), model-level
                 (safety-tuned or injection-robust models). Table: ASR [CI] and utility
                 with/without each defense.
[adaptive]       The attacker knows the defense: the adapted attack, its budget, and the
                 resulting ASR. If the defense holds, say so plainly.
[defender adapts] Optional: the defender knows our attack (e.g. a detector trained on our
                 payloads) and how well it generalises to paraphrased variants.
[mitigations]    What would help, with evidence where measured (and its utility cost);
                 unmeasured ideas are labelled as suggestions.
```

## Rules

- **No "bypasses all defenses".** Name the defenses, their configuration, and report
  each; if one defense works, it is a finding, not an embarrassment.
- **Defenses at their best configuration** (recommended thresholds, the authors'
  prompts), pinned like baselines; a weak configuration invites "strawman defense".
- **Adaptive means the attack changes.** Re-running the same payload against a new
  defense is a non-adaptive evaluation; label it so.
- **Utility cost of defenses** is always reported: a defense that blocks the attack
  by refusing benign tasks is not a mitigation.
- **Detection = TPR at a fixed FPR** (state the FPR), not accuracy on a balanced set.
- Mitigations proposed but not evaluated go to "possible mitigations" with that label.

## Checklist

- [ ] Every defense pinned, at its recommended configuration, with utility reported.
- [ ] At least one adaptive attacker evaluation, clearly labelled.
- [ ] Detection reported as TPR at a stated FPR.
- [ ] Possible mitigations separated from evaluated ones.
- [ ] No universal-bypass wording; matches CLAIMS verdicts.
