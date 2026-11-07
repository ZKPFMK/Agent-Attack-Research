---
name: anonymize-check
description: Use before every double-blind submission, anonymous supplement or rebuttal attachment. Scan TeX, BibTeX, code, archives and PDFs for author identities, private paths, endpoints, metadata, acknowledgements, funding and unredacted project data using a private deny-list.
---

# Anonymize check

Anonymity is a venue requirement and a data-hygiene check. Keep the deny-list private; it may contain author names,
usernames, institutions, private hostnames and project-specific URLs. The scanner does not decide whether a citation
is allowed by a venue, so apply the current CFP manually as well.

## Script

`scripts/anon_check.py` is standard-library only and uses PyMuPDF or poppler when available.

```bash
# 1. keep a private deny-list (never commit a filled-in one publicly)
cp skills/anonymize-check/scripts/denylist.example.txt paper/.denylist.txt   # then edit

# 2. scan sources, the built PDF, the supplementary archive and artifact
python3 skills/anonymize-check/scripts/anon_check.py paper/ paper/main.pdf \
        supplementary.zip artifact/ --deny-file paper/.denylist.txt \
        --allow-url 'github\\.com/<third-party-org>/'

# 3. self-test (synthetic sample; must print PASS)
python3 skills/anonymize-check/scripts/anon_check.py --selftest
```

Exit status is 1 for any HIGH finding. Use `--json` for machine-readable output and `--min-severity MEDIUM` only when
reviewing known informational noise.

## What it flags

| severity | finding |
|---|---|
| HIGH | deny-list term in source, filename or PDF bytes; e-mail; local path (`/home/<u>`, `/Users/<u>`, `C:\Users\<u>`); non-anonymous author/affiliation macros; acknowledgements; author metadata; embedded source path containing a username or deny term; `.git` in an archive; URL containing a deny term |
| MEDIUM | first-person self-citation; personal code-host or profile URL not in the allow-list; funding statement; PDF title/subject/keywords metadata; VCS directory in an artifact; hits inside comments (downgraded one level) |
| LOW | deny term in a bibliography entry, if the venue permits named third-person citations; camera-ready/de-anonymised wording; creator/producer metadata (informational) |

## Manual checks the script cannot do

- Follow the target venue's current self-citation and anonymity policy. Use third person where required, and do not
  replace an identifiable citation with a misleading anonymous placeholder.
- Remove private KB paths, local model endpoints, organization-specific model names, account ids and hostnames from
  cached responses, environment captures, screenshots and figure sources.
- Ensure artifact README does not say “our prior paper”, “same codebase as” or expose a private repository URL.
- Check figures for usernames, terminal prompts, window titles and unredacted transcripts.
- Check the submission form separately: conflicts, author list and abstract fields do not make the PDF anonymous.
- Confirm anonymous mirrors and supplement URLs satisfy the venue's access policy; do not publish or upload from this
  skill without human approval.

## Remediation snippets

```latex
% Empty PDF metadata (hyperref)
\hypersetup{pdfauthor={},pdftitle={},pdfsubject={},pdfkeywords={},pdfcreator={},pdfproducer={}}
% Avoid embedding figure source paths (pdfTeX >= 1.40.15)
\pdfsuppressptexinfo=-1
```

```bash
# strip metadata from a finished PDF when the venue permits it
exiftool -all:all= -overwrite_original main.pdf
qpdf --linearize main.pdf main_clean.pdf
# create an archive without VCS data
zip -r artifact.zip artifact -x '*.git*'
```

Record the final command, summary and PDF SHA-256 in `SUBMISSION.md`. A clean result means the scanner found no
HIGH findings; it does not replace a human review of the CFP or the artifact release decision in `ETHICS.md`.
