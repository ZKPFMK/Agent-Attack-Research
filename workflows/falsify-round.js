export const meta = { name: 'cra-falsify-round', description: 'Adversarially attack every open LLM-agent attack claim with diverse lenses', phases: [{ title: 'Load' }, { title: 'Attack' }, { title: 'Ledger' }] }
const P = (args && args.project) || '.'
const CLAIMS = { type: 'object', properties: { claims: { type: 'array', items: { type: 'object', properties: { id: { type: 'string' }, text: { type: 'string' } }, required: ['id', 'text'] } } }, required: ['claims'] }
const VERDICT = { type: 'object', properties: { verdict: { type: 'string', enum: ['survived', 'weakened', 'refuted'] }, weakened_wording: { type: 'string' }, evidence: { type: 'string' }, script_or_log: { type: 'string' } }, required: ['verdict', 'evidence'] }
const LENSES = [
  'definitions and success criterion: is attack success operational, same across arms, and distinct from capability exposure, vulnerability rate and utility loss?',
  'threat-model realism: can the attacker reach the declared access point with the declared knowledge and budget without already having the claimed effect?',
  'measurement confounds: recompute raw JSONL, compare no-attack and naive injection, validate judge against gold labels, check n, CI, paired tasks, model snapshot and temperature.',
  'defense and adaptive attacker: does the result survive the strongest relevant defense when the attacker knows the defense? Check benign utility and false-trigger rate.',
  'novelty and ethics: compare the user KB plus arXiv/OpenReview/ACL/DBLP/S2 within 30 days; check that release and disclosure do not expose live targets or harmful payloads.'
]
phase('Load')
const { claims } = await agent(`Read ${P}/CLAIMS.md and return every row whose status is open.`, { schema: CLAIMS, effort: 'low' })
log(`${claims.length} open claims`)
phase('Attack')
const results = await pipeline(claims, c => parallel(LENSES.map((lens, i) => agent(`Project: ${P}. Try hard to REFUTE claim ${c.id}: "${c.text}". Lens: ${lens}. Read THREAT-MODEL.md, KB-POSITION.md, EVIDENCE.md and raw results. Run a real script under ${P}/falsify/${c.id}/ when possible. If uncertain answer weakened with precise wording; never invent numbers.`, { agentType: 'falsifier', phase: 'Attack', label: `${c.id}:lens${i + 1}`, schema: VERDICT }))).then(vs => {
  const v = vs.filter(Boolean), refuted = v.filter(x => x.verdict === 'refuted').length, weakened = v.filter(x => x.verdict === 'weakened').length
  return { ...c, status: refuted >= 2 ? 'refuted' : (refuted + weakened ? 'weakened' : 'survived'), votes: v }
}))
phase('Ledger')
await agent(`Update ${P}/CLAIMS.md: for each result set status and append falsifier evidence with script/log paths. For weakened claims include the replacement wording. Do not delete rows. Add any phase loop or ethics decision to DECISIONS.md. Results: ${JSON.stringify(results.filter(Boolean), null, 1)}`, { label: 'write-ledger', effort: 'low' })
return results.filter(Boolean).map(r => ({ id: r.id, status: r.status }))
