# Markdown to PDF Skill (v2.0)

将 Markdown 文档转换为专业的苹果设计风格 PDF 白皮书。

## 快速开始

### 1. 安装依赖

```bash
# Python 依赖
pip3 install markdown pdfkit Pillow

# 系统依赖
brew install wkhtmltopdf  # macOS
# 或
sudo apt-get install wkhtmltopdf  # Linux
```

### 2. 基础使用

```bash
# 转换 Markdown 文件
python scripts/convert.py your-file.md

# 指定输出文件名
python scripts/convert.py your-file.md -o "我的白皮书.pdf"

# 自定义标题和作者
python scripts/convert.py your-file.md --title "技术白皮书" --author "团队"
```

### 3. 完整工作流（推荐）

```bash
# 一键执行：图片处理 + PDF 生成
python scripts/workflow.py your-file.md
```

## v2.0 新特性

### 🎉 主要改进

- ✅ **安装更简单**：使用 wkhtmltopdf 替代 WeasyPrint，无需 pango
- ✅ **图片支持更好**：自动处理 WebP 格式，支持无扩展名图片
- ✅ **完整工具链**：提供图片分析、转换、引用更新工具
- ✅ **一键工作流**：从图片处理到 PDF 生成的自动化流程

### 依赖对比

| 依赖 | v1.0 | v2.0 |
|------|------|------|
| Python 库 | markdown2, weasyprint | markdown, pdfkit, Pillow |
| 系统依赖 | pango (复杂) | wkhtmltopdf (简单) |
| 安装难度 | ⭐⭐⭐⭐ | ⭐⭐ |

## Markdown 格式要求

你的文档应该使用带序号的章节格式：

```markdown
# 文档标题

## 1. 第一章
### 1.1 第一节
内容...

### 1.2 第二节
内容...

## 2. 第二章
### 2.1 第一节
...
```

**关键点**：
- ✅ `## 1. 标题` - 正确（数字.空格标题）
- ❌ `## 标题` - 错误（无序号）
- ✅ `### 1.1 标题` - 正确
- ❌ `### 标题` - 错误

## 工具说明

### convert.py - 核心转换工具

基础的 Markdown 到 PDF 转换：

```bash
python scripts/convert.py input.md
python scripts/convert.py input.md -o output.pdf
python scripts/convert.py input.md --title "标题" --author "作者"
```

### workflow.py - 完整工作流（推荐）

自动处理图片并生成 PDF：

```bash
# 完整流程
python scripts/workflow.py input.md

# 跳过图片处理
python scripts/workflow.py input.md --skip-images

# 自定义输出
python scripts/workflow.py input.md -o output.pdf --title "标题"
```

### analyze_images.py - 图片分析

检测图片格式问题：

```bash
python scripts/analyze_images.py
```

生成 `conversion_plan.json` 报告。

### batch_convert_images.py - 批量转换

转换 WebP 图片为 PNG：

```bash
python scripts/batch_convert_images.py
```

生成 `filename_mapping.json` 映射表。

### update_markdown_refs.py - 引用更新

更新 Markdown 中的图片引用：

```bash
python scripts/update_markdown_refs.py
```

生成 `markdown_update_report.json` 报告。

## 设计特点

- 📖 **书籍级排版**：自动分页、孤行寡行控制
- 🎨 **苹果设计语言**：SF 字体、现代简洁
- 📑 **自动目录**：双列布局、可点击跳转
- 💻 **完美代码块**：语法高亮、圆角边框
- 📊 **专业表格**：清晰网格、自动表头

## 常见问题

### Q: wkhtmltopdf 安装失败？

```bash
# macOS
brew install wkhtmltopdf

# Linux
sudo apt-get install wkhtmltopdf

# 或下载二进制
# https://wkhtmltopdf.org/downloads.html
```

### Q: 目录为空？

确保使用 `## 1.` 和 `### 1.1` 格式。

### Q: 图片显示不正确？

使用完整工作流：
```bash
python scripts/workflow.py input.md
```

### Q: 如何从 v1.0 升级？

查看 `UPGRADE.md` 文档。

## 文件结构

```
.claude/skills/markdown-to-pdf/
├── SKILL.md                      # 完整文档
├── README.md                     # 本文件
├── EXAMPLES.md                   # 使用示例
├── UPGRADE.md                    # 升级指南
├── WORKFLOW.md                   # 工作流文档
└── scripts/
    ├── convert.py                # 核心转换
    ├── analyze_images.py         # 图片分析
    ├── batch_convert_images.py   # 批量转换
    ├── update_markdown_refs.py   # 引用更新
    └── workflow.py               # 完整工作流
```

## 示例

### 基础转换

```bash
python scripts/convert.py document.md
# 输出: document.pdf
```

### 完整工作流

```bash
python scripts/workflow.py document.md
# 自动处理图片并生成 PDF
```

### 自定义输出

```bash
python scripts/convert.py document.md \
  --title "技术白皮书 2025" \
  --author "技术团队" \
  -o "whitepaper-2025.pdf"
```

## 更多信息

- 完整文档：查看 `SKILL.md`
- 使用示例：查看 `EXAMPLES.md`
- 升级指南：查看 `UPGRADE.md`
- 工作流说明：查看 `WORKFLOW.md`

## 更新日志

### v2.0 (2025-01-30)
- 使用 pdfkit 替代 WeasyPrint
- 移除 pango 依赖
- 添加图片处理工具链
- 添加完整工作流
- 改进图片路径处理

### v1.0 (2025-12-24)
- 初始版本
- 苹果设计风格
- 自动目录生成

---

**版本**: v2.0
**更新**: 2025-01-30
**作者**: Claude Code
