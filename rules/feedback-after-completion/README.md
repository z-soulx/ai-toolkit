# Feedback After Completion（任务完成后强制交互反馈）

> 每次完成阶段性任务后，强制调用 MCP `mcp-feedback-enhanced` 询问用户反馈，直到用户明确表示结束

## 问题场景

AI 完成任务后直接结束对话，不主动确认用户是否满意，导致用户需要重新发起对话才能继续修正。

## 核心原则

1. **强制反馈**：每次完成阶段性任务，必须调用 MCP `mcp-feedback-enhanced` 询问反馈
2. **非空继续**：收到非空反馈后，再次调用并根据反馈调整行为
3. **明确结束**：仅当用户明确说「结束」或「不再需要交互」时，才停止反馈循环

## 使用方式

### 项目级启用（推荐）

```bash
cp rules/feedback-after-completion/RULE.md \
   your-project/.claude/feedback-after-completion.md
```

### 全局启用

```bash
cp rules/feedback-after-completion/RULE.md \
   ~/.claude/rules/feedback-after-completion.md
```

## 触发方式

本规则 `alwaysApply: true`，**无需显式触发，始终生效**。

## 结束指令

- 用户明确说「结束」
- 用户明确说「不再需要交互」

## License

MIT
