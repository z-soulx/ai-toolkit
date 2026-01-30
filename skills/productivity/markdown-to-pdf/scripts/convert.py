#!/usr/bin/env python3
"""
Markdown to PDF 转换器 - 苹果设计风格 (v2.0)

改进点:
- 使用 pdfkit + wkhtmltopdf 替代 WeasyPrint (避免 pango 依赖问题)
- 支持 WebP 等特殊格式图片 (通过绝对路径)
- 自动处理无扩展名图片
- 保持专业的苹果设计风格

使用方法:
  python convert.py input.md
  python convert.py input.md -o output.pdf
  python convert.py input.md --title "标题" --author "作者"
"""

import argparse
import markdown
import pdfkit
import re
import os
from pathlib import Path

def extract_metadata(md_content):
    """提取文档元数据"""
    metadata = {
        'title': None,
        'subtitle': None,
        'author': None,
        'date': None,
        'created_for': None,
        'created_for_url': None,
        'based_on': None,
    }

    # 提取第一个 h1 作为标题
    h1_match = re.search(r'^# (.+)$', md_content, re.MULTILINE)
    if h1_match:
        metadata['title'] = h1_match.group(1).strip()

    # 提取 **字段**: 值 格式的元数据
    creator_match = re.search(r'\*\*创建者\*\*:\s*(.+?)$', md_content, re.MULTILINE)
    if creator_match:
        metadata['author'] = creator_match.group(1).strip()

    for_match = re.search(r'\*\*为谁创建\*\*:\s*(.+?)$', md_content, re.MULTILINE)
    if for_match:
        link_match = re.search(r'\[(.+?)\]\((.+?)\)', for_match.group(1))
        if link_match:
            metadata['created_for'] = link_match.group(1)
            metadata['created_for_url'] = link_match.group(2)
        else:
            metadata['created_for'] = for_match.group(1).strip()

    based_match = re.search(r'\*\*基于\*\*:\s*(.+?)$', md_content, re.MULTILINE)
    if based_match:
        metadata['based_on'] = based_match.group(1).strip()

    date_match = re.search(r'\*\*最后更新\*\*:\s*(.+?)$', md_content, re.MULTILINE)
    if date_match:
        metadata['date'] = date_match.group(1).strip()

    return metadata

def extract_toc_structure(md_content):
    """提取章节目录（支持有序号和无序号的标题）"""
    lines = md_content.split('\n')
    toc = []
    h2_counter = 0
    h3_counter = {}

    for line in lines:
        # 主章节: ## 标题 或 ## 1. 标题
        match_h2_numbered = re.match(r'^## (\d+)\.\s+(.+)$', line)
        match_h2_plain = re.match(r'^## (.+)$', line)

        if match_h2_numbered:
            # 有序号的标题
            num = match_h2_numbered.group(1)
            title = match_h2_numbered.group(2).strip()
            title = re.sub(r'[\U0001F300-\U0001F9FF]', '', title).strip()
            h2_counter = int(num)
            h3_counter[h2_counter] = 0
            toc.append({
                'level': 2,
                'number': num,
                'title': title,
                'id': f"{num}-{title}".replace(' ', '-').replace(':', '').lower()
            })
        elif match_h2_plain and not match_h2_numbered:
            # 无序号的标题
            h2_counter += 1
            h3_counter[h2_counter] = 0
            title = match_h2_plain.group(1).strip()
            title = re.sub(r'[\U0001F300-\U0001F9FF]', '', title).strip()
            toc.append({
                'level': 2,
                'number': None,  # 无序号
                'title': title,
                'id': title.replace(' ', '-').replace(':', '').lower()
            })

        # 子章节: ### 标题 或 ### 1.1 标题
        match_h3_numbered = re.match(r'^### (\d+\.\d+)\s+(.+)$', line)
        match_h3_plain = re.match(r'^### (.+)$', line)

        if match_h3_numbered:
            # 有序号的子标题
            num = match_h3_numbered.group(1)
            title = match_h3_numbered.group(2).strip()
            title = re.sub(r'[\U0001F300-\U0001F9FF]', '', title).strip()
            if len(title) > 50:
                title = title[:47] + '...'
            toc.append({
                'level': 3,
                'number': num,
                'title': title,
                'id': f"{num}-{title}".replace(' ', '-').replace(':', '').replace('.', '-').lower()
            })
        elif match_h3_plain and not match_h3_numbered and h2_counter > 0:
            # 无序号的子标题
            h3_counter[h2_counter] = h3_counter.get(h2_counter, 0) + 1
            title = match_h3_plain.group(1).strip()
            title = re.sub(r'[\U0001F300-\U0001F9FF]', '', title).strip()
            if len(title) > 50:
                title = title[:47] + '...'
            toc.append({
                'level': 3,
                'number': None,  # 无序号
                'title': title,
                'id': title.replace(' ', '-').replace(':', '').lower()
            })

    return toc

def generate_toc_html(toc_items):
    """生成目录 HTML"""
    if not toc_items:
        return ""

    toc_html = ""
    for item in toc_items:
        if item['level'] == 2:
            # 主章节
            number_html = f'<span class="toc-number">{item["number"]}</span>' if item.get('number') else ''
            toc_html += f'''
            <div class="toc-item toc-h2">
                <a href="#{item['id']}" class="toc-link">
                    {number_html}
                    <span class="toc-title">{item['title']}</span>
                </a>
            </div>
            '''
        else:
            # 子章节
            number_html = f'<span class="toc-number">{item["number"]}</span>' if item.get('number') else ''
            toc_html += f'''
            <div class="toc-item toc-h3">
                <a href="#{item['id']}" class="toc-link">
                    {number_html}
                    <span class="toc-title">{item['title']}</span>
                </a>
            </div>
            '''

    return toc_html

def create_cover_and_toc(metadata, toc_html):
    """创建封面（不自动生成目录页，MD 文件中有目录就会显示）"""
    title = metadata.get('title', '文档标题')
    subtitle = metadata.get('subtitle', '')
    author = metadata.get('author', '')
    date = metadata.get('date', '')
    created_for = metadata.get('created_for', '')
    created_for_url = metadata.get('created_for_url', '')
    based_on = metadata.get('based_on', '')

    # 不自动生成目录页，让 MD 文件中的内容自然显示
    # 如果 MD 文件中有目录，它会作为正文的一部分显示

    # 构建元信息区域
    meta_items = []
    if subtitle:
        meta_items.append(f'<p class="cover-subtitle">{subtitle}</p>')
    if based_on:
        meta_items.append(f'<p class="cover-based">{based_on}</p>')
    if created_for:
        if created_for_url:
            meta_items.append(f'<p class="cover-for">为 <a href="{created_for_url}">{created_for}</a> 用户创建</p>')
        else:
            meta_items.append(f'<p class="cover-for">为 {created_for} 用户创建</p>')
    if author:
        meta_items.append(f'<p class="cover-author">{author}</p>')
    if date:
        meta_items.append(f'<p class="cover-date">{date}</p>')

    meta_html = '\n'.join(meta_items)

    # 只有当有元信息时才显示封面
    if meta_html:
        return f"""
        <!-- 封面 -->
        <div class="apple-cover">
            <div class="cover-main">
                <h1 class="cover-title">{title}</h1>
                <div class="cover-meta">
                    {meta_html}
                </div>
            </div>
        </div>
        """
    else:
        # 没有元信息，不显示封面
        return ""

def fix_image_paths(md_content, md_file_path):
    """修复 Markdown 中的图片路径为绝对路径"""
    md_dir = Path(md_file_path).parent.absolute()

    def replace_image(match):
        img_tag = match.group(0)
        src_match = re.search(r'src="([^"]+)"', img_tag)
        if not src_match:
            return img_tag

        rel_path = src_match.group(1)

        # 跳过已经是绝对路径的图片
        if rel_path.startswith(('http://', 'https://', 'file://')):
            return img_tag

        abs_path = (md_dir / rel_path).resolve()

        # 如果原文件不存在,尝试添加 .png 扩展名
        if not abs_path.exists():
            png_path = Path(str(abs_path) + '.png')
            if png_path.exists():
                abs_path = png_path
                print(f"  ✓ 找到图片: {abs_path.name}")

        if abs_path.exists():
            # 使用 file:// 协议
            img_tag = img_tag.replace(f'src="{rel_path}"', f'src="file://{abs_path}"')
            print(f"  ✓ 转换路径: {abs_path.name}")
        else:
            print(f"  ⚠️  图片不存在: {rel_path}")

        return img_tag

    # 处理 HTML img 标签
    md_content = re.sub(r'<img[^>]+>', replace_image, md_content)

    # 处理 Markdown 图片语法
    def replace_md_image(match):
        alt = match.group(1)
        path = match.group(2)
        title = match.group(3) if match.lastindex >= 3 else ""

        # 跳过已经是绝对路径的图片
        if not path.startswith(('http://', 'https://', 'file://')):
            abs_path = (md_dir / path).resolve()

            # 如果原文件不存在,尝试添加 .png 扩展名
            if not abs_path.exists():
                png_path = Path(str(abs_path) + '.png')
                if png_path.exists():
                    abs_path = png_path
                    print(f"  ✓ 找到图片: {abs_path.name}")

            if abs_path.exists():
                path = f"file://{abs_path}"
                print(f"  ✓ 转换路径: {abs_path.name}")
            else:
                print(f"  ⚠️  图片不存在: {path}")

        if title:
            return f'![{alt}]({path} "{title}")'
        return f'![{alt}]({path})'

    md_content = re.sub(r'!\[([^\]]*)\]\(([^)]+?)(?:\s+"([^"]+)")?\)', replace_md_image, md_content)

    return md_content

def process_markdown(md_content):
    """处理 Markdown 内容"""

    # 不移除第一个 h1，让它作为文档标题显示
    # md_content = re.sub(r'^# .+?\n', '', md_content, count=1, flags=re.MULTILINE)

    # 移除开头的元数据行
    metadata_patterns = [
        r'^\*\*创建者\*\*:.+?$',
        r'^\*\*为谁创建\*\*:.+?$',
        r'^\*\*基于\*\*:.+?$',
        r'^\*\*最后更新\*\*:.+?$',
        r'^\*\*适用场景\*\*:.+?$',
    ]
    for pattern in metadata_patterns:
        md_content = re.sub(pattern, '', md_content, flags=re.MULTILINE)

    # 移除 emoji
    md_content = re.sub(r'[\U0001F300-\U0001F9FF]', '', md_content)

    # 处理 h2 主章节 - 添加 ID 和分页（支持有序号和无序号）
    # 使用计数器，第一个 h2 不添加分页符
    h2_counter = {'count': 0}

    def add_h2_id(match):
        h2_counter['count'] += 1
        full_match = match.group(0)

        # 第一个 h2 不添加分页符（避免 h1 后单独占页）
        page_break = '' if h2_counter['count'] == 1 else '\n<div class="chapter-break"></div>\n\n'

        # 检查是否有序号
        numbered_match = re.match(r'\n## (\d+)\.\s+(.+?)\n', full_match)
        if numbered_match:
            # 有序号: ## 1. 标题
            num = numbered_match.group(1)
            title = numbered_match.group(2).strip()
            id_str = f"{num}-{title}".replace(' ', '-').replace(':', '').lower()
            return f'{page_break}<h2 id="{id_str}" data-number="{num}">{title}</h2>\n'
        else:
            # 无序号: ## 标题
            plain_match = re.match(r'\n## (.+?)\n', full_match)
            if plain_match:
                title = plain_match.group(1).strip()
                id_str = title.replace(' ', '-').replace(':', '').lower()
                return f'{page_break}<h2 id="{id_str}">{title}</h2>\n'
        return full_match

    md_content = re.sub(r'\n## .+?\n', add_h2_id, md_content)

    # 处理 h3 子章节 - 添加 ID（支持有序号和无序号）
    def add_h3_id(match):
        full_match = match.group(0)
        # 检查是否有序号
        numbered_match = re.match(r'\n### (\d+\.\d+)\s+(.+?)\n', full_match)
        if numbered_match:
            # 有序号: ### 1.1 标题
            num = numbered_match.group(1)
            title = numbered_match.group(2).strip()
            id_str = f"{num}-{title}".replace(' ', '-').replace(':', '').replace('.', '-').lower()
            return f'\n<h3 id="{id_str}" data-number="{num}">{title}</h3>\n'
        else:
            # 无序号: ### 标题
            plain_match = re.match(r'\n### (.+?)\n', full_match)
            if plain_match:
                title = plain_match.group(1).strip()
                id_str = title.replace(' ', '-').replace(':', '').lower()
                return f'\n<h3 id="{id_str}">{title}</h3>\n'
        return full_match

    md_content = re.sub(r'\n### .+?\n', add_h3_id, md_content)

    # 转换 Markdown
    html = markdown.markdown(
        md_content,
        extensions=['extra', 'codehilite', 'toc', 'nl2br', 'tables', 'fenced_code']
    )

    return html

def get_apple_css():
    """获取苹果设计风格 CSS"""
    return """
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    body {
        font-family: -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
        font-size: 11pt;
        line-height: 1.7;
        color: #1d1d1f;
        background: white;
        -webkit-font-smoothing: antialiased;
    }

    /* 封面 */
    .apple-cover {
        height: 100vh;
        background: linear-gradient(135deg, #f5f5f7 0%, #ffffff 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        page-break-after: always;
    }

    .cover-main {
        text-align: center;
        padding: 60px;
    }

    .cover-title {
        font-size: 64pt;
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 24px;
        letter-spacing: -2px;
        font-family: -apple-system, 'SF Pro Display', sans-serif;
        string-set: doc-title content();
    }

    .cover-subtitle {
        font-size: 24pt;
        font-weight: 400;
        color: #1d1d1f;
        margin-bottom: 24px;
    }

    .cover-meta {
        font-size: 12pt;
        color: #86868b;
        line-height: 2;
        margin-top: 36px;
    }

    .cover-based {
        font-size: 11pt;
        color: #86868b;
        margin-bottom: 8px;
    }

    .cover-for {
        font-size: 13pt;
        color: #1d1d1f;
        font-weight: 500;
        margin-bottom: 8px;
    }

    .cover-for a {
        color: #06c;
        text-decoration: none;
    }

    .cover-author {
        font-size: 11pt;
        color: #86868b;
        margin-bottom: 8px;
    }

    .cover-date {
        font-size: 11pt;
        color: #86868b;
        font-weight: 500;
    }

    /* 目录 */
    .toc-page {
        padding: 60px 50px;
        page-break-after: always;
        min-height: 100vh;
    }

    .toc-header {
        font-size: 28pt;
        font-weight: 600;
        color: #1d1d1f;
        margin-bottom: 32px;
    }

    .toc-content {
        column-count: 2;
        column-gap: 40px;
    }

    .toc-item {
        break-inside: avoid;
        margin-bottom: 6px;
    }

    .toc-h2 {
        margin-top: 14px;
        margin-bottom: 4px;
    }

    .toc-h2 .toc-link {
        font-size: 11.5pt;
        font-weight: 600;
        color: #1d1d1f;
    }

    .toc-h2 .toc-number {
        color: #06c;
        font-weight: 700;
        margin-right: 8px;
    }

    .toc-h3 {
        margin-left: 16px;
    }

    .toc-h3 .toc-link {
        font-size: 10pt;
        font-weight: 400;
        color: #424245;
    }

    .toc-h3 .toc-number {
        color: #86868b;
        margin-right: 6px;
        font-size: 9.5pt;
    }

    .toc-link {
        display: block;
        text-decoration: none;
        padding: 4px 0;
    }

    .toc-number {
        font-feature-settings: "tnum";
    }

    /* 标题 */
    h1 {
        font-size: 32pt;
        font-weight: 600;
        color: #1d1d1f;
        margin-top: 40px;
        margin-bottom: 32px;
        padding-bottom: 16px;
        border-bottom: 3px solid #1d1d1f;
        page-break-after: avoid;
    }

    .chapter-break {
        page-break-before: always;
        height: 0;
    }

    h2 {
        font-size: 22pt;
        font-weight: 600;
        color: #1d1d1f;
        margin-top: 0;
        margin-bottom: 28px;
        padding-bottom: 12px;
        border-bottom: 2px solid #d2d2d7;
        page-break-after: avoid;
    }

    /* 通过 CSS 在标题前显示编号 */
    h2[data-number]::before {
        content: attr(data-number) ". ";
    }

    h3 {
        font-size: 17pt;
        font-weight: 600;
        color: #1d1d1f;
        margin-top: 36px;
        margin-bottom: 18px;
        page-break-after: avoid;
    }

    /* 通过 CSS 在标题前显示编号 */
    h3[data-number]::before {
        content: attr(data-number) " ";
    }

    h4 {
        font-size: 13pt;
        font-weight: 600;
        color: #424245;
        margin-top: 24px;
        margin-bottom: 12px;
        page-break-after: avoid;
    }

    /* 正文 */
    p {
        margin-bottom: 16px;
    }

    ul, ol {
        margin-left: 24px;
        margin-bottom: 20px;
    }

    li {
        margin-bottom: 10px;
    }

    /* 代码块 */
    pre {
        background: #f5f5f7;
        border: 1px solid #d2d2d7;
        border-radius: 8px;
        padding: 20px;
        margin: 24px 0;
        overflow-x: auto;
        font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
        font-size: 10pt;
        line-height: 1.6;
        page-break-inside: avoid;
    }

    pre code {
        background: none;
        padding: 0;
        color: #1d1d1f;
    }

    code {
        background: #f5f5f7;
        padding: 3px 6px;
        border-radius: 4px;
        font-family: 'SF Mono', 'Monaco', monospace;
        font-size: 10pt;
        color: #d70050;
        font-weight: 500;
    }

    /* 表格 */
    table {
        width: 100%;
        border-collapse: collapse;
        margin: 28px 0;
        font-size: 10.5pt;
    }

    table thead {
        background: #f5f5f7;
    }

    table th {
        padding: 14px 16px;
        text-align: left;
        font-weight: 600;
        border-bottom: 2px solid #d2d2d7;
    }

    table td {
        padding: 12px 16px;
        border-bottom: 1px solid #d2d2d7;
        color: #424245;
        page-break-inside: avoid;
    }

    /* 引用 */
    blockquote {
        border-left: 3px solid #06c;
        padding-left: 20px;
        margin: 24px 0;
        color: #424245;
        page-break-inside: avoid;
    }

    /* 强调 */
    strong {
        color: #1d1d1f;
        font-weight: 600;
    }

    a {
        color: #06c;
        text-decoration: none;
    }

    hr {
        border: none;
        border-top: 1px solid #d2d2d7;
        margin: 36px 0;
    }

    /* 图片 */
    img {
        max-width: 100%;
        height: auto;
        display: block;
        margin: 0.8em auto;
        page-break-inside: avoid;
    }

    /* 印刷质量 */
    p, li, blockquote {
        orphans: 3;
        widows: 3;
    }

    h2, h3, h4 {
        page-break-after: avoid;
    }

    pre, table, blockquote {
        page-break-inside: avoid;
    }
    """

def convert_markdown_to_pdf(input_file, output_file=None, title=None, author=None, subtitle=None):
    """主转换函数"""

    print(f"📖 读取文件: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        md_content = f.read()

    # 提取元数据
    print("📑 提取元数据...")
    metadata = extract_metadata(md_content)

    # 命令行参数覆盖
    if title:
        metadata['title'] = title
    if author:
        metadata['author'] = author
    if subtitle:
        metadata['subtitle'] = subtitle

    # 提取目录
    print("📂 提取目录结构...")
    toc_structure = extract_toc_structure(md_content)
    print(f"   ✓ 找到 {len([t for t in toc_structure if t['level'] == 2])} 个主章节")
    print(f"   ✓ 找到 {len([t for t in toc_structure if t['level'] == 3])} 个子章节")

    # 生成目录 HTML
    toc_html = generate_toc_html(toc_structure)

    # 处理图片路径
    print("🖼️  处理图片...")
    md_content = fix_image_paths(md_content, input_file)

    # 处理 Markdown
    print("🎨 处理 Markdown 内容...")
    html_content = process_markdown(md_content)

    # 生成完整 HTML
    print("📄 生成 HTML...")
    full_html = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>{metadata.get('title', '文档')}</title>
        <style>
            {get_apple_css()}
        </style>
    </head>
    <body>
        {create_cover_and_toc(metadata, toc_html)}
        <div class="content">
            {html_content}
        </div>
    </body>
    </html>
    """

    # 生成 PDF
    print("📝 生成 PDF...")
    if not output_file:
        output_file = str(Path(input_file).with_suffix('.pdf'))

    # 保存 HTML 用于调试
    html_file = output_file.replace('.pdf', '.html')
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"💾 已保存 HTML: {html_file}")

    # pdfkit 配置
    options = {
        'page-size': 'A4',
        'margin-top': '15mm',
        'margin-right': '15mm',
        'margin-bottom': '15mm',
        'margin-left': '15mm',
        'encoding': 'UTF-8',
        'enable-local-file-access': '',
        # 启用 PDF 书签导航（侧边栏目录）
        'outline': '',
        'outline-depth': 3,
    }

    try:
        pdfkit.from_string(full_html, output_file, options=options)
        print(f"\n✅ PDF 生成成功: {output_file}")
        size_mb = os.path.getsize(output_file) / (1024 * 1024)
        print(f"📊 文件大小: {size_mb:.1f} MB")
        return output_file
    except Exception as e:
        print(f"\n❌ 转换失败: {e}")
        print("\n提示: 请确保已安装 wkhtmltopdf")
        print("  macOS: brew install wkhtmltopdf")
        print("  Linux: sudo apt-get install wkhtmltopdf")
        return None

def main():
    parser = argparse.ArgumentParser(
        description='将 Markdown 转换为苹果设计风格的 PDF 白皮书 (v2.0)'
    )
    parser.add_argument('input', help='输入的 Markdown 文件')
    parser.add_argument('-o', '--output', help='输出的 PDF 文件 (默认: 与输入文件同名)')
    parser.add_argument('--title', help='自定义文档标题')
    parser.add_argument('--subtitle', help='自定义副标题')
    parser.add_argument('--author', help='自定义作者')

    args = parser.parse_args()

    try:
        convert_markdown_to_pdf(
            args.input,
            args.output,
            args.title,
            args.author,
            args.subtitle
        )
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    exit(main())
