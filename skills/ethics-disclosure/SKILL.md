---
name: ethics-disclosure
description: Contain, assess and responsibly disclose research on attacks against LLM agents and multi-agent systems. Use before any attack run that could transfer to a deployed system, before releasing artifacts, and for the paper's ethics section.
---
# ethics-disclosure

Security research is useful only when the experiment is controlled and the release does not create a cheaper
harm path than the paper's defensive value. This skill governs the project record; it does not replace the target
venue's current ethics policy.

## Before running

- Use a local/open model, a project-owned API, or a benchmark sandbox. Do not test live third-party agents,
  public web pages, MCP registries, real users, accounts or production data.
- Remove API keys, cookies, personal data, customer data and real secrets from prompts and logs. Use synthetic
  canaries, toy tools and synthetic misinformation.
- Keep working payloads and raw transcripts outside git when they could transfer to a live service. Commit
  redacted templates and the mock backend needed for reproduction.
- Record the threat model, harm assessment, containment, data retention and release level in ETHICS.md.

## Harm assessment

For each variant, write who could be harmed, the impact (privacy, integrity, availability, code execution,
misinformation), likely transferability, required access, uplift over public work, and defender value. Register
uncertain claims as open claims. Explain why the experiment cannot be performed on a live target.

## Disclosure procedure

1. If a result transfers to a named vendor or service, identify the maintainer's public security channel.
2. Prepare a minimal report: affected component, reproducible high-level condition, impact, safe evidence,
   containment already applied, and a suggested mitigation. Do not place a working exploit or secret in the repo.
3. Send only after human approval. Record date, channel, finding id, response, embargo and status in ETHICS.md.
4. Respect the vendor's response and the venue's deadline policy. Escalate only through published channels.
5. Before publication, update the release decision: full, redacted, on-request or none for code, prompts,
   payloads, model outputs, weights and transcripts.

## Release gate

A harmful artifact is blocked if it targets a live service, contains credentials or personal data, enables an
unbounded attack, violates a model/provider licence or ToS, or has no defensible containment. The paper may
still report the measured, redacted mechanism and a reproducible mock experiment.
