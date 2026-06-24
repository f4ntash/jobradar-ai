# Architecture

JobRadar AI currently uses a FastAPI backend with a SQLite database and a layered structure that can grow toward Clean Architecture over time.

The project should evolve carefully. Architecture decisions must support a real SaaS-quality product, not just a quick prototype.

## Current Backend

Current backend responsibilities:

- Expose HTTP API endpoints.
- Validate request and response data.
- Persist job records.
- Search external job sources.
- Keep job persistence logic separated from route handlers.

Current structure:

- `app/main.py` initializes the FastAPI application, CORS, database tables, and routers.
- `app/routers/` contains API route modules.
- `app/repositories/` contains database access functions.
- `app/models/` contains SQLAlchemy models.
- `app/schemas/` contains Pydantic schemas.
- `app/services/` contains service-style modules such as scraping/search logic.
- `app/core/` contains infrastructure setup such as database configuration.

## Frontend

The frontend has not been implemented yet.

The future frontend should be a SaaS-quality web application focused on job-search operations:

- Dashboard.
- Job pipeline.
- Search results.
- Saved job detail pages.
- Application tracking.
- AI-assisted workflows.
- Settings and integrations.

Frontend architecture should be decided and documented before implementation.

## Database

Current database:

- SQLite.
- Local file: `job_hunter.db`.
- SQLAlchemy ORM.

SQLite is appropriate for the current foundation because it keeps local development simple and removes operational overhead.

Future database:

- PostgreSQL should be introduced when the product needs production-grade concurrency, migrations, hosted deployment, relational constraints at scale, better indexing, and integration with SaaS infrastructure.

## Services

Services should contain application behavior that does not belong directly in routers or repositories.

Examples:

- Job search orchestration.
- Scraping adapters.
- AI matching.
- Resume analysis.
- Email workflow coordination.
- Notification and reminder logic.

Services should be small, testable, and focused on use cases.

## Repositories

Repositories should isolate persistence details from application logic.

They should:

- Read and write database records.
- Hide SQLAlchemy query details from routers and services.
- Keep database access testable.
- Avoid business workflow decisions.

Repositories should not become large service objects. They are data-access boundaries.

## Routers

Routers should define the HTTP interface.

They should:

- Declare endpoints.
- Validate inputs through schemas.
- Call services or repositories.
- Convert application errors into HTTP responses.

Routers should not contain complex business logic.

## Future Architecture

As JobRadar AI grows, the architecture should move toward clearer boundaries:

- API layer: FastAPI routers and HTTP concerns.
- Application layer: use cases and services.
- Domain layer: business concepts and rules.
- Infrastructure layer: database, external APIs, email, AI providers, scrapers, queues.

Expected future components:

- Database migrations.
- Authentication and authorization.
- Background jobs.
- External integrations.
- AI provider abstraction.
- Observability and logging.
- Test suite.
- Configuration management.
- Deployment pipeline.

## Why FastAPI

FastAPI is a strong fit because:

- It is modern and production-ready.
- It has excellent support for typed Python.
- It integrates naturally with Pydantic.
- It generates OpenAPI documentation automatically.
- It is fast enough for API workloads.
- It supports dependency injection patterns.
- It is approachable for contributors.

## Why Repository Pattern

The Repository Pattern keeps database access separate from API and business logic.

This matters because JobRadar AI will eventually need:

- More complex queries.
- Different persistence strategies.
- Tests that do not depend on real infrastructure.
- Safer refactors.
- Cleaner service code.

## Why Clean Architecture

Clean Architecture helps protect the product from becoming tightly coupled to frameworks, databases, AI vendors, or scraping tools.

For JobRadar AI, this matters because the product is expected to grow into a long-term SaaS-quality system.

The architecture should make it possible to change implementation details without rewriting the core product behavior.

