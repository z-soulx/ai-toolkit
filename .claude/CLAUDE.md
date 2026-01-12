# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Repository Purpose

This is a **personal AI programming toolkit** for maintaining skills, plugins, MCP servers, and other AI-related tools.

## Key Architecture

### Repository Structure

```
ai-toolkit/
├── skills/           # Claude Code Skills
│   ├── notes/        # 笔记整理相关
│   └── productivity/ # 生产力工具
├── plugins/          # 编辑器插件和扩展
├── mcp-servers/      # Model Context Protocol 服务器
└── README.md         # 主文档
```

### Skills Structure

Each skill is a directory containing:
- `SKILL.md` (required) - Core instructions that Claude Code reads
- `README.md` (optional) - User documentation
- `examples.md` (optional) - Usage examples
- `reference.md` (optional) - Design references

## Common Operations

### Install Skills

```bash
# 复制 skill 到 Claude Code 配置目录
cp -r skills/notes/learning-notes-organizer ~/.claude/skills/

# 或使用软链接（推荐开发时使用）
ln -s $(pwd)/skills/notes/learning-notes-organizer ~/.claude/skills/
```

### Use Skills

在 Claude Code 中使用 `/` 命令调用已安装的 skills。

## Skill Categories

- **notes/** - 笔记整理、图片处理、大纲生成等
- **productivity/** - 任务规划和工作流工具

## Important Principles

1. **Data Safety**: Backup before modifications, provide dry-run preview
2. **Traceability**: Log all changes, use ledgers
3. **Single Responsibility**: Each skill focuses on one problem
4. **Clear Instructions**: Use numbered steps and explicit rules

## Development Notes

This is a personal repository for individual use. Focus on simplicity and practicality over comprehensive documentation.
