from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.job import SearchAndSaveResponse, SearchRequest
from app.schemas.job_found import JobFound
from app.services import job_search_service

router = APIRouter(prefix="/jobs", tags=["job-search"])


def _search_error_to_http(error: Exception) -> HTTPException:
    if isinstance(error, job_search_service.SearchProviderError):
        return HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=str(error),
        )
    return HTTPException(status_code=500, detail="Unexpected job search error")


@router.get("/search", response_model=list[JobFound])
def search_jobs(
    query: str = Query(...),
    location: str | None = None,
):
    """Buscar ofertas laborales y devolver resultados normalizados."""
    try:
        return job_search_service.search_jobs(query, location)
    except job_search_service.SearchProviderError as error:
        raise _search_error_to_http(error)


@router.post("/search", response_model=list[JobFound])
def search_jobs_legacy(search_request: SearchRequest):
    """Buscar ofertas laborales en multiples portales."""
    try:
        return job_search_service.search_jobs(
            search_request.query,
            search_request.location,
            search_request.max_results,
        )
    except job_search_service.SearchProviderError as error:
        raise _search_error_to_http(error)


@router.post("/search-and-save", response_model=SearchAndSaveResponse)
def search_and_save_jobs(
    search_request: SearchRequest,
    db: Session = Depends(get_db),
):
    """Buscar ofertas y guardar las nuevas en la base de datos."""
    try:
        return job_search_service.search_and_save_jobs(
            db,
            search_request.query,
            search_request.location,
            search_request.max_results,
        )
    except job_search_service.SearchProviderError as error:
        raise _search_error_to_http(error)
