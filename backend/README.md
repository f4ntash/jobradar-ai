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

JobRadar AI is in Sprint 0: Project Foundation.

The current backend contains an initial FastAPI API with job CRUD endpoints, job search endpoints, a SQLite database, SQLAlchemy models, Pydantic schemas, repository functions, routers, and scraper services.

The repository is being professionalized before adding new features.

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
- `PATCH /jobs/{job_id}` - Update a saved job.
- `DELETE /jobs/{job_id}` - Delete a saved job.
- `POST /jobs/search` - Search for jobs across supported sources.
- `POST /jobs/search-and-save` - Search for jobs and save new results.

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

