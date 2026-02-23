# PRD 渐进式维护协议

> 专为多供应商并行开发 + 敏捷迭代场景设计的 PRD 维护方案

## 问题场景

**典型场景**：OTA 酒店直连业务

你在做：
- 如家增量接入
- 华住全量接入
- 如家 mapping
- 锦江增量接入
- ...

**面临的问题**：
1. ❌ 多个供应商的 PRD 混在一起，上下文爆炸
2. ❌ 每次迭代都改 PRD 全文，难以追溯变更历史
3. ❌ AI 容易被旧版本 PRD 带偏，产生幻觉
4. ❌ 团队成员不知道"现在的设计"是什么样

## 解决方案

### 核心思路

**三层结构 + 渐进演进**：

```
Facts（冻结事实）     → 基本不改（术语、约束、边界）
Snapshot（当前版本）  → 反映"现在长什么样"
Changelog（变更历史） → 追加式记录变更
```

**供应商隔离**：
```
docs/hotel-integration/
├── rujia-incremental/    # 如家增量（独立上下文）
├── huazhu-full/          # 华住全量（独立上下文）
└── rujia-mapping/        # 如家 mapping（独立上下文）
```

**渐进演进**：
- 小需求：单文件（包含三层）
- 中需求：拆分 Facts
- 大需求：完全拆分（facts.md + snapshot.md + changelog.md）

## 使用方式

### 1. 启用规则

**项目级启用**（推荐）：
```bash
cp rules/prd-maintenance/RULE.md \
   your-project/.claude/prd-maintenance.md
```

**全局启用**：
```bash
cp rules/prd-maintenance/RULE.md \
   ~/.claude/rules/prd-maintenance.md
```

### 2. 创建 PRD 结构

**小需求（单文件）**：
```bash
mkdir -p docs/hotel-integration/rujia-mapping
cat > docs/hotel-integration/rujia-mapping/prd.md << 'EOF'
# 如家 Mapping PRD

## Facts（冻结事实）
- **增量接入**：只同步变化的数据（vs 全量接入）
- **库存锁定策略**：支付前锁定，30分钟超时释放
- **系统边界**：同程侧 → 如家 PMS

## Snapshot（当前版本）
### 背景
如家需要支持房型 mapping，将 PMS 房型映射到同程房型。

### 关键流程
1. 获取如家房型列表
2. 人工配置 mapping 关系
3. 同步时自动转换

## Changelog（变更历史）
- 2026-02-23: 初始版本
EOF
```

**大需求（多文件）**：
```bash
mkdir -p docs/hotel-integration/rujia-incremental
# 创建 facts.md, snapshot.md, changelog.md
```

### 3. 使用交互指令

**进入 PRD 维护模式**：
```
prd: docs/hotel-integration/rujia-incremental
我们把回调改成异步的
```

**切换供应商**：
```
prd: docs/hotel-integration/huazhu-full
华住需要支持预付
```

**退出维护模式**：
```
stop prd
```

**本轮强制不记录**：
```
no-record
修复一个 bug（不记录到 PRD）
```

## 完整示例

### 场景：如家增量接入，多次迭代

**第 1 次迭代：初始设计**

```
用户：prd: docs/hotel-integration/rujia-incremental/prd.md
     初始设计：支持如家增量接入，同步订单和库存

AI：[进入 PRD 维护模式]
    [创建单文件 PRD]
    [写入 Facts + Snapshot + Changelog]
```

**第 2 次迭代：回调改异步**

```
用户：我们把回调改成异步的，用 MQ

AI：[判定：流程变更，需要记账]
    [更新 Snapshot 章节：回调流程]
    [追加 Changelog：2026-02-24 回调改异步]
```

**第 3 次迭代：修复 bug**

```
用户：修复回调重试的 bug

AI：[判定：纠错不记账]
    [不更新 PRD]
```

**第 4 次迭代：增加预付支持**

```
用户：增加预付支持

AI：[判定：规则变更，需要记账]
    [更新 Snapshot 章节：支付规则]
    [追加 Changelog：2026-02-25 增加预付支持]
```

**第 5 次迭代：需求变大，拆分文件**

```
用户：prd-split-full: docs/hotel-integration/rujia-incremental

AI：[自动拆分]
    [创建 facts.md, snapshot.md, changelog.md]
    [删除 prd.md]
```

**第 6 次迭代：切换到华住**

```
用户：prd: docs/hotel-integration/huazhu-full
     华住需要支持预付

AI：[切换到华住 PRD]
    [独立上下文，不受如家影响]
    [更新华住的 PRD]
```

## 三层结构详解

### Facts（冻结事实层）

**内容**：
- 业务域词典（订单、房型、ratePlan、库存、增量接入等定义）
- 核心约束（库存锁定策略、取消政策边界、价格优先级）
- 系统边界（同程侧、酒店 PMS/CRS、中间件、MQ、缓存）

**特点**：
- 基本不改，或者改得很慢
- 让 AI 每次都能拿到"不容易变"的真相

**示例**：
```markdown
## Facts（冻结事实）

### 业务域词典
- **增量接入**：只同步变化的数据（vs 全量接入）
- **ratePlan**：价格计划，包含房型、日期、价格、库存
- **库存锁定**：支付前锁定库存，防止超卖

### 核心约束
- 库存锁定策略：支付前锁定，30分钟超时释放
- 取消政策边界：入住前 24 小时可免费取消
- 价格优先级：协议价 > 促销价 > 门市价

### 系统边界
- 同程侧：订单系统、支付系统、库存系统
- 酒店侧：如家 PMS、华住 CRS
- 中间件：RabbitMQ、Redis
```

### Snapshot（当前版本）

**内容**：
- 背景/目标/非目标
- 关键流程（1-2 个主流程 + 例外流）
- 关键规则（业务规则、优先级、分支条件）
- 关键接口/字段（只放业务上重要的）

**特点**：
- 反映"现在长什么样"
- 让 AI 快速理解"现在要做什么"

**示例**：
```markdown
## Snapshot（当前版本）

### 背景
如家需要支持增量接入，减少数据同步量，提升性能。

### 目标
- 支持订单增量同步（只同步变化的订单）
- 支持库存增量同步（只同步变化的库存）

### 非目标
- 不支持历史订单全量同步
- 不支持房型 mapping（单独需求）

### 关键流程

#### 订单增量同步
1. 如家推送订单变更（MQ）
2. 同程接收并解析
3. 更新订单状态
4. 回调如家确认（异步）

#### 库存增量同步
1. 如家推送库存变更（MQ）
2. 同程接收并更新缓存
3. 触发价格重算

### 关键规则
- 回调失败重试 3 次（指数退避）
- 库存变更实时生效
- 订单状态以如家为准

### 关键接口
- `POST /order/sync`：订单同步接口
- `POST /inventory/sync`：库存同步接口
- `POST /callback/confirm`：回调确认接口
```

### Changelog（变更历史）

**内容**：
- 每次变更只追加
- 记录变更点、影响面、兼容策略

**特点**：
- 用"补丁"让上下文渐进更新
- 不靠改旧内容维持一致性

**示例**：
```markdown
## Changelog（变更历史）

### 2026-02-23：初始版本
- 初始设计

### 2026-02-24：回调改成异步

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

### 2026-02-25：增加预付支持

**变更点**：
- 支持预付订单（先付款后入住）

**影响面**：
- 规则：预付订单不需要库存锁定
- 接口：订单接口增加 `payment_type` 字段

**兼容策略**：
- 向后兼容：默认 `payment_type=postpay`
```

## 渐进演进路径

### 阶段 1：小需求（单文件）

**适用场景**：
- 需求简单，预计不会频繁变更
- 团队成员少，上下文可控

**文件结构**：
```
rujia-mapping/
└── prd.md  # 包含 Facts + Snapshot + Changelog
```

### 阶段 2：中需求（拆分 Facts）

**触发条件**：
- Facts 内容变多（超过 50 行）
- Facts 需要被多个需求共享

**文件结构**：
```
rujia-incremental/
├── facts.md  # 独立出来
└── prd.md    # 包含 Snapshot + Changelog
```

**迁移指令**：
```
prd-split-facts: docs/hotel-integration/rujia-incremental
```

### 阶段 3：大需求（完全拆分）

**触发条件**：
- Changelog 内容变多（超过 100 行）
- 需要频繁查看变更历史

**文件结构**：
```
rujia-incremental/
├── facts.md
├── snapshot.md
└── changelog.md
```

**迁移指令**：
```
prd-split-full: docs/hotel-integration/rujia-incremental
```

## 版本选择

### RULE-lite.md（精简版，推荐）

**特点**：
- 只有 90 行，节省上下文
- 包含核心逻辑：触发机制、三层结构、去躁点判定、更新策略
- 适合日常使用

**使用场景**：
- 日常 PRD 维护
- 上下文敏感的项目
- 需要节省 token

**启用方式**：
```bash
cp rules/prd-maintenance/RULE-lite.md \
   your-project/.claude/prd-maintenance.md
```

### RULE.md（完整版）

**特点**：
- 465 行，包含详细说明、示例、最佳实践
- 适合学习和参考

**使用场景**：
- 第一次使用，需要详细了解
- 团队培训和文档参考
- 需要查看完整示例

**启用方式**：
```bash
cp rules/prd-maintenance/RULE.md \
   your-project/.claude/prd-maintenance.md
```

**建议**：先用完整版学习，熟悉后切换到精简版。

## 与 docs-writing-protocol 的关系

**docs-writing-protocol**：
- 通用的文档写入协议
- 适用于所有类型的文档
- 定义"何时写入"和"去躁点"规则

**prd-maintenance**：
- 专门针对 PRD 维护的协议
- 继承 docs-writing-protocol 的"去躁点"规则
- 增加"三层结构"和"供应商隔离"
- 增加"渐进演进"机制

**关系**：
- prd-maintenance 是 docs-writing-protocol 的特化版本
- 可以同时启用两个规则（prd-maintenance 优先级更高）

## 最佳实践

### 1. 供应商隔离

每个供应商/大需求独立目录：
```
docs/hotel-integration/
├── rujia-incremental/
├── huazhu-full/
└── jinjiang-incremental/
```

### 2. Facts 共享

如果多个供应商共享相同的 Facts：
```
docs/hotel-integration/
├── common-facts.md       # 共享的冻结事实
├── rujia-incremental/
│   └── facts.md          # 引用 common-facts.md
└── huazhu-full/
    └── facts.md          # 引用 common-facts.md
```

### 3. 迭代管理

如果需要按迭代管理（敏捷开发）：
```
docs/hotel-integration/rujia-incremental/
├── facts.md
├── snapshot.md
├── changelog.md
└── iterations/
    ├── sprint-1.md
    ├── sprint-2.md
    └── sprint-3.md
```

## License

MIT
