---
name: markdown-to-pdf
description: |
  将 Markdown 文档转换为专业的 PDF 白皮书，采用苹果设计风格 (v2.0)。

  v2.0 改进:
  - 使用 pdfkit + wkhtmltopdf 替代 WeasyPrint (避免 pango 依赖问题)
  - 支持 WebP 等特殊格式图片处理
  - 自动处理无扩展名图片
  - 提供完整的图片处理工具链
  - 一键式工作流

  支持完整的 Markdown 语法 (代码块、表格、引用、列表等)。
  自动生成封面、目录、页眉页脚。
  使用场景: 技术文档、白皮书、教程、报告等需要专业排版的 Markdown 文档。
user-invocable: true
metadata:
  short-description: "Markdown 转专业 PDF 白皮书（苹果设计风格）"
  version: "2.0.0"
  category: "productivity"
---

# Markdown to PDF Skill (v2.0)

将 Markdown 文档转换为专业的苹果设计风格 PDF 白皮书。

## 版本更新

### v2.0 (2025-01-30)

**重大改进**:
- ✅ 使用 pdfkit + wkhtmltopdf 替代 WeasyPrint
- ✅ 移除 pango 依赖,安装更简单
- ✅ 支持 WebP 图片格式
- ✅ 自动处理无扩展名图片
- ✅ 添加完整图片处理工具链
- ✅ 提供一键式工作流

**依赖变更**:
```bash
# 旧版本 (v1.0)
pip3 install markdown2 weasyprint
brew install pango  # 复杂

# 新版本 (v2.0)
pip3 install markdown pdfkit Pillow
brew install wkhtmltopdf  # 简单
```

## 核心功能

1. **专业排版**: 书籍级排版质量,自动处理分页、孤行寡行
2. **苹果设计**: SF 字体系统、现代简洁风格、专业配色
3. **完整目录**: 自动提取章节结构,双列布局,可点击跳转
4. **Markdown 完美支持**: 代码块、表格、引用、列表等全部正确渲染
5. **图片处理**: 自动检测和转换 WebP 图片,处理无扩展名图片
6. **一键工作流**: 从图片处理到 PDF 生成的完整自动化流程

## 使用方法

### 方式 1: 基础转换

```bash
# 转换单个文件
python scripts/convert.py input.md

# 指定输出文件名
python scripts/convert.py input.md -o "我的白皮书.pdf"

# 自定义标题和作者
python scripts/convert.py input.md --title "技术白皮书" --author "花叔"
```

### 方式 2: 完整工作流 (推荐)

```bash
# 一键执行: 图片处理 + PDF 生成
python scripts/workflow.py input.md

# 跳过图片处理
python scripts/workflow.py input.md --skip-images

# 完整自定义
python scripts/workflow.py input.md \
  --title "技术白皮书" \
  --author "团队" \
  -o "output.pdf"
```

### 方式 3: 分步执行

```bash
# 步骤 1: 分析图片格式
python scripts/analyze_images.py

# 步骤 2: 转换 WebP 图片
python scripts/batch_convert_images.py

# 步骤 3: 更新 Markdown 引用
python scripts/update_markdown_refs.py

# 步骤 4: 生成 PDF
python scripts/convert.py input.md
```

## Markdown 文档要求

你的 Markdown 文档应该遵循以下结构:

```markdown
# 文档标题

## 1. 第一章
### 1.1 第一节
### 1.2 第二节

## 2. 第二章
### 2.1 第一节
```

**关键规则**:
- 主章节: `## 1. 标题` (数字 + 点 + 空格 + 标题)
- 子章节: `### 1.1 标题` (数字.数字 + 空格 + 标题)
- 这样才能正确提取目录

## 工具说明

### convert.py - 核心转换工具

将 Markdown 转换为 PDF,支持:
- 元数据提取 (标题、作者、日期等)
- 目录生成 (双列布局)
- 图片路径处理 (绝对路径 + 扩展名补全)
- 苹果设计风格 CSS

### analyze_images.py - 图片格式分析

检测图片实际格式:
- 通过 Magic Bytes 检测真实格式
- 识别无扩展名的 WebP
- 识别错误扩展名的 WebP
- 生成转换计划报告

### batch_convert_images.py - 批量图片转换

批量转换 WebP 为 PNG:
- 根据转换计划执行
- 自动删除原 WebP 文件
- 生成文件名映射表
- 生成转换报告

### update_markdown_refs.py - 引用更新

更新 Markdown 中的图片引用:
- 支持 HTML img 标签
- 支持 Markdown 图片语法
- 根据映射表批量替换
- 生成更新报告

### workflow.py - 完整工作流

一键执行所有步骤:
- 自动分析图片
- 自动转换格式
- 自动更新引用
- 自动生成 PDF

## 设计特点

### 封面设计
- 淡灰色渐变背景
- 大标题: 64pt,简洁现代
- 副标题和元信息

### 目录设计
- 双列布局,单页展示
- 主章节粗体,子章节缩进
- 可点击跳转到对应章节

### 正文排版
- SF 字体系列 (苹果设计语言)
- 行高 1.7,舒适阅读
- 章节自动分页
- 孤行寡行控制

### 代码块
- 浅灰背景 + 细边框
- 圆角 8px
- SF Mono 等宽字体
- 自动避免分页

### 表格
- 清晰网格线
- 浅灰表头
- 自动保留表头 (长表格分页时)

## 依赖安装

### Python 依赖

```bash
pip3 install markdown pdfkit Pillow
```

### 系统依赖

```bash
# macOS
brew install wkhtmltopdf

# Linux
sudo apt-get install wkhtmltopdf

# 或下载二进制: https://wkhtmltopdf.org/downloads.html
```

## 常见问题

### Q: 目录为什么是空的?
A: 确保你的 Markdown 使用了正确的章节格式:
- `## 1. 标题` 而不是 `## 标题`
- `### 1.1 标题` 而不是 `### 标题`

### Q: 代码块显示不正确?
A: 确保使用三个反引号包裹:
````markdown
```python
def hello():
    print("Hello")
```
````

### Q: 表格格式乱了?
A: 使用标准的 Markdown 表格语法:
```markdown
| 列1 | 列2 |
|-----|-----|
| 值1 | 值2 |
```

### Q: wkhtmltopdf 安装失败?
A:
```bash
# macOS
brew install wkhtmltopdf

# Linux
sudo apt-get install wkhtmltopdf

# 或下载二进制
# https://wkhtmltopdf.org/downloads.html
```

### Q: 图片显示不正确?
A: 使用完整工作流:
```bash
python scripts/workflow.py input.md
```
它会自动处理所有图片问题。

### Q: 如何从 v1.0 升级?
A: 查看 UPGRADE.md 文档了解详细升级步骤。

## 配置选项

如果需要自定义样式,可以修改 `scripts/convert.py` 中的 CSS 变量:

```python
# 主色调
PRIMARY_COLOR = '#06c'      # 苹果蓝
TEXT_COLOR = '#1d1d1f'      # 主文本黑色
GRAY_COLOR = '#86868b'      # 浅灰色

# 字体大小
COVER_TITLE_SIZE = '64pt'
H2_SIZE = '22pt'
H3_SIZE = '17pt'
BODY_SIZE = '11pt'
```

## 文件结构

```
.claude/skills/markdown-to-pdf/
├── SKILL.md                      # 本文件
├── README.md                     # 快速开始
├── EXAMPLES.md                   # 使用示例
├── UPGRADE.md                    # 升级指南
├── WORKFLOW.md                   # 工作流文档
└── scripts/
    ├── convert.py                # 核心转换工具
    ├── analyze_images.py         # 图片分析
    ├── batch_convert_images.py   # 批量转换
    ├── update_markdown_refs.py   # 引用更新
    └── workflow.py               # 完整工作流
```

## 技术实现

本 Skill 使用:
- **markdown**: 官方 Markdown 解析库
- **pdfkit**: HTML to PDF 转换 (基于 wkhtmltopdf)
- **Pillow**: 图片处理和格式转换
- **苹果设计系统**: SF 字体、专业配色、现代排版

## 更新日志

### v2.0 (2025-01-30)
- 使用 pdfkit 替代 WeasyPrint
- 移除 pango 依赖
- 添加图片处理工具链
- 添加完整工作流
- 改进图片路径处理
- 改进错误提示

### v1.0 (2025-12-24)
- 初始版本
- 支持完整 Markdown 语法
- 苹果设计风格
- 自动目录生成
- 书籍级排版质量
