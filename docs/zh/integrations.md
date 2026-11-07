# 在各 AI 平台上使用 Agent Attack Research Agents

[English](../integrations/README.md) · [平台兼容性参考](../integrations/COMPATIBILITY.md)

本仓库提供两种接入方式：Claude Code 插件中的 agents/skills/commands，以及不依赖特定宿主的 `cra-mcp` 和 `aa` CLI。MCP 服务器只执行确定性的项目工具，不自行调用模型，也不需要 API key；宿主模型负责读取角色卡、写黑板和决定下一步。

## 安装

```bash
git clone <本仓库> ~/agent-attack-research-agents
cd ~/agent-attack-research-agents
python3 -m pip install -e lib/core -e lib/agentattack -e lib/mcp -e lib/bench
./install.sh /path/to/project
export CRA_KB=/absolute/path/to/user/attack-knowledge-base.md
export CRA_PAPERS=/absolute/path/to/papers
cra init /path/to/project
```

在项目的 `STATE.md` 中确认 `kb:` 和 `papers:` 路径。KB 可来自用户的本地知识库，不能把私有论文内容复制进仓库。

## Claude Code、Codex 和其他 MCP 宿主

```bash
cra-mcp install --host claude-code --project /path/to/project
cra-mcp doctor --project /path/to/project
```

可用 host 包括 `claude-code`、`codex`、`gemini`、`cursor`、`cline`、`roo`、`windsurf`、`vscode`、`jetbrains`、`zed`、`opencode`、`continue` 和 `generic`。安装器只写项目内配置，保留其他配置；全局配置只打印建议内容，不自动覆盖。

接入后先让宿主调用 `cra_resume`，再读取 `STATE.md` 和对应角色卡。项目内的 `CLAIMS.md`、`EVIDENCE.md`、`DECISIONS.md` 只能通过专门工具或本地 CLI 更新；阶段门不过不能推进。

## 工具档位

| profile | 用途 |
|---|---|
| `core` | 黑板、claim、evidence、phase gate、decision、project status、role/skill 读取 |
| `full` | core 加公开 paper search、KB search、rate/CI、threat check、audit 和本地文件辅助工具 |
| `remote` | 适合远程 MCP 宿主的受限项目文件访问和只读 search/fetch |

实际工具和数量以 `cra-mcp --help`、`cra-mcp doctor` 和当前 `lib/mcp` 版本为准；不要把旧版本工具名（如 ePrint、core-SVP、textbook lookup）当成 Agent Attack 默认流程。

## OpenAI-compatible 与本地模型

`lib/agentattack/llm.py` 的 `OpenAICompatible` 支持用户明确配置的兼容 endpoint；API key 只从环境变量读取，`CachedBackend` 把 response 写入项目指定的本地 cache。也可以导出 function schema：

```bash
cra-mcp --export openai
cra-mcp --export openai-compat
cra-mcp --export anthropic
cra-mcp --export gemini
```

自定义循环把 tool call 交给同源 `ToolBox`/MCP 工具执行。使用第三方模型 endpoint 前，用户必须知道项目内容和 prompt 会离开本机；默认优先 MockBackend、本地模型或组织批准的沙箱 endpoint。不要把 key 写入项目、日志或 git。

## 远程 HTTP

远程模式只能由用户自行部署在受控环境中，使用 bearer token 或秘密路径、Host/Origin 校验和项目根目录限制。仓库不提供发布、投稿、发邮件、公开 MCP registry 或 live target 操作工具。任何外部发送必须由用户人工批准。

## 平台限制

不同宿主对 prompts、resources、strict schema、审批和 Streamable HTTP 的支持不同。工具调用失败时读取 `violations` 和 `next_actions`，修正原因后再调用；不要重复同一个无效调用。实验仍需在用户自己的终端运行，完成后用 `aa rate` 和 `crbench evidence add` 登记结果。
