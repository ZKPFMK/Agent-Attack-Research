# IDEAS
## I-1 provenance stripping at a summarising relay (status: controlled)
pre-gate: surface = 03 multi-agent; access point = one peer's outgoing message; harmful-only? no — tests provenance defenses
bottleneck metric: final-agent adoption of a synthetic claim; naive baseline = direct claim injection
freed assumption (Gate A): a relay preserves the source label; fixed in toy summaries
anomaly (Gate B): compare identical claim with and without label; root cause = toy provenance weighting; control = no-label arm
KB delta: synthetic mechanism only; no novelty claim   claims: C1   notes: none   kill switch: difference < 0.10

## Run log
| date | target | freed assumption | anomaly | root cause | control passed? | real-system result | verdict |
|---|---|---|---|---|---|---|---|
| generated | mock chain | source label | computed by script | toy parser | yes | not run on real model | teaching case |
