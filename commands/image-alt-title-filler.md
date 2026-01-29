---
description: "脚本化图片 alt/title 补全工具。脚本负责提取和替换，模型只负责看图生成描述。支持 Markdown 和 HTML 图片，严格不改路径、不丢图。"
---

Invoke the notes-skills:image-alt-title-filler skill and follow it exactly as presented to you.

IMPORTANT: Always start with --dry-run to preview changes before applying them.

Execute the image alt/title filling workflow:
1. Extract all images from the target file
2. Generate descriptive alt/title text for each image
3. Preview changes (dry-run mode)
4. Apply changes after user confirmation
