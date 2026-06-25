# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project aims to follow [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Changed

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
