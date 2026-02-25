# Rules（行为规则）

> 约束 AI 行为的协议模板库，放入 `.claude/` 后每次对话全量加载

## 什么是 Rule？

**Claude Code 的 Rule** = 放在 `.claude/` 目录下的 `.md` 文件，每次对话开始时**无条件全文加载**进 system prompt。没有触发条件、没有 globs、没有开关——唯一的粒度控制是**文件存不存在**。

> **关于 `.mdc` 文件**：本仓库的 `.mdc` 是给 Cursor 用的元数据（支持 `alwaysApply` / `globs` 等 frontmatter 控制）。Claude Code 不读 `.mdc`，两者互不干扰。

## Rule 与 Skill 的边界正在融合——但没有消失

### 行业趋势

各家 AI 工具正在走向同一个方向：

- **指令/规则文件**（`AGENTS.md`、`CLAUDE.md`、`.cursor/rules`）成为"基本盘"——每次对话的上下文基础
- **技能/插件**（Skills、Agent Skills）成为"可复用能力层"——按需注入的工作流模块
- **Agent Skills 开放标准**正在推动跨工具兼容（Claude Code、Cursor 均已支持）

### Cursor：Skills 以"规则形态"注入

Cursor 官方文档明确：Skills 进入模型上下文时，以"由 Agent 决定是否应用的规则"形式注入（类似 `Apply Intelligently`），且**不能**配置成 `alwaysApply` 或 `manual`。

所以在 Cursor 里，Skill 和 Rule 的**使用接口统一了**（都是上下文注入），但**语义边界仍在**：

| | Rule | Skill |
|---|---|---|
| 本质 | 做事原则 / 规范 / 约束 | 可复用能力包（含脚本/资源/命令） |
| 典型形式 | `.mdc` / `CLAUDE.md` / `AGENTS.md` | `SKILL.md` + 可选脚本/参考资料 |
| 调用方式 | 自动加载（alwaysApply / globs / description） | `/skill-name` 手动调用 或 description 匹配自动触发 |
| 能否 alwaysApply | ✅ | ❌（Cursor 中 Skill 不支持） |

### Claude Code vs Cursor：Rule 机制对比

| | Cursor `.mdc` | Claude Code Rule `.md` |
|---|---|---|
| `description` 语义自动触发 | ✅ AI 根据上下文自主判断 | ❌ Rule 无此机制，全量加载 |
| 按文件路径触发 | ✅ `globs: **/*.ts` | ❌ 不支持 |
| 强制全量加载 | ✅ `alwaysApply: true` | ✅ 放进 `.claude/` 即全量加载 |
| Token 效率 | ✅ 按需加载 | ❌ 每次对话都烧 |
| Skill 自动触发 | ✅ description 匹配 | ⚠️ 理论支持，实践可靠性差 |

**本仓库的兼容策略**：`RULE.md` 是内容层（两个工具通用），`.mdc` 是 Cursor 的激活策略层，Claude Code 用户只需复制 `RULE.md` 到 `.claude/`。

> **双版本说明**：`docs-writing-protocol` 和 `prd-maintenance` 同时提供 Rule 版（`rules/`）和 Skill 版（`skills/doc-processing/`）。高频 → Rule；低频 → Skill。

## Rule vs Skill 怎么选？（Claude Code 标准）

| | Rule | Skill | 手动 @ |
|---|---|---|---|
| 触发方式 | 自动（全量加载） | `/command` 或 description 匹配 | 手动 @ 文件 |
| Token 成本 | 每次对话都烧 | 按需加载 | 完全按需 |
| 可靠性 | 强制，不会失效 | 长对话可能遗忘 | 需定期重新 @ |
| 适合场景 | 持续约束、高频使用 | 一次性任务、低频工作流 | 灵活控制 |

**决策口诀**：规则短（< 100 行）且高频 → Rule；规则长或低频 → Skill 或手动 @。

Rule 超过 200 行就该考虑改成 Skill，每次对话都在烧 token。

## 如何使用

```bash
# 项目级启用（推荐）
cp rules/<rule-name>/RULE.md your-project/.claude/<rule-name>.md

# 全局启用
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

- `alwaysApply: true`（Cursor）/ Claude Code 中直接全量加载
- 收到非空反馈继续循环，用户说「结束」才停止

[查看详情](./feedback-after-completion/README.md)

## Rule 结构规范

```
rules/rule-name/
├── RULE.md                  # 协议正文（精简，< 100 行）
├── README.md                # 用户文档（问题/用法/触发词）
└── rule-name.mdc            # Cursor 元数据（可选）
```

RULE.md 只放核心逻辑，详细说明、示例放 README.md（不会被加载，不烧 token）。

## License

MIT
