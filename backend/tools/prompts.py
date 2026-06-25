"""Prompt helpers for the JobRadar AI DevOS CLI."""

from __future__ import annotations


SPRINT_QUESTIONS = [
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
]


def ask_with_default(question: str, default: str = "") -> str:
    if default:
        answer = input(f"{question} [{default}]: ").strip()
        return answer or default

    return input(f"{question}: ").strip()


def collect_sprint_answers() -> dict[str, str]:
    print("\n== Sprint notes ==")
    answers: dict[str, str] = {}
    for key, question in SPRINT_QUESTIONS:
        answers[key] = ask_with_default(question)
    return answers


def collect_commit_parts() -> dict[str, str]:
    print("\n== Conventional Commit ==")
    return {
        "commit_type": ask_with_default("Commit type", "refactor"),
        "commit_scope": ask_with_default("Commit scope", "dev-flow"),
        "commit_message": ask_with_default(
            "Commit message",
            "introduce modular devos cli",
        ),
    }


def build_commit_message(commit_parts: dict[str, str]) -> str:
    commit_type = commit_parts["commit_type"].strip()
    scope = commit_parts["commit_scope"].strip()
    message = commit_parts["commit_message"].strip()
    return f"{commit_type}({scope}): {message}"


def collect_workflow_data() -> tuple[dict[str, str], str]:
    answers = collect_sprint_answers()
    commit_parts = collect_commit_parts()
    answers.update(commit_parts)
    commit = build_commit_message(commit_parts)
    print(f"\nSuggested commit: {commit}")
    return answers, commit
