from app.schemas.job_found import JobFound
from app.services.getonboard_provider import GetOnBoardProvider
from app.services.remotive_provider import RemotiveProvider


class JobScraper:
    """Job search provider wrapper.

    Get on Board is the primary LATAM-focused provider.
    Remotive is kept as a fallback when the primary provider has no results.
    """

    def search(
        self,
        query: str,
        max_results: int | None = 20,
        location: str | None = None,
    ) -> list[JobFound]:
        primary_provider = GetOnBoardProvider()
        primary_jobs = primary_provider.search(
            query,
            max_results=max_results,
            location=location,
        )
        if primary_jobs:
            return primary_jobs

        fallback_provider = RemotiveProvider()
        return fallback_provider.search(
            query,
            max_results=max_results,
            location=location,
        )
