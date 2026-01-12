---
name: image-alt-title-filler
description: 脚本化图片 alt/title 补全工具。脚本负责提取和替换，模型只负责看图生成描述。支持 Markdown 和 HTML 图片，严格不改路径、不丢图。
metadata:
  version: v5-planning
  safety: 必须先 --dry-run 预览，确认无误后再执行
  dependencies:
    - planning-with-files
---

# Image Alt/Title Filler (脚本化版本)

## 核心特性

✅ **脚本化操作** - 查找和替换都由脚本完成，速度快
✅ **模型只看图** - 模型只负责读取图片生成描述，不做文本操作
✅ **批次处理** - 支持分批处理大量图片
✅ **降级机制** - 图片读取失败时自动使用上下文推断
✅ **完整账本** - 记录每张图片的变更详情
✅ **预览模式** - 必须先预览再执行，保证数据安全
✅ **自动备份** - 执行前自动创建带时间戳的备份文件

## 3-File Pattern (遵循 planning-with-files)

本 skill 采用 planning-with-files 的 3-file 模式：

| 文件 | 用途 | 更新时机 |
|------|------|----------|
| task_plan.md | 跟踪 A-D 工作流阶段进度 | 每个阶段完成后 |
| notes.md | 记录批次处理发现（可选） | 处理批次时 |
| image_ledger.md | 最终交付物：图片变更账本 | 步骤 D 完成后 |

### 工作流程
1. **开始前**: 创建 task_plan.md，定义 4 个阶段
2. **每个阶段后**: 更新 task_plan.md，标记完成
3. **处理批次时**: 可选记录到 notes.md
4. **完成后**: image_ledger.md 作为最终交付物

## 硬性规则

- ❌ 不删除任何图片引用
- ❌ 不修改 src 路径
- ❌ 不重命名图片文件
- ✅ 每张图片必须出现在变更账本中
- ✅ 能读到图片时必须基于图片内容生成（不是文件名）
- ✅ 读不到图片必须降级为上下文推断，并标记 FALLBACK_CONTEXT
- ⚠️ **必须先执行 --dry-run 预览，确认无误后再正式执行**

## 使用流程

### 步骤 0: 创建任务计划（必须！）

⚠️ **遵循 planning-with-files 原则**

创建 `task_plan.md`:
```markdown
# Task Plan: 图片 Alt/Title 补全

## Goal
为 [文档名] 的所有图片生成语义化的 alt/title

## Phases
- [ ] Phase A: 提取图片清单
- [ ] Phase B: 生成批次任务
- [ ] Phase C: 处理批次（看图生成描述）
- [ ] Phase D: 应用补丁并验证

## Status
**Currently in Phase A** - 准备提取图片清单
```

### 步骤 A: 提取图片清单

```bash
python scripts/01_extract_manifest.py --target_md <你的文档.md> --out_dir .
```

**输出**: `manifest.json` - 包含所有图片的位置、上下文信息

**完成后**: 更新 task_plan.md，标记 Phase A 完成

### 步骤 B: 生成批次任务

```bash
python scripts/02_make_batch_prompts.py --manifest manifest.json --out_dir batches --batch_size 8
```

**输出**: `batches/batch_001.md`, `batch_002.md`, ... - 每个批次的处理任务

**完成后**: 更新 task_plan.md，标记 Phase B 完成

### 步骤 C: 处理批次（在 IDE 中执行）

打开 `batches/batch_001.md`，按照提示：

1. **逐个打开图片文件** - 使用 Read 工具查看本地图片
2. **生成 alt/title** - 基于图片内容生成简洁的中文描述
3. **保存结果** - 将结果保存为 `results/batch_001.results.json`
4. **可选**: 记录发现到 `notes.md`

**结果格式示例**:
```json
{
  "batch": 1,
  "results": [
    {
      "index": 0,
      "src": "images/architecture.png",
      "new_alt": "系统架构图展示微服务间的调用关系",
      "new_title": "系统架构图展示微服务间的调用关系",
      "fallback": false,
      "note": ""
    },
    {
      "index": 1,
      "src": "images/missing.png",
      "new_alt": "Redis 缓存穿透解决方案流程图",
      "new_title": "Redis 缓存穿透解决方案流程图",
      "fallback": true,
      "note": "图片无法打开，基于上下文推断"
    }
  ]
}
```

重复处理所有批次，直到完成。

**完成后**: 更新 task_plan.md，标记 Phase C 完成

### 步骤 D: 应用补丁

#### D1: 预览变更（必须！）

⚠️ **安全要求**: 必须先预览，确认无误后再执行

```bash
python scripts/03_apply_patch.py \
  --target_md <你的文档.md> \
  --manifest manifest.json \
  --results_dir results \
  --out_md patched.md \
  --out_ledger image_ledger.md \
  --update_policy smart \
  --title_policy same_as_alt \
  --max_len_alt 40 \
  --max_len_title 40 \
  --dry-run
```

**预览输出**:
- 显示将要更新的图片数量
- 显示前 3 个变更示例
- **不会实际修改文件**

**检查要点**:
1. 图片数量是否正确
2. src 路径是否匹配
3. 变更示例是否合理
4. 是否有意外的覆盖

**完成后**: 在 task_plan.md 中记录预览结果

#### D2: 正式应用补丁

⚠️ **仅在预览确认无误后执行**

```bash
python scripts/03_apply_patch.py \
  --target_md <你的文档.md> \
  --manifest manifest.json \
  --results_dir results \
  --out_md patched.md \
  --out_ledger image_ledger.md \
  --update_policy smart \
  --title_policy same_as_alt \
  --max_len_alt 40 \
  --max_len_title 40
```

**输出**:
- `patched.md` - 更新后的文档
- `image_ledger.md` - 完整的变更账本（最终交付物）
- 自动创建备份文件（带时间戳）

**完成后**: 更新 task_plan.md，标记 Phase D 完成

### 步骤 E: 验证结果

```bash
# 1. 检查账本文件
cat image_ledger.md

# 2. 对比原文件和新文件
diff <你的文档.md> patched.md

# 3. 确认无误后替换原文件
cp patched.md <你的文档.md>
```

## 参数说明

### update_policy（更新策略）
- `always` - 总是更新 alt/title
- `smart` - 智能更新（如果原有内容不像文件名则保留）
- `empty_only` - 仅更新空的 alt/title

### title_policy（title 策略）
- `same_as_alt` - title 与 alt 相同（推荐）
- `keep` - 保持原 title 不变
- `update` - 独立更新 title

### max_len_alt / max_len_title
- 限制 alt/title 的最大长度（默认 40 字符）

### ledger_format（账本格式）
- `table` - 表格汇总格式（默认，推荐）
  - 一行一张图片，便于快速浏览
  - 包含统计信息（总计、已更新、保留、降级）
  - 类似老版本格式
- `detailed` - 详细逐条格式
  - 包含原片段和新片段代码块
  - 适合需要查看具体变更的场景

### 备份选项
- `--no-backup` - 不创建备份文件（完全信任流程）
- `--auto-cleanup-backup` - 执行成功后自动删除备份文件（推荐）
  - 仍会创建备份（防止写入错误）
  - 验证输出文件成功后自动清理
  - 避免累积备份文件

## 目录结构

### Skill 目录（只包含脚本）
```
.codex/skills/image-alt-title-filler/
├── SKILL.md                          # 本文件
├── scripts/
│   ├── 01_extract_manifest.py        # 提取图片清单
│   ├── 02_make_batch_prompts.py      # 生成批次任务
│   └── 03_apply_patch.py             # 应用补丁
├── SAFETY_REVIEW.md                  # 安全审查报告
└── CHANGELOG.md                      # 版本更新记录
```

### 工作目录（执行时创建）
```
working_directory/
├── task_plan.md              # 任务计划（遵循 planning-with-files）
├── notes.md                  # 批次处理笔记（可选）
├── manifest.json             # 提取的图片元数据
├── batches/                  # 批次任务
│   ├── batch_001.md
│   └── batch_002.md
├── results/                  # AI 生成的描述
│   ├── batch_001.results.json
│   └── batch_002.results.json
├── patched.md                # 更新后的文档
└── image_ledger.md           # 最终交付物：变更账本
```

## 快速开始示例

```bash
# 0. 创建任务计划
cat > task_plan.md <<'EOF'
# Task Plan: 图片 Alt/Title 补全

## Goal
为 node/中间件/redis/redis实战.md 的所有图片生成语义化的 alt/title

## Phases
- [ ] Phase A: 提取图片清单
- [ ] Phase B: 生成批次任务
- [ ] Phase C: 处理批次
- [ ] Phase D: 应用补丁并验证

## Status
**Currently in Phase A**
EOF

# A. 提取图片
python scripts/01_extract_manifest.py --target_md "node/中间件/redis/redis实战.md" --out_dir .

# 更新 task_plan.md: 标记 Phase A 完成

# B. 生成批次（每批 8 张图）
python scripts/02_make_batch_prompts.py --manifest manifest.json --out_dir batches --batch_size 8

# 更新 task_plan.md: 标记 Phase B 完成

# C. 在 IDE 中打开 batches/batch_001.md，按提示处理
# 更新 task_plan.md: 标记 Phase C 完成

# D1. 预览变更（必须！）
python scripts/03_apply_patch.py \
  --target_md "node/中间件/redis/redis实战.md" \
  --manifest manifest.json \
  --results_dir results \
  --out_md patched.md \
  --out_ledger image_ledger.md \
  --dry-run

# D2. 确认预览无误后，正式执行（使用表格格式 + 自动清理备份）
python scripts/03_apply_patch.py \
  --target_md "node/中间件/redis/redis实战.md" \
  --manifest manifest.json \
  --results_dir results \
  --out_md patched.md \
  --out_ledger image_ledger.md \
  --ledger_format table \
  --auto-cleanup-backup

# 更新 task_plan.md: 标记 Phase D 完成

# E. 检查账本并替换原文件
cat image_ledger.md
cp patched.md "node/中间件/redis/redis实战.md"
```

## 注意事项

1. **⚠️ 安全第一** - 必须先执行 `--dry-run` 预览，确认无误后再正式执行
2. **自动备份** - 正式执行时会自动创建备份文件（格式：`原文件名.backup_时间戳.md`）
3. **图片路径** - 脚本会自动处理相对路径和绝对路径
4. **批次大小** - 建议每批 5-10 张图片，避免单次处理过多
5. **降级处理** - 图片无法打开时，基于上下文推断并标记 `fallback: true`
6. **账本检查** - 完成后务必检查 `image_ledger.md` 确认所有图片都已处理

## 常见问题

**Q: 为什么要分批处理？**
A: 避免单次处理过多图片导致超时或内存问题，分批处理更稳定。

**Q: 图片打不开怎么办？**
A: 设置 `fallback: true`，基于上下文推断生成描述，脚本会自动标记。

**Q: 如何只更新空的 alt/title？**
A: 使用 `--update_policy empty_only` 参数。

**Q: 可以自定义 alt 和 title 的长度吗？**
A: 可以，使用 `--max_len_alt` 和 `--max_len_title` 参数。
