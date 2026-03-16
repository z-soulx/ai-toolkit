# Rules（行为规则）

> 放进 system prompt 的持续约束——不需要触发，会话开始即生效

[claude code 官方文档](https://code.claude.com/docs/zh-CN/memory)

## Rule 是什么

**Rule = 静态前缀（system prompt）的一部分**，会话开始时全文加载，每轮对话都在场。

**Skill** = 触发后才注入动态上下文的工作流模块。Rule 和 Skill 的核心区别是**在哪里**，不是触发方式。

`CLAUDE.md` / `AGENTS.md` = 同一概念在不同工具的命名，本质都是 system prompt。

> ⚠️ **误解："Rule 和 Skill 本质相同"** → 不同。Rule 在静态前缀，Skill body 在动态上下文，两者的可靠性完全不同。

## Rule vs Skill

| | Rule | Skill |
|---|---|---|
| 位置 | 静态前缀（system prompt） | 动态上下文（触发时注入） |
| 可靠性 | 强制，Compaction 不丢 | 长对话可能被摘要/丢弃 |
| Token 成本 | 首轮全量，后续缓存 ~10% | 按需加载 |
| 适合场景 | 持续约束、高频使用 | 一次性任务、低频工作流 |

**选择口诀**：持续约束 / 高频 → Rule；一次性工作流 / 长文档 → Skill（按需，不占 system prompt）。

Rule 超过 200 行就该考虑改成 Skill——不是因为"每轮都烧"，而是因为**规则太长模型遵循质量会下降**。

> 关于压缩机制、上下文生命周期、Context Drift 等深入内容，见 [Context 管理指南](../docs/context-management.md)。

## Cursor 参考：四种规则模式

Cursor 中 Rule/Skill 边界更模糊（<u>*Skill 也以规则形态注入*</u>），但它的四种模式展示了从"强制全量"到"完全懒加载"的完整光谱：

| 类型 | Frontmatter | 注入时机 |
|---|---|---|
| Always | `alwaysApply: true` | **每次 API 请求**（每轮），无条件 |
| Auto Attached | `globs: ["**/*.ts"]` | 匹配文件在上下文中时 |
| Agent Requested | 只有 `description` | AI 根据描述自主决定是否拉取 |
| Manual | 无 frontmatter | 仅用户显式引用时 |

> ⚠️ **误解："alwaysApply: true = 新会话加载一次"** → 是每次 API 请求（每轮对话）注入，不只是会话开始。

**Claude Code 中只有一种模式**：文件存在即全文加载进静态前缀，没有 globs / 懒加载 / 按需拉取。Cursor 的四种模式是对比参考，不是 Claude Code 的功能。

## 如何使用

```bash
# 项目级启用（推荐）
cp rules/<rule-name>/RULE.md your-project/.claude/<rule-name>.md

# 全局启用（所有项目生效）
cp rules/<rule-name>/RULE.md ~/.claude/rules/<rule-name>.md

# 临时禁用
mv .claude/<rule-name>.md .claude/<rule-name>.md.disabled
```

## 当前 Rules

### docs-writing-protocol

控制 AI 何时写入文档、写入什么，避免文档噪声。

- 写入门槛：没点名文件，就不写入
- 去躁点：纠错不记账；改契约/流程/规则/语义，才记账
- 触发：`update: path` / `switch: path` / `stop writing` / `no-record`
- Skill 版：`skills/doc-processing/docs-writing-protocol/`

[查看详情](./docs-writing-protocol/README.md)

### prd-maintenance

多供应商并行开发 + 敏捷迭代场景的 PRD 维护协议。

- 三层结构：Facts（冻结）+ Snapshot（当前）+ Changelog（历史）
- 供应商隔离，避免上下文爆炸
- 触发：`prd: path` / `stop prd` / `prd-split-facts:` / `prd-split-full:`
- Skill 版：`skills/doc-processing/prd-maintenance/`

[查看详情](./prd-maintenance/README.md)

### feedback-after-completion

任务完成后强制调用 MCP `mcp-feedback-enhanced` 询问用户反馈。

- 收到非空反馈继续循环，用户说「结束」才停止

[查看详情](./feedback-after-completion/README.md)

## Rule 结构规范

```
rules/rule-name/
├── RULE.md          # 协议正文（精简，< 100 行）——加载进 system prompt
├── README.md        # 用户文档（问题/用法/触发词）——不加载，不烧 token
└── rule-name.mdc    # Cursor 元数据（可选）
```

`RULE.md` 只放核心逻辑，详细说明和示例放 `README.md`。
