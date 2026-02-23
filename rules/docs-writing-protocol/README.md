# Docs Writing Protocol（文档写入协议）

> 控制 AI 何时写入文档、写入什么内容，避免文档噪声

## 问题场景

在与 AI 协作开发时，常见问题：
- AI 频繁修改文档，把 bug 修复、重试过程都写进去
- 文档充斥大量噪声，难以追溯真正的设计变更
- 不知道什么时候该更新文档，什么时候不该

## 解决方案

这个协议定义了两个核心原则：

1. **写入门槛**：没点名文件，就不写入（避免过度主动）
2. **去躁点**：纠错不记账；改契约/流程/规则/语义，才记账（避免噪声）

## 使用方式

### 方式 1：项目级启用（推荐）

将规则复制到项目的 `.claude/` 目录：

```bash
cp rules/docs-writing-protocol/RULE.md \
   your-project/.claude/docs-writing-protocol.md
```

Claude Code 会自动加载并遵守该规则。

### 方式 2：全局启用

复制到 Claude Code 全局配置目录：

```bash
cp rules/docs-writing-protocol/RULE.md \
   ~/.claude/rules/docs-writing-protocol.md
```

所有项目都会应用该规则。

## 触发方式

协议通过关键词触发：

- `update: path/to/doc.md` - 指定写入目标
- `switch: another.md` - 切换写入目标
- `stop writing` - 停止写入
- `no-record` - 本轮强制不写入

**示例**：
```
这正是你需要的"渐进式维护"：
用户：update: docs/api.md
     我们把回调改成异步的

AI：[检测到 update: 触发，进入沉淀模式]
    [判定：流程变更，需要记账]
    [更新 docs/api.md]
用户：update: docs/rujia-prd.md
       我们把回调改成异步的
AI：[进入沉淀模式，DocTarget = rujia-prd.md]
      [更新文档]
用户：再加个重试机制
AI：[继续更新 rujia-prd.md]
      [记录变更]
用户：修复一个 bug
AI：[判定：纠错不记账]
      [不更新文档]
用户：stop writing
AI：[退出沉淀模式]
```

## 版本选择

- **RULE.md**（Standard 版）- 完整协议，支持 snapshot/patch/facts/changelog/ADR 分层管理
- **RULE-lite.md**（Lite 版，待添加）- 简化版，适合个人小项目

## 协议详情

查看 [RULE.md](./RULE.md) 了解完整协议内容。

## License

MIT
