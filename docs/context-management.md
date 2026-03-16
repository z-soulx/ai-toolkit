# Claude Code 上下文与提示词体系

> 新手入门指南——从 Agent vs 模型两个角度，搞懂压缩、Skill 注入、System Prompt 的完整生命周期。
>
> ==记住核心思想，agent的实现不同谋些设计可能会变动==

## 阅读顺序

1. 先看 [核心速查表](#核心速查表) 建立全局印象
2. 再按需深入各章节

---

## 核心速查表

### 表 1：Agent vs 模型——谁负责什么

| 层级 | 负责方 | 做了什么 |
|---|---|---|
| 提示注入 / 初始规则加载 | **Agent** | 将规则 / CLAUDE.md 加载到模型上下文 |
| 压缩触发 & 管理 | **Agent** | 检测 token 阈值，触发模型生成摘要，替换历史 |
| 真实生成文本 | **模型 (LLM)** | 根据当前可见上下文推理输出 |

### 表 2：所有内容的完整行为对照

| 类型 | Agent 是否管理 | 是否注入到模型上下文 | 是否可能因压缩而"不被模型看到" | 说明 |
|---|---|---|---|---|
| **System Prompt** | 是 | 每次调用 | 不会丢失 | Agent 每次必传给模型的核心控制指令 |
| **CLAUDE.md / rules** | 是 | 会注入为上下文背景 | 可能被压缩 | 作为 session context 注入，超长会优先保留最近内容 |
| **Skill 元数据（YAML 描述）** | 是 | 启动时读取 | 可能被压缩(*:man: 推测不容易被压缩*) | <u>:man: 推测作为 “early context / context 前端” 的一部分，越前面越不容易被压缩</u> |
| **Skill 全部内容（正文/执行模板）** | 是 | Skill 被触发时注入 | 可能被压缩 | 用于执行技能逻辑的实际 prompt 片段 |
| **用户普通 Prompt** | 是 | 每条对话都注入 | 可能被压缩 | 用户每次消息作为模型输入的一部分 |
| **历史对话记录** | 管理 | 模型看到过 | 可能被压缩摘要 | 模型上下文堆叠历史 |

### 表 3：什么时候加载 / 什么时候更新

| 场景 | 是否自动重载 |
|---|---|
| 新 session（打开或 `/clear`） | 是，会重新读取最新文件 |
| 当前会话运行中修改 CLAUDE.md 或 rules 文件 | 否，不会自动取新内容 |
| Skill 配置变更 | 否，需要重新 session 或手动调用 |
| System Prompt 修改 | 取决于 Agent 调用模式（需要重启/触发才生效） |

### 表 4：一眼看懂的最终对比

| 项 | 固态/永久 | 模型可见 | 会被压缩 | 加载时机 | 更新时机 |
|---|---|---|---|---|---|
| System Prompt | 是 | 始终 | 否 | 每次调用 | 修改需重启/设定 |
| CLAUDE.md / rules | 是 | 注入后可见 | 可能 | 新 session | 需重启 |
| Skill 元数据 | 是 | 按需可见 | 可能 | 初始扫描 | 需重载会话 |
| Skill 全部内容 | 是 | 注入执行时可见 | 可能 | 触发执行时 | 重新触发 |
| User Prompt | 否 | 当前对话可见 | 可能 | 每条输入 | N/A |
| 历史对话 | 否 | 过去对话可见 | 可能 | 每轮累积 | N/A |

---

## Claude Code 加载层级

全部拼接进同一 system prompt，全局 → 局部：

1. `~/.claude/CLAUDE.md` — 全局，所有项目
2. `<project-root>/CLAUDE.md` — 项目根目录
3. `<project-root>/.claude/CLAUDE.md` — 项目 `.claude/` 子目录
4. `<subdir>/CLAUDE.md` — Claude 在该子目录操作时额外加载
5. `@import` 显式引入的文件

### CLAUDE.md vs AGENTS.md

Claude Code 两个都读，有则全部拼接。区别在受众：

| 文件        | 适合放什么                                            |
| ----------- | ----------------------------------------------------- |
| `CLAUDE.md` | Claude Code 专属配置（工具调用偏好、项目约定）        |
| `AGENTS.md` | 跨工具通用规范（OpenAI Codex、Gemini CLI 等也读这个） |

跨工具共享的规范放 `AGENTS.md`，Claude Code 专属的放 `CLAUDE.md`；两者共存时都生效，不冲突。

## 1. 核心概念区分：Agent 与模型

| 层级 | 定义 | 所在位置 | 主要职责 |
|---|---|---|---|
| **Agent（Claude Code）** | 智能体框架/系统 | 运行在用户机器 + API | 管理触发、读取规则、控制上下文与压缩、选技能 |
| **模型（LLM，如 Claude）** | 语言理解与生成引擎 | Anthropic 提供的 API 服务器 | 仅根据当前上下文推理输出 |

**Agent 不等于模型。** Claude Code 不是模型内部，它只是一个 agent 系统，调用模型提供推理能力，而所有规则、技能等都是由 agent 注入到模型上下文再让模型去执行。

**模型只看到它收到的上下文 token**，它无法直接访问规则文件或 agent 内部状态。

> 参考：[Claude Code Features Overview][1] / [Context Management - DeepWiki][2]

---

## 2. 上下文压缩：到底是谁做？如何做？

### 核心结论

**触发主体是 Agent（Claude Code）。**

模型本身不会自动判定去压缩自己的上下文，它只是按照当前给定的上下文执行推理。当上下文接近限制阈值时：

- Agent（Claude Code）调用模型的压缩机制/摘要策略
- Agent 指示模型**折叠历史上下文**生成精简摘要
- Agent 用生成的摘要**替换掉旧消息/上下文片段**

简单理解：**模型不会自己忘记东西，但 Agent 会用模型来生成摘要/压缩历史内容。**

> 参考：[Claude API 压缩文档][3]

### 压缩流程

```
对话历史 → 达到阈值 → Agent 触发压缩策略 →
模型生成"摘要信息" → 用摘要替换旧令牌 → 保留精华
```

这是一种 **agent 主导 + 模型辅助** 的行为。

---

## 3. 规则 / Skills 会不会被"遗忘"？

### 遗忘 ≠ 删除文件

Claude Code 的规则文件（如 CLAUDE.md、rules、skills）：

- Agent 会**读取文件内容并将其注入模型上下文**
- 但随着会话越来越长，Agent 可能压缩掉旧的推入上下文的令牌（包括规则文本出现过的那些 token）

因此：

- 文件本身仍然存在于 project 目录 — **文件不会丢失**
- 但在当前模型上下文中可能不再"可见"（被摘要/压缩掉）

这种情况通常叫上下文**漂移（Context Drift）**，即"规则/背景信息不再出现在当前有效上下文中"。

> 参考：[Claude Code 定制化指南][4]

---

## 4. System Prompt 为什么不会丢失

System Prompt 的关键特点：

- 由 Agent 每次在调用模型时**显式传入**
- 与历史上下文的消息堆叠不同，它是一条**固定层级**的输入
- 模型每次生成输出都有它在上下文里

因此：
- 它不会被摘要/压缩掉
- 无论对话多长，它都会影响每一次推理
- 文件层面的规则不是 system prompt，但你可以通过配置让一些关键信息变成 System Prompt 的一部分

**真正关键的长期行为规范应该放在 System Prompt / 固定层级。**

> 参考：[Claude Code Ultimate Guide - Compact Command][5]

---

## 5. Skill 元数据 vs Skill 全部内容

### Skill 元数据（YAML 描述）

- 存在于 Agent 内部
- 用于判断是否要执行这个 Skill（是否 relevant）
- 不等于 System Prompt
- 不是自动每次都注入模型上下文
- 在匹配阶段可能注入少量信息（用于确认与当前对话的关联）

### Skill 全部内容（执行模板 + Prompt）

- 只有当 Skill 被触发后才注入到模型上下文
- 注入后模型才能执行该 Skill 逻辑
- 这部分内容一旦进入上下文，也可能随着压缩策略逐渐不再可见

---

## 6. 压缩发生时到底"会丢失什么"

压缩优化不等同于物理删除，有几种策略：

**微观压缩（micro-compact）**：自动替换很早的工具输出为简单占位/标记。

**自动压缩（auto-compact）**：Agent 在接近窗口限制时让模型生成摘要，然后替换掉旧上下文。

**手动压缩（/compact）**：用户显式触发，让 Agent 制作更紧凑更精炼的历史。

压缩的目标是保留**重要信息的核心摘要**，而不是永久删除文件或配置本身。

> 参考：[Claude API 压缩文档][3] / [从零手写 ClaudeCode 实战笔记][7]

---

## 7. 关键核心思维模型

便于记忆的四条核心区分：

1. **System Prompt 是模型每次生成输出的基础约束** — 不会被压缩
2. **CLAUDE.md / rules 是 session context 级注入的背景信息** — 不是永久内部逻辑，可能被压缩
3. **Agent 主动控制"压缩"，模型只是依据当前上下文** — 压缩是 Agent 行为
4. **规则永远不会从磁盘丢失，但可能不再进入模型的注意力窗口** — 这叫 Context Drift

---

## 参考来源

[1]: https://code.claude.com/docs/en/features-overview "Extend Claude Code - Claude Code Docs"
[2]: https://deepwiki.com/shanraisshan/claude-code-best-practice/4-context-management "Context Management | DeepWiki"
[3]: https://platform.claude.com/docs/zh-CN/build-with-claude/compaction "压缩 - Claude API Docs"
[4]: https://nealst.github.io/2026/01/11/claude-code-customization/ "Claude Code 定制化指南"
[5]: https://deepwiki.com/FlorianBruniaux/claude-code-ultimate-guide/3.2-the-compact-command "Context Window Management | DeepWiki"
[6]: https://zhuanlan.zhihu.com/p/1935398779978252415 "Claude Code 记忆管理深度解析"
[7]: https://cloud.tencent.com/developer/article/2636374 "从零手写 ClaudeCode：learn-claude-code 项目实战笔记"
