# Markdown to PDF 完整工作流文档

从图片处理到 PDF 生成的完整自动化流程

---

## 工作流概述

v2.0 提供了完整的图片处理和 PDF 生成工作流，解决了 WebP 图片兼容性和无扩展名图片的问题。

### 工作流程图

```
输入 Markdown 文件
        ↓
[1] 分析图片格式 (analyze_images.py)
        ↓
    检测问题图片
        ↓
[2] 批量转换图片 (batch_convert_images.py)
        ↓
    WebP → PNG
        ↓
[3] 更新 Markdown 引用 (update_markdown_refs.py)
        ↓
    更新图片路径
        ↓
[4] 生成 PDF (convert.py)
        ↓
输出 PDF 文件
```

---

## 使用方式

### 方式 1: 一键式工作流（推荐）

最简单的方式，自动执行所有步骤：

```bash
python scripts/workflow.py input.md
```

**适用场景**:
- 首次转换文档
- 文档包含图片
- 不确定图片格式是否正确

**输出**:
- `input.pdf` - 生成的 PDF
- `input.html` - 中间 HTML（用于调试）
- `conversion_plan.json` - 图片分析报告
- `filename_mapping.json` - 文件名映射表
- `markdown_update_report.json` - 引用更新报告

### 方式 2: 分步执行

更精细的控制，适合调试和定制：

```bash
# 步骤 1: 分析图片
python scripts/analyze_images.py

# 步骤 2: 转换图片
python scripts/batch_convert_images.py

# 步骤 3: 更新引用
python scripts/update_markdown_refs.py

# 步骤 4: 生成 PDF
python scripts/convert.py input.md
```

**适用场景**:
- 需要检查每一步的结果
- 只需要执行部分步骤
- 调试问题

### 方式 3: 仅转换（跳过图片处理）

如果图片已经处理好，或者没有图片：

```bash
python scripts/convert.py input.md
```

**适用场景**:
- 文档不包含图片
- 图片格式已经正确
- 快速重新生成 PDF

---

## 工具详解

### 1. analyze_images.py - 图片格式分析

#### 功能

检测 `image/` 目录中的图片实际格式：
- 通过 Magic Bytes 检测真实格式
- 识别无扩展名的 WebP
- 识别错误扩展名的 WebP（如 .png 但实际是 WebP）
- 生成转换计划报告

#### 使用方法

```bash
# 在 Markdown 文件所在目录执行
cd /path/to/markdown/dir
python /path/to/scripts/analyze_images.py

# 或指定目录
python scripts/analyze_images.py image/
```

#### 输出

生成 `conversion_plan.json`:

```json
{
  "stats": {
    "total_files": 150,
    "webp_no_ext_count": 25,
    "webp_wrong_ext_count": 10,
    "correct_format_count": 115
  },
  "conversion_plan": {
    "webp_no_ext": [
      {
        "file": "640-20250716165831849",
        "new_name": "640-20250716165831849.png"
      }
    ],
    "webp_wrong_ext": [
      {
        "file": "image.png",
        "extension": ".png",
        "actual_format": "webp"
      }
    ]
  },
  "potential_conflicts": [],
  "unknown_format": [],
  "errors": []
}
```

#### 报告解读

- **webp_no_ext**: 无扩展名的 WebP 文件，需要添加 .png 扩展名
- **webp_wrong_ext**: 扩展名错误的 WebP 文件，需要转换为真正的 PNG
- **potential_conflicts**: 文件名冲突（如 `image` 和 `image.png` 同时存在）
- **unknown_format**: 无法识别的格式
- **errors**: 读取错误的文件

### 2. batch_convert_images.py - 批量图片转换

#### 功能

根据转换计划批量转换图片：
- 将无扩展名的 WebP 转换为 PNG 并添加扩展名
- 将错误扩展名的 WebP 转换为真正的 PNG
- 自动删除原 WebP 文件
- 生成文件名映射表

#### 使用方法

```bash
# 自动读取 conversion_plan.json
python scripts/batch_convert_images.py

# 或指定文件
python scripts/batch_convert_images.py conversion_plan.json image/
```

#### 输出

1. **转换后的图片**: 在 `image/` 目录中
2. **filename_mapping.json**: 文件名映射表

```json
{
  "640-20250716165831849": "640-20250716165831849.png",
  "640-20250716170159558": "640-20250716170159558.png"
}
```

#### 转换过程

```
开始批量转换图片
============================================================

处理无扩展名的 WebP 文件（25 个）...
  ✓ 640-20250716165831849 → 640-20250716165831849.png
  ✓ 640-20250716170159558 → 640-20250716170159558.png
  ...

处理有错误扩展名的 WebP 文件（10 个）...
  ✓ image.png (已转换为真正的 PNG)
  ...

转换完成
============================================================
总计：35 个文件
成功：35 个
跳过：0 个
失败：0 个

文件名映射表已保存到：filename_mapping.json
映射条目数：25
```

### 3. update_markdown_refs.py - 引用更新

#### 功能

更新 Markdown 文件中的图片引用：
- 支持 HTML `<img>` 标签
- 支持 Markdown `![]()`语法
- 根据映射表批量替换
- 生成更新报告

#### 使用方法

```bash
# 更新指定文件
python scripts/update_markdown_refs.py path/to/file.md

# 或在脚本中指定
# 修改 update_markdown_refs.py 的 __main__ 部分
```

#### 输出

生成 `markdown_update_report.json`:

```json
{
  "markdown_file": "node/网络与通信/netty.md",
  "stats": {
    "total_refs": 50,
    "updated_refs": 25,
    "skipped_refs": 25
  },
  "updates": [
    {
      "type": "img_tag",
      "old": "640-20250716165831849",
      "new": "640-20250716165831849.png"
    }
  ]
}
```

#### 更新过程

```
更新 Markdown 文件：node/网络与通信/netty.md
============================================================
映射条目数：25

  ✓ 640-20250716165831849 → 640-20250716165831849.png
  ✓ 640-20250716170159558 → 640-20250716170159558.png
  ...

更新完成
============================================================
总引用数：50
已更新：25
跳过：25

✓ Markdown 文件已更新
更新报告已保存到：markdown_update_report.json
```

### 4. convert.py - PDF 生成

#### 功能

将 Markdown 转换为 PDF：
- 提取元数据（标题、作者等）
- 生成目录（双列布局）
- 处理图片路径（绝对路径 + 扩展名补全）
- 应用苹果设计风格 CSS
- 生成专业 PDF

#### 使用方法

```bash
# 基础转换
python scripts/convert.py input.md

# 指定输出
python scripts/convert.py input.md -o output.pdf

# 自定义元数据
python scripts/convert.py input.md \
  --title "技术白皮书" \
  --subtitle "副标题" \
  --author "团队"
```

#### 输出

```
📖 读取文件: input.md
📑 提取元数据...
📂 提取目录结构...
   ✓ 找到 5 个主章节
   ✓ 找到 12 个子章节
🖼️  处理图片...
  ✓ 转换路径: image1.png
  ✓ 找到图片: image2.png
  ⚠️  图片不存在: missing.png
🎨 处理 Markdown 内容...
📄 生成 HTML...
💾 已保存 HTML: input.html
📝 生成 PDF...

✅ PDF 生成成功: input.pdf
📊 文件大小: 1.2 MB
```

### 5. workflow.py - 完整工作流

#### 功能

整合所有步骤的一键式工作流：
- 自动执行图片分析
- 自动转换图片
- 自动更新引用
- 自动生成 PDF
- 生成完整报告

#### 使用方法

```bash
# 完整流程
python scripts/workflow.py input.md

# 跳过图片处理
python scripts/workflow.py input.md --skip-images

# 自定义输出
python scripts/workflow.py input.md \
  -o output.pdf \
  --title "标题" \
  --author "作者"
```

#### 输出

```
============================================================
Markdown to PDF 完整工作流 v2.0
============================================================
输入文件: input.md

============================================================
步骤 1/4: 分析图片格式
============================================================
正在扫描 image 目录...
...

============================================================
步骤 2/4: 转换 WebP 图片
============================================================
开始批量转换图片
...

============================================================
步骤 3/4: 更新 Markdown 引用
============================================================
更新 Markdown 文件：input.md
...

============================================================
步骤 4/4: 生成 PDF
============================================================
📖 读取文件: input.md
...

============================================================
✅ 工作流完成
============================================================
PDF 文件: input.pdf
HTML 文件: input.html

报告文件:
  - conversion_plan.json
  - filename_mapping.json
  - markdown_update_report.json
```

---

## 实际案例

### 案例 1: 技术文档转换

**场景**: 将 netty.md 技术文档转换为 PDF

```bash
# 1. 进入文档目录
cd /path/to/documents

# 2. 执行完整工作流
python /path/to/scripts/workflow.py node/网络与通信/netty.md

# 3. 检查输出
ls -lh node/网络与通信/netty.pdf
```

**结果**:
- 自动处理了 50+ 个无扩展名的 WebP 图片
- 生成了 100+ 页的专业 PDF
- 包含完整的目录和封面

### 案例 2: 仅图片处理

**场景**: 只需要处理图片，不生成 PDF

```bash
# 1. 分析图片
python scripts/analyze_images.py

# 2. 查看报告
cat conversion_plan.json

# 3. 转换图片
python scripts/batch_convert_images.py

# 4. 更新引用
python scripts/update_markdown_refs.py
```

### 案例 3: 快速重新生成

**场景**: 图片已处理，只需重新生成 PDF

```bash
# 直接转换
python scripts/convert.py input.md
```

### 案例 4: 批量转换

**场景**: 转换多个文档

```bash
# 方式 1: 循环
for file in *.md; do
  python scripts/workflow.py "$file"
done

# 方式 2: 脚本
cat > batch_convert.sh << 'EOF'
#!/bin/bash
for file in "$@"; do
  echo "转换: $file"
  python scripts/workflow.py "$file"
done
EOF

chmod +x batch_convert.sh
./batch_convert.sh doc1.md doc2.md doc3.md
```

---

## 最佳实践

### 1. 文档组织

```
project/
├── docs/
│   ├── guide.md
│   ├── api.md
│   └── image/
│       ├── screenshot1.png
│       ├── diagram1.png
│       └── ...
└── output/
    ├── guide.pdf
    └── api.pdf
```

### 2. 图片命名

- ✅ 使用有意义的名称: `architecture-diagram.png`
- ✅ 使用扩展名: `.png`, `.jpg`, `.gif`
- ❌ 避免无扩展名: `640-20250716165831849`
- ❌ 避免特殊字符: `图片 (1).png`

### 3. Markdown 格式

```markdown
# 文档标题

**创建者**: 团队
**最后更新**: 2025-01-30

## 1. 第一章
### 1.1 第一节

内容...

![图片说明](../../image/diagram.png)
```

### 4. 工作流选择

| 场景 | 推荐方式 |
|------|---------|
| 首次转换 | workflow.py |
| 图片已处理 | convert.py |
| 调试问题 | 分步执行 |
| 批量转换 | workflow.py + 循环 |

---

## 故障排查

### 问题 1: 图片不显示

**症状**: PDF 中图片缺失

**排查步骤**:
```bash
# 1. 检查图片是否存在
ls -la image/

# 2. 分析图片格式
python scripts/analyze_images.py

# 3. 查看报告
cat conversion_plan.json

# 4. 使用完整工作流
python scripts/workflow.py input.md
```

### 问题 2: 转换失败

**症状**: `OSError: No wkhtmltopdf executable found`

**解决方案**:
```bash
# 检查 wkhtmltopdf
which wkhtmltopdf

# 如果没有，安装
brew install wkhtmltopdf  # macOS
sudo apt-get install wkhtmltopdf  # Linux
```

### 问题 3: 目录为空

**症状**: PDF 中没有目录

**原因**: Markdown 章节格式不正确

**解决方案**:
```markdown
# 错误格式
## 第一章
### 第一节

# 正确格式
## 1. 第一章
### 1.1 第一节
```

### 问题 4: 中文乱码

**症状**: PDF 中中文显示为方块

**解决方案**:
```bash
# Linux 安装中文字体
sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei

# macOS 通常自带中文字体，无需处理
```

---

## 性能优化

### 1. 大文档处理

对于 100+ 页的大文档：

```bash
# 使用 --skip-images 跳过图片处理（如果已处理）
python scripts/workflow.py large-doc.md --skip-images
```

### 2. 批量转换优化

```bash
# 并行处理（需要 GNU parallel）
ls *.md | parallel python scripts/workflow.py {}
```

### 3. 图片优化

```bash
# 压缩图片（使用 ImageMagick）
mogrify -resize 1920x1920\> -quality 85 image/*.png
```

---

## 总结

### 工作流优势

✅ **自动化**: 一键完成所有步骤
✅ **智能**: 自动检测和处理图片问题
✅ **可靠**: 生成详细报告，便于排查
✅ **灵活**: 支持分步执行和自定义

### 使用建议

1. **首次使用**: 使用 `workflow.py` 完整工作流
2. **日常使用**: 根据需要选择合适的工具
3. **问题排查**: 使用分步执行，查看每步输出
4. **批量处理**: 编写脚本，循环调用工具

---

**文档版本**: v1.0
**更新日期**: 2025-01-30
**作者**: Claude Code
