# Architecture Decision Records

This document records important technical decisions for JobRadar AI.

Each decision should explain context, decision, rationale, and consequences.

## ADR-001: Use Python for the Backend

Status: Accepted

### Context

JobRadar AI needs a backend that can support APIs, scraping, data processing, AI workflows, and integrations.

### Decision

Use Python as the backend language.

### Rationale

Python is a strong fit for:

- Fast API development.
- AI and data workflows.
- Scraping and automation.
- Large ecosystem support.
- Readability for contributors.

### Consequences

The project should maintain strong typing habits, clear module boundaries, tests, and formatting standards to keep Python code maintainable as the codebase grows.

## ADR-002: Use FastAPI

Status: Accepted

### Context

The product needs a modern API framework that supports typed request and response models, OpenAPI documentation, and clean dependency injection.

### Decision

Use FastAPI for the backend API.

### Rationale

FastAPI provides:

- Pydantic integration.
- Automatic API documentation.
- Good performance.
- Clear route organization.
- Dependency injection.
- Strong developer experience.

### Consequences

Route handlers should stay thin. Business logic should move into services and data access should remain in repositories.

## ADR-003: Use SQLite First

Status: Accepted

### Context

The project is in early foundation and local development mode.

### Decision

Use SQLite as the initial database.

### Rationale

SQLite keeps the early project simple:

- No external database server.
- Easy local setup.
- Good enough for early CRUD workflows.
- Low operational overhead.

### Consequences

SQLite should not be treated as the final production database. The code should avoid assumptions that make PostgreSQL migration difficult.

## ADR-004: Move to PostgreSQL Later

Status: Proposed

### Context

A production SaaS product will eventually need stronger database capabilities.

### Decision

Plan to move to PostgreSQL when production readiness requires it.

### Rationale

PostgreSQL provides:

- Production-grade reliability.
- Better concurrency.
- Strong indexing.
- Rich query capabilities.
- Better support for hosted SaaS deployments.
- Strong ecosystem support.

### Consequences

Database access should remain behind repositories and migrations should be introduced before the schema becomes complex.

## ADR-005: Use Repository Pattern

Status: Accepted

### Context

The project already separates job persistence into a repository module.

### Decision

Continue using the Repository Pattern for database access.

### Rationale

Repositories:

- Keep SQLAlchemy details out of routers.
- Make tests easier.
- Make future database changes safer.
- Clarify ownership of persistence operations.

### Consequences

Repositories should stay focused on data access. They should not contain complex business workflows.

## ADR-006: Use a Service Layer

Status: Accepted

### Context

JobRadar AI will grow beyond simple CRUD into search orchestration, AI workflows, integrations, reminders, and analytics.

### Decision

Use a service layer for application behavior.

### Rationale

Services:

- Keep routers thin.
- Coordinate repositories and external systems.
- Represent use cases.
- Improve testability.
- Prevent business logic from spreading across API handlers.

### Consequences

Services should be small, focused, and explicit. They should not become unstructured utility modules.

## ADR-007: Prefer Clean Architecture as the Long-Term Direction

Status: Accepted

### Context

The project is intended to become a long-term portfolio-grade SaaS application.

### Decision

Use Clean Architecture principles as the direction for future growth.

### Rationale

Clean boundaries will help the project avoid tight coupling to:

- Web framework details.
- Database implementation.
- Scraping providers.
- AI vendors.
- Email providers.
- Frontend assumptions.

### Consequences

Future changes should preserve separation between API, application, domain, and infrastructure concerns.

