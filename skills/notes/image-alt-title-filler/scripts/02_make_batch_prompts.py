#!/usr/bin/env python3
"""将图片清单分批，生成供 agent 处理的 prompt 文件"""
import json
import argparse
import sys
from pathlib import Path

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def make_batches(manifest, batch_size):
    """将图片分批"""
    images = manifest['images']
    batches = []
    for i in range(0, len(images), batch_size):
        batches.append(images[i:i + batch_size])
    return batches

def generate_batch_prompt(batch_num, images, source_file):
    """生成批次处理的 prompt"""
    prompt = f"""# 批次 {batch_num} - 图片 alt/title 生成任务

源文件: {source_file}
本批次图片数: {len(images)}

## 任务说明
1. 逐个打开下面列出的本地图片文件
2. 基于图片内容（不是文件名）生成简洁的中文 alt 和 title
3. 如果图片无法打开，使用上下文推断，并标记 fallback: true
4. 将结果写入 JSON 文件

## 图片列表

"""

    for idx, img in enumerate(images):
        prompt += f"""### 图片 {idx + 1}
- 图片路径: `{img['src']}`
- 当前 alt: `{img['alt']}`
- 当前 title: `{img['title']}`
- 位置: 第 {img['line']} 行
- 上下文:
```
{img['context']}
```

"""

    prompt += f"""## 输出格式

请将结果保存为 JSON 文件: `outputs/results/batch_{batch_num:03d}.results.json`

JSON 格式:
```json
{{
  "batch": {batch_num},
  "results": [
    {{
      "index": 0,
      "src": "图片路径",
      "new_alt": "新的 alt 文本",
      "new_title": "新的 title 文本",
      "fallback": false,
      "note": "说明（可选）"
    }}
  ]
}}
```

## 注意事项
- alt/title 应简洁（建议不超过 40 字）
- 必须基于图片内容，不是文件名
- 如果图片打不开，设置 fallback: true 并基于上下文推断
"""

    return prompt

def main():
    parser = argparse.ArgumentParser(description='生成批次处理 prompt')
    parser.add_argument('--manifest', required=True, help='manifest.json 路径')
    parser.add_argument('--out_dir', default='batches', help='批次输出目录')
    parser.add_argument('--batch_size', type=int, default=8, help='每批图片数量')
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(manifest_path, 'r', encoding='utf-8') as f:
        manifest = json.load(f)

    batches = make_batches(manifest, args.batch_size)

    for batch_num, batch in enumerate(batches, 1):
        prompt = generate_batch_prompt(batch_num, batch, manifest['source_file'])
        prompt_path = out_dir / f'batch_{batch_num:03d}.md'
        with open(prompt_path, 'w', encoding='utf-8') as f:
            f.write(prompt)
        print(f"✓ 批次 {batch_num}: {len(batch)} 张图片 -> {prompt_path}")

    print(f"\n总计: {len(batches)} 个批次, {manifest['total_images']} 张图片")

if __name__ == '__main__':
    main()
