import re
from html import unescape
import logging

import requests

from app.schemas.job_found import JobFound


logger = logging.getLogger(__name__)


LATAM_FRIENDLY_TERMS = (
    "argentina",
    "latin america",
    "latam",
    "south america",
    "americas",
    "worldwide",
    "global",
    "remote",
)

EXCLUDED_MARKET_TERMS = (
    "us only",
    "united states only",
    "usa only",
    "canada only",
    "europe only",
    "uk only",
    "united kingdom only",
)

TECH_RELATED_TERMS = {
    "react": (
        "react",
        "frontend",
        "front-end",
        "front end",
        "javascript",
        "typescript",
        "web developer",
    ),
}

TECH_ROLE_TERMS = (
    "developer",
    "engineer",
    "software",
    "frontend",
    "front-end",
    "front end",
    "backend",
    "fullstack",
    "full-stack",
    "web",
    "programmer",
)

NON_DEVELOPER_ROLE_TERMS = (
    "quality assurance",
    "qa engineer",
    "quality engineer",
    "product management",
    "product manager",
    "product engineer",
    "marketing",
    "sales",
    "customer support",
    "data scientist",
    "data science",
    "support",
    "finance",
    "operations",
)


class RemotiveProvider:
    """Small adapter for the Remotive public jobs API."""

    API_URL = "https://remotive.com/api/remote-jobs"
    SOURCE_NAME = "Remotive"

    def search(
        self,
        query: str,
        max_results: int | None = 20,
        location: str | None = None,
    ) -> list[JobFound]:
        result_limit = max_results or 20
        response = requests.get(
            self.API_URL,
            params={"search": query, "limit": result_limit},
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        raw_jobs = data.get("jobs", [])

        jobs = []
        skipped_by_region = 0
        skipped_by_relevance = 0
        for raw_job in raw_jobs:
            if not _matches_market(raw_job, location):
                skipped_by_region += 1
                continue
            if not _matches_relevance(raw_job, query):
                skipped_by_relevance += 1
                continue
            jobs.append(_to_job_found(raw_job))

        logger.debug(
            "Remotive search filters: raw=%s kept=%s skipped_by_region=%s skipped_by_relevance=%s",
            len(raw_jobs),
            len(jobs),
            skipped_by_region,
            skipped_by_relevance,
        )
        return jobs[:result_limit]


def _to_job_found(raw_job: dict) -> JobFound:
    return JobFound(
        title=raw_job.get("title", ""),
        company=raw_job.get("company_name"),
        location=raw_job.get("candidate_required_location"),
        url=raw_job.get("url", ""),
        portal=RemotiveProvider.SOURCE_NAME,
        remote=True,
        stack=raw_job.get("tags") or [],
        snippet=_clean_html(raw_job.get("description", ""))[:300],
    )


def _matches_market(raw_job: dict, location: str | None) -> bool:
    market_text = _searchable_market_text(raw_job)
    candidate_location = str(raw_job.get("candidate_required_location") or "").lower()
    if any(term in market_text for term in EXCLUDED_MARKET_TERMS):
        return False

    if not location:
        return True

    requested_location = location.strip().lower()
    if requested_location and requested_location in candidate_location:
        return True

    if any(term in candidate_location for term in LATAM_FRIENDLY_TERMS):
        return True

    if candidate_location.strip():
        return False

    return any(term in market_text for term in LATAM_FRIENDLY_TERMS)


def _matches_relevance(raw_job: dict, query: str) -> bool:
    query_terms = _terms(query)
    if not query_terms:
        return True

    searchable_text = _searchable_relevance_text(raw_job)
    related_terms = _related_terms_for_query(query_terms)

    if _is_technical_query(query_terms):
        if _has_non_developer_role(raw_job):
            return False
        has_technical_context = any(term in searchable_text for term in TECH_ROLE_TERMS)
        if related_terms:
            has_related_tech_term = any(term in searchable_text for term in related_terms)
            return has_related_tech_term and has_technical_context
        has_query_tech_term = any(term in searchable_text for term in query_terms)
        return has_query_tech_term and has_technical_context

    if all(term in searchable_text for term in query_terms):
        return True

    return any(term in searchable_text for term in query_terms)


def _searchable_market_text(raw_job: dict) -> str:
    return " ".join(
        [
            str(raw_job.get("title", "")),
            str(raw_job.get("candidate_required_location", "")),
            " ".join(raw_job.get("tags") or []),
            _clean_html(raw_job.get("description", "")),
        ]
    ).lower()


def _searchable_relevance_text(raw_job: dict) -> str:
    return " ".join(
        [
            str(raw_job.get("title", "")),
            str(raw_job.get("category", "")),
            " ".join(raw_job.get("tags") or []),
            _clean_html(raw_job.get("description", "")),
        ]
    ).lower()


def _has_non_developer_role(raw_job: dict) -> bool:
    role_text = " ".join(
        [
            str(raw_job.get("title", "")),
            str(raw_job.get("category", "")),
        ]
    ).lower()
    return any(term in role_text for term in NON_DEVELOPER_ROLE_TERMS)


def _related_terms_for_query(query_terms: list[str]) -> tuple[str, ...]:
    related_terms = []
    for term in query_terms:
        related_terms.extend(TECH_RELATED_TERMS.get(term, ()))
    return tuple(related_terms)


def _is_technical_query(query_terms: list[str]) -> bool:
    return any(
        term in TECH_RELATED_TERMS or term in TECH_ROLE_TERMS
        for term in query_terms
    )


def _terms(value: str) -> list[str]:
    return [term for term in re.split(r"\s+", value.strip().lower()) if term]


def _clean_html(value: str) -> str:
    text = re.sub(r"<[^>]+>", " ", value or "")
    text = unescape(text)
    return re.sub(r"\s+", " ", text).strip()
