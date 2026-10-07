# backend-toolkit

The backend team's Claude Code plugin, built during AI Day. It must work for **any** stack: nothing
in it may assume Django or this one project. It reads each project's own conventions and tools.

## What to build

| Folder | Building block | It must |
| --- | --- | --- |
| `skills/onboard-project/` | Skill (CLAUDE.md) | Inspect any repo and write a short, factual CLAUDE.md |
| `skills/implementing-tickets/` | Skill | Implement a ticket the project's way, with tests and a security review |
| `agents/security-reviewer.md` | Subagent | Review changes read-only for real security problems |
| `hooks/hooks.json` + scripts | Hooks | Block secret files and edits to applied migrations; format edited files |
| `.mcp.json` | MCP server | Connect Claude to Linear, so it reads tickets by ID and comments a summary when done |
| `.claude-plugin/plugin.json` | Plugin | Name, version, description (already here) |

Paths inside the plugin use `${CLAUDE_PLUGIN_ROOT}`; the project being worked on is `${CLAUDE_PROJECT_DIR}`.

## Try it while you build

```
/plugin marketplace add <path to your ai-toolkit clone>
/plugin install backend-toolkit@ai-toolkit
```

Claude Code reads your clone in place: after each change run `/reload-plugins`.
Check it with `claude plugin validate plugins/backend-toolkit`.
