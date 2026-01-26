# AI Programming Toolkit

> 个人 AI 编程工具集 - Skills、Plugins、MCP Servers 等

个人维护的 AI 编程相关工具集合，包含 Claude Code Skills、插件、MCP 服务器等，用于提升 AI 辅助编程效率。
## Quick Install
```bash
/plugin marketplace add z-soulx/ai-toolkit
/plugin install image-alt-title-filler@z-soulx
```
## 新手知识

**Agent（智能体）**：负责“理解目标 → 拆解计划 → 调用工具 → 读结果 → 再迭代”的执行体（带状态、会规划、会行动）。

- **勘误：** Agent 的“执行体”一定是一个 runtime（*CLI/SDK/程序*），可以是（Python/TS）来写“你自己的 Agent 程序”，也可以用*文件声明Subagent(但依赖主agent CLI本身，CLI就是一个agent执行体agentic runtime)*。
- subagent相比skill 一个“分身”，**独立上下文**、独立权限/工具集，专门跑一类任务（比如 code review）。 可以把“噪音”隔离在子上下文里，主对话只拿总结

**Tool（工具）**：确定性的能力接口（读写文件、跑命令、查 API、访问数据库……）。

- 内置 tools 和 利用MCP扩展tool(:bulb: *Tool 和 MCP 不是同一层的概念,着重利用*)。

**Command**：Slash command（/xxx）是“你手动触发的快捷指令 / 提示词模板 / 控制面板”

**MCP**：让 agent/LLM 以**标准方式**连接到外部工具与数据源的“通用插口/协议”（客户端 ↔ 服务器）。

**Skill（技能）**：把你团队/你个人的“做事流程与专业知识”封装成可复用模块，让 agent **更会做这类事**。

**Hook（钩子）**：在 agent/工具链生命周期的关键节点插入“必定执行”的规则/脚本，用来做**强约束、审计、自动化**。

**Plugin（插件）**：把 skills / hooks / agents / slash commands / MCP servers 等打包成可分发、可版本化、可团队复用的一套扩展。

## 目录结构

```
ai-toolkit/
├── skills/           # Claude Code Skills
│   ├── notes/        # 笔记整理相关
│   └── productivity/ # 生产力工具
├── plugins/          # 编辑器插件和扩展
├── mcp-servers/      # Model Context Protocol 服务器
└── README.md         # 本文档
```

综合参考源

- [综合源-everything-claude-code](https://github.com/affaan-m/everything-claude-code)

## Skills

Claude Code 自定义技能，用于特定工作流。

### 笔记整理 (notes/)

- **learning-notes-organizer** - 学习笔记系统化整理
- **image-alt-title-filler** - 图片 alt/title 批量补全
- **note-outline-checklist** - 笔记大纲生成
- **section-refactor-with-todo-routing** - 章节重构工具

### 生产力工具 (productivity/)

（暂无）

### 外部 Skills

> :registered: 本项目已经引入仓库，可直接安装skill无需单独再加入市场

[:registered: planning-with-files](https://github.com/OthmanAdi/planning-with-files) - 任务规划和进度跟踪

- 解决ai易在长上下文中迷失，出现”幻觉“或遗忘。

[:registered: superpowers](https://github.com/obra/superpowers) - 头脑风暴、写计划、执行计划

- An agentic skills framework & software development methodology that works.

## Agents



## Plugins

编辑器插件和扩展（待添加）

- [anthropics官方插件列表](https://github.com/anthropics/claude-code/tree/main/plugins)

[ralph-wiggum](https://github.com/anthropics/claude-code/tree/main/plugins/ralph-wiggum) - Ralph 就是一个 Bash 循环,**自我纠正修复**

- ⚠️--max-iterations 设置最大迭代次数，否者遇见死题上演token消失术。

## MCP Servers

Model Context Protocol 服务器（待添加）

[notebooklm-mcp](https://github.com/PleasePrompto/notebooklm-mcp) - NotebookLM笔记操作，但是不支持上传文件

## 使用说明

### 手动安装 Skills

```bash
# 复制 skill 到 Claude Code 配置目录
cp -r skills/notes/learning-notes-organizer ~/.claude/skills/

# 或使用软链接（推荐开发时使用）
ln -s $(pwd)/skills/notes/learning-notes-organizer ~/.claude/skills/
```

### 使用 Skills

在 Claude Code 中使用 `/` 命令调用已安装的 skills。

## License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**维护者**: [@soulx](https://github.com/soulx)
**最后更新**: 2026-01-12
