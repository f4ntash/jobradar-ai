"""Developer workflow helper for JobRadar AI.

This script documents a sprint/day, refreshes the static developer journal,
stages changes, and optionally creates a Conventional Commit.
"""

from __future__ import annotations

import html
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DAILY_DIR = ROOT / "content" / "daily"
LINKEDIN_DIR = ROOT / "content" / "linkedin"
JOURNAL_INDEX = ROOT / "public" / "dev-journal" / "index.html"


FIELDS = [
    ("day", "Day number"),
    ("slug", "Short slug"),
    ("goal", "What was the goal?"),
    ("changes", "What did you build/change?"),
    ("went_wrong", "What went wrong?"),
    ("learnings", "What did you learn?"),
    ("technologies", "Technologies used"),
    ("ai_tools", "AI tools used"),
    ("programs", "Programs/tools used"),
    ("next_step", "Next step"),
    ("commit_type", "Commit type"),
    ("commit_scope", "Commit scope"),
    ("commit_message", "Commit message"),
]


def run_command(command: list[str], check: bool = False) -> subprocess.CompletedProcess:
    """Run a command from the project root and return the completed process."""
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


def show_git_status() -> None:
    print("\n== Git status ==")
    result = run_command(["git", "status", "--short"])
    if result.returncode == 0:
        print_command_output(result)
        return
    print("Warning: could not read git status.")
    print_command_output(result)


def run_tests() -> None:
    print("\n== Tests ==")
    if not (ROOT / "app").exists():
        print("Warning: backend app directory not found. Skipping tests.")
        return

    result = run_command(["python", "-m", "pytest"])
    if result.returncode == 0:
        print_command_output(result)
        return

    output = f"{result.stdout}\n{result.stderr}".lower()
    if "no module named pytest" in output or "no tests ran" in output:
        print("Warning: pytest is not installed or no tests exist. Continuing.")
        print_command_output(result)
        return

    print("Warning: tests did not pass. Continuing so the day can be documented.")
    print_command_output(result)


def ask_fields() -> dict[str, str]:
    print("\n== Daily notes ==")
    answers: dict[str, str] = {}
    for key, prompt in FIELDS:
        answers[key] = input(f"{prompt}: ").strip()
    return answers


def slugify(value: str) -> str:
    slug = value.strip().lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")
    return slug or "daily-update"


def build_commit_message(data: dict[str, str]) -> str:
    commit_type = data["commit_type"].strip()
    scope = data["commit_scope"].strip()
    message = data["commit_message"].strip()
    return f"{commit_type}({scope}): {message}"


def daily_markdown(data: dict[str, str], commit: str) -> str:
    return f"""# Day {data["day"]} - {data["slug"]}

## Goal
{data["goal"]}

## Changes
{data["changes"]}

## What went wrong
{data["went_wrong"]}

## Learnings
{data["learnings"]}

## Technologies used
{data["technologies"]}

## AI tools used
{data["ai_tools"]}

## Programs/tools used
{data["programs"]}

## Commit
{commit}

## Next step
{data["next_step"]}
"""


def linkedin_markdown(data: dict[str, str]) -> str:
    return f"""Hoy fue el Day {data["day"]} construyendo JobRadar AI.

Trabaje en: {data["changes"]}

El objetivo del dia era: {data["goal"]}

La parte mas importante no fue solo avanzar, sino entender esto: {data["learnings"]}

Tambien hubo algo que no salio perfecto: {data["went_wrong"]}

Tecnologias y herramientas usadas:
- {data["technologies"]}
- AI tools: {data["ai_tools"]}
- Programas/tools: {data["programs"]}

Lo proximo: {data["next_step"]}

Estoy construyendo este proyecto en publico, con foco en aprender bien, documentar el proceso y convertir JobRadar AI en un producto real para desarrolladores que buscan trabajo.

#BuildInPublic #Python #FastAPI #SoftwareDevelopment #OpenSource #JobSearch #LearningInPublic
"""


def write_markdown_files(data: dict[str, str], commit: str) -> list[Path]:
    safe_slug = slugify(data["slug"])
    file_name = f"{data['day']}-{safe_slug}.md"
    data["slug"] = safe_slug
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    LINKEDIN_DIR.mkdir(parents=True, exist_ok=True)

    daily_path = DAILY_DIR / file_name
    linkedin_path = LINKEDIN_DIR / file_name
    daily_path.write_text(daily_markdown(data, commit), encoding="utf-8")
    linkedin_path.write_text(linkedin_markdown(data), encoding="utf-8")
    return [daily_path, linkedin_path]


def section_value(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_daily_file(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ").strip()
    day_match = re.search(r"Day\s+(\d+)", title, flags=re.IGNORECASE)
    day = day_match.group(1) if day_match else "0"
    slug = title.split(" - ", 1)[1] if " - " in title else path.stem
    return {
        "day": day,
        "slug": slug,
        "goal": section_value(text, "Goal"),
        "learnings": section_value(text, "Learnings"),
        "technologies": section_value(text, "Technologies used"),
        "ai_tools": section_value(text, "AI tools used"),
        "commit": section_value(text, "Commit"),
    }


def render_journal_item(item: dict[str, str]) -> str:
    return f"""<article>
  <h2>Day {html.escape(item["day"])} - {html.escape(item["slug"])}</h2>
  <p><strong>Goal:</strong> {html.escape(item["goal"])}</p>
  <p><strong>Learnings:</strong> {html.escape(item["learnings"])}</p>
  <p><strong>Technologies:</strong> {html.escape(item["technologies"])}</p>
  <p><strong>AI tools:</strong> {html.escape(item["ai_tools"])}</p>
  <p><strong>Commit:</strong> <code>{html.escape(item["commit"])}</code></p>
</article>"""


def build_index_html(items: list[dict[str, str]]) -> str:
    body = "\n".join(render_journal_item(item) for item in items)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>JobRadar AI Dev Journal</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; line-height: 1.5; }}
    main {{ max-width: 860px; margin: 0 auto; }}
    article {{ border-bottom: 1px solid #ddd; padding: 1rem 0; }}
    code {{ background: #f4f4f4; padding: 0.1rem 0.3rem; }}
  </style>
</head>
<body>
  <main>
    <h1>JobRadar AI Dev Journal</h1>
    {body}
  </main>
</body>
</html>
"""


def update_journal_index() -> Path:
    JOURNAL_INDEX.parent.mkdir(parents=True, exist_ok=True)
    items = [parse_daily_file(path) for path in DAILY_DIR.glob("*.md")]
    items.sort(key=lambda item: int(item["day"]))
    JOURNAL_INDEX.write_text(build_index_html(items), encoding="utf-8")
    return JOURNAL_INDEX


def git_add_all() -> None:
    print("\n== Staging files ==")
    result = run_command(["git", "add", "."])
    if result.returncode != 0:
        print("Warning: could not stage files.")
    print_command_output(result)


def maybe_commit(commit: str) -> None:
    answer = input('\nCreate commit? y/n: ').strip().lower()
    if answer != "y":
        print("Commit skipped.")
        return

    result = run_command(["git", "commit", "-m", commit])
    if result.returncode != 0:
        print("Warning: commit was not created.")
    print_command_output(result)


def print_summary(paths: list[Path], commit: str) -> None:
    print("\n== Summary ==")
    for path in paths:
        print(path.relative_to(ROOT))
    print(f"Commit message: {commit}")
    print("Review the generated LinkedIn post before publishing.")
    print("Run git push manually when ready.")


def main() -> None:
    show_git_status()
    run_tests()
    data = ask_fields()
    commit = build_commit_message(data)
    paths = write_markdown_files(data, commit)
    paths.append(update_journal_index())
    git_add_all()
    show_git_status()
    maybe_commit(commit)
    print_summary(paths, commit)


if __name__ == "__main__":
    main()
