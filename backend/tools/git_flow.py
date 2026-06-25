"""Git workflow helpers for the JobRadar AI DevOS CLI."""

from __future__ import annotations

from utils import ask_yes_no, print_command_output, run_command


def current_branch() -> str:
    result = run_command(["git", "branch", "--show-current"])
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def working_tree_is_dirty() -> bool:
    result = run_command(["git", "status", "--short"])
    return bool(result.stdout.strip())


def show_git_status() -> None:
    print("\n== Git status ==")
    branch = current_branch()
    if branch:
        print(f"Branch: {branch}")
    else:
        print("Warning: could not detect current branch.")

    result = run_command(["git", "status", "--short"])
    if result.returncode == 0:
        if result.stdout.strip():
            print_command_output(result)
        else:
            print("Working tree clean.")
        return

    print("Warning: could not read git status.")
    print_command_output(result)


def create_branch(branch_name: str) -> bool:
    result = run_command(["git", "checkout", "-b", branch_name])
    if result.returncode != 0:
        print("Warning: branch was not created.")
        print_command_output(result)
        return False

    print_command_output(result)
    return True


def ensure_not_on_main() -> bool:
    branch = current_branch()
    if branch != "main":
        return True

    print("\nWarning: working directly on main is not allowed.")
    if working_tree_is_dirty():
        print("Warning: the working tree is dirty. New branch checkout will carry these changes.")

    if not ask_yes_no("Create a new branch now?", default=False):
        print("Workflow stopped safely. No branch was created.")
        return False

    branch_name = input("New branch name: ").strip()
    if not branch_name:
        print("Workflow stopped safely. Branch name cannot be empty.")
        return False

    return create_branch(branch_name)


def stage_changes() -> bool:
    print("\n== Stage changes ==")
    if not ask_yes_no("Stage all changes with git add .?", default=False):
        print("Staging skipped.")
        return False

    result = run_command(["git", "add", "."])
    if result.returncode != 0:
        print("Warning: could not stage files.")
        print_command_output(result)
        return False

    print_command_output(result)
    print("Changes staged.")
    return True


def commit_changes(commit_message: str) -> bool:
    print("\n== Commit changes ==")
    if not ask_yes_no(f'Commit with "{commit_message}"?', default=False):
        print("Commit skipped.")
        return False

    result = run_command(["git", "commit", "-m", commit_message])
    if result.returncode != 0:
        print("Warning: commit was not created.")
        print_command_output(result)
        return False

    print_command_output(result)
    return True


def merge_current_branch_into_main() -> bool:
    print("\n== Merge into main ==")
    source_branch = current_branch()
    if not source_branch:
        print("Warning: could not detect current branch. Merge skipped.")
        return False

    if source_branch == "main":
        print("Already on main. Merge skipped.")
        return False

    if not ask_yes_no(f"Merge {source_branch} into main?", default=False):
        print("Merge skipped.")
        return False

    checkout_result = run_command(["git", "checkout", "main"])
    if checkout_result.returncode != 0:
        print("Warning: could not checkout main.")
        print_command_output(checkout_result)
        return False

    merge_result = run_command(["git", "merge", source_branch])
    if merge_result.returncode != 0:
        print("Warning: merge did not complete cleanly.")
        print_command_output(merge_result)
        return False

    print_command_output(merge_result)
    return True


def push_main() -> bool:
    print("\n== Push main ==")
    if not ask_yes_no("Push main to origin?", default=False):
        print("Push skipped.")
        return False

    branch = current_branch()
    if branch != "main":
        print("Warning: push skipped because current branch is not main.")
        return False

    result = run_command(["git", "push", "origin", "main"])
    if result.returncode != 0:
        print("Warning: push failed.")
        print_command_output(result)
        return False

    print_command_output(result)
    return True
