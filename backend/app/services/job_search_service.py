from sqlalchemy.orm import Session

from app.schemas.job import JobCreate, SearchAndSaveResponse
from app.schemas.job_found import JobFound
from app.services import job_service
from app.services.job_scraper import JobScraper


def search_jobs(query: str, max_results: int | None):
    scraper = JobScraper()
    return scraper.search(query, max_results)


def search_and_save_jobs(
    db: Session, query: str, max_results: int | None
) -> SearchAndSaveResponse:
    found_jobs = search_jobs(query, max_results)
    created_jobs = []
    duplicates_count = 0

    for job_found in found_jobs:
        job_create = _convert_job_found_to_create(job_found)
        try:
            created_jobs.append(job_service.create_job(db, job_create))
        except job_service.DuplicateJobUrlError:
            duplicates_count += 1

    return SearchAndSaveResponse(
        found=len(found_jobs),
        created=len(created_jobs),
        duplicates=duplicates_count,
        jobs=created_jobs,
    )


def _convert_job_found_to_create(job_found: JobFound) -> JobCreate:
    stack_str = ", ".join(job_found.stack) if job_found.stack else None
    return JobCreate(
        title=job_found.title,
        url=job_found.url,
        company=job_found.company,
        location=job_found.location,
        remote=job_found.remote,
        portal=job_found.portal,
        stack=stack_str,
        match_score=0,
        status="saved",
        notes=job_found.snippet,
    )
