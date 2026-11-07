# 14 Appendix

## Principle

Supplementary material: reviewers are not obliged to read it, so **nothing in the
appendix may be load-bearing for the body's claims**. Put this as a comment at the top
of the appendix source. Check the CFP: some venues cap appendix length, some require
it in the same PDF, some in a separate supplement, and some count it toward the limit.

## Organisation (typical attack paper)

- **A. Prompts and payload templates.** System prompts of victim agents (or pointers
  to the framework defaults at a pinned commit), attack templates with slots, and
  example payloads with harmful parts redacted as `[REDACTED: <category>]`. Anything
  gated by the release policy is described, not printed.
- **B. Judge prompt and validation.** Judge model snapshot, full prompt, temperature,
  parsing rule; the human-labelled validation set (size, how sampled, who labelled),
  accuracy, Cohen's κ, precision/recall of "success", confusion matrix; failure modes
  of the judge. (A summary sentence with κ and n stays in the body.)
- **C. Per-model / per-task results.** Full grids behind the body's summary tables,
  generated from the same data files, each cell with n and CI.
- **D. Additional ablations and sensitivity.** Temperature, attempts per task, prompt
  paraphrases, date/snapshot drift checks.
- **E. Cost accounting.** Tokens, calls, $ with price date, wall-clock.
- **F. Synthetic case study.** One end-to-end transcript (synthetic, redacted).
- **G. Reproducibility.** Commands, cached responses, seeds, framework commits,
  hardware for open-weight models (pointer to the artifact README).
- **H. Checklist answers** if the venue puts them in the PDF.

## Rules

- Each appendix section opens with one sentence stating which body result it supports
  (`\Cref` to the body table/figure).
- Appendix tables are generated from the same data files as body tables.
- Every "see the appendix" in the body names the exact subsection label.
- Redaction is consistent: the same payload is redacted identically everywhere.
- Do not `\input` files that are entirely commented out.

## Full version vs proceedings version

Use one shared source with a switch (`\newif\iffull`) so the proceedings build and
the full version (arXiv/artifact) cannot drift apart. Material that does not fit the
proceedings limit lives in `\iffull ... \fi`. If the proceedings version points to a
full version, the full version must be public before the camera-ready deadline. See
`skills/camera-ready`.

## Checklist

- [ ] "Not load-bearing" comment at the top of the appendix source.
- [ ] Judge prompt + validation present; body has the κ/n summary.
- [ ] Prompts and payloads redacted per `ETHICS.md`.
- [ ] Each appendix section states which body results it supports.
- [ ] All body pointers to the appendix are specific labels.
