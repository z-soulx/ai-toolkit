#!/usr/bin/env python3
"""
更新 Markdown 文件中的图片引用
根据 filename_mapping.json 批量替换无扩展名的图片引用
"""

import re
import json
from pathlib import Path


def update_markdown_refs(markdown_file, mapping_file='filename_mapping.json'):
    """更新 Markdown 文件中的图片引用"""

    # 读取文件名映射表
    if not Path(mapping_file).exists():
        print(f"错误：找不到映射文件 {mapping_file}")
        print("请先运行 batch_convert_images.py 生成映射表")
        return

    with open(mapping_file, 'r', encoding='utf-8') as f:
        filename_mapping = json.load(f)

    if not filename_mapping:
        print("映射表为空，无需更新")
        return

    # 读取 Markdown 文件
    md_path = Path(markdown_file)
    if not md_path.exists():
        print(f"错误：找不到 Markdown 文件 {markdown_file}")
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 统计数据
    stats = {
        'total_refs': 0,
        'updated_refs': 0,
        'skipped_refs': 0
    }

    # 更新详情
    updates = []

    print("="*60)
    print(f"更新 Markdown 文件：{markdown_file}")
    print("="*60)
    print(f"映射条目数：{len(filename_mapping)}")

    # 匹配图片引用的正则表达式
    # 匹配 <img src="../../image/filename" ...> 和 ![alt](../../image/filename)
    patterns = [
        (r'src="(../../image/([^"]+))"', 'img_tag'),
        (r'!\[[^\]]*\]\((../../image/([^)]+))\)', 'markdown')
    ]

    for pattern, ref_type in patterns:
        matches = list(re.finditer(pattern, content))
        stats['total_refs'] += len(matches)

        for match in matches:
            full_path = match.group(1)  # ../../image/filename
            filename = match.group(2)   # filename

            # 检查是否需要更新
            if filename in filename_mapping:
                new_filename = filename_mapping[filename]
                new_full_path = f"../../image/{new_filename}"

                # 替换
                old_ref = match.group(0)
                new_ref = old_ref.replace(full_path, new_full_path)

                content = content.replace(old_ref, new_ref, 1)

                stats['updated_refs'] += 1
                updates.append({
                    'type': ref_type,
                    'old': filename,
                    'new': new_filename
                })

                print(f"  ✓ {filename} → {new_filename}")
            else:
                stats['skipped_refs'] += 1

    # 生成报告
    print("\n" + "="*60)
    print("更新完成")
    print("="*60)
    print(f"总引用数：{stats['total_refs']}")
    print(f"已更新：{stats['updated_refs']}")
    print(f"跳过：{stats['skipped_refs']}")

    # 保存更新后的文件
    if content != original_content:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"\n✓ Markdown 文件已更新")

        # 保存更新报告
        report = {
            'markdown_file': markdown_file,
            'stats': stats,
            'updates': updates
        }

        report_file = 'markdown_update_report.json'
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        print(f"更新报告已保存到：{report_file}")
    else:
        print("\n无需更新（没有匹配的引用）")

    print("="*60)


if __name__ == '__main__':
    # 更新 netty.md
    update_markdown_refs('node/网络与通信/netty.md')
