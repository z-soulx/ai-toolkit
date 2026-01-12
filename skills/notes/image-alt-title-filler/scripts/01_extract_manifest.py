#!/usr/bin/env python3
"""提取 Markdown 文件中的所有图片引用，记录位置和上下文"""
import re
import json
import argparse
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def extract_images(md_path):
    """提取图片并记录精确位置"""
    try:
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines(keepends=True)
    except FileNotFoundError:
        print(f"❌ 错误: 文件不存在: {md_path}")
        return []
    except UnicodeDecodeError:
        print(f"❌ 错误: 文件编码不是 UTF-8: {md_path}")
        return []

    images = []

    # Markdown 图片: ![alt](src "title")
    md_pattern = r'!\[([^\]]*)\]\(([^)]+?)(?:\s+"([^"]*)")?\)'
    # HTML 图片: <img src="..." alt="..." title="...">
    # 改进的 HTML 模式，支持单引号和无引号
    html_pattern = r'<img\s+([^>]*?)>'

    offset = 0
    for line_num, line in enumerate(lines, 1):
        # 查找 Markdown 图片
        for match in re.finditer(md_pattern, line):
            alt = match.group(1)
            src = match.group(2)
            title = match.group(3) or ""

            # 计算字符偏移
            char_offset = offset + match.start()

            # 提取上下文（前后各100字符）
            context_start = max(0, offset - 100)
            context_end = min(len(content), offset + len(line) + 100)
            context = content[context_start:context_end]

            images.append({
                'type': 'markdown',
                'src': src,
                'alt': alt,
                'title': title,
                'line': line_num,
                'char_offset': char_offset,
                'original_text': match.group(0),
                'context': context.strip()
            })

        # 查找 HTML 图片
        for match in re.finditer(html_pattern, line):
            attrs = match.group(1)
            # 改进的属性匹配，支持单引号、双引号和无引号
            src_match = re.search(r'src\s*=\s*["\']?([^"\'>\s]+)["\']?', attrs)
            alt_match = re.search(r'alt\s*=\s*["\']([^"\']*)["\']', attrs)
            title_match = re.search(r'title\s*=\s*["\']([^"\']*)["\']', attrs)

            if src_match:
                src = src_match.group(1)
                alt = alt_match.group(1) if alt_match else ""
                title = title_match.group(1) if title_match else ""

                char_offset = offset + match.start()
                context_start = max(0, offset - 100)
                context_end = min(len(content), offset + len(line) + 100)
                context = content[context_start:context_end]

                images.append({
                    'type': 'html',
                    'src': src,
                    'alt': alt,
                    'title': title,
                    'line': line_num,
                    'char_offset': char_offset,
                    'original_text': match.group(0),
                    'context': context.strip()
                })

        offset += len(line)

    return images

def main():
    parser = argparse.ArgumentParser(description='提取 Markdown 图片清单')
    parser.add_argument('--target_md', required=True, help='目标 Markdown 文件')
    parser.add_argument('--out_dir', default='.', help='输出目录')
    args = parser.parse_args()

    md_path = Path(args.target_md)

    if not md_path.exists():
        print(f"❌ 错误: 文件不存在: {md_path}")
        return 1

    if not md_path.is_file():
        print(f"❌ 错误: 不是文件: {md_path}")
        return 1

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    images = extract_images(md_path)

    if not images:
        print(f"⚠️ 警告: 未找到任何图片")
        return 0

    manifest = {
        'source_file': str(md_path),
        'total_images': len(images),
        'images': images
    }

    manifest_path = out_dir / 'manifest.json'
    try:
        with open(manifest_path, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"❌ 错误: 无法写入清单文件: {e}")
        return 1

    print(f"✓ 提取 {len(images)} 张图片")
    print(f"✓ 清单保存到: {manifest_path}")
    return 0

if __name__ == '__main__':
    main()
