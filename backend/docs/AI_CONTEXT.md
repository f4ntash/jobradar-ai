# AI Context for JobRadar AI

This file is mandatory reading for any AI assistant or AI coding tool working on JobRadar AI.

JobRadar AI is a serious long-term open-source project. It is intended to become a SaaS-quality application and the main portfolio project of its creator.

Do not treat this repository as a coding exercise.

## Project Philosophy

JobRadar AI is not a job board.

It is an operating system for job searching.

The product exists to help software developers manage the full job-search workflow: discovery, tracking, applications, follow-ups, research, resume alignment, and decision-making.

Every feature should reduce real friction for developers.

## Long-Term Vision

JobRadar AI should become an AI-powered Job Search Operating System.

Long-term capabilities may include:

- Job discovery.
- Saved jobs.
- Application tracking.
- AI job-fit analysis.
- Resume matching.
- Company research.
- Gmail workflows.
- Follow-up reminders.
- Analytics.
- Frontend dashboard.
- User accounts.
- Production SaaS deployment.

## Architecture

Current backend architecture:

- FastAPI for HTTP API.
- SQLAlchemy for ORM.
- SQLite for local persistence.
- Pydantic for schemas.
- Routers for HTTP endpoints.
- Repositories for data access.
- Services for application behavior and external workflows.

Preferred long-term architecture:

- API layer.
- Application service layer.
- Domain concepts and rules.
- Infrastructure layer.
- Repository interfaces or repository modules.
- Clear dependency boundaries.

## Coding Standards

Code should be:

- Simple.
- Typed where practical.
- Small in function size.
- Easy to test.
- Explicit rather than clever.
- Consistent with existing project patterns.

Prefer:

- Small functions.
- Clear names.
- Dependency injection.
- Repository Pattern.
- Service Layer.
- SOLID principles.
- Focused modules.
- Tests for meaningful behavior.

Avoid:

- Large route handlers.
- Business logic inside routers.
- Database queries scattered across the app.
- Hidden side effects.
- Global state unless justified.
- Premature abstractions.
- Unrelated refactors.

## Documentation Standards

Documentation should be updated when decisions change.

Document:

- Product direction.
- Architecture decisions.
- New setup steps.
- New environment variables.
- New API behavior.
- New dependencies.
- Breaking changes.

Documentation is part of the product, not an afterthought.

## Commit Rules

Use Conventional Commits.

Examples:

- `docs(project): initialize project documentation`
- `feat(jobs): add saved search model`
- `fix(api): validate duplicate job urls`
- `refactor(database): isolate session management`
- `test(jobs): add repository tests`

Commits should be small and focused.

Do not mix unrelated changes in the same commit.

## Engineering Principles

Follow these principles:

- Make the smallest useful change.
- Preserve existing behavior unless the task explicitly changes it.
- Explain architectural decisions.
- Keep boundaries clear.
- Prefer maintainability over cleverness.
- Optimize for future contributors.
- Add tests when behavior changes.
- Avoid building features before the product direction is clear.

## What Should Never Be Done

Never:

- Modify unrelated files.
- Rewrite existing backend code without explicit instruction.
- Add endpoints without product context.
- Add business logic directly to routers.
- Introduce a dependency without explaining why.
- Hide architectural decisions.
- Rename major concepts casually.
- Replace SQLite with PostgreSQL without a migration plan.
- Add AI behavior without guardrails and explainability.
- Treat scraped data as always reliable.
- Commit secrets.
- Store API keys in source code.
- Add large generated files without justification.
- Ignore the project documentation.

## AI Assistant Behavior

When working on this project, an AI assistant should behave like a senior software engineer:

- Read the existing code before changing it.
- Respect the current architecture.
- Ask only when context is genuinely missing.
- Keep changes scoped.
- Explain tradeoffs.
- Prefer incremental progress.
- Update documentation when needed.
- Avoid speculative features.
- Protect the long-term quality of the project.

## Current Priority

The current priority is project foundation and professionalization.

Before adding new features, the repository should have:

- Clear documentation.
- Stable architecture direction.
- Consistent naming.
- Tests.
- Contribution standards.
- A clean development setup.

