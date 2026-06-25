from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job import JobCreate, JobResponse, JobUpdate
from app.services import job_service

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _service_error_to_http(error: Exception) -> HTTPException:
    if isinstance(error, job_service.JobNotFoundError):
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    if isinstance(error, job_service.DuplicateJobUrlError):
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return HTTPException(
        status_code=422,
        detail=str(error),
    )


@router.get("", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    """Obtener lista de todas las ofertas laborales."""
    return job_service.list_jobs(db)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Obtener una oferta laboral por ID."""
    try:
        return job_service.get_job(db, job_id)
    except job_service.JobNotFoundError as error:
        raise _service_error_to_http(error)


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Crear una nueva oferta laboral."""
    try:
        return job_service.create_job(db, job)
    except (
        job_service.DuplicateJobUrlError,
        job_service.InvalidJobStatusError,
    ) as error:
        raise _service_error_to_http(error)


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    """Actualizar una oferta laboral."""
    try:
        return job_service.update_job(db, job_id, job)
    except (
        job_service.JobNotFoundError,
        job_service.DuplicateJobUrlError,
        job_service.InvalidJobStatusError,
    ) as error:
        raise _service_error_to_http(error)


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Eliminar una oferta laboral."""
    try:
        job_service.delete_job(db, job_id)
    except job_service.JobNotFoundError as error:
        raise _service_error_to_http(error)
