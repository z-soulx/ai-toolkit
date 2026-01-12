---
name: image-alt-title-filler-scripted
description: 脚本抽取图片清单与位置；IDE agent 分批看本地图片生成 alt/title；脚本按 offset 回写并输出图片变更账本。严格不改 src/路径、不丢图，支持 Markdown 图片与 HTML <img>。
metadata:
  version: v2
  dependencies:
    - planning-with-files
---

# Image Alt/Title Filler (scripted v2)

## Hard Rules（继承 v1）
- 不删除任何图片引用；不修改 src/路径；不重命名图片文件
- 每张图片必须出现在图片变更账本中：原片段/原 alt/title/新 alt/title/新片段/状态/说明
- 能读到图片时必须基于图片内容生成（不是文件名）
- 读不到图片必须降级为上下文补全，并标记 FALLBACK_CONTEXT，不得假装看过图
- alt/title 需简洁，默认不超过 max_len_alt/max_len_title

## 工作流（脚本 + agent）
### A) 脚本抽取（你只需要运行命令）
python scripts/01_extract_manifest.py --target_md <PATH_TO_MD> --out_dir outputs
=> outputs/manifest.json

### B) 生成批次 prompt
python scripts/02_make_batch_prompts.py --manifest outputs/manifest.json --out_dir outputs/batches --batch_size 8

### C) agent 分批“看本地图片”并写结果 JSON
- 打开 outputs/batches/batch_XXX.md
- 对每条图片：
  - 打开本地图片查看
  - 生成更有语义的中文 alt/title
  - 按 batch 文件中的 JSON schema 写到 outputs/results/batch_XXX.results.json

### D) 脚本回写（只用脚本改 md）
python scripts/03_apply_patch.py --target_md <PATH_TO_MD> --manifest outputs/manifest.json --results_dir outputs/results \
  --out_md outputs/patched.md --out_ledger outputs/image_ledger.md \
  --update_policy smart --title_policy same_as_alt --max_len_alt 40 --max_len_title 40