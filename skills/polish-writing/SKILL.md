---
name: polish-writing
description: Use for a final language pass on a paper section, or when translating a Chinese draft into English academic prose. Removes AI-sounding phrasing, tightens sentences, enforces consistent notation and terminology, and never changes numbers, claims or LaTeX semantics.
---

# Polish writing

## Invariants (never violate)

- Do not change numbers, CIs, n, threat-model statements, success criteria,
  citations, labels or math.
- Do not strengthen claims ("in 3 of 4 models" → "across models", "evaluated
  defenses" → "all defenses", "reduces" → "eliminates", "sandboxed" → "real-world").
- Keep LaTeX commands intact, including `\evid{...}` and `\claimref{...}` tags; do not
  introduce packages.
- Never "un-redact" or paraphrase a redacted payload into a working one.
- In the last 24 hours before a deadline: no style passes at all, only error fixes.
- Output: revised text + a short modification log (what and why) so the author can
  accept/reject each change.

## Pass 1 — de-AI

Replace or delete:

| avoid | prefer |
|---|---|
| leverage, utilize | use |
| delve into, explore (as a result) | examine, study (or state the result) |
| pivotal, crucial, paramount | important, key (or delete) |
| underscore, highlight (as filler) | show |
| tapestry, landscape, realm | (delete; name the area) |
| seamless(ly), robust (without a metric) | (delete or quantify) |
| "It is worth noting that", "Notably," | (delete; state the fact) |
| "In this paper, we aim to" | "We ..." |
| "First and foremost", "Last but not least" | (delete) |
| "plays a crucial role in" | "determines", "dominates" (be specific) |
| "novel" about own work | (delete; let the reader judge) |
| "significantly" without numbers | the number |
| "obviously", "it is easy to see" | give the one-line reason, or delete |
| "the agent believes/wants/decides" | "the agent outputs/selects/forwards" (what was measured) |
| "devastating", "alarming", "catastrophic" | the measured effect and its scope |
| "real-world attack" (for a sandbox) | "in a sandboxed deployment of <framework>" |

Also: convert `itemize` inside running text into connected prose when the items are
reasoning steps (keep lists for contributions/parameters); avoid three connectives
in a row; vary sentence openings; no rhetorical questions in the body.

## Pass 2 — concision

- One idea per sentence; aim for ≤ 30 words.
- Remove throat-clearing openers and doubled phrases ("in order to" → "to",
  "the fact that" → "that", "a number of" → "several"/the number).
- Prefer verbs over nominalisations ("perform an evaluation of" → "evaluate").
- Active voice for what *we* did; passive is fine for standard facts.
- Avoid dashes as sentence punctuation (use commas, colons, or split sentences).

## Pass 3 — consistency

- Terminology: one name per concept (attack name, roles, metrics, baseline names).
  Build a term list from `paper/NOTATION.md` and `grep` for variants
  (e.g. "malicious agent"/"adversarial agent"/"compromised agent",
  "attack success rate"/"ASR"/"success rate", "multi-agent system"/"MAS"/"multi-agent
  framework", "prompt injection"/"prompt-injection").
- Model names: full snapshot id at first use, the same short name afterwards; never
  mix a family name ("the GPT model") with a specific snapshot.
- Notation: symbols match the notation table; no symbol reused with two meanings.
- Spelling variety: pick US or UK and stay with it.
- Capitalisation of references: `Section~\ref`, `Table~\ref`, or `\Cref` consistently;
  non-breaking spaces before `\cite` and `\ref`.
- Numbers: consistent precision for rates (e.g. one decimal for percentages), the
  same CI format everywhere (`41.0 [35.2, 47.0]`), "pp" or "points" for differences
  of rates (never "%" for a difference in percentage points).

## Pass 4 — Chinese → English (for drafts written in Chinese)

1. Translate meaning, not word order: Chinese topic-comment sentences often become
   English subject-verb sentences with the conclusion first.
2. Split long Chinese sentences joined by commas (一逗到底) into several English
   sentences.
3. Watch for common calques: "has important significance" → "matters because ...";
   "realize/achieve an algorithm" → "implement"; "the proposed scheme" repeated →
   name it once, then "our scheme"/its name; "in recent years" as an opener → delete or
   give the year range; "greatly improve" → the number; "攻击成功率高达" → the rate
   with its scope, not "up to"; "智能体认为" → what the agent output.
4. Articles: every singular countable noun needs a/the; "the" for things already
   introduced or unique ("the orchestrator of [X]").
5. Tense: present for facts and what the paper does; past for what prior work did
   or for experiments that were run.
6. Produce three parts: `[LaTeX]` English text, `[Back-translation]` literal Chinese
   of the English (so the author can check meaning), `[Log]` list of changes.

## Pass 5 — read-aloud check

Read the abstract and the first page aloud (or via TTS). Any sentence that needs a
second breath gets split.
