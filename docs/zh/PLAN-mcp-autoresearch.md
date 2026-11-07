# Agent Attack：MCP 与可审计研究循环

> 状态：核心迁移已完成；本文件记录当前架构、约束和后续路线。它是设计说明，不是另一套旧密码学流程。

## 目标

把面向 LLM agent/MAS 攻击研究的黑板、门检、KB 查询、威胁模型、评测指标和证据台账提供给不同 AI 宿主，同时保留本地、可审计和可暂停的研究循环。服务器是确定性状态机和工具箱，宿主模型是 worker；服务器默认不调用大模型。

## 已实现能力

- `lib/core`：P0–P8 phase gate、claims/evidence/decision 不变量、STATE、文件锁、事件流和项目初始化；
- `lib/agentattack`：Wilson rate/CI、judge agreement、ThreatModel、KB parser/search、Mock/OpenAI-compatible/Cached backend、MAS topology/injection hooks、resumable runner；
- `lib/mcp`：paper search、KB search、rate/CI、threat check、黑板和 gate 工具；
- `lib/bench`：环境记录、raw log parsing、EVIDENCE ledger、`audit-tex`；
- `cra-mcp` profiles：core/full/remote；`install --host` 生成宿主配置；
- Studio：本地 UI、MCP、CLI、agent loop 和审批；
- skills/agents：攻击 KB、威胁模型、judge validation、adaptive evaluation、MAS testbed、ethics/disclosure、baseline pin、figure 和 submission 流程。

## 研究循环

```text
cra_resume
  → claim_register(open + kill switch)
  → falsify-first
  → threat_check + ETHICS containment
  → baseline pin
  → trial protocol + mock pilot
  → interleaved trials + cache
  → aa rate / aa kappa / evidence_add
  → falsifier verdict
  → gate_check
  → phase advance（只由 orchestrator）
```

每个真实实验前都要冻结 protocol；每个 trial 记录 arm、model/snapshot、framework、defense、task、seed、temperature、success、utility、detected、tokens、queries、cost、judge fingerprint 和 transcript path。中断可从 JSONL 恢复，失败不删除。

## 研究边界

攻击只允许在 owned、local 或 sandbox target 上运行；不得访问 live third-party service、真实用户/账号、生产网页、公开 MCP registry、credentials、personal data 或私有研究内容。working payload 只放在项目外的受控目录；发布决策按 `ETHICS.md` 记录为 `full`、`redacted`、`on-request` 或 `none`。外发、披露、投稿和公开发布没有自动工具，必须人工批准。

## 后续路线

1. 继续完善用户 `papers/01–09` 的本地 KB/论文扫描和 paper-search 适配；
2. 为 `aa sim` 与真实 backend 增加更严格的 transcript schema、judge fixtures 和 cost accounting；
3. 扩展 `baseline-pin` 的框架/benchmark recipe，但不把第三方源码 vendoring 进仓库；
4. 完善 figures、中文镜像和跨宿主文档；
5. 在 CI 中运行 core、agentattack、MCP、Studio、bench、skills 和 figures 的全套检查。

验收标准是：新项目能从 P0 初始化，KB 和 threat model 能过 gate，toy case 能离线复现，所有印刷数字可由 EVIDENCE 重算，且 quick check 不再引用已删除的 crypto 专用包或 skills。
