export const meta = { name: 'cra-mock-review-panel', description: 'Run venue-calibrated reviews of an LLM-agent attack paper', phases: [{ title: 'Review' }, { title: 'Verify' }, { title: 'Route' }] }
const P = (args && args.project) || '.', V = args?.venue || 'security or ML/NLP venue'
phase('Review')
const personas = ['security expert skeptic: threat-model reachability, adaptive defenses, disclosure', 'ML/NLP generalist: mechanism clarity, metric/judge validity, novelty vs KB', 'implementer: snapshots, seeds, framework, cache, artifact reproducibility', 'ethics reviewer: live-target boundaries, payload release, vendor disclosure']
const reviews = await parallel(personas.map((p, i) => agent(`Review ${P}/paper for ${V}. Persona: ${p}. Read CLAIMS.md, EVIDENCE.md, THREAT-MODEL.md, ETHICS.md and LITERATURE.md. Return critical/major/minor findings with an executable fix and evidence id or missing evidence.`, { label: `persona-${i}`, effort: 'low' })))
phase('Verify')
const checked = await parallel(reviews.filter(Boolean).map((r, i) => agent(`Adversarially verify these review findings against ${P}'s files and raw logs. Keep only real findings, say what command or file proves each. ${JSON.stringify(r)}`, { label: `verify-${i}`, effort: 'low' })))
phase('Route')
return await agent(`Write ${P}/REVIEWS.md with verified findings, severity, evidence and owner agent. Route missing experiment findings to experimenter, threat gaps to threat-modeler, KB gaps to kb-curator, and ethics/release findings to submission-rebuttal. ${JSON.stringify(checked)}`, { label: 'meta-review', effort: 'low' })
