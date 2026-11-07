# BIGMAP（中文）

![BIGMAP](../bigmap/bigmap.png)

图从上到下六层：

1. **阶段层**：P0 Scoping → P1 Literature & KB → P2 Ideation → P3 Threat model & attack design → P4 Baselines → P5 Experiments → P6 Falsification → P7 Writing + figures → P8 Review / submit / rebuttal / camera-ready；红色虚线是回退路线。
2. **agent 层**：12 个 Agent Attack 角色。PI 总控负责阶段，falsifier 拥有否决权，kb-curator 负责用户 KB 定位，threat-modeler 负责攻击者和入口的可检查定义。
3. **黑板层**：研究项目目录中的 `STATE.md`、`CLAIMS.md`、`EVIDENCE.md`、`LITERATURE.md`、`KB-POSITION.md`、`THREAT-MODEL.md`、`ETHICS.md`、`REVIEWS.md` 和 `baselines/MANIFEST.md`。只有 survived/weakened 的主张和有日志的数字进入 `paper/`。
4. **skills 层**：评测协议、攻击 KB、威胁模型、judge validation、adaptive defense、MAS testbed、伦理披露、写作、图表、匿名和提交脚本。
5. **评测库层**：`lib/agentattack` 提供 ASR/CI、judge agreement、ThreatModel、KB search、local/mock backend、MAS topology、resumable runner；`lib/bench` 提供环境记录和 EVIDENCE 审计。
6. **工具层**：`aa` CLI、`cra-mcp`、本地/沙箱模型、owned testbed、公开文献来源和 LaTeX/Matplotlib/TikZ。网络检索是可选的，实验目标必须是自有、离线或沙箱系统。

用户的攻击论文知识库通过 `STATE.md` 的 `kb:` 或 `CRA_KB` 指定，PDF 树通过 `papers:` 或 `CRA_PAPERS` 指定。04–06 用于防御 baseline，07–09 用于框架、benchmark、传播和信任操纵背景。

交接契约见英文版 `docs/BIGMAP.md`。安全边界见 `SPEC.md` 和 `ETHICS.md` 模板。
