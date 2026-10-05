#!/usr/bin/env python3
"""PreToolUse hook: keep Claude away from secrets and applied migrations. Works in any stack.

Claude Code sends the tool call as JSON on stdin. Exit code 2 blocks the call,
and the message on stderr is shown to Claude as the reason.

Blocks:
  1. Reading or writing secret files: .env and .env.* (except example/sample/template files),
     private keys (*.pem, *.key, id_rsa, id_ed25519) — through file tools and shell commands.
  2. Editing migrations that already exist (Django, Alembic, Laravel, Rails, Prisma, SQL).
     Creating a new migration file is allowed.
"""

import json
import os
import re
import sys

event = json.load(sys.stdin)
tool = event.get("tool_name", "")
tool_input = event.get("tool_input", {})

SAFE_ENV = (".env.example", ".env.sample", ".env.template", ".env.dist")
KEY_NAMES = ("id_rsa", "id_ed25519", "id_ecdsa")
KEY_EXTENSIONS = (".pem", ".key", ".p12", ".pfx")
MIGRATION_DIRS = re.compile(
    r"(^|/)(migrations|alembic/versions|database/migrations|db/migrate|prisma/migrations)/"
)
SHELL_SECRET = re.compile(
    r"(^|[\s/'\"=<>])\.env(?!\.(example|sample|template|dist)\b)(\.[\w-]+)?(?=$|[\s'\";|&)<>])"
    r"|\b(id_rsa|id_ed25519|id_ecdsa)\b|\S+\.(pem|p12|pfx)\b"
)


def block(reason):
    print(f"Blocked by the protect hook: {reason}", file=sys.stderr)
    sys.exit(2)


def is_secret(path):
    name = os.path.basename(path)
    if name in SAFE_ENV:
        return False
    if name == ".env" or name.startswith(".env."):
        return True
    return name.startswith(KEY_NAMES) or name.endswith(KEY_EXTENSIONS)


path = (
    tool_input.get("file_path") or tool_input.get("notebook_path") or tool_input.get("path") or ""
)

# 1a. Secret files through file tools (Read, Edit, Write, Grep...)
if path and is_secret(path):
    block(
        f"{os.path.basename(path)} may hold secrets and is off limits. Use the example file instead."
    )

# 1b. Secret files through the shell (cat .env, cp .env x, grep KEY .env.local ...)
if tool == "Bash" and SHELL_SECRET.search(tool_input.get("command", "")):
    block("shell commands may not read or copy secret files (.env, private keys).")

# 2. Applied migrations never change; add a new one instead
if tool in ("Edit", "MultiEdit", "Write") and path and os.path.exists(path):
    normalized = path.replace(os.sep, "/")
    if MIGRATION_DIRS.search(normalized) and not normalized.endswith("__init__.py"):
        block("this migration already exists and must not change. Create a new migration instead.")

sys.exit(0)
