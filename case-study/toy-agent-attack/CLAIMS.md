# CLAIMS
| ID | claim (precise, falsifiable, with parameter range) | proposer | status | falsifier evidence / counterexample | EVIDENCE / THREAT-MODEL refs |
|---|---|---|---|---|---|
| C1 | On the deterministic five-agent chain and seeds 0..39, removing the source label at the summarising relay changes final adoption by at least 10 percentage points versus preserving it. Kill: absolute difference < 0.10. | idea-miner | survived | `python3 code/check_claim.py` recomputes both arms from raw trials; no counterexample in the declared toy range. | E1, THREAT-MODEL TM-1 |
