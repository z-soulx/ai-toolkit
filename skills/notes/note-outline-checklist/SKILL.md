---
name: note-outline-checklist
description: 基于 Markdown 笔记，仅用全部标题与少量正文线索，生成学习笔记重构清单：新规划目录（基础→进阶）、旧标题→新目录映射、重命名建议；遵循 planning-with-files（task_plan/notes）与 learning-notes-organizer 的重划边界/归类重组思路，不改正文。
---

# Outline Checklist Generator

## Purpose
对指定 Markdown 学习笔记做“结构重构规划”，并生成一个同级的“可操作框架 md 文档”，便于用户按块手动复制原文完成迁移。

核心约束：
- 只读：标题 + 少量内容（用于判断边界）
- 不改正文、不搬运正文
- 交付：清单 + 框架（scaffold）文件内容/路径

## Dependencies
- skill: planning-with-files
  - 执行步骤与交付结构必须遵循该 skill 的流程骨架（Read → Diagnose → Propose → Map → Deliver）
- skill: learning-notes-organizer
  - 重构原则必须遵循该 skill（重划边界、归类重组、精简口语化、加引导注释、基础→高级串联）
  - 仍遵守“只交付清单/不改正文”的总约束

## Inputs
- target_file: <path/to/file.md>
- scope_policy (default: headings + small content)
  - 提取全部标题（H1-H6）
  - 每个标题下最多读取前 N 行或 1-3 段（仅用于判断主题归属）
  - 禁止通读全文、禁止重写正文
- scaffold_suffix (default): "-待整理"
- scaffold_same_dir (default): true
- scaffold_overwrite_policy (default): "safe"
  - safe: 若输出文件名已存在，则在文件名末尾追加 "-v2"/"-v3"（或加时间戳）
- optional: domain_hint（例如 netty / node 网络 / RPC / TCP）

## Outputs
1) Checklist（对话输出）
   - 新的规划标题结构（含引导注释）
   - 旧标题 → 新标题映射表（含动作标签）
   - 重命名建议（全局汇总）
   - 待确认问题（少量）
   - 迁移顺序建议（操作步骤）
2) Scaffold Markdown Content（框架 md 完整内容）
   - 写入路径规则：
     - dir = dirname(target_file)
     - base = basename(target_file, ".md")
     - out = dir + "/" + base + scaffold_suffix + ".md"
   - 若无法自动写文件：仍必须输出“应写入的路径 + 完整 md 内容”，由用户自行保存到该路径。

## Procedure (must be expressed using planning-with-files)
### Step 1 — Read (limited)
- 提取标题树（层级结构：H1-H6）
- 对每个标题仅抽取 scope_policy 允许的少量内容，用于判断：
  - 属于哪个主题域
  - 是否重复/过宽/过碎
  - 是否应合并/拆分/移动
- 不输出正文摘抄（除非极短用于定位问题，且不超过几行）

### Step 2 — Diagnose
- 标记并解释（用简短 bullet）：
  - 重复/交叉
  - 过宽/过碎
  - 顺序不合理（缺前置概念或高级内容提前）
  - 标题命名不规范（口语化、不可检索、含糊）
  - 缺失模块（例如：概念/机制/实践/坑点/优化/源码）

### Step 3 — Propose New Outline (from basics to advanced)
- 给出新的 2-4 层标题结构（建议）
- 每个一级/二级标题必须有 1 行“引导注释：读完你会……”
- 结构优先级：
  1) 概念与背景
  2) 核心机制/模型
  3) 实战与模式
  4) 常见坑/排障
  5) 性能优化/原理/源码（如适用）

### Step 4 — Mapping (old → new)
- 对每个旧标题给出归宿：新标题路径
- 标注动作标签（必选其一）：
  - KEEP / MOVE / MERGE / SPLIT / RENAME / DROP / TBD
- 合并/拆分必须在备注里说明原因与去向

### Step 5 — Rename Suggestions
- 只对“确实需要改名”的旧标题给建议
- 不需要改名的不要列入本清单（保持干净）
- 命名建议原则：
  - 可检索（标准术语）
  - 短、明确、边界清晰
  - 避免“杂谈/随记/一些想法”等弱标题

### Step 6 — Generate Scaffold File (operational md)
- 生成 <base>-待整理.md 框架内容，放在 target_file 同级目录
- 框架文件必须：
  - 顶部元信息（源文件、范围、规则）
  - 主体：新大纲结构（含引导注释）
  - 每个新标题下面生成“迁移块”（见 Scaffold Format）
  - 附录：旧→新映射表、重命名建议汇总、待确认问题、迁移顺序建议

### Step 7 — Deliver
- 在对话输出：
  - Checklist（A-E）
  - 输出文件路径 + 完整 Scaffold Markdown 内容

---

## Output Format (Checklist in chat)
### A) 新的规划标题结构（建议大纲）
- H1 ...
  - H2 ...（引导注释：...）
    - H3 ...

### B) 旧标题 → 新标题映射表
| 旧标题(含层级) | 动作(KEEP/MOVE/MERGE/SPLIT/RENAME/DROP/TBD) | 新标题路径 | 备注 |
| -------------- | ------------------------------------------- | ---------- | ---- |

### C) 重命名建议（全局汇总，仅列需要的）
- `旧标题` -> `建议标题`（原因：更标准/更短/更可检索/边界更准确）

### D) 待确认问题（最多 3-7 条）
- ...

### E) 迁移顺序建议（操作步骤）
1. 先创建新结构骨架（用 Scaffold）
2. 再按映射表逐块复制正文到对应迁移块
3. 最后统一处理交叉引用/重复段落/术语一致性

---

## Scaffold Markdown Format (must follow exactly)
> 文件名：<base>-待整理.md  
> 目标：让用户“打开就能一块块处理”，每块都有：来源旧标题 +（可选）重命名建议 + 迁移要点 + 粘贴区。

### Scaffold file structure

以下都为H1级别

1) 标题 + 元信息
2) 新大纲与迁移工作区（每个新标题一个迁移块）
3) 附录A：旧→新映射表（全量）
4) 附录B：重命名建议汇总（全量，仅列需要的）
5) 附录C：待确认问题
6) 附录D：迁移顺序建议

### Migration Block Template (for every new section)
- 必须包含“来源旧标题（可多条）”
- “重命名建议”段落：仅当本块存在需要改名的旧标题时才出现；否则整段省略
- 必须包含“迁移要点”和“粘贴区”

模板如下（逐节生成）：

#### Template
### <新标题>
> 引导注释：<一句话>

**来源旧标题（可多条，可能合并）：**
- (<动作>) `<旧标题1>`
- (<动作>) `<旧标题2>`
- (<动作>) `<旧标题3>`

**重命名建议（仅列需要重命名的旧标题）：**
- `<旧标题2>` -> `<建议标题2>`（原因：...）
- `<旧标题3>` -> `<建议标题3>`（原因：...）

**迁移要点（你复制时注意）：**
- <要点1>
- <要点2>
- <要点3>

⬇️ 在下面粘贴原文内容 ⬇️

（把原文复制到这里）
