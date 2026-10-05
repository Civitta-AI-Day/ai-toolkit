# backend-toolkit

A Claude Code plugin for backend work in **any** stack: Django, FastAPI, Laravel, Node, Go and others.
Nothing in it is tied to one project; it reads each project's own conventions and tools.

| Piece | Type | What it does |
| --- | --- | --- |
| `onboard-project` | Skill | Inspects a repo and writes a short, factual CLAUDE.md (commands, conventions, hard rules) |
| `implementing-tickets` | Skill | Implements a ticket the project's way: find the closest example, check the schema, validate, authorize, test, review |
| `security-reviewer` | Subagent | Read-only review for authorization gaps, missing validation, injection, data exposure, abuse, audit |
| `protect` | Hook (before tools) | Blocks reading or copying `.env` files and private keys, and editing applied migrations |
| `format` | Hook (after edits) | Formats each edited file with the project's own formatter (ruff, black, prettier, pint, gofmt) and reports lint errors back |
| `linear` | MCP server | Read-only access to Linear: Claude reads tickets, acceptance criteria and comments by ID |

## Install

From GitHub (the team's marketplace):

```
/plugin marketplace add Civitta-AI-Day/ai-toolkit
/plugin install backend-toolkit@ai-toolkit
```

From a local clone (to develop the plugin; edits apply after `/reload-plugins`):

```
/plugin marketplace add ~/Desktop/code/ai-toolkit
/plugin install backend-toolkit@ai-toolkit
```

Then restart Claude Code and check `/agents`, `/hooks` and `/mcp`.

## Use it in a project

1. Open Claude Code in the project.
2. No CLAUDE.md yet? Ask: "Onboard this project." Review and trim what it writes.
3. Give it the work: "Implement Linear ticket CIV-5."

## Requirements

- `python3` for the hooks (any version 3.8+).
- A Linear account with access to your team's workspace. The first time, run `/mcp` in Claude Code,
  pick `linear` and sign in; the browser opens Linear's login. The server is read-only
  (`https://mcp.linear.app/mcp/readonly`): Claude can read tickets but can't change them.

## Make it install automatically in a repo

Add to the project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "ai-toolkit": { "source": { "source": "github", "repo": "Civitta-AI-Day/ai-toolkit" } }
  },
  "enabledPlugins": { "backend-toolkit@ai-toolkit": true }
}
```
