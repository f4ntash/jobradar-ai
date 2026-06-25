import logging
import re
from urllib.parse import urlparse

from sqlalchemy.orm import Session

from app.schemas.job import JobCreate, SearchAndSaveResponse
from app.schemas.job_found import JobFound
from app.services import job_service
from app.services.job_scraper import JobScraper


logger = logging.getLogger(__name__)


class SearchProviderError(Exception):
    """Raised when the job search provider cannot return results."""


def search_jobs(
    query: str,
    location: str | None = None,
    max_results: int | None = 20,
) -> list[JobFound]:
    logger.info(
        "Job search received: query=%r location=%r max_results=%r",
        query,
        location,
        max_results,
    )
    try:
        raw_jobs = _search_provider(query, location, max_results)
    except Exception as error:
        logger.exception("Job search provider failed")
        raise SearchProviderError("Job search provider failed") from error

    logger.info("Job search raw results count: %s", len(raw_jobs))
    valid_jobs, skipped_reasons = _normalize_jobs(raw_jobs)
    logger.info(
        "Job search normalized results count: %s skipped results count: %s",
        len(valid_jobs),
        len(skipped_reasons),
    )
    for reason in skipped_reasons:
        logger.debug("Skipped search result: %s", reason)

    return valid_jobs[: max_results or 20]


def search_and_save_jobs(
    db: Session,
    query: str,
    location: str | None = None,
    max_results: int | None = 20,
) -> SearchAndSaveResponse:
    found_jobs = search_jobs(query, location, max_results)
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


def _search_provider(
    query: str,
    location: str | None = None,
    max_results: int | None = 20,
) -> list[JobFound]:
    logger.info("Calling job search provider")
    scraper = JobScraper()
    return scraper.search(query, max_results=max_results, location=location)


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


def _normalize_jobs(jobs: list[JobFound]) -> tuple[list[JobFound], list[str]]:
    valid_jobs = []
    skipped_reasons = []

    for job in jobs:
        normalized_job, skipped_reason = _normalize_job_found(job)
        if normalized_job is None:
            skipped_reasons.append(skipped_reason)
            continue
        valid_jobs.append(normalized_job)

    return valid_jobs, skipped_reasons


def _normalize_job_found(job_found: JobFound) -> tuple[JobFound | None, str]:
    title = _normalize_required_text(job_found.title)
    url = _normalize_required_text(job_found.url)

    if not title:
        return None, "missing title"
    if not url:
        return None, f"missing URL for title {title!r}"
    if not _is_valid_url(url):
        return None, f"invalid URL {url!r} for title {title!r}"

    return (
        JobFound(
            title=title,
            company=_normalize_optional_text(job_found.company),
            location=_normalize_optional_text(job_found.location),
            url=url,
            portal=_normalize_optional_text(job_found.portal) or "",
            remote=job_found.remote,
            stack=job_found.stack or [],
            snippet=_normalize_optional_text(job_found.snippet),
        ),
        "",
    )


def _normalize_required_text(value: str | None) -> str:
    if not value:
        return ""
    return re.sub(r"\s+", " ", value.strip())


def _normalize_optional_text(value: str | None) -> str | None:
    normalized = _normalize_required_text(value)
    return normalized or None


def _is_valid_url(url: str) -> bool:
    parsed_url = urlparse(url)
    return parsed_url.scheme in {"http", "https"} and bool(parsed_url.netloc)
