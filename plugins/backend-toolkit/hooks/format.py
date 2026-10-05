#!/usr/bin/env python3
"""PostToolUse hook: format every file Claude edits with the project's own formatter. Any stack.

Uses only tools the project already has (its virtualenv, node_modules, vendor) or that are on PATH:
  .py              ruff (safe fixes, then format), else black
  .js .ts .jsx ... prettier
  .php             pint
  .go              gofmt
If no formatter is found, the hook does nothing. If ruff still reports lint errors after fixing,
the hook exits with code 2 so Claude sees them and fixes them.
"""

import json
import os
import shutil
import subprocess
import sys

event = json.load(sys.stdin)
path = event.get("tool_input", {}).get("file_path", "")
if not path or not os.path.isfile(path):
    sys.exit(0)

project = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
ext = os.path.splitext(path)[1].lower()


def find(*candidates):
    """Return the first formatter that exists: project-local paths first, then PATH."""
    for candidate in candidates:
        local = os.path.join(project, candidate)
        if os.sep in candidate and os.path.isfile(local):
            return local
        if os.sep not in candidate and shutil.which(candidate):
            return shutil.which(candidate)
    return None


def run(*cmd):
    return subprocess.run(list(cmd), cwd=project, capture_output=True, text=True)


if ext == ".py":
    ruff = find(os.path.join(".venv", "bin", "ruff"), os.path.join("venv", "bin", "ruff"), "ruff")
    if ruff:
        run(ruff, "check", "--fix", "--quiet", path)
        run(ruff, "format", "--quiet", path)
        remaining = run(ruff, "check", "--output-format=concise", path)
        if remaining.returncode == 1 and remaining.stdout.strip():
            print(f"ruff found problems in {path}:\n{remaining.stdout}", file=sys.stderr)
            sys.exit(2)
    elif black := find(os.path.join(".venv", "bin", "black"), "black"):
        run(black, "--quiet", path)
elif ext in (".js", ".jsx", ".ts", ".tsx", ".mjs", ".cjs", ".json", ".css", ".scss"):
    if prettier := find(os.path.join("node_modules", ".bin", "prettier")):
        run(prettier, "--write", "--log-level", "warn", path)
elif ext == ".php":
    if pint := find(os.path.join("vendor", "bin", "pint")):
        run(pint, "--quiet", path)
elif ext == ".go":
    if gofmt := find("gofmt"):
        run(gofmt, "-w", path)

sys.exit(0)
