# Docs Writing Protocol（文档写入协议）

> 控制 AI 何时写入文档、写入什么内容，避免文档噪声

## 问题场景

与 AI 协作时，AI 容易把 bug 修复、重试过程、风格调整都写进文档，导致文档充斥噪声，难以追溯真正的设计变更。

## 核心原则

1. **写入门槛**：没点名文件，就不写入
2. **去躁点**：纠错不记账；改契约/流程/规则/语义，才记账

## 使用方式

### 项目级启用（推荐）

```bash
cp rules/docs-writing-protocol/RULE.md \
   your-project/.claude/docs-writing-protocol.md
```

### 全局启用

```bash
cp rules/docs-writing-protocol/RULE.md \
   ~/.claude/rules/docs-writing-protocol.md
```

## 触发指令

- `update: path/to/doc.md` — 指定写入目标
- `switch: another.md` — 切换写入目标
- `stop writing` — 停止写入
- `no-record` — 本轮强制不写入

## License

MIT
