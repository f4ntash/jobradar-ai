from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job import JobResponse
from app.schemas.job_ingestion import RawJobIngestion
from app.services import job_ingestion_service, job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _service_error_to_http(error: Exception) -> HTTPException:
    if isinstance(error, job_service.DuplicateJobUrlError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    if isinstance(error, job_service.InvalidJobStatusError):
        return HTTPException(status_code=422, detail=str(error))
    return HTTPException(status_code=500, detail="Unexpected job ingestion error")


@router.post("/ingest", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def ingest_job(raw_job: RawJobIngestion, db: Session = Depends(get_db)):
    """Create a saved job from manually provided raw job data."""
    try:
        return job_ingestion_service.ingest_job(db, raw_job)
    except (
        job_service.DuplicateJobUrlError,
        job_service.InvalidJobStatusError,
    ) as error:
        raise _service_error_to_http(error)
