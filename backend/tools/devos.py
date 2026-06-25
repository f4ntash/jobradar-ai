"""JobRadar AI Developer OS CLI."""

from __future__ import annotations

import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from tools import git_flow, journal, linkedin, prompts, website
from tools.utils import ROOT, ask_yes_no, print_command_output, relative_path, run_command


def print_header() -> None:
    print("=" * 34)
    print(" JobRadar AI DevOS")
    print("=" * 34)


def run_tests() -> bool:
    print("\n== Tests ==")
    if not (ROOT / "app").exists():
        print("Warning: backend app directory not found. Skipping tests.")
        return True

    result = run_command(["python", "-m", "pytest"])
    print_command_output(result)
    if result.returncode == 0:
        return True

    print("Warning: tests failed.")
    return ask_yes_no("Continue workflow anyway?", default=False)


def generate_files(data: dict[str, str], commit: str) -> list[Path]:
    print("\n== Generate files ==")
    daily_path = journal.save_daily_journal(data, commit)
    linkedin_path = linkedin.save_linkedin_draft(data)
    website_path = website.update_journal_index()
    return [daily_path, linkedin_path, website_path]


def show_generated_paths(paths: list[Path]) -> None:
    print("\n== Generated files ==")
    for path in paths:
        print(relative_path(path))


def print_summary(paths: list[Path], commit: str) -> None:
    print("\n== Final summary ==")
    print("Generated files:")
    for path in paths:
        print(f"- {relative_path(path)}")
    print(f"Suggested commit: {commit}")
    print("LinkedIn draft saved only. Nothing was published.")
    print("No push was run unless you explicitly confirmed it.")


def main() -> None:
    print_header()
    git_flow.show_git_status()

    if not git_flow.ensure_not_on_main():
        return

    if not run_tests():
        print("Workflow stopped safely after test failure.")
        return

    data, commit = prompts.collect_workflow_data()
    paths = generate_files(data, commit)
    show_generated_paths(paths)

    git_flow.stage_changes()
    git_flow.show_git_status()
    git_flow.commit_changes(commit)
    git_flow.merge_current_branch_into_main()
    git_flow.push_main()
    print_summary(paths, commit)


if __name__ == "__main__":
    main()
