export const meta = { name: 'cra-idea-tournament', description: 'Generate, position and kill candidate LLM-agent attack ideas', phases: [{ title: 'Generate' }, { title: 'Screen' }, { title: 'Select' }] }
const P = (args && args.project) || '.'
phase('Generate')
const out = await parallel(['01 external interaction', '02 internal cognition', '03 multi-agent collaboration', 'cross-surface defense-aware'].map((axis, i) => agent(`Project ${P}. Read STATE.md, LITERATURE.md, KB-POSITION.md and the user KB. Generate one attack idea on ${axis}. Name access point, mechanism, naive baseline, metric, kill switch and why it is not just more agents/topology. Use toy/sandbox examples only.`, { label: `axis-${i}`, effort: 'low' })))
phase('Screen')
const screen = await agent(`Project ${P}. Read the candidate ideas below and the KB. For each, try to kill it using a one-line pilot or prior-art comparison. Return survivors, weakened ideas and dead ideas with reasons. Do not write paper prose. ${JSON.stringify(out)}`, { label: 'screen', effort: 'low' })
phase('Select')
return await agent(`Project ${P}. Write IDEAS.md and KB-POSITION.md for the selected candidate(s), then register every dependent paper-facing claim as open in CLAIMS.md. ${JSON.stringify(screen)}`, { label: 'select', effort: 'low' })
