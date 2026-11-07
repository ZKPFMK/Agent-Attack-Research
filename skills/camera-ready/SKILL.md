---
name: camera-ready
description: Prepare the final version of an LLM-agent attack paper after acceptance: current venue format, evidence/claim audit, anonymisation, ethics/disclosure, safe artifact and clean compile. Use only after the draft is frozen.
---
# camera-ready

Acceptance does not broaden the threat model or grant permission to release harmful material. Follow the accepted
venue's current instructions, copyright/licence forms and responsible-research policy.

## Checklist

### Content and evidence

- [ ] every paper claim maps to a survived/weakened CLAIMS row with adopted wording;
- [ ] every number/rate maps to EVIDENCE.md, with n, CI, raw log, code commit, model snapshot and judge fingerprint;
- [ ] no withdrawn or superseded rate remains in abstract, tables, captions, appendix or artifact README;
- [ ] threat model, limitations, benign utility, adaptive defense and ethics/disclosure text match the final evidence;
- [ ] citations pass bib-verify and every KB/public characterization has been checked against the source.

### Build and anonymity

- [ ] final venue class, page limit, fonts, metadata, supplement and copyright forms follow the current CFP;
- [ ] clean checkout compiles with no undefined refs, missing figures or significant overfull boxes;
- [ ] `crbench audit-tex paper/main.tex EVIDENCE.md` passes;
- [ ] `anon_check` scans TeX, BibTeX, PDF metadata, compressed streams, paths, e-mails, author names, personal
      repositories and model-hosting URLs as required by the venue;
- [ ] no private KB path, API key, username, local hostname or raw transcript is embedded.

### Ethics, disclosure and artifact

- [ ] ETHICS.md records harm, containment, vendor disclosure or a reason no disclosure was needed;
- [ ] release decision is explicit per code, prompts, payloads, transcripts, weights and cached responses;
- [ ] artifact runs offline in its mock/synthetic path from a clean checkout;
- [ ] model/provider licences and ToS allow every distributed component;
- [ ] a human approved every upload, disclosure, public repository, e-mail and submission.

## Final commands

```bash
cra gate P8 --paper paper
crbench audit-tex paper/main.tex EVIDENCE.md
python3 skills/anonymize-check/scripts/anon_check.py paper/ refs.bib
python3 skills/artifact-pack/scripts/package.py . --out artifact/   # if the skill script is available
```

If any check is unavailable, record the skipped check and reason in SUBMISSION.md; do not represent it as passed.
