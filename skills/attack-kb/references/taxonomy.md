# Attack taxonomy distilled from the user's KB

This is a method-level index for positioning ideas. The source KB and paper PDFs remain outside this repository;
exact claims and numbers must be checked against the public paper. IDs use the user's folder/KB convention.

## 01 — external interaction

| branch | representative public work (id; venue/year) | mechanism axis |
|---|---|---|
| web/content and evidence | `24_arxiv(preprint)_wipi` (arXiv 2024); `26_ndss_obliinjection` (NDSS 2026); `25_icml_advagent` (ICML 2025); `26_aaai_fact2fiction` (AAAI 2026) | attacker-controlled web or retrieved evidence is interpreted as instructions or misleading support |
| chat/role boundary | `26_iclr_chatinject` (ICLR 2026); `26_icml_role_confusion` (ICML 2026) | serialised roles, authority cues or reasoning style are confused with trusted instructions |
| visual/UI environment | `25_iclr_eia` (ICLR 2025); `25_acl_popup_attacks` (ACL 2025); `25_neurips_mip_against_agent` (NeurIPS 2025) | pixels, DOM/ARIA, pop-ups or image patches alter perception and action selection |
| tool/MCP metadata and choice | `25_neurips_attractive_metadata` (NeurIPS 2025); `26_aaai_mpma` (AAAI 2026); `26_aaai_mcptox` (AAAI 2026); `26_ndss_tool_selection_injection` (NDSS 2026) | descriptions, preferences or schemas steer retrieval and invocation toward a malicious tool |
| toolchain/resource consequence | `26_sp_parasites_toolchain` (S&P 2026); `26_acl_webagents_cost_attacks` (ACL 2026) | an accepted tool action creates a cross-tool consequence or consumes disproportionate resources |
| evaluation/search infrastructure | `24_neurips(datasets-benchmarks)_agentdojo` (NeurIPS 2024); `25_emnlp(findings)_agentvigil` (EMNLP Findings 2025); `26_iclr_vpi_bench` (ICLR 2026); `26_icml_safesearch` (ICML 2026) | dynamic tasks and automated red-team search define how external attacks are measured |

## 02 — internal cognition

| branch | representative public work (id; venue/year) | mechanism axis |
|---|---|---|
| training/model backdoor | `24_acl_badagent` (ACL 2024); `24_neurips_watch_out_agents` (NeurIPS 2024); `25_emnlp(findings)_demonagent` (EMNLP Findings 2025) | a trigger activates an implanted policy or action-level deviation |
| reasoning and availability | `25_icml_udora` (ICML 2025); `26_acl_stop_fixating_prompts` (ACL 2026); `25_emnlp_breaking_agents` (EMNLP 2025) | reasoning, constraints or malfunction feedback is redirected to change actions or amplify failure |
| memory/RAG poisoning | `24_neurips_agentpoison` (NeurIPS 2024); `25_neurips_memory_injection` (NeurIPS 2025); `26_icml_memincept` (ICML 2026); `26_acl_visual_inception` (ACL 2026) | normal write/retrieval paths preserve attacker-controlled state and reactivate it later |
| privacy and knowledge files | `25_acl_agent_memory_privacy` (ACL 2025); `25_acl_gpt_spills_tea` (ACL 2025) | black-box interaction extracts remembered private content or hidden knowledge files |
| propagation crossover | `24_icml_agent_smith` (ICML 2024) | a multimodal or state payload spreads between many agents |

## 03 — multi-agent collaboration

| branch | representative public work (id; venue/year) | mechanism axis |
|---|---|---|
| roles/collusion/covert channel | `23_arxiv(preprint)_evil_geniuses` (arXiv 2023); `24_neurips_secret_collusion` (NeurIPS 2024); `26_acl_lying_with_truths` (ACL 2026) | cooperating agents coordinate through role-compatible public or hidden messages |
| infectious/distributed prompts | `25_esorics(workshop)_prompt_infection` (ESORICS Workshop 2025); `25_acl_contagious_jailbreak` (ACL 2025); `25_aaai_multiagent_security_tax` (AAAI 2025); `26_acl_conjunctive_prompt_attacks` (ACL 2026) | a message or split trigger is copied, routed or jointly recombined across agents |
| message tampering and hidden agents | `25_acl(findings)_communication_attacks` (ACL Findings 2025); `25_acl_agents_under_siege` (ACL 2025); `25_arxiv(preprint)_whos_the_mole` (arXiv 2025); `26_aaai_attack_messages` (AAAI 2026) | the communication layer or an intention-hiding participant changes what peers observe |
| malicious code/control flow | `25_colm_mas_malicious_code` (COLM 2025); `26_aaai_shadows_in_code` (AAAI 2026); `26_acl_evo_attacker` (ACL 2026) | collaborative software/tool execution turns messages into persistent or privileged actions |
| manipulated knowledge and belief | `26_acl_lying_with_truths` (ACL 2026); `26_scis_flooding_manipulated_knowledge` (Science China Information Sciences 2026) | true fragments or persuasive false knowledge are assembled and propagated to alter collective belief |
| blocking and resilience | `26_acl(findings)_corba` (ACL Findings 2026); `25_icml_faulty_agent_resilience` (ICML 2025) | recursive blocking or faulty participants reduce collaboration and expose topology dependence |

## Defense and benchmark neighbours

Use `papers/04_防御_外部交互`, `05_防御_内部认知`, `06_防御_多智能体协作`, `07_安全框架`, `08_安全评测基准`
and `09_虚假信息传播与信任操纵` as baseline sources. The same id may appear in more than one conceptual
branch; compare access point, victim state and success criterion before merging rows.

## Positioning rule

A changed topology, more agents, longer prompts or a stack of known attacks is a configuration unless the
paper identifies a new attacker capability, entry point, mechanism or measurable trade-off. `KB-POSITION.md`
must state the difference in one falsifiable line.
