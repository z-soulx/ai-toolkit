#!/usr/bin/env python3
"""应用 agent 生成的结果，回写到 Markdown 文件"""
import json
import argparse
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def load_results(results_dir):
    """加载所有批次结果"""
    results_dir = Path(results_dir)
    all_results = []

    for result_file in sorted(results_dir.glob('batch_*.results.json')):
        with open(result_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            all_results.extend(data['results'])

    return all_results

def apply_patches(md_path, manifest, results, update_policy, title_policy, max_len_alt, max_len_title):
    """应用补丁到 Markdown 文件"""
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    images = manifest['images']
    ledger = []

    # 按字符偏移倒序排序，从后往前替换，避免偏移变化
    sorted_items = sorted(zip(images, results), key=lambda x: x[0]['char_offset'], reverse=True)

    for img, result in sorted_items:
        old_text = img['original_text']
        old_alt = img['alt']
        old_title = img['title']

        # update_policy 处理 - 必须在赋值前判断
        should_update_alt = True
        should_update_title = True

        if update_policy == 'smart':
            # 如果原来有内容且不是文件名，保留原内容
            if old_alt and not _is_filename_like(old_alt):
                should_update_alt = False
            if old_title and not _is_filename_like(old_title):
                should_update_title = False
        elif update_policy == 'empty_only':
            if old_alt:
                should_update_alt = False
            if old_title:
                should_update_title = False

        # 根据策略决定是否更新
        new_alt = result['new_alt'][:max_len_alt] if (should_update_alt and result['new_alt']) else old_alt
        new_title = result['new_title'][:max_len_title] if (should_update_title and result['new_title']) else old_title

        # title_policy 处理
        if title_policy == 'same_as_alt':
            new_title = new_alt
        elif title_policy == 'keep':
            new_title = old_title

        # 生成新文本
        if img['type'] == 'markdown':
            if new_title:
                new_text = f"![{new_alt}]({img['src']} \"{new_title}\")"
            else:
                new_text = f"![{new_alt}]({img['src']})"
        else:  # html
            new_text = f'<img src="{img["src"]}" alt="{new_alt}" title="{new_title}">'

        # 替换
        offset = img['char_offset']
        content = content[:offset] + new_text + content[offset + len(old_text):]

        # 记录到账本
        ledger.append({
            'src': img['src'],
            'line': img['line'],
            'old_alt': old_alt,
            'old_title': old_title,
            'new_alt': new_alt,
            'new_title': new_title,
            'old_text': old_text,
            'new_text': new_text,
            'fallback': result.get('fallback', False),
            'note': result.get('note', '')
        })

    return content, ledger

def _is_filename_like(text):
    """判断是否像文件名或占位符"""
    if not text:
        return True  # 空文本视为需要更新
    text_lower = text.lower()
    # 包含文件扩展名、路径分隔符、或常见占位符
    if re.search(r'\.(png|jpg|jpeg|gif|svg|webp)|[/\\]', text_lower):
        return True
    # 常见占位符模式
    placeholders = ['image-', 'img', '图片', '在这里插入图片描述', '640']
    return any(placeholder in text_lower for placeholder in placeholders)

def _clean_table_cell(text):
    """清理表格单元格内容，避免破坏表格格式"""
    if not text:
        return "-"
    # 替换管道符
    text = text.replace('|', '\\|')
    # 替换换行符
    text = text.replace('\n', ' ').replace('\r', ' ')
    # 去除多余空格
    text = ' '.join(text.split())
    return text

def generate_ledger_table(ledger, source_file, update_policy):
    """生成表格式图片变更账本（类似老版本格式）"""
    # 统计信息
    total = len(ledger)
    updated = sum(1 for item in ledger
                  if item['old_alt'] != item['new_alt'] or item['old_title'] != item['new_title'])
    kept = total - updated
    fallback = sum(1 for item in ledger if item['fallback'])

    # 头部
    md = f"# 图片变更账本 - {Path(source_file).name}\n\n"
    md += f"**目标文件**: `{source_file}`  \n"
    md += f"**处理时间**: {datetime.now().strftime('%Y-%m-%d')}  \n"
    md += f"**处理策略**: {update_policy}\n\n"

    # 统计
    md += "## 变更统计\n\n"
    md += f"- **总计图片**: {total} 张\n"
    md += f"- **已更新 (UPDATED)**: {updated} 张\n"
    md += f"- **保留原值 (KEPT)**: {kept} 张\n"
    md += f"- **降级补全 (FALLBACK_CONTEXT)**: {fallback} 张\n"
    md += f"- **未解决 (UNRESOLVED)**: 0 张\n\n"

    # 表格
    md += "## 变更明细\n\n"
    md += "| # | 资源路径(src) | 语法 | 原 alt | 原 title | 新 alt | 新 title | 状态 |\n"
    md += "|---|-------------|------|--------|----------|--------|----------|------|\n"

    for idx, item in enumerate(ledger, 1):
        # 路径用反引号包裹
        src = f"`{item['src']}`"

        # 判断语法类型
        syntax = "MD" if "![" in item['old_text'] else "HTML"

        # 清理单元格内容
        old_alt = _clean_table_cell(item['old_alt'])
        old_title = _clean_table_cell(item['old_title'])
        new_alt = _clean_table_cell(item['new_alt'])
        new_title = _clean_table_cell(item['new_title'])

        # 状态判断
        if item['fallback']:
            status = "FALLBACK_CONTEXT"
        elif item['old_alt'] != item['new_alt'] or item['old_title'] != item['new_title']:
            status = "UPDATED"
        else:
            status = "KEPT"

        md += f"| {idx} | {src} | {syntax} | {old_alt} | {old_title} | {new_alt} | {new_title} | {status} |\n"

    return md

def generate_ledger_detailed(ledger):
    """生成详细逐条格式的图片变更账本"""
    md = "# 图片变更账本\n\n"

    for idx, item in enumerate(ledger, 1):
        md += f"## {idx}. {item['src']}\n\n"
        md += f"- **位置**: 第 {item['line']} 行\n"
        md += f"- **原 alt**: `{item['old_alt']}`\n"
        md += f"- **原 title**: `{item['old_title']}`\n"
        md += f"- **新 alt**: `{item['new_alt']}`\n"
        md += f"- **新 title**: `{item['new_title']}`\n"
        md += f"- **状态**: {'⚠️ FALLBACK_CONTEXT' if item['fallback'] else '✓ 基于图片内容'}\n"

        if item['note']:
            md += f"- **说明**: {item['note']}\n"

        md += f"\n**原片段**:\n```\n{item['old_text']}\n```\n\n"
        md += f"**新片段**:\n```\n{item['new_text']}\n```\n\n"
        md += "---\n\n"

    return md

def main():
    parser = argparse.ArgumentParser(description='应用补丁回写 Markdown')
    parser.add_argument('--target_md', required=True, help='目标 Markdown 文件')
    parser.add_argument('--manifest', required=True, help='manifest.json 路径')
    parser.add_argument('--results_dir', required=True, help='结果目录')
    parser.add_argument('--out_md', required=True, help='输出 Markdown 文件')
    parser.add_argument('--out_ledger', required=True, help='输出账本文件')
    parser.add_argument('--update_policy', default='smart', choices=['always', 'smart', 'empty_only'])
    parser.add_argument('--title_policy', default='same_as_alt', choices=['same_as_alt', 'keep', 'update'])
    parser.add_argument('--max_len_alt', type=int, default=40)
    parser.add_argument('--max_len_title', type=int, default=40)
    parser.add_argument('--ledger_format', default='table', choices=['table', 'detailed'],
                        help='账本格式：table=表格汇总(默认), detailed=详细逐条')
    parser.add_argument('--no-backup', action='store_true', help='不创建备份文件')
    parser.add_argument('--auto-cleanup-backup', action='store_true',
                        help='执行成功后自动删除备份文件')
    parser.add_argument('--dry-run', action='store_true', help='预览模式，不实际修改文件')
    args = parser.parse_args()

    # 加载数据
    with open(args.manifest, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    results = load_results(args.results_dir)

    # 验证数量匹配
    if len(manifest['images']) != len(results):
        print(f"❌ 错误: 图片数量 ({len(manifest['images'])}) 与结果数量 ({len(results)}) 不匹配")
        print(f"   这可能导致数据错位，请检查结果文件是否完整")
        return 1

    # 验证 src 匹配
    print("🔍 验证数据完整性...")
    mismatches = []
    for i, (img, result) in enumerate(zip(manifest['images'], results)):
        if img['src'] != result.get('src', ''):
            mismatches.append(f"  位置 {i+1}: manifest={img['src']}, result={result.get('src', 'MISSING')}")

    if mismatches:
        print(f"❌ 错误: 发现 {len(mismatches)} 处 src 不匹配:")
        for m in mismatches[:5]:  # 只显示前5个
            print(m)
        if len(mismatches) > 5:
            print(f"  ... 还有 {len(mismatches)-5} 处不匹配")
        print("   数据可能错位，拒绝执行以保护数据安全")
        return 1

    print(f"✓ 数据验证通过: {len(manifest['images'])} 张图片")

    # 创建备份
    backup_path = None
    if not args.no_backup and not args.dry_run:
        target_path = Path(args.target_md)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_path = target_path.parent / f"{target_path.stem}.backup_{timestamp}{target_path.suffix}"
        shutil.copy2(target_path, backup_path)
        print(f"✓ 备份已创建: {backup_path}")

    # 应用补丁
    new_content, ledger = apply_patches(
        args.target_md, manifest, results,
        args.update_policy, args.title_policy,
        args.max_len_alt, args.max_len_title
    )

    if args.dry_run:
        print("\n🔍 预览模式 - 不会修改文件")
        print(f"   将更新 {len(ledger)} 张图片")
        print(f"   输出文件: {args.out_md}")
        print(f"   变更账本: {args.out_ledger}")

        # 显示前3个变更示例
        print("\n变更示例:")
        for i, item in enumerate(ledger[:3], 1):
            print(f"\n  {i}. {item['src']}")
            print(f"     原 alt: {item['old_alt']}")
            print(f"     新 alt: {item['new_alt']}")
        return 0

    # 保存结果
    with open(args.out_md, 'w', encoding='utf-8') as f:
        f.write(new_content)

    # 根据格式选择生成函数
    if args.ledger_format == 'table':
        ledger_md = generate_ledger_table(ledger, args.target_md, args.update_policy)
    else:
        ledger_md = generate_ledger_detailed(ledger)

    with open(args.out_ledger, 'w', encoding='utf-8') as f:
        f.write(ledger_md)

    print(f"✓ 已处理 {len(ledger)} 张图片")
    print(f"✓ 输出文件: {args.out_md}")
    print(f"✓ 变更账本: {args.out_ledger}")

    # 自动清理备份
    if args.auto_cleanup_backup and backup_path and backup_path.exists():
        # 验证输出文件已成功创建
        if Path(args.out_md).exists() and Path(args.out_ledger).exists():
            backup_path.unlink()
            print(f"✓ 备份已清理: {backup_path}")
        else:
            print(f"⚠️ 输出文件未完全创建，保留备份: {backup_path}")

    return 0

if __name__ == '__main__':
    main()
