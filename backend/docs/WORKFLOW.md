# Development Workflow

JobRadar AI uses a simple sprint-based workflow. The goal is to keep each change easy to review, document, and ship safely.

## Branching Rules

Never develop directly on `main`.

Use one branch per sprint or cleanup task. Keep branch names short and descriptive:

- `feature/<short-name>`
- `refactor/<short-name>`
- `docs/<short-name>`
- `fix/<short-name>`
- `test/<short-name>`

Examples:

- `refactor/devos-cli`
- `docs/project-workflow`
- `test/jobs-api`

## Commits

Use Conventional Commits:

```text
type(scope): message
```

Common types:

- `feat`
- `fix`
- `docs`
- `refactor`
- `test`
- `chore`

Example:

```text
docs(project): improve workflow documentation and project foundation
```

## Pull Request Workflow

1. Create a branch for the sprint.
2. Make focused changes only for that sprint.
3. Run tests locally.
4. Update documentation when behavior or workflow changes.
5. Use DevOS to generate the sprint journal and LinkedIn draft.
6. Review the generated files before committing.
7. Open a Pull Request into `main`.
8. Merge only after review.
9. Push `main` only when you explicitly choose to do so.

## DevOS

DevOS is the internal developer workflow CLI for JobRadar AI. It helps document the sprint, run tests, generate the developer journal, prepare a LinkedIn draft, and guide Git actions with confirmation prompts.

Run it from the backend project:

```bash
python tools/devos.py
```

DevOS does not publish posts, create CI/CD workflows, or push changes without explicit confirmation.

## Sprint Definition of Done

A sprint is done when:

- The branch contains only changes related to the sprint goal.
- Tests pass locally, or any failing test is documented before continuing.
- Documentation is updated when needed.
- DevOS generated the daily journal entry.
- DevOS generated the LinkedIn draft.
- The static developer journal website was updated.
- The commit uses Conventional Commit format.
- The Pull Request is ready to review or merge.
