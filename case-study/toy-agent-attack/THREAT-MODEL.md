# THREAT-MODEL
### TM-1 — synthetic label relay (claims: C1; surface: 03 collaboration; status: checked)
**Goal.** Cause a downstream toy agent to answer YES to a synthetic bridge-closure probe.
**Victim system.** Five deterministic mock agents in a directed chain; one summarising relay; no tools or persistence.
**Access point.** The first agent's outgoing message, controlled by the toy simulation.
**Knowledge.** black-box: topology and toy rule are declared.
**Capabilities.** Control one outgoing message per round.
**Constraints / stealth.** Synthetic claim only; no network; 40 fixed seeds.
**Success criterion.** Final non-malicious agent answers YES to the probe.
**Defenses assumed.** Source label preservation is the control; no deployed defense.
**Out of scope.** Real models, users, services, credentials, live pages, model weights.
**Realism.** This is a teaching simulation, not evidence of access in a deployed system.
