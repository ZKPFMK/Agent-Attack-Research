# Theorist 角色已退休

本仓库现在面向 LLM agent 与多智能体系统攻击研究，默认工作流不再包含密码学理论家角色。该路径仅作为旧中文链接的兼容说明，不应在新的 project 中派工。

- 把攻击想法写成可检查的 attacker goal、access point、capabilities 和 success criterion：使用 [`threat-modeler`](../../../agents/threat-modeler.md)。
- 对传播、预算或攻击优化做 toy formalisation：使用 `lib/agentattack` 和 [`mas-testbed`](../../../skills/mas-testbed/SKILL.md)，并明确标注 toy/mock。
- 由真实 trial 验证 rate、utility、stealth 和成本：使用 [`experimenter`](../../../agents/experimenter.md)。
- 由 [`falsifier`](../../../agents/falsifier.md) 独立攻击每条 claim；只有 survived 或 weakened 才能进入论文。

新的项目不创建 `THEORY.md`、`lean/` 或 `lib/cryptomath` 依赖；相关数学背景若确实需要，作为经核验的普通文献由 `lit-scout` 管理。
