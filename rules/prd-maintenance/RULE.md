# PRD 渐进式维护协议

> 目标：支持多供应商并行开发 + 敏捷迭代 + 渐进式文档维护，避免上下文爆炸

---

## 0. 核心原则

- **供应商隔离**：每个供应商/大需求独立维护，避免上下文混乱
- **三层结构**：Facts（冻结事实）+ Snapshot（当前版本）+ Changelog（变更历史）
- **渐进演进**：小需求单文件 → 中需求拆 Facts → 大需求完全拆分
- **去躁点**：纠错不记账；改契约/流程/规则/数据语义，才记账

---

## 1. 触发方式

### 1.1 进入 PRD 维护模式

```
prd: path/to/prd-dir-or-file
```

**示例**：
```
prd: docs/hotel-integration/rujia-incremental
我们把回调改成异步的
```

### 1.2 切换供应商/需求

```
prd: path/to/another-prd
```

**示例**：
```
prd: docs/hotel-integration/huazhu-full
华住需要支持预付
```

### 1.3 退出 PRD 维护模式

```
stop prd
```

### 1.4 本轮强制不记录

```
no-record
```

---

## 2. 文件结构识别

AI 自动识别 PRD 的组织方式：

### 2.1 单文件模式（小需求）

```
docs/hotel-integration/rujia-mapping/prd.md
```

**文件内容结构**：
```markdown
# 如家 Mapping PRD

## Facts（冻结事实）
- 业务域词典
- 核心约束
- 系统边界

## Snapshot（当前版本）
- 背景/目标/非目标
- 关键流程
- 关键规则
- 关键接口/字段

## Changelog（变更历史）
- 2026-02-23: 初始版本
```

**AI 行为**：
- 读取整个文件
- 根据变更类型更新对应章节

### 2.2 部分拆分模式（中需求）

```
docs/hotel-integration/rujia-incremental/
├── facts.md      # 独立的冻结事实
└── prd.md        # 包含 Snapshot + Changelog
```

**AI 行为**：
- 读取 facts.md（冻结事实）
- 读取 prd.md（当前版本 + 变更历史）
- Facts 很少改，主要更新 prd.md

### 2.3 完全拆分模式（大需求）

```
docs/hotel-integration/rujia-incremental/
├── facts.md      # 冻结事实层
├── snapshot.md   # 当前有效版本
└── changelog.md  # 变更补丁
```

**AI 行为**：
- 读取 facts.md（冻结事实）
- 读取 snapshot.md（当前版本）
- 读取 changelog.md（变更历史）
- 根据变更类型更新对应文件

---

## 3. 三层结构定义

### 3.1 Facts（冻结事实层）

**内容**：基本不改，或者改得很慢

- **业务域词典**：订单、房型、ratePlan、库存、增量接入等定义
- **核心约束**：支付前库存锁定策略、取消政策边界、渠道价格优先级
- **系统边界**：同程侧、酒店PMS/CRS、第三方中间件、消息队列、缓存

**目的**：让 AI 每次都能拿到"不容易变"的真相，减少被 PRD 版本带偏

**更新时机**：
- ✅ 术语定义变了
- ✅ 系统边界变了
- ✅ 核心约束变了
- ❌ 具体流程变了（应该更新 Snapshot）
- ❌ 接口字段变了（应该更新 Snapshot + Changelog）

### 3.2 Snapshot（当前有效版本）

**内容**：每个大需求的"当前有效版本摘要"

- **背景/目标/非目标**：为什么做、做什么、不做什么
- **关键流程**：1-2 个主流程 + 例外流
- **关键规则**：业务规则、优先级、分支条件
- **关键接口/字段**：只放业务上重要的，不要全量 API 文档

**目的**：让 AI 快速理解"现在要做什么"

**更新时机**：
- ✅ 流程变了
- ✅ 规则变了
- ✅ 接口/字段变了
- ✅ 目标/范围变了
- ❌ 修 bug（不更新）
- ❌ 重构不改外部行为（不更新）

### 3.3 Changelog（变更补丁层）

**内容**：每次变更只追加

```markdown
## 2026-02-23：回调改成异步

**变更点**：
- 回调从同步改成异步（MQ）
- 增加重试机制（3次，指数退避）

**影响面**：
- 接口：回调接口增加 `async: true` 字段
- 规则：回调失败不阻塞主流程
- 数据：新增 `callback_retry_log` 表

**兼容策略**：
- 向后兼容：老接口保持同步，新接口支持异步
- 灰度开关：`enable_async_callback`
```

**目的**：用"补丁"让上下文渐进更新，不靠改旧内容维持一致性

**更新时机**：
- ✅ 任何需要记账的变更（契约/流程/规则/数据语义）
- ❌ 纠错不记账

---

## 4. 去躁点判定（继承 docs-writing-protocol）

### 4.1 不更新（不记账）

- 修复编译/语法/单测挂了
- 修正 AI 理解错导致的实现偏差，但**不改变**既定设计
- 重试/提示词调整/代码风格调整/重构不改外部行为

> 口诀：**纠错不记账**

### 4.2 必须更新（记账）

只要满足任意一条：

1. **对外契约变了**：接口字段、枚举、返回码、回调语义
2. **流程变了**：状态机、时序、重试策略、库存扣减点、对账口径
3. **规则变了**：优先级、分支条件、灰度开关含义
4. **数据含义变了**：字段意义、来源、映射、默认值

> 口诀：**改契约/改流程/改规则/改语义，就记账**

---

## 5. 更新策略

### 5.1 判定变更类型

AI 根据变更内容判定更新哪一层：

| 变更类型 | 更新 Facts | 更新 Snapshot | 追加 Changelog |
|---------|-----------|--------------|---------------|
| 术语定义变了 | ✅ | ✅ | ✅ |
| 系统边界变了 | ✅ | ✅ | ✅ |
| 核心约束变了 | ✅ | ✅ | ✅ |
| 流程变了 | ❌ | ✅ | ✅ |
| 规则变了 | ❌ | ✅ | ✅ |
| 接口/字段变了 | ❌ | ✅ | ✅ |
| 目标/范围变了 | ❌ | ✅ | ✅ |
| 修 bug | ❌ | ❌ | ❌ |

### 5.2 单文件模式更新

在单文件中更新对应章节：

```markdown
# 如家 Mapping PRD

## Facts（冻结事实）
[如果 Facts 变了，更新这里]

## Snapshot（当前版本）
[如果 Snapshot 变了，更新这里]

## Changelog（变更历史）
- 2026-02-23: 初始版本
- 2026-02-24: 回调改成异步 [追加新条目]
```

### 5.3 多文件模式更新

分别更新对应文件：

- Facts 变了 → 更新 `facts.md`
- Snapshot 变了 → 更新 `snapshot.md`
- 任何需要记账的变更 → 追加 `changelog.md`

---

## 6. 演进路径

### 6.1 阶段1：小需求（单文件）

**适用场景**：
- 需求简单，预计不会频繁变更
- 团队成员少，上下文可控

**文件结构**：
```
rujia-mapping/
└── prd.md  # 包含 Facts + Snapshot + Changelog
```

### 6.2 阶段2：中需求（拆分 Facts）

**触发条件**：
- Facts 内容变多（超过 50 行）
- Facts 需要被多个需求共享
- Facts 变更频率远低于 Snapshot

**文件结构**：
```
rujia-incremental/
├── facts.md  # 独立出来
└── prd.md    # 包含 Snapshot + Changelog
```

**迁移方式**：
```
prd-split-facts: docs/hotel-integration/rujia-incremental
```

AI 自动：
1. 从 prd.md 中提取 Facts 章节
2. 创建 facts.md
3. 更新 prd.md（移除 Facts 章节）

### 6.3 阶段3：大需求（完全拆分）

**触发条件**：
- Changelog 内容变多（超过 100 行）
- 需要频繁查看变更历史
- 多人协作，需要清晰的变更追溯

**文件结构**：
```
rujia-incremental/
├── facts.md
├── snapshot.md
└── changelog.md
```

**迁移方式**：
```
prd-split-full: docs/hotel-integration/rujia-incremental
```

AI 自动：
1. 从 prd.md 中提取 Snapshot 和 Changelog 章节
2. 创建 snapshot.md 和 changelog.md
3. 删除 prd.md

---

## 7. 交互示例

### 示例 A：单文件模式

```
用户：prd: docs/hotel-integration/rujia-mapping/prd.md
     我们把回调改成异步的

AI：[进入 PRD 维护模式]
    [读取 prd.md]
    [判定：流程变更，需要记账]
    [更新 Snapshot 章节]
    [追加 Changelog 条目]

用户：修复一个 bug

AI：[判定：纠错不记账]
    [不更新文档]

用户：stop prd

AI：[退出 PRD 维护模式]
```

### 示例 B：多文件模式

```
用户：prd: docs/hotel-integration/rujia-incremental
     术语"增量接入"定义变了

AI：[进入 PRD 维护模式]
    [读取 facts.md + snapshot.md + changelog.md]
    [判定：术语定义变更，需要更新 Facts]
    [更新 facts.md]
    [更新 snapshot.md（如果引用了该术语）]
    [追加 changelog.md]

用户：prd: docs/hotel-integration/huazhu-full
     华住需要支持预付

AI：[切换到华住 PRD]
    [读取 huazhu-full 的文件]
    [判定：规则变更，需要记账]
    [更新对应文件]
```

---

## 8. 写入格式（最小化）

每次追加 Changelog 时，使用以下格式：

```markdown
## YYYY-MM-DD：变更标题（1 行）

**变更点**：
- 变更点 1（1 行）
- 变更点 2（1 行）

**影响面**：
- 接口/规则/数据/任务/灰度（1-3 行）

**兼容策略**：
- 向后兼容/双写/开关/迁移路径（1-3 行）
```

**总计不超过 10 行**。

---

## 9. 特殊指令

### 9.1 拆分 Facts

```
prd-split-facts: path/to/prd-dir
```

从单文件中提取 Facts 章节，创建独立的 facts.md。

### 9.2 完全拆分

```
prd-split-full: path/to/prd-dir
```

将单文件拆分为 facts.md + snapshot.md + changelog.md。

### 9.3 合并回单文件

```
prd-merge: path/to/prd-dir
```

将多文件合并回单文件（用于需求缩小时）。

---

## 10. 最佳实践

### 10.1 供应商隔离

每个供应商/大需求独立目录：

```
docs/hotel-integration/
├── rujia-incremental/    # 如家增量
├── rujia-mapping/        # 如家 mapping
├── huazhu-full/          # 华住全量
└── jinjiang-incremental/ # 锦江增量
```

### 10.2 Facts 共享

如果多个供应商共享相同的 Facts（如通用术语），可以：

```
docs/hotel-integration/
├── common-facts.md       # 共享的冻结事实
├── rujia-incremental/
│   ├── facts.md          # 如家特有的 Facts（引用 common-facts.md）
│   ├── snapshot.md
│   └── changelog.md
└── huazhu-full/
    ├── facts.md          # 华住特有的 Facts（引用 common-facts.md）
    ├── snapshot.md
    └── changelog.md
```

### 10.3 迭代管理

如果需要按迭代管理（敏捷开发），可以：

```
docs/hotel-integration/rujia-incremental/
├── facts.md
├── snapshot.md
├── changelog.md
└── iterations/
    ├── sprint-1.md       # 第 1 个迭代的详细记录
    ├── sprint-2.md       # 第 2 个迭代的详细记录
    └── sprint-3.md       # 第 3 个迭代的详细记录
```

Changelog 只记录"值得关注的变更"，详细的迭代记录放在 `iterations/` 目录。

---
