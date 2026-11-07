# Agent Attack 论文写作手册（中文摘要）

> 英文原文：`skills/paper-playbook/`。本文件是中文镜像，冲突时以英文 skill 和目标 venue 的 CFP 为准。
> 相关技能：`abstract-craft`、`technique-overview`、`related-work-writing`、`experiments-writing`、`threat-model`、`ethics-disclosure`、`venue-calibration`、`mock-review`、`rebuttal`、`anonymize-check`、`camera-ready`、`artifact-pack`、`polish-writing`。
> 所有 toy/mock 数字都必须明确标注，不能表述为真实漏洞结果。

## 总原则

1. 每个数字只有一个来源：从 `trials.jsonl` 生成表格，在 `EVIDENCE.md` 留命令、日志、commit、snapshot、日期和 n/CI。
2. 每条贡献先写成 `CLAIMS.md` 的可证伪行，经过 falsifier 后才能写进正文。
3. 先查用户 KB 和公开文献，再声称 novelty；KB 位置写入 `KB-POSITION.md`。
4. 威胁模型决定攻击者知识、能力、访问点、victim 和 success criterion；正文不能偷偷扩大攻击者。
5. 攻击只能在 owned/local/sandbox 系统运行；payload、transcript、endpoint 和个人数据按 `ETHICS.md` 脱敏。
6. 投稿前重跑 judge、baseline、defense、匿名、bib、EVIDENCE 和 release 检查；截止前 24 小时只修可验证错误。

## 推荐结构

| 节 | 任务 |
|---|---|
| Abstract | 研究缺口 → 攻击机制 → 条件化结果、限制和 artifact |
| Introduction | agent/MAS 场景、具体失效、现有攻击与防御的缺口、研究问题、贡献 |
| Background / Related Work | 按 01 外部交互、02 内部认知、03 多智能体协作组织，并连接 04–09 |
| Threat Model | attacker goal、knowledge、capabilities、access point、victim、success rubric、stealth、defenses、out-of-scope、realism、ETHICS |
| Attack Design | payload 进入点、状态或消息变化、传播/优化过程、预算、不可转移的假设 |
| Evaluation | models/snapshots、framework/topology、tasks、arms、judge κ、n、温度、cost、raw cache、失败计数规则 |
| Defenses | static defense、adaptive attacker、utility-under-defense、false-trigger、检测和开销 |
| Discussion & Ethics | 机制边界、负结果、可迁移性、危害、containment、release、disclosure |
| Conclusion / Appendix | 只重述已存活结果；附录给协议、额外表格和脱敏复现细节 |

安全 venue 应尽早出现 threat model、攻击者成本、防御和 disclosure；ML/NLP venue 应说明 model coverage、ablation、limitations 和 responsible research 要求。页数与计数口径只以当前 CFP 为准。

## 关键写法

- rate 写为 `41.0% [35.2, 47.0] (n=300)`，不要写裸百分比；
- 表格至少包含 no-attack、naive injection、closest prior、proposed、ablation、defense 和 adaptive arm（不适用时记录原因）；
- ASR 旁边说明 success rubric、judge fingerprint、人工 agreement 和 κ；
- utility 同时报告无攻击和受攻击，stealth 报 detection，成本报 query/token/latency/估计金额；
- 模型名称带完整 snapshot id、provider 和 API/weights 日期；
- payload 示例只能是抽象、截断或合成内容，不出现针对真实产品的工作利用串；
- 图表从日志生成，图注写 n/CI、模型、defense、topology 和 toy/mock 标记；
- 贡献措辞不能超过 `CLAIMS.md` 的 survived/weakened 文本，weakened 必须使用窄化后的表述。

## 一致性检查

写作完成后检查：摘要、引言、评测和结论的 attack name、access point、snapshot、数字和条件一致；`paper/` 中每个数字有 `EVIDENCE`；每条 claim 有 verdict；`THREAT-MODEL.md`、`ETHICS.md`、artifact 和 release decision 一致；运行 `crbench evidence check`、`crbench audit-tex`、`bib-verify`、`anon_check.py`、PDF checks 和 mock review。
