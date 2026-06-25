"""Shared helpers for the JobRadar AI developer tools."""

from __future__ import annotations

import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "content" / "daily"
LINKEDIN_DIR = ROOT / "content" / "linkedin"
JOURNAL_INDEX = ROOT / "public" / "dev-journal" / "index.html"


def run_command(command: list[str], check: bool = False) -> subprocess.CompletedProcess:
    """Run a command from the project root."""
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=check,
    )


def print_command_output(result: subprocess.CompletedProcess) -> None:
    if result.stdout:
        print(result.stdout.rstrip())
    if result.stderr:
        print(result.stderr.rstrip())


def ask_yes_no(question: str, default: bool = False) -> bool:
    """Ask a yes/no question. Dangerous actions should use default=False."""
    suffix = "Y/n" if default else "y/N"
    answer = input(f"{question} [{suffix}]: ").strip().lower()

    if not answer:
        return default

    return answer in {"y", "yes"}


def slugify(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "daily-update"


def relative_path(path: Path) -> str:
    return str(path.relative_to(ROOT))
