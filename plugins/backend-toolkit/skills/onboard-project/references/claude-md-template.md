# CLAUDE.md template

Fill in what is true for this repo. Delete any section that has nothing real to say.

```markdown
# <project name>

<Framework and version>, <database>, <language and version>. <One line on what it is: API only, monolith, worker...>

## Commands
- Setup: `<command>`
- Tests: `<command>` (single test: `<command>`)
- Lint and format: `<command>` / `<command>`
- Run: `<command>`
- <Anything non-obvious, e.g. "Python is .venv/bin/python, not the system python">

## Conventions
- <Rule> — <where it lives, e.g. "use `CanViewCustomer` in apps/customers/permissions.py">
- <Rule>
- (5 to 8 rules; each one should have at least two examples in the code)

## Do not
- <Hard rules, e.g. "edit existing migrations", "commit .env">
```

## What makes a good line

| Good | Too vague or in the wrong place |
| --- | --- |
| "Money is integer cents; format with `format_cents`" | "Handle money carefully" |
| "Authorize with `CanViewCustomer` (detail) or `visible_to()` (lists)" | "Check permissions" |
| "Tests: `make test`" | A 15-step guide to adding an endpoint (that is a skill) |

Remember: the "Do not" section is a request. Rules that must never be broken also need a hook.
