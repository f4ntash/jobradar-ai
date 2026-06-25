from sqlalchemy.orm import Session

from app.repositories import jobs_repository
from app.schemas.job import ALLOWED_JOB_STATUSES, JobCreate, JobUpdate


class JobNotFoundError(Exception):
    """Raised when a job does not exist."""


class DuplicateJobUrlError(Exception):
    """Raised when a job URL is already saved."""


class InvalidJobStatusError(Exception):
    """Raised when a job status is not allowed."""


def list_jobs(db: Session):
    return jobs_repository.get_all(db)


def get_job(db: Session, job_id: int):
    job = jobs_repository.get_by_id(db, job_id)
    if not job:
        raise JobNotFoundError(f"Job with ID {job_id} was not found")
    return job


def create_job(db: Session, job_data: JobCreate):
    status = job_data.status or "saved"
    _validate_status(status)
    if jobs_repository.get_by_url(db, job_data.url):
        raise DuplicateJobUrlError("This URL already exists in the database")

    create_data = job_data.model_dump()
    create_data["status"] = status
    create_data["remote"] = create_data.get("remote") or False
    create_data["match_score"] = create_data.get("match_score") or 0
    return jobs_repository.create(db, create_data)


def update_job(db: Session, job_id: int, job_data: JobUpdate):
    job = get_job(db, job_id)
    update_data = job_data.model_dump(exclude_unset=True)

    if "status" in update_data:
        _validate_status(update_data["status"])
    if _url_belongs_to_another_job(db, update_data.get("url"), job_id):
        raise DuplicateJobUrlError("This URL already exists in the database")

    return jobs_repository.update(db, job, update_data)


def delete_job(db: Session, job_id: int):
    job = get_job(db, job_id)
    jobs_repository.delete(db, job)


def _validate_status(status: str | None) -> None:
    if status not in ALLOWED_JOB_STATUSES:
        allowed = "\n".join(ALLOWED_JOB_STATUSES)
        raise InvalidJobStatusError(
            f"Invalid status '{status}'.\nAllowed statuses:\n{allowed}"
        )


def _url_belongs_to_another_job(db: Session, url: str | None, job_id: int) -> bool:
    if not url:
        return False
    existing_job = jobs_repository.get_by_url(db, url)
    return bool(existing_job and existing_job.id != job_id)
