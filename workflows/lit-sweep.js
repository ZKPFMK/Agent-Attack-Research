export const meta = { name: 'cra-lit-sweep', description: 'Search and position LLM-agent attack papers against the user KB', phases: [{ title: 'Search' }, { title: 'Verify' }, { title: 'Synthesize' }] }
const P = (args && args.project) || '.'
phase('Search')
const hits = await agent(`Read ${P}/STATE.md and the KB path. Search the user attack KB with aa kb-search and public sources with skills/paper-search. Return candidate competitors grouped into 01 external, 02 internal, 03 collaboration, plus defense/benchmark neighbours. Do not edit ledgers.`, { label: 'search', effort: 'low' })
phase('Verify')
const verified = await agent(`Read ${P}/LITERATURE.md and the search result below. Verify the true competitors by opening public abstracts/pages, checking access point, victim state, success metric and n. Update LITERATURE.md, refs.bib and notes/papers/. Mark unresolved network results UNCHECKED. Search result: ${JSON.stringify(hits)}`, { label: 'verify', effort: 'low' })
phase('Synthesize')
return await agent(`Read ${P}/LITERATURE.md, ${P}/STATE.md and the user's KB. Write KB-POSITION.md for the current idea, with nearest KB ids and one falsifiable delta. Do not claim novelty from no search hit.`, { label: 'synthesize', effort: 'low' })
