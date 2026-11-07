# Paper template for agent-attack research

A neutral `article` skeleton for papers about attacks, defenses and evaluations of LLM agents or multi-agent
systems. It keeps one source for anonymous submission, full version and camera-ready; adapt the document driver
to the target venue's current template before submission. Do not vendor `acmart`, IEEE, ACL, NeurIPS, ICLR,
USENIX or other classes into this repository.

## Files

- `main.tex`: anonymous submission driver.
- `main_camera.tex`: camera-ready driver; reads `authors.tex`.
- `main_full.tex`: full technical/artifact version.
- `macros.tex`: `\\claimref{C<n>}` and `\\evid{E<n>}` provenance markers.
- `sections/`: abstract, introduction, background/related work, threat model, attack design, evaluation,
  defenses, discussion/ethics, conclusion and appendix.
- `Makefile`: `make`, `make camera`, `make full`, `make check`, `make anon`, `make clean`.

Numbers in the paper must have an EVIDENCE row, and claims must resolve to survived/weakened CLAIMS rows.
Use synthetic prompts/transcripts in the template. Read the current CFP and responsible-research policy for the
chosen security or ML/NLP venue before changing the driver.
