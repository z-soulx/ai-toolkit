# AI Programming Toolkit

> 个人 AI 编程工具集 - Skills、Plugins、MCP Servers 等

个人维护的 AI 编程相关工具集合，包含 Claude Code Skills、插件、MCP 服务器等，用于提升 AI 辅助编程效率。
## Quick Install
```bash
/plugin marketplace add z-soulx/ai-toolkit
/plugin install image-alt-title-filler@z-soulx
```
## 目录结构

```
ai-toolkit/
├── skills/           # Claude Code Skills
│   ├── notes/        # 笔记整理相关
│   └── productivity/ # 生产力工具
├── plugins/          # 编辑器插件和扩展
├── mcp-servers/      # Model Context Protocol 服务器
└── README.md         # 本文档
```

## Skills

Claude Code 自定义技能，用于特定工作流。

### 笔记整理 (notes/)

- **learning-notes-organizer** - 学习笔记系统化整理
- **image-alt-title-filler** - 图片 alt/title 批量补全
- **note-outline-checklist** - 笔记大纲生成
- **section-refactor-with-todo-routing** - 章节重构工具

### 生产力工具 (productivity/)

（暂无）

### 外部 Skills

- [**(可直接安装skill无需单独再加入市场)planning-with-files**](https://github.com/OthmanAdi/planning-with-files) - 任务规划和进度跟踪

## Plugins

编辑器插件和扩展（待添加）

## MCP Servers

Model Context Protocol 服务器（待添加）

## 使用说明

### 手动安装 Skills

```bash
# 复制 skill 到 Claude Code 配置目录
cp -r skills/notes/learning-notes-organizer ~/.claude/skills/

# 或使用软链接（推荐开发时使用）
ln -s $(pwd)/skills/notes/learning-notes-organizer ~/.claude/skills/
```

### 使用 Skills

在 Claude Code 中使用 `/` 命令调用已安装的 skills。

## License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**维护者**: [@soulx](https://github.com/soulx)
**最后更新**: 2026-01-12
