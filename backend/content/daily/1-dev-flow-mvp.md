# Day 1 - dev-flow-mvp

## Goal
Build the first version of a developer workflow that documents each sprint, generates a development journal, prepares a LinkedIn draft, and suggests a professional Git commit.

## Changes
Built a CLI tool called dev_flow.py that checks the Git status, runs tests, collects sprint notes, generates Markdown files for the development journal and LinkedIn, updates a static HTML journal, stages changes, and optionally creates a Conventional Commit.

## What went wrong
The script grew beyond the original MVP scope. It currently handles multiple responsibilities in a single file and still needs to be refactored into smaller, more maintainable components.

## Learnings
I learned how to automate parts of a real development workflow using Python, including interacting with Git, generating documentation, and organizing the end of each sprint into a repeatable process.

## Technologies used
Python, Git, Markdown, HTML

## AI tools used
ChatGPT, Codex

## Programs/tools used
Cursor, Git, Terminal

## Commit
feat(dev-flow): add sprint journal generator

## Next step
Refactor the script by separating responsibilities, improving maintainability, and preparing it to become part of the standard development workflow.
