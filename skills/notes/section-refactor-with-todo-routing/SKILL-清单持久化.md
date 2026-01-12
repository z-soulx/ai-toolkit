---
name: section-refactor-with-todo-routing
description: 基于 learning-notes-organizer 的方法论，对指定文件执行“全标题索引+含义/引导注释 + 指定章节重构 + 越界内容路由到合适标题并按需新增待整理容器”的局部重构工作流；用 planning-with-files 输出抽取→规划→映射→交付，范围外章节默认不改，仅做迁移所需最小改动。
metadata:
  short-description: 指定章节精修 + 越界内容路由到目标标题/待整理（含全标题含义与引导注释）
  version: v2
  dependencies:
    - learning-notes-organizer
    - planning-with-files
  notes:
    - v2 增强：支持“含义/引导注释”双输出、章节路径匹配、多级最小改动策略、待整理容器策略、迁移块ID便于后续点名继续整理

---

# Section Refactor with Todo Routing (v2)

## 目的

在不必全篇重构的情况下，完成三件事：

1) **全局导航**：抽取文件内所有标题（H1-H6），并为每个标题输出：
   - 一句话“含义/本节讲什么”
   - 一句话“引导注释：读完你会…”
2) **局部重构**：只对用户指定章节（1~N 个，可变）进行重构整理（精简啰嗦、增强连贯、边界清晰、学习路径更顺滑、术语一致）。
3) **越界内容路由**：指定章节中若存在不属于该章节边界的内容块：
   - 路由到更合适的目标标题下；
   - 若目标标题下缺少合适容器或需要暂存，则在该目标标题下新增子标题 `待整理` 并把内容放入其中；
   - 便于用户后续“点名某个待整理模块”继续整理。

## 依赖

- `$learning-notes-organizer`
  - 用于边界判断、归类、学习路径、精修重写、格式保真等规范（本 skill 不重复展开细则）
- `$planning-with-files`
  - 用于组织执行流程与交付结构（抽取→规划→映射→交付）

---

## 输入

必填：
- `target_file`: 目标 Markdown 文件路径
- `focus_sections`: 需要重构的章节列表（1~N 个，可变）
  - 支持：标题名（模糊）或标题路径（精确）
  - 示例：
    - `["学习资源与概览", "核心概念与内存背景"]`
    - `["核心概念与内存背景/ByteBuf", "Pipeline/Handler"]`

可选参数（v2 新增，推荐默认即可）：

### 读取/抽取
- `heading_level_support`: 默认 `H1-H6`
- `meaning_source`: `"title_plus_snippets"` | `"full_text"`
  - 默认 `"title_plus_snippets"`（含义/引导注释基于标题+少量内容）
- `intro_policy`: `"prefer_existing_then_generate"` | `"generate_if_missing"` | `"existing_only"`
  - 默认 `"prefer_existing_then_generate"`

### 匹配策略
- `section_match_policy`: `"prefer_path_then_title"` | `"title_only"`
  - 默认 `"prefer_path_then_title"`
- `duplicate_title_policy`: `"ask_tbd"` | `"pick_best_match_with_reason"`
  - 默认 `"pick_best_match_with_reason"`（并在摘要说明匹配理由；实在不确定标记 TBD）

### 越界内容与待整理容器
- `routing_unit`: `"subsection"` | `"paragraph_block"`
  - 默认 `"paragraph_block"`（更细粒度；必要时可按小节搬）
- `todo_bucket_name`: 默认 `"待整理"`
- `add_todo_bucket_policy`: `"only_when_needed"` | `"always_when_routing"`
  - 默认 `"only_when_needed"`
- `todo_insert_position`: `"top_of_target_section"` | `"bottom_of_target_section"`
  - 默认 `"top_of_target_section"`（更醒目）

### 范围外改动策略
- `outside_scope_edit_policy`: `"minimal_only"` | `"allow_small_fixes"`
  - 默认 `"minimal_only"`
  - minimal_only：只允许在目标标题下新增待整理并插入迁移内容
  - allow_small_fixes：在 minimal 基础上，允许做小修复（断链/术语一致/必要过渡），但不得扩展为范围外重写

### 可追踪标记（便于后续点名继续整理）
- `migration_id_policy`: `"auto_ids"` | `"none"`
  - 默认 `"auto_ids"`（为迁移内容块生成可引用 ID）

---

## 执行步骤（必须按 $planning-with-files 输出）

### Step 1 — 抽取（Extract）
- 提取完整标题树（H1-H6，含层级路径）
- 为每个标题输出：
  - **含义**：一句话“这节讲什么”
  - **引导注释**：一句话“读完你会…”
- 引导注释生成遵循 `intro_policy`

### Step 2 — 规划（Plan）
- 仅针对 `focus_sections`：
  - 给出章节边界（应包含/不包含什么）
  - 调整内部结构与顺序（基础→机制→实践→坑点/优化；按内容需要）
  - 标记越界内容块（按 `routing_unit`）

### Step 3 — 映射（Map）
- 对指定章节内内容块：
  - 旧位置 → 新位置（同章内部重排）
- 对越界内容块：
  - 来源位置 → 目标标题路径
  - 若目标标题下缺少合适容器或需要暂存：
    - 新增子标题 `待整理`（按 `todo_bucket_name`）
    - 将内容放入该 `待整理`（按 `todo_insert_position`）
- 若 `migration_id_policy=auto_ids`：
  - 为每个迁移内容块生成 `MIG-xxx` 标记，便于后续点名继续整理

### Step 4 — 交付（Deliver）
- 输出“全标题索引+含义+引导注释”
- 输出“指定章节重构后的最终 Markdown”（可直接替换回原文件）
- 输出“迁移与待整理新增清单”（可追踪、可复盘）
- 输出“变更摘要”

---

## 交付物格式（必须包含）

### A) 全标题索引（H1-H6）+ 含义 + 引导注释
- 用树形层级展示（路径清晰）
- 每个标题至少两行：
  - `含义：...`
  - `引导注释：...`

### B) 指定章节重构结果（可直接替换的 Markdown）
- 仅输出被重构的章节（包含必要的父级标题上下文）
- 标题不自动编号；强调标记/代码块结构尽量保真（细则由 learning-notes-organizer 管）
- **必须在该 Markdown 输出的末尾追加一个“整理记录（本次路由与待整理）”区块**，将 C) 与 D) 两张表写入其中（见“写入位置规范”）

### C) 越界内容路由清单（从指定章节迁出）
| MIG-ID | 来源位置（章节/小节） | 内容块简述 | 目标标题路径 | 落点（目标标题/待整理） |
| ------ | --------------------- | ---------- | ------------ | ----------------------- |

### D) 新增 `待整理` 清单

| 目标标题路径 | 是否新增 `待整理` | 插入位置（bottom） | 放入了哪些 MIG-ID/内容块 |
| ------------ | ----------------: | ------------------ | ------------------------ |

---

## 写入位置规范（v2.1 新增）

- C) 越界内容路由清单 与 D) 新增 `待整理` 清单必须**同时**：
  1) 在聊天交付中以表格形式单独输出（便于快速查看）
  2) 追加写入到“B) 指定章节重构结果”的末尾，作为文档内留档

- 追加写入的区块格式必须固定如下（放在 B 的最后）：

### 整理记录（本次路由与待整理）
> 说明：本区块用于留档本次从指定章节迁出的内容及“待整理”容器新增情况，便于后续点名继续整理。

#### 越界内容路由清单
（插入 C 表格）

#### 新增 `待整理` 清单
（插入 D 表格）

## 调用模板（推荐）

```text
使用 $section-refactor-with-todo-routing（v2）
target_file: <path/to/file.md>
focus_sections: ["章节1", "章节2", ...]
# 可选：
outside_scope_edit_policy: minimal_only
add_todo_bucket_policy: only_when_needed
migration_id_policy: auto_ids