---
name: onboard-project
description: Use when a repository has no CLAUDE.md yet, when asked to onboard, set up or describe a project for Claude, or to create or improve a CLAUDE.md. Works for any language or framework.
---

# Onboard a project: write its CLAUDE.md

Goal: a short CLAUDE.md (under 40 lines) with only what is true in every session for this repo.
Facts come from the code, never from guesses.

1. **Detect the stack.** Run `python3 ${CLAUDE_SKILL_DIR}/scripts/detect_stack.py` from the project
   root. It reports languages, frameworks, the setup/test/lint/format/run commands, migration folders
   and the local database, each with the file it came from.
2. **Read, don't assume.** Open the README, the dependency file, the settings or config entry point,
   and two or three existing features end to end (route, handler, validation, data access, tests).
3. **Find the conventions.** Look for patterns the code repeats: how input is validated, how
   permissions are checked, how money, dates and errors are handled, how audit or logging is done,
   where tests live and which fixtures they use. A convention needs at least two examples in the code.
4. **Write CLAUDE.md** using `references/claude-md-template.md`. Name real files, classes and commands.
   Leave out anything Claude can see from one file, any step-by-step procedure (that belongs in a
   skill), and anything you are not sure of.
5. **Check it.** Every command in the file must run. Run the test command once.
6. **Show the result** and list any convention you were unsure about, so the person can confirm it.

If a CLAUDE.md already exists, improve it instead: remove procedures and stale facts, add missing
commands, keep it under 40 lines.
