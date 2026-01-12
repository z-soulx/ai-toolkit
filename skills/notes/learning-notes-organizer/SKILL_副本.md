---
name: learning-notes-organizer
description: 整理与重构已有学习笔记：重划边界、归类重组、合并冗余、精简口语化表达；优化排版与可读性；为各部分补充引导与注释；按从基础到高级建立学习路径并打通知识关联；同时尽量保留原文 Markdown/HTML 强调标记（如 ==高亮==、<u>、Setext 标题等），输出结构清晰、可检索、便于长期维护的笔记体系。
metadata:
  short-description: 零散笔记 → 可维护知识库（保留强调标记；标题不编号；含引导注释与学习路径）
---

# Study Note Refactor

## 目标

将“长期积累但逐渐散乱”的学习笔记重构成：边界清晰、体系完整、渐进可学、可检索、可持续增量维护的学习笔记。：对文件内容进行整理重构，边界清晰，知识规划成体系，适合后续维护的学习笔记：

## 分步计划

1. 先做整体规划与移动：通读全篇，规划章节顺序，移动/归类段落与要点，但暂不改动原句内容。
2. 先局部优化，再整体优化：先在单个章节内完成排版/引导/去冗余等微调，确认局部质量后，再做全局一致性与跨章节的优化。

## 强制规则

### 题目不要有编号

- 所有 Markdown 标题（`#`/`##`/`###`…，包含 Setext 标题）不得以任何编号开头（如 `1.`、`一、`、`(1)`、emoji 序号等）

- 允许在正文列表中使用编号步骤，但不得写进标题文本

### Markdown 与强调标记保真

目标：精简与重构后，尽量保留原文的“强调语义”和“标记形态”。

必须遵守：

- 尽量保留并不改动：
  - `==高亮==`
  - `<u>...</u>`、`<mark>...</mark>` 等内联 HTML
  - `**粗体**`、`*斜体*`、`~~删除线~~`、`` `行内代码` ``、代码块围栏
  - 引用块 `>`、分隔线 `---` / `***`
  - Setext 标题（`标题` + `====` 或 `----`）
  - 链接/锚点（移动章节后要修复引用，保证可用）

- 允许“等价替换”仅在必要时发生，并满足：
  - 强调强度不降低
  - 含义更清晰或渲染更一致
  - 优先保留原写法；必要时可“保留原写法 + 增强补标记”（可选）

## 提示词模版

```
请阅读 {目标文件路径} 的所有内容，对文件内容进行整理重构，边界清晰，知识规划成体系，适合后续维护的学习笔记：
I'm planning a thorough reorganization of the design document by renaming sections, redefining boundaries, and adding intros to clarify scope. The goal is to group related content more logically—like combining guiding principles with architecture steps, reorganizing abilities into clearer categories, and elevating local design to its own top-level section—while removing redundancies and adjusting headings systematically. I'll approach this by applying structured edits and patches to implement the new layout steadily

1. 归类与标题重命名
根据知识点的内容和主题，进行合理的分类。将相似或相关的知识点放入同一类别下。
重命名笔记标题，确保每个标题能准确反映该部分内容，避免模糊和重复的标题。

2. 重新定义边界与组织结构
评估现有的分类和章节划分，确保它们具备逻辑性和层次感。
对内容进行细致划分，避免知识点过于分散，确保每个部分有明确的边界和内容关联。

3. 合并冗余与重复内容
查找并删除重复的记录，避免相同的知识点在不同位置多次出现。
合并类似或重叠的内容，精简信息，使笔记更简洁清晰。

4. 增加引导性文字与注释
在各部分的开头添加简短的引导性文字，帮助理解该部分知识点的核心思想。
在必要时添加注释，尤其是复杂的内容，帮助后期查看时更易理解。

5. 知识体系化与层次化组织
将知识点从基础到高级进行排序，按难度和重要性排列，使学习过程更为渐进。
确保每一部分内容都能形成一个完整的知识体系，且能够与其他部分形成有机联系。

6. 对于规划后的标题内的内容，可优化排版甚至重新组织成更合适的
审查当前版本笔记并识别需聚焦/排版问题。
设计更紧凑的段落结构（概念归纳、要点列表、过长段落拆分。
应用修改并复核格式/引用。
```
