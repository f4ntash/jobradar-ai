import re

from sqlalchemy.orm import Session

from app.schemas.job import JobCreate
from app.schemas.job_ingestion import RawJobIngestion
from app.services import job_service


def ingest_job(db: Session, raw_job: RawJobIngestion):
    normalized_job = JobCreate(
        title=_normalize_text(raw_job.title),
        company=_normalize_optional_text(raw_job.company),
        location=_normalize_optional_text(raw_job.location),
        url=_normalize_text(raw_job.url),
    )
    return job_service.create_job(db, normalized_job)


def _normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip())


def _normalize_optional_text(value: str | None) -> str | None:
    if value is None:
        return None
    return _normalize_text(value)
