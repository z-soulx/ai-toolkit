# CLAUDE.md

This file provides guidance to Claude Code when working in this repository.

## Repository Purpose

This is a **Claude Code Marketplace** - a comprehensive AI programming toolkit that packages and distributes:
- **Skills** - Reusable workflows and domain knowledge
- **Plugins** - Editor extensions and integrations
- **MCP Servers** - Model Context Protocol servers for external data/tools
- **Agents** - Specialized subagents for specific tasks

This is NOT just a skills repository - it's a **distributable marketplace** that users can install via:
```bash
/plugin marketplace add z-soulx/ai-toolkit
/plugin install notes-skills@z-soulx
```

## Key Architecture

### Marketplace Structure

```
ai-toolkit/
├── .claude-plugin/
│   └── marketplace.json      # Marketplace definition (defines plugins)
├── commands/                 # Slash commands (appear in command list)
│   ├── learning-notes-organizer.md
│   ├── image-alt-title-filler.md
│   ├── note-outline-checklist.md
│   ├── section-refactor-with-todo-routing.md
│   └── markdown-to-pdf.md
├── skills/                   # Local skills (detailed workflows)
│   ├── notes/               # Note organization skills
│   │   ├── learning-notes-organizer/
│   │   ├── image-alt-title-filler/
│   │   ├── note-outline-checklist/
│   │   └── section-refactor-with-todo-routing/
│   └── productivity/        # Productivity tools
│       └── markdown-to-pdf/
├── plugins/                 # Editor plugins (future)
├── mcp-servers/            # MCP servers (future)
└── agents/                 # Custom agents (future)
```

### Marketplace vs Plugin vs Skill vs Command

- **Marketplace** (`.claude-plugin/marketplace.json`): A collection of plugins that can be distributed together
- **Plugin**: A named group of skills/hooks/agents (e.g., "notes-skills")
- **Skill**: Individual executable workflow with detailed instructions (e.g., "learning-notes-organizer")
- **Command**: Slash command shortcut that invokes a skill (e.g., `/learning-notes-organizer`)

**IMPORTANT**: Commands are what make skills appear in the command list! The `commands/` directory is the key to visibility.

### Current Plugins in This Marketplace

1. **notes-skills** (local) - Note organization and processing
   - learning-notes-organizer
   - image-alt-title-filler
   - note-outline-checklist
   - section-refactor-with-todo-routing

2. **productivity-skills** (local) - Productivity and document processing tools
   - markdown-to-pdf

3. **planning-with-files** (external) - Task planning and progress tracking
   - From: github.com/OthmanAdi/planning-with-files

4. **superpowers** (external) - Core skills library
   - From: github.com/obra/superpowers

### Skill Structure

Each skill directory must contain:
- `SKILL.md` (required) - Core instructions with frontmatter
  ```yaml
  ---
  name: skill-name
  description: Full description
  user-invocable: true  # Optional: alternative to commands/
  metadata:
    short-description: Brief description for command list
    version: v1.0
  ---
  ```
- `README.md` (optional) - User documentation
- `examples.md` (optional) - Usage examples
- `reference.md` (optional) - Design references

### Command Structure

Each command file in `commands/` directory:
- Filename becomes the command name (e.g., `plan.md` → `/plan`)
- Contains frontmatter with description
- Invokes the corresponding skill
- **This is the primary way to make commands visible in the command list**

Example `commands/my-command.md`:
```markdown
---
description: "Brief description shown in command list"
---

Invoke the plugin-name:skill-name skill and follow it exactly as presented to you.

Additional instructions or context for the command.
```

## Common Operations

### For Users (Installing This Marketplace)

```bash
# Add marketplace
/plugin marketplace add z-soulx/ai-toolkit

# Install specific plugin
/plugin install notes-skills@z-soulx

# Use skills
/learning-notes-organizer
/notes-skills:learning-notes-organizer  # With namespace
```

### For Developers (Working on This Repo)

#### Adding a New Skill

1. Create skill directory: `skills/category/skill-name/`
2. Create `SKILL.md` with proper frontmatter (include `user-invocable: true`)
3. Add skill path to `.claude-plugin/marketplace.json`
4. Test locally by symlinking or copying to `~/.claude/skills/`
5. Commit and push

#### Testing Skills Locally

```bash
# Option 1: Symlink (recommended for development)
ln -s $(pwd)/skills/notes/learning-notes-organizer ~/.claude/skills/

# Option 2: Copy
cp -r skills/notes/learning-notes-organizer ~/.claude/skills/

# Reload Claude Code to see changes
```

#### Making Skills Appear in Command List

Skills must have `user-invocable: true` in their SKILL.md frontmatter:

```yaml
---
name: my-skill
description: Full description
user-invocable: true  # This makes it show in /command list
metadata:
  short-description: Brief description shown in list
---
```

## Skill Categories

### notes/
- **learning-notes-organizer** - 零散笔记 → 可维护知识库
- **image-alt-title-filler** - 图片 alt/title 批量补全
- **note-outline-checklist** - 笔记大纲重构清单
- **section-refactor-with-todo-routing** - 指定章节精修

### productivity/
- **markdown-to-pdf** - Markdown 转专业 PDF 白皮书（苹果设计风格）

## Important Principles

### For Marketplace Configuration

**Current Configuration**: We are testing if both `skills` and `commands` arrays can be specified together.

#### Current Setup (Testing)
```json
{
  "name": "notes-skills",
  "source": "./",
  "skills": [
    "./skills/notes/section-refactor-with-todo-routing",
    "./skills/notes/note-outline-checklist",
    "./skills/notes/learning-notes-organizer",
    "./skills/notes/image-alt-title-filler"
  ],
  "commands": [
    "./commands/section-refactor-with-todo-routing.md",
    "./commands/note-outline-checklist.md",
    "./commands/learning-notes-organizer.md",
    "./commands/image-alt-title-filler.md"
  ]
}
```

**Benefits of this approach**:
- ✅ Explicit management of skills (categorization, selective loading)
- ✅ Explicit declaration of commands
- ✅ Clear configuration, easy to maintain

**If this doesn't work**, fallback to:
```json
{
  "name": "notes-skills",
  "source": "./"
}
```
And use directory structure + README.md for categorization.

### Skills Categorization

Current categories in `skills/notes/`:
- **learning-notes-organizer** - 零散笔记 → 可维护知识库
- **image-alt-title-filler** - 图片 alt/title 批量补全
- **note-outline-checklist** - 笔记大纲重构清单
- **section-refactor-with-todo-routing** - 指定章节精修

Future categories:
- `skills/productivity/` - 生产力工具
- `skills/code-review/` - 代码审查工具
- etc.

### For Skill Development

1. **Data Safety**: Always backup before modifications, provide dry-run preview
2. **Traceability**: Log all changes, use ledgers for tracking
3. **Single Responsibility**: Each skill focuses on one problem
4. **Clear Instructions**: Use numbered steps and explicit rules
5. **User-Invocable**: Add `user-invocable: true` to make skills discoverable

### For Marketplace Maintenance

1. **Version Control**: Update version in marketplace.json when adding/changing plugins
2. **Documentation**: Keep README.md in sync with marketplace.json
3. **Testing**: Test all skills locally before pushing
4. **Dependencies**: Document skill dependencies in SKILL.md metadata

## Concepts Reference

From README.md:

- **Agent**: 执行体（runtime），负责理解目标 → 拆解计划 → 调用工具 → 迭代
- **Tool**: 确定性的能力接口（读写文件、跑命令、查 API）
- **Command**: Slash command（/xxx），手动触发的快捷指令
- **MCP**: 让 agent/LLM 以标准方式连接外部工具与数据源的协议
- **Skill**: 封装"做事流程与专业知识"的可复用模块
- **Hook**: 在生命周期关键节点插入的强约束/审计/自动化规则
- **Plugin**: 打包 skills/hooks/agents/commands/MCP servers 的扩展包

## Development Notes

This is a personal marketplace for individual use, but designed to be shareable. Focus on:
- Simplicity and practicality over comprehensive documentation
- Clear skill boundaries and responsibilities
- Safe operations with dry-run previews
- Traceable changes with ledgers
