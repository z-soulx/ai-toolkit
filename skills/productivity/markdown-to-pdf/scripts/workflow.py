#!/usr/bin/env python3
"""
Markdown to PDF 完整工作流脚本

整合所有步骤:
1. 分析图片格式
2. 转换 WebP 图片
3. 更新 Markdown 引用
4. 生成 PDF

使用方法:
  python workflow.py input.md
  python workflow.py input.md -o output.pdf
  python workflow.py input.md --skip-images  # 跳过图片处理
"""

import argparse
import sys
import os
from pathlib import Path
import subprocess

# 导入其他脚本的功能
try:
    from analyze_images import analyze_images
    from batch_convert_images import batch_convert
    from update_markdown_refs import update_markdown_refs
    from convert import convert_markdown_to_pdf
except ImportError:
    print("❌ 无法导入必要的模块")
    print("请确保所有脚本都在同一目录下")
    sys.exit(1)

def print_section(title):
    """打印章节标题"""
    print("\n" + "="*60)
    print(title)
    print("="*60)

def run_workflow(input_file, output_file=None, skip_images=False, title=None, author=None, subtitle=None):
    """运行完整工作流"""

    print_section("Markdown to PDF 完整工作流 v2.0")
    print(f"输入文件: {input_file}")
    if output_file:
        print(f"输出文件: {output_file}")

    # 检查输入文件是否存在
    if not Path(input_file).exists():
        print(f"\n❌ 错误: 找不到文件 {input_file}")
        return False

    # 获取文件所在目录
    md_dir = Path(input_file).parent
    image_dir = md_dir / 'image'

    # 步骤 1: 图片处理 (可选)
    if not skip_images and image_dir.exists():
        print_section("步骤 1/4: 分析图片格式")
        try:
            # 切换到 Markdown 文件所在目录
            original_dir = os.getcwd()
            os.chdir(md_dir)

            analyze_images(str(image_dir))

            # 检查是否有需要转换的图片
            plan_file = md_dir / 'conversion_plan.json'
            if plan_file.exists():
                import json
                with open(plan_file, 'r', encoding='utf-8') as f:
                    plan = json.load(f)

                needs_conversion = (
                    len(plan['conversion_plan']['webp_no_ext']) > 0 or
                    len(plan['conversion_plan']['webp_wrong_ext']) > 0
                )

                if needs_conversion:
                    print_section("步骤 2/4: 转换 WebP 图片")
                    batch_convert(str(plan_file), str(image_dir))

                    print_section("步骤 3/4: 更新 Markdown 引用")
                    update_markdown_refs(input_file)
                else:
                    print("\n✓ 无需转换图片")

            os.chdir(original_dir)
        except Exception as e:
            print(f"\n⚠️  图片处理出错: {e}")
            print("继续生成 PDF...")
            os.chdir(original_dir)
    else:
        if skip_images:
            print("\n⏭️  跳过图片处理")
        else:
            print(f"\n⏭️  未找到 image 目录: {image_dir}")

    # 步骤 4: 生成 PDF
    print_section("步骤 4/4: 生成 PDF")
    try:
        result = convert_markdown_to_pdf(
            input_file,
            output_file,
            title,
            author,
            subtitle
        )

        if result:
            print_section("✅ 工作流完成")
            print(f"PDF 文件: {result}")

            # 显示生成的文件
            html_file = result.replace('.pdf', '.html')
            if Path(html_file).exists():
                print(f"HTML 文件: {html_file}")

            # 显示报告文件
            report_files = []
            if (md_dir / 'conversion_plan.json').exists():
                report_files.append('conversion_plan.json')
            if (md_dir / 'filename_mapping.json').exists():
                report_files.append('filename_mapping.json')
            if (md_dir / 'markdown_update_report.json').exists():
                report_files.append('markdown_update_report.json')

            if report_files:
                print(f"\n报告文件:")
                for f in report_files:
                    print(f"  - {f}")

            return True
        else:
            print("\n❌ PDF 生成失败")
            return False
    except Exception as e:
        print(f"\n❌ PDF 生成失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Markdown to PDF 完整工作流 (v2.0)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 基础用法
  python workflow.py document.md

  # 指定输出文件
  python workflow.py document.md -o output.pdf

  # 跳过图片处理
  python workflow.py document.md --skip-images

  # 自定义标题和作者
  python workflow.py document.md --title "技术白皮书" --author "团队"
        """
    )

    parser.add_argument('input', help='输入的 Markdown 文件')
    parser.add_argument('-o', '--output', help='输出的 PDF 文件 (默认: 与输入文件同名)')
    parser.add_argument('--skip-images', action='store_true', help='跳过图片处理步骤')
    parser.add_argument('--title', help='自定义文档标题')
    parser.add_argument('--subtitle', help='自定义副标题')
    parser.add_argument('--author', help='自定义作者')

    args = parser.parse_args()

    success = run_workflow(
        args.input,
        args.output,
        args.skip_images,
        args.title,
        args.author,
        args.subtitle
    )

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
