import logging
import re
from html import unescape

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
    "chile",
    "colombia",
    "mexico",
    "peru",
    "uruguay",
    "brazil",
)

EXCLUDED_MARKET_TERMS = (
    "us only",
    "united states only",
    "usa only",
    "usa, canada",
    "usa timezones",
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


class GetOnBoardProvider:
    """Adapter for Get on Board's public LATAM tech jobs API."""

    API_URL = "https://www.getonbrd.com/api/v0/search/jobs"
    SOURCE_NAME = "Get on Board"

    def search(
        self,
        query: str,
        max_results: int | None = 20,
        location: str | None = None,
    ) -> list[JobFound]:
        result_limit = max_results or 20
        response = requests.get(
            self.API_URL,
            params={
                "query": query,
                "remote": "true",
                "per_page": result_limit,
                "lang": "en",
                "expand[]": "company",
            },
            timeout=10,
        )
        response.raise_for_status()

        data = response.json()
        raw_jobs = data.get("data", [])

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
            "Get on Board provider metadata: provider=%s raw=%s normalized=%s skipped_by_region=%s skipped_by_relevance=%s",
            self.SOURCE_NAME,
            len(raw_jobs),
            len(jobs),
            skipped_by_region,
            skipped_by_relevance,
        )
        return jobs[:result_limit]


def _to_job_found(raw_job: dict) -> JobFound:
    attributes = raw_job.get("attributes", {})
    return JobFound(
        title=attributes.get("title", ""),
        company=_company_name(attributes),
        location=_location(attributes),
        url=(raw_job.get("links") or {}).get("public_url", ""),
        portal=GetOnBoardProvider.SOURCE_NAME,
        remote=bool(attributes.get("remote")),
        stack=_tags(attributes),
        snippet=_snippet(attributes),
    )


def _company_name(attributes: dict) -> str | None:
    company = attributes.get("company") or {}
    company_data = company.get("data") or {}
    company_attributes = company_data.get("attributes") or {}
    return company_attributes.get("name")


def _location(attributes: dict) -> str | None:
    countries = attributes.get("countries") or []
    if countries:
        return ", ".join(countries)
    return attributes.get("remote_zone") or attributes.get("remote_modality")


def _tags(attributes: dict) -> list[str]:
    tags = attributes.get("tags") or {}
    tag_data = tags.get("data") or []
    names = []
    for tag in tag_data:
        tag_attributes = tag.get("attributes") or {}
        name = tag_attributes.get("name")
        if name:
            names.append(name)
    return names


def _snippet(attributes: dict) -> str | None:
    text = " ".join(
        [
            _clean_html(attributes.get("description", "")),
            _clean_html(attributes.get("projects", "")),
            _clean_html(attributes.get("functions", "")),
        ]
    )
    normalized = re.sub(r"\s+", " ", text).strip()
    return normalized[:300] if normalized else None


def _matches_market(raw_job: dict, location: str | None) -> bool:
    if not location:
        return True

    attributes = raw_job.get("attributes", {})
    market_text = _market_text(attributes)
    if any(term in market_text for term in EXCLUDED_MARKET_TERMS):
        return False

    requested_location = location.strip().lower()
    if requested_location and requested_location in market_text:
        return True

    return any(term in market_text for term in LATAM_FRIENDLY_TERMS)


def _matches_relevance(raw_job: dict, query: str) -> bool:
    query_terms = _terms(query)
    if not query_terms:
        return True

    attributes = raw_job.get("attributes", {})
    searchable_text = _searchable_relevance_text(attributes)
    related_terms = _related_terms_for_query(query_terms)

    if _is_technical_query(query_terms):
        if _has_non_developer_role(attributes):
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


def _market_text(attributes: dict) -> str:
    return " ".join(
        [
            str(attributes.get("remote_zone", "")),
            str(attributes.get("remote_modality", "")),
            " ".join(attributes.get("countries") or []),
            _clean_html(attributes.get("description", "")),
            _clean_html(attributes.get("functions", "")),
        ]
    ).lower()


def _searchable_relevance_text(attributes: dict) -> str:
    return " ".join(
        [
            str(attributes.get("title", "")),
            str(attributes.get("category_name", "")),
            " ".join(_tags(attributes)),
            _clean_html(attributes.get("description", "")),
            _clean_html(attributes.get("projects", "")),
            _clean_html(attributes.get("functions", "")),
        ]
    ).lower()


def _has_non_developer_role(attributes: dict) -> bool:
    role_text = " ".join(
        [
            str(attributes.get("title", "")),
            str(attributes.get("category_name", "")),
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
