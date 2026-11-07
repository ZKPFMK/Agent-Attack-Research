---
name: artifact-pack
description: Package a reproducible, anonymous and safely redacted artifact for an LLM-agent attack paper. Use for review supplements, artifact evaluation and camera-ready release.
---
# artifact-pack

The artifact must reproduce the paper's controlled evidence without becoming a ready-to-run attack against a live
service. A reviewer should be able to run the mock path without credentials or network access.

## Package layout

```text
artifact/
  README.md                 # one-command smoke run, expected output shape and limits
  pyproject.toml            # pinned local dependencies, no secrets
  run_smoke.sh
  configs/                  # synthetic tasks and threat models
  src/                     # agentattack adapter / evaluation code
  tests/
  expected/                # tolerances and schema, not fabricated headline values
  results/                  # generated, ignored raw cache
  REDACTION.md             # what is omitted and why
```

## Procedure

1. Map every paper claim/number to a command, source file, model snapshot or cached response and EVIDENCE row.
2. Include `lib/agentattack` mock backend and a synthetic testbed. If a real model is needed, provide a local
   adapter and a clear user-supplied snapshot path; do not include API keys or make network calls by default.
3. Pin dependencies and public baseline commits. Check model/provider licenses and ToS; do not redistribute a
   proprietary model, private transcript, real user data or copyrighted PDF.
4. Redact working payloads, live URLs, credentials, canaries that could affect production systems, personal data
   and private research details. Explain the redaction and give a non-transferable synthetic substitute.
5. Run the smoke command from a clean checkout with network disabled. Check output schema, metric definitions,
   threat-check, judge configuration and no path leaks.
6. Include a claims-to-commands map, expected tolerances, environment capture and failure troubleshooting.
7. Run anonymisation, secrets scan, tests, `crbench audit-tex` and the artifact's own release checklist.
8. Record the artifact release level in ETHICS.md: `full`, `redacted`, `on-request` or `none`, with a human
   approval and disclosure status. Publishing is a separate human-approved action.

## Failure gate

Stop if the package contacts a live service, contains a secret or private data, depends on an unavailable hidden
resource without saying so, or makes the harmful mechanism easier to deploy than the paper's defensive value.
