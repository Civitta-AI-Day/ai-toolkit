# ai-toolkit

Civitta's shared Claude Code plugins. One plugin so far: **backend-toolkit**, a stack-agnostic
toolkit for backend work. See [plugins/backend-toolkit/README.md](plugins/backend-toolkit/README.md).

## Install

```
/plugin marketplace add Civitta-AI-Day/ai-toolkit
/plugin install backend-toolkit@ai-toolkit
```

Restart Claude Code, then check `/agents`, `/hooks` and `/mcp`.

| Task | Command |
| --- | --- |
| Get the latest version | `/plugin marketplace update ai-toolkit` |
| Turn it off for a while | `/plugin disable backend-toolkit@ai-toolkit` |
| Turn it back on | `/plugin enable backend-toolkit@ai-toolkit` |
| Remove it | `/plugin uninstall backend-toolkit@ai-toolkit` |

## Develop it

Clone this repo, then add your clone as a local marketplace. Claude Code reads a local marketplace
in place, so your edits apply after `/reload-plugins`:

```
/plugin marketplace add ~/Desktop/code/ai-toolkit
/plugin install backend-toolkit@ai-toolkit
```

Before pushing: `claude plugin validate .` and `claude plugin validate plugins/backend-toolkit`.

## AI Day branches

| Branch | Contains |
| --- | --- |
| `main` | The marketplace and an empty plugin to build on |
| `stage-1-onboard` | + `onboard-project` skill (writes CLAUDE.md) |
| `stage-2-skill` | + `implementing-tickets` skill |
| `stage-3-subagent` | + `security-reviewer` subagent |
| `stage-4-hooks` | + `protect` and `format` hooks |
| `stage-5-mcp` | + Linear MCP server (read tickets, post a summary comment) |
| `stage-6-plugin` | The finished plugin: version 1.0.0, docs, auto-install snippet |
