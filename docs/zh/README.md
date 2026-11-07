# agent-attack-research-agents

这是一个面向 **LLM Agent 与多智能体系统攻击研究** 的可审计多智能体科研工具包。它把原来的密码学论文流程
改造成适合用户 `papers/01`、`02`、`03` 三类攻击文章的工作流，并使用 `04–09` 目录中的防御、框架、基准和
虚假信息传播论文作为对照。

- **01 外部交互**：网页/证据/工具/MCP/GUI/视觉/工具选择与资源消耗攻击；
- **02 内部认知**：后门、推理劫持、记忆/RAG 投毒、隐私提取与可用性攻击；
- **03 多智能体协作**：提示感染、消息篡改、恶意 Agent、勾结、组合式提示、操纵知识传播与协作阻断。

核心规则是：先查知识库和已有工作，再写威胁模型；先攻击自己的 claim，再写论文；每个 ASR 都要有样本数和置信区间，
每个论文数字都要回溯到 `EVIDENCE.md`；攻击只允许在自有、离线或沙箱系统中执行。

## 快速开始

```bash
python3 -m pip install -e lib/core -e lib/agentattack -e lib/mcp -e lib/bench
./install.sh /path/to/project
export CRA_KB=/absolute/path/to/Agent安全论文知识库.md
cd /path/to/project && cra init .
```

Claude Code 中使用 `/cra-lit`、`/cra-ideas`、`/cra-phase P3`、`/cra-falsify`；其他客户端使用 `cra-mcp`，每次先调用
`cra_resume`。离线示例位于 `case-study/toy-agent-attack`。
