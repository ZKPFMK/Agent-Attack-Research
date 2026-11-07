# EVIDENCE — every number in the paper traces to a log

> Owner: `experimenter`. Audited by `falsifier` and by `crbench audit-tex paper/main.tex EVIDENCE.md`.
> Rates are printed with n and a 95% CI (`aa rate trials.jsonl --by ... --log results/<exp>/rate.log`).
> The machine column names the model snapshot / backend, the judge fingerprint (if a judge decided success)
> and the host.

> Example row (add real ones with `crbench evidence add`, `cra evidence add` or the `evidence_add` tool;
> the log must exist — its sha256 is recorded in `.cra/evidence-hashes.json`):
> `| E1 | 41.0% | ASR of attack A on victim V, no defense, judge J (kappa 0.82) | aa rate results/main/trials.jsonl --by model,defense --log results/main/rate.log | results/main/rate.log | abc1234 | <model snapshot>, T=0, judge sha 1f2e.. / host:aa | YYYY-MM-DD | n=300, Wilson 95% CI [35.6, 46.6] |`

| ID | value as printed | meaning | command | log path | code commit | machine / model snapshot | date | runs, statistic |
|---|---|---|---|---|---|---|---|---|
