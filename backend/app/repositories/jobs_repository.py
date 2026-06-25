from datetime import datetime

from sqlalchemy.orm import Session

from app.models.job import Job


def get_all(db: Session):
    """Obtener todas las ofertas laborales."""
    return db.query(Job).all()


def get_by_id(db: Session, job_id: int):
    """Obtener una oferta laboral por ID."""
    return db.query(Job).filter(Job.id == job_id).first()


def get_by_url(db: Session, url: str):
    """Obtener una oferta laboral por URL."""
    return db.query(Job).filter(Job.url == url).first()


def create(db: Session, job_data: dict):
    """Crear una nueva oferta laboral."""
    db_job = Job(
        title=job_data["title"],
        url=job_data["url"],
        company=job_data.get("company"),
        location=job_data.get("location"),
        remote=job_data.get("remote", False),
        portal=job_data.get("portal"),
        stack=job_data.get("stack"),
        match_score=job_data.get("match_score", 0),
        status=job_data.get("status", "saved"),
        notes=job_data.get("notes"),
    )
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def update(db: Session, db_job: Job, update_data: dict):
    """Actualizar una oferta laboral."""
    update_data["updated_at"] = datetime.utcnow()

    for field, value in update_data.items():
        setattr(db_job, field, value)

    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def delete(db: Session, db_job: Job):
    """Eliminar una oferta laboral."""
    db.delete(db_job)
    db.commit()
