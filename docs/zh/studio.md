# CRA Studio：桌面工作台

[English](../studio.md) · [各平台接入](integrations.md)

CRA Studio 把 Agent Attack research toolkit 打包成一个本地可执行程序，包含图形界面、`cra-mcp` 服务器、`cra` CLI 和 `cra-agent` 循环。它用于查看黑板、调用角色和工具、运行门检并审批项目内写入。

## 获取与运行

- 从 release 下载对应平台的构建，或用 `pyinstaller` 从源码构建；
- 从源码安装：

```bash
python3 -m pip install -e lib/core -e lib/agentattack -e lib/mcp -e lib/bench -e lib/studio
cra-studio
```

程序只绑定 `http://127.0.0.1:8770`。打开项目后可以查看 phase、open claims、evidence 行、gate 结果、`STATE.md` 和下一项任务。

## 使用

1. 在 Project 中打开或初始化一个研究目录；
2. 在 Settings 中配置允许的本地或兼容模型 endpoint。API key 只写入本机用户配置，保存后不能从 UI 读回；
3. 在 Overview 查看 P0–P8 状态、风险和 `next_tasks`；
4. 在 Research Assistant 中让模型通过 cra 工具读取和更新项目。每次 tool call 和返回都显示；`phase_advance`、账本写入等破坏性动作需要人工批准；
5. 在 Ledger 查看 `CLAIMS.md`、`EVIDENCE.md`、`DECISIONS.md` 和审计结果；
6. 在 Integrations 为 Claude Code、Codex、Cursor、Cline、VS Code 等宿主生成 MCP 配置。

实验由用户在本地或沙箱终端执行，结果写入 `trials.jsonl` 后再用 `aa rate` 和 `crbench evidence add` 登记。Studio 不替用户访问 live third-party agent，也没有投稿、发邮件或公开发布功能。

## 命令模式

```text
CRA-Studio                                      图形界面
CRA-Studio mcp --project <dir> [--http]        cra-mcp（stdio / Streamable HTTP）
CRA-Studio install --host <host> --project <dir> 生成宿主配置
CRA-Studio agent --model <id> --project <dir>  OpenAI-compatible agent loop
CRA-Studio cra <args>                           黑板 CLI
CRA-Studio doctor --project <dir>              自检
```

## 安全

界面只监听本机；请求需要启动时生成的 token 和合法 Host；模型接口会看到用户发送的 prompt 以及 agent 读取的项目文件，因此应选择用户批准的本地、组织内或沙箱 endpoint。项目规则仍要求不把 secrets、credentials、personal data、私有研究内容和工作 payload 放进 git。
