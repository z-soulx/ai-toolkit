---
name: prd-maintenance
description: PRD 渐进式维护协议。多供应商并行开发 + 敏捷迭代场景下维护 PRD 文档。当用户说"prd: path"、"维护 PRD"、"更新需求文档"时使用。依赖 docs-writing-protocol 的去躁点判定。
user-invocable: true
metadata:
  short-description: PRD 三层结构维护（Facts/Snapshot/Changelog），供应商隔离，渐进演进
  version: v1.0
---

# PRD 渐进式维护协议

> 基于 docs-writing-protocol 的 PRD 专属扩展。
> 去躁点判定、写入门槛、操作指令均继承基础协议，本协议只定义 PRD 特有的三层结构与文件管理。

---

## 核心原则

- **继承去躁点**：纠错不记账；改契约/流程/规则/语义，就记账（详见 docs-writing-protocol）
- **三层结构**：Facts（冻结事实）+ Snapshot（当前版本）+ Changelog（变更历史）
- **渐进演进**：单文件 → 拆 Facts → 完全拆分，按需演进
- **供应商隔离**：每个供应商/大需求独立目录，避免上下文混乱

---

## 1. 触发方式

- `prd: path/to/prd` — 进入 PRD 维护模式，设置 DocTarget
- `prd: path/to/another` — 切换 DocTarget
- `stop prd` — 退出 PRD 维护模式
- `no-record` — 本轮强制不记录（继承基础协议）

触发后 AI 自动识别文件结构（单文件 or 多文件），读取相关文件，进入持续维护模式。

---

## 2. 文件结构识别

### 单文件模式（小需求）
```
prd.md          # Facts + Snapshot + Changelog 三章节合一
```

### 部分拆分模式（中需求）
```
facts.md        # 独立冻结事实
prd.md          # Snapshot + Changelog
```

### 完全拆分模式（大需求）
```
facts.md
snapshot.md
changelog.md
```

AI 根据目录下文件自动判断模式，无需手动指定。

---

## 3. 三层结构

### Facts（冻结事实）
业务域词典、核心约束、系统边界。基本不改，或改得很慢。

更新时机：术语定义变了 / 系统边界变了 / 核心约束变了

### Snapshot（当前版本）
背景/目标、关键流程、关键规则、关键接口字段。反映"现在长什么样"。

更新时机：流程/规则/接口/目标范围变了

### Changelog（变更历史）
每次变更只追加，格式如下（总计不超过 10 行）：

```markdown
## YYYY-MM-DD：变更标题

**变更点**：
- 变更点 1
- 变更点 2

**影响面**：接口/规则/数据/灰度

**兼容策略**：向后兼容/双写/开关/迁移路径
```

---

## 4. 更新策略

| 变更类型 | Facts | Snapshot | Changelog |
|---------|-------|----------|-----------|
| 术语/边界/约束变了 | ✅ | ✅ | ✅ |
| 流程/规则/接口变了 | ❌ | ✅ | ✅ |
| 修 bug / 纠错 | ❌ | ❌ | ❌ |

---

## 5. 演进路径

**单文件 → 拆 Facts**：Facts 超过 50 行，或需要被多个需求共享时
```
prd-split-facts: path/to/prd-dir
```

**拆 Facts → 完全拆分**：Changelog 超过 100 行，或多人协作需要清晰追溯时
```
prd-split-full: path/to/prd-dir
```

**合并回单文件**：需求缩小时
```
prd-merge: path/to/prd-dir
```
