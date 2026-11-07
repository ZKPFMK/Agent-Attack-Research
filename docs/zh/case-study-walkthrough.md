# 案例走读：toy-agent-attack

> 这是一个离线教学项目，不是漏洞报告，也不估计真实模型的脆弱性。它使用五个 Agent 的 chain、确定性的 `mock-rumor` backend 和合成 claim，演示一个恶意起点 Agent 经过 summarising relay 后的 adoption。唯一变量是 relay 是否保留 source label。

## 一键复现

```bash
cd case-study/toy-agent-attack
PYTHONPATH=../../lib/agentattack python3 code/run_experiment.py
PYTHONPATH=../../lib/agentattack python3 code/check_claim.py
python3 ../../skills/phase-gate/scripts/gate_check.py --project . --phase P6
```

实验使用 `agentattack.mas.Simulation`、`toy.rumor_mock`、`runner.run_matrix` 和 `aa rate`，不访问网络、不调用真实模型。`results/trials.jsonl` 可以断点续跑，`results/rate.log` 是 E1 引用的生成表。

## 项目文件

- `STATE.md`：P0–P8 状态、预算和教学 claim；
- `IDEAS.md`：03 multi-agent collaboration 分支下的 provenance stripping idea；
- `THREAT-MODEL.md`、`threat/toy.json`：一个 peer 的 outgoing message 是入口，目标是观察最终 adoption；
- `ETHICS.md`：synthetic/local only、无 live target、无 working payload；
- `baselines/MANIFEST.md`：clean/no attack、source-label preserved 和 source-label stripped 的对照定义；
- `results/trials.jsonl`、`results/rate.log`：原始 trial 和 Wilson CI；
- `CLAIMS.md`、`EVIDENCE.md`、`falsify/`：主张、证据和独立检查；
- `paper/`：占位论文源文件，完整研究还需要真实的 approved local study、更多模型和正式 release decision。

## 各阶段

### P0 立项

`STATE.md` 将问题写成可证伪句子：在确定性的五 Agent chain 和 seeds 0–39 上，relay 删除 source label 是否使 final adoption 相比保留 label 改变至少 10 个百分点？预算是零网络调用，kill switch 是差异小于 0.10。目标是教学，不是 novelty claim。

### P1 文献与 KB

`LITERATURE.md` 和 `KB-POSITION.md` 说明这个 toy 只用于演示如何把 idea 放到用户的 03 collaboration KB 分支。它不声称击败或取代 prompt infection、message tampering、manipulated knowledge 或 misinformation 论文；真实项目必须先运行 `aa kb-search`、公开文献查新和 `bib-verify`。

### P2 构思

`IDEAS.md` 把一个固定假设写成可释放参数：summarising relay 是否保留 source label。naive baseline 是直接发送 synthetic claim；control 是完全相同的 chain、seed 和 claim，只删除 label。toy parser 的 provenance weighting 是预先声明的机制，结果不能直接外推到 LLM。

### P3 威胁模型与攻击设计

`THREAT-MODEL.md` 规定：攻击者只控制起点 peer 的 outgoing message；不知道 backend 的内部规则；不能修改 system prompt、memory store、操作系统或真实用户数据；victim 是五 Agent chain；success 是最终 Agent 在固定 round 仍采用合成 claim。`aa threat-check threat/toy.json` 必须通过，`ETHICS.md` 记录 local deterministic containment。

### P4 基线

`baselines/MANIFEST.md` 固定相同的 Agent、topology、rounds、task、seed 和 backend。比较 arm 是：

- clean/no attack；
- source label preserved；
- source label stripped。

这里的 preserved arm 是机制对照，不是“最强现实攻击”；真实研究还应加入 naive injection、closest prior attack、static defense 和 adaptive attacker。

### P5 实验

`code/run_experiment.py` 用 `run_matrix` 交错运行两个 arm，每个 arm 40 个 seed，保存 trial、cache、环境和生成 rate。结果格式必须带 `k/n` 和 Wilson 95% CI；toy 输出只能写成 synthetic/mock result。失败记录留在 JSONL，不从结果目录删除。

### P6 证伪

`code/check_claim.py` 从原始 trial 重新计算两臂差异，并检查 kill switch。当前教学 claim C1 为 survived，表述是“在声明的确定性 toy range 内，删除 label 改变 final adoption 至少 10 个百分点”。这不等于“真实 MAS 一定如此”，也不等于 stripping 一定提高 adoption；方向由生成结果决定。

### P7 写作与图表

论文只引用 E1 中的生成值，图表从 `results/` 读取。写作要包含 threat model、toy limitation、无真实模型结论、伦理 containment 和 release policy。若把这个机制带到真实系统，必须重新注册 protocol、验证 judge、加入至少两个 model families/frameworks 和防御 baseline。

### P8 评审与发布

`REVIEWS.md`、`SUBMISSION.md` 和 `bib-verify-report.md` 是教学占位文件。真正上传、披露、公开 artifact 或把结果发送到外部服务前，必须完成人工 release decision；本案例本身不发送任何内容，也不测试 live third-party agent。

## 这个案例要教的事情

1. 先把 access point、victim 和 success criterion 写成机器可检查的 threat model；
2. 同一 claim 要有 no-attack、naive 和 mechanism control；
3. raw JSONL、n、CI、judge 和 EVIDENCE 比一段漂亮 transcript 更重要；
4. falsifier 要从原始记录重算，而不是接受 summary；
5. toy backend 只能验证 harness 和定性机制，不能当作真实模型漏洞证据。
