#!/usr/bin/env python3
"""
分析 image/ 目录中的图片文件
检测实际格式，生成转换计划报告
"""

import os
import json
from pathlib import Path
from collections import defaultdict


def detect_format(file_path):
    """通过 Magic Bytes 检测文件的实际格式"""
    try:
        with open(file_path, 'rb') as f:
            header = f.read(12)

        if header.startswith(b'RIFF') and b'WEBP' in header:
            return 'webp'
        elif header.startswith(b'\x89PNG'):
            return 'png'
        elif header.startswith(b'\xff\xd8\xff'):
            return 'jpeg'
        elif header.startswith(b'GIF'):
            return 'gif'
        else:
            return 'unknown'
    except Exception as e:
        return f'error: {str(e)}'


def analyze_images(image_dir='image'):
    """分析图片目录，生成转换计划"""

    image_path = Path(image_dir)
    if not image_path.exists():
        print(f"错误：目录 {image_dir} 不存在")
        return None

    # 统计数据
    stats = {
        'total_files': 0,
        'webp_no_ext': [],           # 无扩展名的 WebP
        'webp_wrong_ext': [],         # 有错误扩展名的 WebP
        'correct_format': [],         # 格式正确的文件
        'unknown_format': [],         # 未知格式
        'errors': []                  # 错误文件
    }

    # 文件名冲突检测
    potential_conflicts = []

    print(f"正在扫描 {image_dir} 目录...")

    # 扫描所有文件
    for file_path in image_path.iterdir():
        if file_path.is_file() and not file_path.name.startswith('.'):
            stats['total_files'] += 1

            actual_format = detect_format(file_path)
            file_name = file_path.name
            file_ext = file_path.suffix.lower()

            # 分类处理
            if actual_format.startswith('error'):
                stats['errors'].append({
                    'file': file_name,
                    'error': actual_format
                })
            elif actual_format == 'unknown':
                stats['unknown_format'].append({
                    'file': file_name,
                    'extension': file_ext
                })
            elif actual_format == 'webp':
                if not file_ext:
                    # 无扩展名的 WebP
                    stats['webp_no_ext'].append({
                        'file': file_name,
                        'new_name': f"{file_name}.png"
                    })

                    # 检查是否会产生冲突
                    new_path = image_path / f"{file_name}.png"
                    if new_path.exists():
                        potential_conflicts.append({
                            'original': file_name,
                            'new_name': f"{file_name}.png",
                            'conflict_with': f"{file_name}.png"
                        })
                elif file_ext != '.webp':
                    # 有错误扩展名的 WebP（如 .png 但实际是 WebP）
                    stats['webp_wrong_ext'].append({
                        'file': file_name,
                        'extension': file_ext,
                        'actual_format': 'webp'
                    })
            else:
                # 格式正确的文件
                stats['correct_format'].append({
                    'file': file_name,
                    'format': actual_format
                })

    # 生成报告
    print("\n" + "="*60)
    print("图片格式分析报告")
    print("="*60)
    print(f"\n总文件数：{stats['total_files']}")
    print(f"\n需要转换的文件：")
    print(f"  - 无扩展名的 WebP：{len(stats['webp_no_ext'])} 个")
    print(f"  - 有错误扩展名的 WebP：{len(stats['webp_wrong_ext'])} 个")
    print(f"\n格式正确的文件：{len(stats['correct_format'])} 个")
    print(f"未知格式文件：{len(stats['unknown_format'])} 个")
    print(f"错误文件：{len(stats['errors'])} 个")

    if potential_conflicts:
        print(f"\n⚠️  检测到 {len(potential_conflicts)} 个潜在的文件名冲突：")
        for conflict in potential_conflicts[:5]:  # 只显示前5个
            print(f"  - {conflict['original']} → {conflict['new_name']} (已存在)")
        if len(potential_conflicts) > 5:
            print(f"  ... 还有 {len(potential_conflicts) - 5} 个冲突")

    # 显示示例
    if stats['webp_no_ext']:
        print(f"\n无扩展名 WebP 示例（前5个）：")
        for item in stats['webp_no_ext'][:5]:
            print(f"  {item['file']} → {item['new_name']}")

    if stats['webp_wrong_ext']:
        print(f"\n错误扩展名 WebP 示例（前5个）：")
        for item in stats['webp_wrong_ext'][:5]:
            print(f"  {item['file']} (扩展名: {item['extension']}, 实际: webp)")

    # 保存详细报告
    report = {
        'stats': {
            'total_files': stats['total_files'],
            'webp_no_ext_count': len(stats['webp_no_ext']),
            'webp_wrong_ext_count': len(stats['webp_wrong_ext']),
            'correct_format_count': len(stats['correct_format']),
            'unknown_format_count': len(stats['unknown_format']),
            'errors_count': len(stats['errors'])
        },
        'conversion_plan': {
            'webp_no_ext': stats['webp_no_ext'],
            'webp_wrong_ext': stats['webp_wrong_ext']
        },
        'potential_conflicts': potential_conflicts,
        'unknown_format': stats['unknown_format'],
        'errors': stats['errors']
    }

    report_file = 'conversion_plan.json'
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n详细报告已保存到：{report_file}")
    print("="*60)

    return report


if __name__ == '__main__':
    analyze_images()
