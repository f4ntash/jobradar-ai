# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

- Replaced Remotive as the primary search provider with Get on Board's public LATAM tech jobs API.
- Moved Remotive to fallback status when the primary provider returns no results.
- Added internal provider metadata for Get on Board result counts and skipped results.
- Improved Remotive search filtering for LATAM-friendly remote developer roles.
- Added simple technical relevance filtering for developer searches such as `React Developer`.
- Excluded clearly region-restricted jobs such as US-only, Canada-only, Europe-only, and UK-only roles from LATAM searches.
- Replaced the placeholder job search provider with a Remotive public API provider.
- Added internal search tracing for query, location, provider calls, raw result count, normalized result count, skipped result count, and skipped-result reasons.
- Improved the existing job search workflow with normalized results and clear provider error handling.
- Updated search-and-save to skip invalid search results and save jobs through the existing Jobs service.
- Stabilized the Jobs domain boundaries across model, schemas, repository, service, and router.
- Centralized default job status usage in the Jobs schema/service layer.
- Clarified Jobs documentation around default status, duplicate URLs, missing jobs, and invalid statuses.
- Refactored the developer workflow into the modular DevOS CLI.
- Improved Git safety prompts for branch creation, staging, committing, merging, and pushing.
- Refactored the Jobs feature to use a service layer between routers and repositories.
- Isolated job search routes and search orchestration from saved-job CRUD routes.
- Renamed Jobs repository operations around focused database access.
- Changed default job status from `pending` to `saved`.
- Removed empty duplicate modules from the root of `app/`.

### Added

- Added Get on Board provider tests with mocked HTTP responses.
- Added a fallback dominance test to ensure Remotive does not override primary provider results.
- Added tests for LATAM-friendly job inclusion, region-restricted job exclusion, developer relevance filtering, and filtered search-and-save behavior.
- Added Remotive provider tests with mocked HTTP responses.
- Added a job search test for providers that return no jobs.
- Added `GET /jobs/search` with `query` and optional `location` parameters.
- Added job search tests using mocked provider results.
- Added `POST /jobs/ingest` for controlled manual job ingestion.
- Added manual ingestion normalization for simple string values.
- Added Jobs ingestion tests for creation, trimming, repeated-space normalization, default status, duplicate URL rejection, and missing required fields.
- Added Jobs API tests for create-time invalid status and valid non-default status.
- Added Dev Journal Markdown generation through DevOS.
- Added LinkedIn draft generation through DevOS.
- Added static Dev Journal website generation through DevOS.
- Added allowed job statuses: `saved`, `applied`, `interview`, `rejected`, and `offer`.
- Added basic Jobs API tests for create, duplicate URL rejection, get by ID, status update, and invalid status rejection.

## [0.1.0] - 2026-06-24

### Added

- Initialized project documentation.
- Added project vision.
- Added product documentation.
- Added architecture overview.
- Added roadmap through v1.0.
- Added architecture decision record document.
- Added AI contributor context.
- Added GitHub Copilot engineering instructions.
