#!/usr/bin/env python3
"""
批量转换 WebP 图片为 PNG 格式
根据 conversion_plan.json 执行转换
"""

import os
import json
import shutil
from pathlib import Path
from PIL import Image


def convert_webp_to_png(input_path, output_path):
    """将 WebP 图片转换为 PNG 格式"""
    try:
        with Image.open(input_path) as img:
            # 处理 RGBA 模式
            if img.mode in ('RGBA', 'LA', 'P'):
                # 保持透明度
                img.save(output_path, 'PNG', optimize=True)
            else:
                # 转换为 RGB
                rgb_img = img.convert('RGB')
                rgb_img.save(output_path, 'PNG', optimize=True)
        return True, None
    except Exception as e:
        return False, str(e)


def batch_convert(plan_file='conversion_plan.json', image_dir='image'):
    """批量转换图片"""

    # 读取转换计划
    if not Path(plan_file).exists():
        print(f"错误：找不到转换计划文件 {plan_file}")
        print("请先运行 analyze_images.py 生成转换计划")
        return

    with open(plan_file, 'r', encoding='utf-8') as f:
        plan = json.load(f)

    image_path = Path(image_dir)
    if not image_path.exists():
        print(f"错误：目录 {image_dir} 不存在")
        return

    # 统计数据
    stats = {
        'total': 0,
        'success': 0,
        'skipped': 0,
        'failed': 0
    }

    # 文件名映射表（用于更新 Markdown）
    filename_mapping = {}

    # 错误日志
    errors = []

    print("="*60)
    print("开始批量转换图片")
    print("="*60)

    # 处理无扩展名的 WebP
    webp_no_ext = plan['conversion_plan']['webp_no_ext']
    if webp_no_ext:
        print(f"\n处理无扩展名的 WebP 文件（{len(webp_no_ext)} 个）...")

        for item in webp_no_ext:
            stats['total'] += 1
            old_name = item['file']
            new_name = item['new_name']

            old_path = image_path / old_name
            new_path = image_path / new_name

            # 检查目标文件是否已存在
            if new_path.exists():
                print(f"  跳过：{new_name} 已存在")
                stats['skipped'] += 1
                continue

            # 转换图片
            success, error = convert_webp_to_png(old_path, new_path)

            if success:
                print(f"  ✓ {old_name} → {new_name}")
                stats['success'] += 1

                # 删除原文件
                old_path.unlink()

                # 记录文件名映射
                filename_mapping[old_name] = new_name
            else:
                print(f"  ✗ {old_name} 转换失败：{error}")
                stats['failed'] += 1
                errors.append({
                    'file': old_name,
                    'error': error
                })

    # 处理有错误扩展名的 WebP
    webp_wrong_ext = plan['conversion_plan']['webp_wrong_ext']
    if webp_wrong_ext:
        print(f"\n处理有错误扩展名的 WebP 文件（{len(webp_wrong_ext)} 个）...")

        for item in webp_wrong_ext:
            stats['total'] += 1
            file_name = item['file']
            file_path = image_path / file_name

            # 创建临时文件
            temp_path = image_path / f"{file_name}.temp"

            # 转换图片
            success, error = convert_webp_to_png(file_path, temp_path)

            if success:
                # 替换原文件
                shutil.move(str(temp_path), str(file_path))
                print(f"  ✓ {file_name} (已转换为真正的 PNG)")
                stats['success'] += 1
            else:
                print(f"  ✗ {file_name} 转换失败：{error}")
                stats['failed'] += 1
                errors.append({
                    'file': file_name,
                    'error': error
                })

                # 清理临时文件
                if temp_path.exists():
                    temp_path.unlink()

    # 生成报告
    print("\n" + "="*60)
    print("转换完成")
    print("="*60)
    print(f"总计：{stats['total']} 个文件")
    print(f"成功：{stats['success']} 个")
    print(f"跳过：{stats['skipped']} 个")
    print(f"失败：{stats['failed']} 个")

    if errors:
        print(f"\n错误详情：")
        for err in errors[:10]:  # 只显示前10个
            print(f"  - {err['file']}: {err['error']}")
        if len(errors) > 10:
            print(f"  ... 还有 {len(errors) - 10} 个错误")

    # 保存文件名映射表
    if filename_mapping:
        mapping_file = 'filename_mapping.json'
        with open(mapping_file, 'w', encoding='utf-8') as f:
            json.dump(filename_mapping, f, ensure_ascii=False, indent=2)
        print(f"\n文件名映射表已保存到：{mapping_file}")
        print(f"映射条目数：{len(filename_mapping)}")

    # 保存错误日志
    if errors:
        error_file = 'conversion_errors.json'
        with open(error_file, 'w', encoding='utf-8') as f:
            json.dump(errors, f, ensure_ascii=False, indent=2)
        print(f"错误日志已保存到：{error_file}")

    print("="*60)


if __name__ == '__main__':
    batch_convert()
