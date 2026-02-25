# MCP Interactive Feedback 规则

## 核心规则

1. 在任何流程、任务、对话进行时，无论是询问、回复、或完成阶段性任务，皆必须调用 MCP `mcp-feedback-enhanced`。
2. 每当收到用户反馈，若反馈内容非空，必须再次调用 MCP `mcp-feedback-enhanced`，并根据反馈内容调整行为。
3. 仅当用户明确表示「结束」或「不再需要交互」时，才可停止调用 MCP `mcp-feedback-enhanced`，流程才算结束。
4. 除非收到结束指令，否则所有步骤都必须重复调用 MCP `mcp-feedback-enhanced`。
5. 完成任务前，必须使用 MCP `mcp-feedback-enhanced` 工具向用户询问反馈。
6. 超时后再次调用 MCP `mcp-feedback-enhanced` 工具向用户询问反馈。

## 完成确认循环

完成任务后，在终端询问用户是否满意：

```bash
read -P "修复完成，是否满意？(y/n) " response && echo $response
```

- 收到 `yes` → 退出
- 未收到或收到其他回复 → 继续修复，重复上述过程
