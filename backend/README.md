# JobRadar AI

JobRadar AI is an open-source project that helps software developers centralize and automate their job search.

Instead of manually switching between LinkedIn, Greenhouse, Lever, Gmail, spreadsheets, notes, and AI tools, JobRadar AI aims to become a single workspace for discovering opportunities, tracking applications, preparing outreach, and making better job-search decisions.

The long-term goal is to become an AI-powered Job Search Operating System for developers.

## Main Goal

Build a SaaS-quality portfolio project that solves real job-search pain points for software developers:

- Find relevant jobs faster.
- Save and organize opportunities.
- Track application status.
- Reduce repetitive manual work.
- Add AI assistance where it improves real workflows.

## Tech Stack

Current backend:

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- Requests
- BeautifulSoup
- DDGS
- OpenPyXL

Planned frontend:

- A modern web application for managing the job-search workflow.
- The frontend stack is not finalized yet.
- Future decisions should be documented before implementation.

## Current Status

JobRadar AI is in Sprint 2: Jobs domain stabilization.

The current backend contains an initial FastAPI API with job CRUD endpoints, job search endpoints, a SQLite database, SQLAlchemy models, Pydantic schemas, repository functions, routers, and services.

The Jobs feature routes CRUD behavior through a service layer, keeps repositories focused on database access, validates job status values, supports controlled manual ingestion, normalizes search results, and has basic REST coverage for create, read, update, delete, duplicate URL, invalid status, ingestion, and search behavior.

The repository is being cleaned up and documented before adding new product features.

## DevOS

DevOS is the internal developer workflow CLI for JobRadar AI.

It helps with the end-of-sprint workflow:

- Shows Git branch and status.
- Prevents working directly on `main`.
- Runs tests.
- Collects sprint notes.
- Generates the daily developer journal.
- Generates a LinkedIn draft.
- Updates the static developer journal website.
- Guides staging, commits, merges, and pushes with explicit confirmation prompts.

Run DevOS from the backend directory:

```bash
python tools/devos.py
```

DevOS never publishes anything and does not push without explicit confirmation.

## Project Structure

```text
app/
  core/          Database setup and shared backend infrastructure
  models/        SQLAlchemy models
  repositories/  Database access functions
  routers/       FastAPI route handlers
  schemas/       Pydantic request and response schemas
  services/      Business logic and orchestration
content/
  daily/         Markdown developer journal entries
  linkedin/      LinkedIn draft posts
docs/            Project documentation
public/
  dev-journal/   Static developer journal website
tests/           Backend API tests
tools/           DevOS CLI and developer workflow helpers
```

## How to Run the Backend

From the backend directory:

```bash
python -m venv venv
```

Activate the virtual environment.

On Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://localhost:8000
```

Interactive API docs:

```text
http://localhost:8000/docs
```

## Current API Endpoints

Root:

- `GET /` - Health-style root endpoint.

Jobs:

- `GET /jobs` - List saved jobs.
- `GET /jobs/{job_id}` - Get a saved job by ID.
- `POST /jobs` - Create a saved job.
- `POST /jobs/ingest` - Create a saved job from manually provided raw job data.
- `PATCH /jobs/{job_id}` - Update a saved job.
- `DELETE /jobs/{job_id}` - Delete a saved job.
- `GET /jobs/search?query=...&location=...` - Search for jobs across supported sources.
- `POST /jobs/search` - Legacy search endpoint using a JSON body.
- `POST /jobs/search-and-save` - Search for jobs and save new results.

Jobs behavior:

- New jobs default to `saved` status.
- Job URLs must be unique.
- Manual ingestion trims and normalizes simple string values before saving.
- Search results are normalized before being returned or saved.
- Search filtering is currently optimized for LATAM-friendly remote developer roles.
- Search-and-save skips duplicate URLs instead of creating duplicate jobs.
- The primary search provider is Get on Board's public jobs API, focused on LATAM tech roles.
- Remotive is kept only as a fallback when the primary provider returns no results.
- Missing jobs return `404`.
- Duplicate URLs return `400`.
- Invalid statuses return `422`.

Search provider status:

- The search service uses Get on Board as its primary external provider.
- Remotive remains available as a fallback provider, but it does not run when Get on Board returns results.
- Tests use mocked provider HTTP responses and do not depend on real websites.
- Empty search responses mean no configured provider returned matching results after filtering and normalization.
- Region filtering keeps LATAM, Americas, worldwide, global, and generally remote roles while excluding clearly restricted roles such as US-only or Europe-only jobs.
- Technical filtering favors software and web development relevance for developer queries such as `React Developer`.
- Provider calls and normalization counts are logged internally for debugging.

Allowed job statuses:

- `saved`
- `applied`
- `interview`
- `rejected`
- `offer`

## Future Frontend

The future frontend should be a professional SaaS-style application focused on daily job-search operations. It should prioritize clarity, speed, and practical workflows over marketing pages.

Expected future areas include:

- Job discovery dashboard.
- Saved jobs pipeline.
- Application tracker.
- AI-assisted job matching.
- Email and outreach workflows.
- Resume and profile management.
- Analytics for the job search process.

## Documentation

Project documentation lives in `docs/`:

- `docs/VISION.md`
- `docs/PRODUCT.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP.md`
- `docs/CHANGELOG.md`
- `docs/DECISIONS.md`
- `docs/AI_CONTEXT.md`
