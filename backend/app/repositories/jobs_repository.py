from sqlalchemy.orm import Session
from app.models.job import Job
from app.schemas.job import JobCreate, JobUpdate
from datetime import datetime


def get_jobs(db: Session):
    """Obtener todas las ofertas laborales"""
    return db.query(Job).all()


def get_job_by_id(db: Session, job_id: int):
    """Obtener una oferta laboral por ID"""
    return db.query(Job).filter(Job.id == job_id).first()


def get_job_by_url(db: Session, url: str):
    """Obtener una oferta laboral por URL"""
    return db.query(Job).filter(Job.url == url).first()


def create_job(db: Session, job_data: JobCreate):
    """Crear una nueva oferta laboral"""
    db_job = Job(
        title=job_data.title,
        url=job_data.url,
        company=job_data.company,
        location=job_data.location,
        remote=job_data.remote if job_data.remote is not None else False,
        portal=job_data.portal,
        stack=job_data.stack,
        match_score=job_data.match_score if job_data.match_score is not None else 0,
        status=job_data.status if job_data.status is not None else "pending",
        notes=job_data.notes,
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update_job(db: Session, job_id: int, job_data: JobUpdate):
    """Actualizar una oferta laboral"""
    db_job = get_job_by_id(db, job_id)
    if not db_job:
        return None

    update_data = job_data.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_job, field, value)

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def delete_job(db: Session, job_id: int):
    """Eliminar una oferta laboral"""
    db_job = get_job_by_id(db, job_id)
    if not db_job:
        return False

    db.delete(db_job)
    db.commit()
    return True
