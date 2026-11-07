# ETHICS — harm, containment, release, disclosure

> `threat-modeler` owns "Harm assessment / containment" (per variant); `submission-rebuttal` owns the
> disclosure log and release decision. Procedure: skills/ethics-disclosure.

## Ground rules (project-wide)
- Attacks run only against owned or locally hosted systems and sandboxed benchmarks; never live third-party
  agent products, public registries/pages, real users or real accounts.
- API keys are project-owned and never committed; payload corpora live outside the repo.
- Findings that transfer to a deployed product are disclosed to the vendor before publication.

## TM-<n> harm & containment   (<YYYY-MM-DD>)
harm: <who/what could be harmed; severity; uplift vs public work; defender value>
containment: <sandbox, models, no-live-targets statement, key ownership, payload storage>
release: full | redacted | on-request | none — <rationale>

## Disclosure log (append-only)
| date | vendor / maintainer | channel | what was reported (finding id, no payload here) | response | embargo until | status |
|---|---|---|---|---|---|---|

## Release decision
| artifact item | level (full / redacted / on-request / none) | reason | approved by |
|---|---|---|---|
