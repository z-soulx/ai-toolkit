# PRD 渐进式维护协议

> 基于 docs-writing-protocol 的 PRD 专属扩展，专为多供应商并行开发 + 敏捷迭代场景设计

## 问题场景

与 AI 协作维护 PRD 时的常见问题：
- 多个供应商的 PRD 混在一起，上下文爆炸
- 每次迭代都改 PRD 全文，难以追溯变更历史
- AI 容易被旧版本 PRD 带偏

## 解决方案

**三层结构**：Facts（冻结事实）+ Snapshot（当前版本）+ Changelog（变更历史）

**供应商隔离**：每个供应商/大需求独立目录，独立上下文

**渐进演进**：单文件 → 拆 Facts → 完全拆分，按需演进

## 与 docs-writing-protocol 的关系

- `docs-writing-protocol` 是基础层：写入门槛 + 去躁点判定（通用）
- `prd-maintenance` 是 PRD 专属扩展：三层结构 + 文件识别 + 演进路径
- 去躁点判定直接继承基础协议，不重复定义
- 建议同时启用两个规则，`prd-maintenance` 优先级更高

## 使用方式

### 项目级启用（推荐）

```bash
# 同时启用两个规则
cp rules/docs-writing-protocol/RULE.md \
   your-project/.claude/docs-writing-protocol.md

cp rules/prd-maintenance/RULE.md \
   your-project/.claude/prd-maintenance.md
```

### 全局启用

```bash
cp rules/prd-maintenance/RULE.md \
   ~/.claude/rules/prd-maintenance.md
```

## 触发指令

- `prd: path/to/prd` — 进入 PRD 维护模式
- `prd: path/to/another` — 切换 DocTarget
- `stop prd` — 退出 PRD 维护模式
- `no-record` — 本轮强制不记录（继承基础协议）
- `prd-split-facts: path` — 从单文件提取 Facts
- `prd-split-full: path` — 完全拆分为三文件
- `prd-merge: path` — 合并回单文件

## 协议详情

查看 [RULE.md](./RULE.md) 了解完整协议内容。

## License

MIT
