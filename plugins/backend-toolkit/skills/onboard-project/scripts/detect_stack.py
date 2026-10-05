#!/usr/bin/env python3
"""Detect a project's stack and the commands it uses. Standard library only.

Usage (from the project root):  python3 detect_stack.py [project_dir]

Prints a short report: language, framework, how to run tests, lint and format,
where migrations live, and which database it uses locally. Every finding names
the file it came from, so a person (or Claude) can check it.
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
facts = {
    "project": root.name,
    "languages": [],
    "frameworks": [],
    "commands": {},
    "migrations": [],
    "database": None,
    "evidence": [],
}


def read(name):
    path = root / name
    try:
        return path.read_text(errors="ignore") if path.is_file() else ""
    except OSError:
        return ""


def note(what, source):
    facts["evidence"].append(f"{what} ({source})")


def command(kind, cmd, source):
    if kind not in facts["commands"]:
        facts["commands"][kind] = cmd
        note(f"{kind}: {cmd}", source)


# Makefile targets win: they are the project's own entry points.
makefile = read("Makefile")
targets = set(re.findall(r"^([A-Za-z][\w-]*):", makefile, re.M))
for kind, names in {
    "setup": ["setup", "install"],
    "test": ["test"],
    "lint": ["lint"],
    "format": ["format", "fmt"],
    "run": ["run", "serve", "dev"],
}.items():
    for name in names:
        if name in targets:
            command(kind, f"make {name}", "Makefile")
            break

# Python
pyproject, requirements = read("pyproject.toml"), read("requirements.txt")
python_deps = (pyproject + requirements).lower()
if pyproject or requirements or (root / "manage.py").exists():
    facts["languages"].append("Python")
    venv = ".venv/bin/" if (root / ".venv").exists() or "venv" in makefile else ""
    if (root / "manage.py").exists() or "django" in python_deps:
        facts["frameworks"].append("Django")
        note("Django", "manage.py" if (root / "manage.py").exists() else "dependencies")
        if "djangorestframework" in python_deps:
            facts["frameworks"].append("Django REST Framework")
        facts["migrations"].append("*/migrations/ (Django)")
    if "fastapi" in python_deps:
        facts["frameworks"].append("FastAPI")
    if "flask" in python_deps:
        facts["frameworks"].append("Flask")
    if "alembic" in python_deps or (root / "alembic").is_dir():
        facts["migrations"].append("alembic/versions/ (Alembic)")
    if "pytest" in python_deps:
        command("test", f"{venv}python -m pytest", "pytest in dependencies")
    if "ruff" in python_deps:
        command("lint", f"{venv}ruff check .", "ruff in dependencies")
        command("format", f"{venv}ruff format .", "ruff in dependencies")

# PHP
composer = read("composer.json")
if composer:
    facts["languages"].append("PHP")
    if "laravel/framework" in composer:
        facts["frameworks"].append("Laravel")
        facts["migrations"].append("database/migrations/ (Laravel)")
        command("test", "php artisan test", "composer.json")
    if "laravel/pint" in composer:
        command("format", "./vendor/bin/pint", "composer.json")

# JavaScript / TypeScript
package = read("package.json")
if package:
    try:
        pkg = json.loads(package)
    except json.JSONDecodeError:
        pkg = {}
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    facts["languages"].append("TypeScript" if "typescript" in deps else "JavaScript")
    for dep, name in [
        ("@nestjs/core", "NestJS"),
        ("express", "Express"),
        ("fastify", "Fastify"),
        ("next", "Next.js"),
        ("react", "React"),
    ]:
        if dep in deps:
            facts["frameworks"].append(name)
    if "prisma" in deps or (root / "prisma").is_dir():
        facts["migrations"].append("prisma/migrations/ (Prisma)")
    runner = (
        "pnpm"
        if (root / "pnpm-lock.yaml").exists()
        else "yarn"
        if (root / "yarn.lock").exists()
        else "npm run"
    )
    for kind in ("test", "lint", "format", "dev"):
        if kind in pkg.get("scripts", {}):
            command("run" if kind == "dev" else kind, f"{runner} {kind}", "package.json scripts")

# Go
gomod = read("go.mod")
if gomod:
    facts["languages"].append("Go")
    for dep, name in [("gin-gonic/gin", "Gin"), ("go-chi/chi", "Chi"), ("labstack/echo", "Echo")]:
        if dep in gomod:
            facts["frameworks"].append(name)
    command("test", "go test ./...", "go.mod")
    command("format", "gofmt -w .", "go.mod")
    if (root / "migrations").is_dir():
        facts["migrations"].append("migrations/ (SQL)")

# Rails
if read("Gemfile") and "rails" in read("Gemfile"):
    facts["languages"].append("Ruby")
    facts["frameworks"].append("Rails")
    facts["migrations"].append("db/migrate/ (Rails)")

# Local database
for pattern in ("*.sqlite3", "*.sqlite", "*.db"):
    found = sorted(root.glob(pattern))
    if found:
        facts["database"] = f"SQLite: {found[0].name}"
        note("SQLite database", found[0].name)
        break
if facts["database"] is None:
    env_example = read(".env.example") + read(".env.sample")
    match = re.search(r"^(DATABASE_URL|DB_CONNECTION)=(\S+)", env_example, re.M)
    if match:
        facts["database"] = f"{match.group(1)}={match.group(2)} (from the example env file)"

# Instructions already present
for name in ("CLAUDE.md", "README.md", "TICKET.md", "CONTRIBUTING.md"):
    if (root / name).exists():
        note("has " + name, name)

print(f"Project:     {facts['project']}")
print(f"Languages:   {', '.join(facts['languages']) or 'unknown'}")
print(f"Frameworks:  {', '.join(facts['frameworks']) or 'none detected'}")
for kind in ("setup", "run", "test", "lint", "format"):
    if kind in facts["commands"]:
        print(f"{kind.capitalize() + ':':<12} {facts['commands'][kind]}")
print(f"Migrations:  {', '.join(facts['migrations']) or 'none detected'}")
print(f"Database:    {facts['database'] or 'not detected'}")
print("\nEvidence:")
for line in facts["evidence"]:
    print(f"  - {line}")
