---
name: implementing-tickets
description: Use when implementing a ticket, feature or change in a backend codebase — new or changed API endpoints, exports or downloads, query parameters, validation, authorization, rate limits, audit logging, database queries and their tests. Works for any language or framework.
---

# Implementing a ticket

Follow these steps in order. The project's CLAUDE.md wins over anything here.

1. **Understand the ticket.** Given a ticket ID such as `CIV-5`, read it from the tracker with the
   `linear` MCP tools: the description, acceptance criteria and comments (comments often change the
   scope). If the tracker isn't connected or the ID isn't found, look for the ticket in the repo
   (for example `TICKET.md`) and say which source you used. List every requirement as a checklist
   and keep it to the end.
2. **Know the project.** Read CLAUDE.md. If there is none, run the `onboard-project` skill first.
   If you're unsure of the commands, run
   `python3 ${CLAUDE_SKILL_DIR}/../onboard-project/scripts/detect_stack.py`.
3. **Find the closest existing example** of the same kind of change (a similar endpoint, job or query)
   and follow its structure: same layers, same naming, same helpers. Don't invent a new pattern when
   the codebase already has one.
4. **Check the data shape before writing queries.** Read the models and migrations for the tables
   you touch: columns, types, existing indexes. If a large query filters or sorts on columns without
   an index, add one in a **new** migration.
5. **Plan,** then implement. For API work, go through `references/api-checklist.md`. For
   framework-specific idioms, read the matching file in `references/stacks/`.
6. **Test.** Add tests next to the existing ones, using the project's fixtures. Cover at least: the
   happy path, a user without access, invalid input, and an empty result.
7. **Verify.** Run the project's test and lint commands and fix everything they report.
8. **Review.** Ask the `security-reviewer` subagent to review the change, fix what it finds, and run
   the tests again.
9. **Report** against the checklist from step 1: done, not done, and anything you assumed.
10. **Comment on the ticket.** If the ticket came from Linear, post the report as **one** comment on
    it with the `linear` MCP tools. Start with "Implemented with Claude Code", then: what changed (main
    files), tests run and their result, the security review result, and anything not done or
    assumed. Keep it under 15 lines and show the text to the user before posting. Only add a
    comment: never change the ticket's status, assignee, title, description or labels.
