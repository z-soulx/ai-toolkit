# Markdown to PDF Skill 升级指南

从 v1.0 升级到 v2.0

---

## 升级概述

**版本**: v1.0 → v2.0
**发布日期**: 2025-01-30
**升级类型**: 重大更新（依赖变更）

### 为什么要升级？

#### v1.0 的问题

1. **pango 依赖安装困难**
   - macOS 需要 `brew install pango`
   - Linux 需要多个系统包
   - 安装经常失败，错误难以排查

2. **WebP 图片不兼容**
   - 某些 WebP 格式图片无法渲染
   - 图片显示异常或缺失

3. **特殊格式图片处理**
   - 无扩展名的图片无法识别
   - 错误扩展名的图片无法处理

#### v2.0 的改进

1. **安装简化**
   - 使用 wkhtmltopdf 替代 WeasyPrint
   - 无需 pango 依赖
   - 一条命令完成安装

2. **图片兼容性**
   - 支持 WebP 格式
   - 自动处理无扩展名图片
   - 提供完整图片处理工具链

3. **功能增强**
   - 一键式工作流
   - 详细的错误提示
   - 完整的报告生成

---

## 升级前准备

### 1. 检查当前版本

```bash
# 查看当前 skill 目录
ls -la .claude/skills/markdown-to-pdf/

# 查看 convert.py 导入
head -20 .claude/skills/markdown-to-pdf/scripts/convert.py
```

如果看到 `from weasyprint import`，说明是 v1.0。

### 2. 备份现有文件

```bash
# 自动备份（推荐）
cp -r .claude/skills/markdown-to-pdf \
     .claude/skills/markdown-to-pdf.v1.0.backup

# 验证备份
ls -la .claude/skills/markdown-to-pdf.v1.0.backup/
```

### 3. 检查依赖

```bash
# 检查 Python 版本
python3 --version  # 需要 3.8+

# 检查已安装的包
pip3 list | grep -E "markdown|weasyprint|pdfkit"
```

---

## 升级步骤

### 方式 1: 自动升级（推荐）

如果你已经有 v2.0 的文件：

```bash
# 1. 备份
cp -r .claude/skills/markdown-to-pdf \
     .claude/skills/markdown-to-pdf.v1.0.backup

# 2. 替换文件
# （已完成，跳过此步）

# 3. 卸载旧依赖（可选）
pip3 uninstall markdown2 weasyprint

# 4. 安装新依赖
pip3 install markdown pdfkit Pillow
brew install wkhtmltopdf  # macOS
# 或
sudo apt-get install wkhtmltopdf  # Linux

# 5. 验证安装
python3 -c "import markdown, pdfkit; from PIL import Image; print('✅ 依赖安装成功')"
which wkhtmltopdf
```

### 方式 2: 手动升级

如果需要手动升级：

```bash
# 1. 备份
cp -r .claude/skills/markdown-to-pdf \
     .claude/skills/markdown-to-pdf.v1.0.backup

# 2. 下载新版本文件
# （从升级包或仓库获取）

# 3. 替换核心文件
cp new-version/scripts/convert.py \
   .claude/skills/markdown-to-pdf/scripts/

# 4. 复制新工具
cp new-version/scripts/analyze_images.py \
   .claude/skills/markdown-to-pdf/scripts/
cp new-version/scripts/batch_convert_images.py \
   .claude/skills/markdown-to-pdf/scripts/
cp new-version/scripts/update_markdown_refs.py \
   .claude/skills/markdown-to-pdf/scripts/
cp new-version/scripts/workflow.py \
   .claude/skills/markdown-to-pdf/scripts/

# 5. 更新文档
cp new-version/SKILL.md .claude/skills/markdown-to-pdf/
cp new-version/README.md .claude/skills/markdown-to-pdf/

# 6. 安装依赖
pip3 install markdown pdfkit Pillow
brew install wkhtmltopdf
```

---

## 依赖迁移

### 卸载旧依赖（可选）

```bash
# 卸载 v1.0 依赖
pip3 uninstall markdown2 weasyprint

# 注意：pango 是系统包，可以保留
```

### 安装新依赖

```bash
# Python 依赖
pip3 install markdown pdfkit Pillow

# 系统依赖
# macOS
brew install wkhtmltopdf

# Linux (Ubuntu/Debian)
sudo apt-get install wkhtmltopdf

# Linux (CentOS/RHEL)
sudo yum install wkhtmltopdf

# 或下载二进制
# https://wkhtmltopdf.org/downloads.html
```

### 验证安装

```bash
# 验证 Python 包
python3 -c "
import markdown
import pdfkit
from PIL import Image
print('✅ Python 依赖安装成功')
"

# 验证 wkhtmltopdf
which wkhtmltopdf
wkhtmltopdf --version
```

---

## 使用方法变更

### 基础转换（无变化）

```bash
# v1.0 和 v2.0 命令相同
python scripts/convert.py input.md
python scripts/convert.py input.md -o output.pdf
python scripts/convert.py input.md --title "标题" --author "作者"
```

### 新增功能

#### 1. 完整工作流

```bash
# v2.0 新增
python scripts/workflow.py input.md
```

#### 2. 图片处理

```bash
# v2.0 新增
python scripts/analyze_images.py
python scripts/batch_convert_images.py
python scripts/update_markdown_refs.py
```

---

## 测试验证

### 1. 基础功能测试

```bash
# 创建测试文件
cat > test.md << 'EOF'
# 测试文档

## 1. 第一章
### 1.1 第一节
这是测试内容。

## 2. 第二章
### 2.1 第一节
这是测试内容。
EOF

# 测试转换
python scripts/convert.py test.md

# 检查输出
ls -lh test.pdf test.html
```

### 2. 图片处理测试

```bash
# 如果有 image 目录
python scripts/workflow.py test.md
```

### 3. 完整测试

```bash
# 使用实际文档测试
python scripts/workflow.py your-document.md
```

---

## 常见问题

### Q1: wkhtmltopdf 安装失败

**问题**: `brew install wkhtmltopdf` 失败

**解决方案**:
```bash
# 方案 1: 更新 Homebrew
brew update
brew install wkhtmltopdf

# 方案 2: 下载二进制
# 访问 https://wkhtmltopdf.org/downloads.html
# 下载对应系统的安装包

# 方案 3: 使用 Cask
brew install --cask wkhtmltopdf
```

### Q2: pdfkit 找不到 wkhtmltopdf

**问题**: `OSError: No wkhtmltopdf executable found`

**解决方案**:
```bash
# 检查 wkhtmltopdf 位置
which wkhtmltopdf

# 如果找不到，手动指定路径
# 在 convert.py 中添加：
config = pdfkit.configuration(wkhtmltopdf='/usr/local/bin/wkhtmltopdf')
pdfkit.from_string(html, output, options=options, configuration=config)
```

### Q3: 中文显示不正确

**问题**: PDF 中中文显示为方块

**解决方案**:
```bash
# macOS 通常自带中文字体，无需处理

# Linux 需要安装中文字体
sudo apt-get install fonts-wqy-zenhei fonts-wqy-microhei
```

### Q4: 图片不显示

**问题**: PDF 中图片缺失

**解决方案**:
```bash
# 使用完整工作流
python scripts/workflow.py input.md

# 或手动处理图片
python scripts/analyze_images.py
python scripts/batch_convert_images.py
python scripts/update_markdown_refs.py
python scripts/convert.py input.md
```

### Q5: 升级后旧 PDF 还能用吗？

**回答**: 可以。PDF 文件格式不变，只是生成方式改变。

### Q6: 必须卸载 WeasyPrint 吗？

**回答**: 不必须，但建议卸载以避免混淆和节省空间。

---

## 回滚方案

如果升级后遇到问题，可以快速回滚：

### 快速回滚

```bash
# 删除新版本
rm -rf .claude/skills/markdown-to-pdf

# 恢复旧版本
mv .claude/skills/markdown-to-pdf.v1.0.backup \
   .claude/skills/markdown-to-pdf

# 恢复旧依赖
pip3 install markdown2 weasyprint
```

### 依赖回滚

```bash
# 卸载新依赖
pip3 uninstall markdown pdfkit Pillow

# 恢复旧依赖
pip3 install markdown2 weasyprint
brew install pango  # 如果之前卸载了
```

---

## 功能对比

| 功能 | v1.0 | v2.0 |
|------|------|------|
| 基础转换 | ✅ | ✅ |
| 封面生成 | ✅ | ✅ |
| 目录生成 | ✅ | ✅ |
| 代码高亮 | ✅ | ✅ |
| 表格支持 | ✅ | ✅ |
| WebP 图片 | ❌ | ✅ |
| 无扩展名图片 | ❌ | ✅ |
| 图片分析工具 | ❌ | ✅ |
| 批量转换工具 | ❌ | ✅ |
| 引用更新工具 | ❌ | ✅ |
| 完整工作流 | ❌ | ✅ |
| 安装难度 | ⭐⭐⭐⭐ | ⭐⭐ |

---

## 性能对比

| 指标 | v1.0 | v2.0 |
|------|------|------|
| 安装时间 | ~5-10 分钟 | ~2-3 分钟 |
| 转换速度 | 快 | 快 |
| PDF 大小 | 正常 | 正常 |
| 内存占用 | 中等 | 中等 |

---

## 升级检查清单

升级完成后，请检查以下项目：

- [ ] 备份已完成
- [ ] 新依赖已安装
- [ ] wkhtmltopdf 可用
- [ ] 基础转换测试通过
- [ ] 图片处理测试通过（如适用）
- [ ] 完整工作流测试通过
- [ ] 旧文档可以正常转换
- [ ] 生成的 PDF 质量正常

---

## 获取帮助

如果遇到问题：

1. **查看文档**
   - `SKILL.md` - 完整文档
   - `README.md` - 快速开始
   - `EXAMPLES.md` - 使用示例
   - `WORKFLOW.md` - 工作流说明

2. **检查日志**
   - 查看转换过程的输出信息
   - 检查生成的 HTML 文件

3. **回滚测试**
   - 如果问题严重，先回滚到 v1.0
   - 确认问题后再重新升级

---

## 总结

### 升级收益

✅ **安装简化**: 移除 pango 依赖，安装更简单
✅ **兼容性提升**: 支持 WebP 等特殊格式图片
✅ **功能增强**: 添加完整的图片处理工具链
✅ **用户体验**: 提供一键式工作流
✅ **可维护性**: 代码结构更清晰

### 升级成本

⚠️ **学习成本**: 新增工具需要学习（但提供详细文档）
⚠️ **依赖变更**: 需要重新安装依赖（但更简单）
⚠️ **测试成本**: 需要全面测试（但风险可控）

### 建议

✅ **建议升级**: 收益远大于成本
✅ **保留备份**: 升级前备份 v1.0
✅ **逐步迁移**: 先测试，再全面使用

---

**文档版本**: v1.0
**更新日期**: 2025-01-30
**作者**: Claude Code
