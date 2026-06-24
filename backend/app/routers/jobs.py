from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.job import (
    JobCreate,
    JobUpdate,
    JobResponse,
    SearchRequest,
    SearchAndSaveResponse,
)
from app.schemas.job_found import JobFound
from app.repositories import jobs_repository
from app.services.job_scraper import JobScraper

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobResponse])
def list_jobs(db: Session = Depends(get_db)):
    """Obtener lista de todas las ofertas laborales"""
    return jobs_repository.get_jobs(db)


@router.get("/{job_id}", response_model=JobResponse)
def get_job(job_id: int, db: Session = Depends(get_db)):
    """Obtener una oferta laboral por ID"""
    db_job = jobs_repository.get_job_by_id(db, job_id)
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oferta laboral con ID {job_id} no encontrada",
        )
    return db_job


@router.post("", response_model=JobResponse, status_code=status.HTTP_201_CREATED)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    """Crear una nueva oferta laboral"""
    # Verificar si la URL ya existe
    existing_job = jobs_repository.get_job_by_url(db, job.url)
    if existing_job:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta URL ya existe en la base de datos",
        )
    return jobs_repository.create_job(db, job)


@router.post("/search", response_model=list[JobFound])
def search_jobs(search_request: SearchRequest):
    """Buscar ofertas laborales en múltiples portales"""
    scraper = JobScraper()
    return scraper.search(search_request.query, search_request.max_results)


@router.post("/search-and-save", response_model=SearchAndSaveResponse)
def search_and_save_jobs(
    search_request: SearchRequest, db: Session = Depends(get_db)
):
    """Buscar ofertas y guardar las nuevas en la base de datos"""
    scraper = JobScraper()
    found_jobs = scraper.search(search_request.query, search_request.max_results)

    created_jobs = []
    duplicates_count = 0

    for job_found in found_jobs:
        # Verificar si ya existe por URL
        existing_job = jobs_repository.get_job_by_url(db, job_found.url)
        if existing_job:
            duplicates_count += 1
            continue

        # Convertir a JobCreate
        job_create = _convert_job_found_to_create(job_found)

        # Guardar en BD
        created_job = jobs_repository.create_job(db, job_create)
        created_jobs.append(created_job)

    return SearchAndSaveResponse(
        found=len(found_jobs),
        created=len(created_jobs),
        duplicates=duplicates_count,
        jobs=created_jobs,
    )


@router.patch("/{job_id}", response_model=JobResponse)
def update_job(job_id: int, job: JobUpdate, db: Session = Depends(get_db)):
    """Actualizar una oferta laboral"""
    db_job = jobs_repository.update_job(db, job_id, job)
    if not db_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oferta laboral con ID {job_id} no encontrada",
        )
    return db_job


@router.delete("/{job_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    """Eliminar una oferta laboral"""
    success = jobs_repository.delete_job(db, job_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oferta laboral con ID {job_id} no encontrada",
        )


def _convert_job_found_to_create(job_found: JobFound) -> JobCreate:
    """Convertir JobFound (resultado de búsqueda) a JobCreate (para guardar)"""
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
        status="pending",
        notes=job_found.snippet,
    )
