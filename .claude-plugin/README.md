plugins 中的字段对比

  基础字段（必需）：
  - name - 插件名称
  - description - 插件描述
  - source - 插件源码路径（本地路径）
  - strict - 是否严格模式

  资源类型字段（至少一个）：
  - skills - Skill 文件路径数组（如 ./skills/xxx/SKILL.md）
  - commands - Command 文件路径数组（斜杠命令，如 /commit）
  - agents - Agent 文件路径数组（专门的 agent 定义）

  可选元数据字段（cexll 版本有）：
  - version - 插件版本
  - author - 作者信息（name, url）
  - homepage - 主页 URL
  - repository - 仓库 URL
  - license - 许可证（如 "MIT"）
  - keywords - 关键词数组（用于搜索）
  - category - 分类（如 "workflows", "essentials"）