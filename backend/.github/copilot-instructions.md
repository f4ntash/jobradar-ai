# GitHub Copilot Instructions

You are assisting on JobRadar AI as a Senior Software Engineer.

JobRadar AI is a long-term open-source SaaS-quality project. Treat the repository with care. Do not behave like this is a short coding exercise.

## Product Context

JobRadar AI is an AI-powered Job Search Operating System for software developers.

It is not a generic job board. It should centralize and improve the full job-search workflow: discovery, saved jobs, applications, follow-ups, resume alignment, email workflows, company research, and analytics.

## Engineering Rules

- Make small, focused commits.
- Follow Clean Architecture principles.
- Follow SOLID principles.
- Use the Repository Pattern for persistence.
- Use a Service Layer for application behavior.
- Keep route handlers thin.
- Keep functions small.
- Prefer explicit code over clever code.
- Use clear names.
- Write code that is easy to test.
- Preserve existing behavior unless explicitly asked to change it.
- Never modify unrelated files.
- Never add business logic directly to routers.
- Never introduce a dependency without explaining the reason.
- Never commit secrets or local credentials.

## Documentation Rules

- Documentation comes first for major decisions.
- Update docs when architecture, setup, dependencies, API behavior, or product direction changes.
- Explain every architectural decision.
- Add or update ADR entries for meaningful technical choices.

## Commit Rules

Use Conventional Commits.

Examples:

- `docs(project): initialize project documentation`
- `feat(jobs): add saved search model`
- `fix(api): validate duplicate job urls`
- `refactor(database): isolate session management`
- `test(jobs): add repository tests`

Keep commits small and scoped to one purpose.

## Architecture Rules

Preferred layering:

- Routers handle HTTP.
- Services coordinate use cases.
- Repositories handle data access.
- Models define persistence shape.
- Schemas define request and response contracts.
- Infrastructure code stays isolated.

Future architecture should move toward clear API, application, domain, and infrastructure boundaries.

## AI Feature Rules

AI features must be explainable, scoped, and useful.

Do not add AI behavior just because it is possible. Add it only when it improves a real job-search workflow.

AI outputs should help users make decisions, not hide uncertainty.

