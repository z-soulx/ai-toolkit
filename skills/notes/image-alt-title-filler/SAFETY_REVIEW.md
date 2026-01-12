# 脚本安全审查报告

**审查日期**: 2026-01-10
**审查范围**: image-alt-title-filler 脚本工具链

## 🚨 已修复的严重问题

### 1. **CRITICAL: update_policy 逻辑错误** ✅ 已修复

**位置**: `03_apply_patch.py` 原 lines 36-51

**问题描述**:
```python
# 错误的逻辑顺序
new_alt = result['new_alt'][:max_len_alt]  # 先赋值
if update_policy == 'smart':
    if old_alt and not _is_filename_like(old_alt):
        new_alt = old_alt  # 然后又覆盖回去！
```

**影响**:
- AI 生成的描述被丢弃
- 用户以为更新了，实际没有更新
- 数据不一致

**修复方案**:
- 先判断是否需要更新（`should_update_alt`）
- 再根据判断结果赋值
- 逻辑清晰，不会误覆盖

---

### 2. **数据验证缺失** ✅ 已修复

**问题**: 原脚本只检查数量，不检查 src 是否匹配

**风险**:
- 如果结果文件顺序错误，会导致图片描述错位
- 可能把 A 图片的描述写到 B 图片上

**修复方案**:
```python
# 验证 src 匹配
for i, (img, result) in enumerate(zip(manifest['images'], results)):
    if img['src'] != result.get('src', ''):
        # 报错并拒绝执行
```

---

### 3. **缺少备份机制** ✅ 已修复

**问题**: 直接覆盖原文件，无法恢复

**修复方案**:
- 自动创建带时间戳的备份文件
- 支持 `--no-backup` 参数跳过备份
- 备份文件命名: `原文件名.backup_20260110_143025.md`

---

### 4. **缺少预览模式** ✅ 已修复

**问题**: 无法预览变更就直接执行

**修复方案**:
- 新增 `--dry-run` 参数
- 预览模式显示将要修改的内容
- 不实际写入文件

---

### 5. **占位符识别不完整** ✅ 已修复

**问题**: `_is_filename_like()` 只识别文件扩展名和路径

**遗漏的占位符**:
- `image-20230101123456` (常见时间戳格式)
- `img` (常见占位符)
- `图片` (中文占位符)
- `在这里插入图片描述` (编辑器默认文本)
- `640` (微信图片默认名)

**修复方案**:
```python
placeholders = ['image-', 'img', '图片', '在这里插入图片描述', '640']
return any(placeholder in text_lower for placeholder in placeholders)
```

---

### 6. **HTML 属性解析不健壮** ✅ 已修复

**问题**: 只支持双引号，不支持单引号或无引号

**修复方案**:
```python
# 改进的正则，支持多种引号格式
src_match = re.search(r'src\s*=\s*["\']?([^"\'>\s]+)["\']?', attrs)
```

---

### 7. **错误处理缺失** ✅ 已修复

**问题**: 文件操作没有 try-catch

**修复方案**:
- 添加文件存在性检查
- 添加编码错误处理
- 添加写入失败处理
- 所有错误都返回非零退出码

---

## ✅ 新增的安全特性

### 1. **数据完整性验证**
- 验证图片数量匹配
- 验证 src 路径匹配
- 发现不匹配立即拒绝执行

### 2. **自动备份**
- 默认创建备份文件
- 带时间戳，不会覆盖
- 可选择跳过备份

### 3. **预览模式**
- `--dry-run` 参数
- 显示变更预览
- 不实际修改文件

### 4. **详细的错误提示**
- 明确的错误信息
- 显示错误位置
- 提供修复建议

---

## 📋 使用建议

### 推荐的安全工作流程

```bash
# 1. 提取清单
python scripts/01_extract_manifest.py \
  --target_md "你的文档.md" \
  --out_dir outputs

# 2. 生成批次
python scripts/02_make_batch_prompts.py \
  --manifest outputs/manifest.json \
  --out_dir outputs/batches \
  --batch_size 8

# 3. 处理批次（在 IDE 中）
# ... 生成 results 文件 ...

# 4. 预览变更（推荐！）
python scripts/03_apply_patch.py \
  --target_md "你的文档.md" \
  --manifest outputs/manifest.json \
  --results_dir outputs/results \
  --out_md outputs/patched.md \
  --out_ledger outputs/ledger.md \
  --dry-run

# 5. 确认无误后正式执行
python scripts/03_apply_patch.py \
  --target_md "你的文档.md" \
  --manifest outputs/manifest.json \
  --results_dir outputs/results \
  --out_md outputs/patched.md \
  --out_ledger outputs/ledger.md \
  --update_policy smart

# 6. 检查账本
cat outputs/ledger.md

# 7. 如果满意，替换原文件
cp outputs/patched.md "你的文档.md"
```

---

## ⚠️ 仍需注意的事项

### 1. **相对路径问题**
- 脚本不会解析相对路径为绝对路径
- 如果图片路径是 `../../image/xxx.png`，需要确保从正确的目录运行脚本

### 2. **字符编码**
- 脚本假设所有文件都是 UTF-8 编码
- 如果文件是 GBK 等其他编码，需要先转换

### 3. **大文件处理**
- 脚本一次性读取整个文件到内存
- 对于超大文件（>100MB）可能有性能问题

### 4. **并发安全**
- 脚本不支持并发执行
- 不要同时对同一个文件运行多个脚本实例

---

## 🔍 测试建议

### 在正式使用前，建议测试以下场景：

1. **小文件测试**
   - 用一个只有 2-3 张图片的测试文件
   - 验证整个流程是否正常

2. **边界情况测试**
   - 空 alt/title
   - 超长 alt/title
   - 特殊字符（引号、尖括号等）
   - 中英文混合

3. **错误恢复测试**
   - 故意制造 src 不匹配
   - 验证脚本是否正确拒绝执行
   - 验证备份是否正常创建

4. **预览模式测试**
   - 使用 `--dry-run` 预览
   - 确认预览内容正确
   - 确认没有实际修改文件

---

## 📊 修复前后对比

| 问题 | 修复前 | 修复后 |
|------|--------|--------|
| update_policy 逻辑 | ❌ 错误，会覆盖 AI 结果 | ✅ 正确，先判断再赋值 |
| 数据验证 | ⚠️ 只检查数量 | ✅ 检查数量和 src 匹配 |
| 备份机制 | ❌ 无备份 | ✅ 自动备份 + 时间戳 |
| 预览模式 | ❌ 无预览 | ✅ --dry-run 参数 |
| 占位符识别 | ⚠️ 不完整 | ✅ 识别常见占位符 |
| HTML 解析 | ⚠️ 只支持双引号 | ✅ 支持单引号/无引号 |
| 错误处理 | ❌ 无错误处理 | ✅ 完整的错误处理 |
| 退出码 | ⚠️ 总是 0 | ✅ 错误时返回非零 |

---

## ✅ 结论

**所有严重的数据安全问题已修复。**

现在的脚本具备：
- ✅ 正确的更新逻辑
- ✅ 完整的数据验证
- ✅ 自动备份机制
- ✅ 预览模式
- ✅ 健壮的错误处理
- ✅ 详细的日志输出

**建议**:
1. 先在测试文件上运行完整流程
2. 使用 `--dry-run` 预览变更
3. 检查生成的账本文件
4. 确认无误后再替换原文件
5. 保留备份文件至少一周

**数据安全等级**: 🟢 高（从 🔴 低提升）
