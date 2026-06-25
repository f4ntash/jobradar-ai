# Day 2 - latam-job-search-provider

## Goal
Improve the job search workflow by replacing the generic provider with a LATAM-focused search source so JobRadar AI can return more useful opportunities for Argentina and Latin America.

## Changes
Added Get on Board as the primary LATAM-focused job search provider, improved normalized job search results, kept Remotive as a fallback provider, and tested the search flow with real developer queries.

## What went wrong
The first provider returned mostly US-focused jobs and some unrelated results, which made the search experience poor for a LATAM developer. I also noticed repeated results, which shows that the next step needs better duplicate handling and a usable frontend.

## Learnings
I learned that choosing the right data source is a product decision, not only a technical one. A job search tool for LATAM developers needs providers that match the user's market, otherwise the backend can work technically but still be useless in practice.

## Technologies used
Python, FastAPI, SQLAlchemy, SQLite, Pytest, HTTP requests, Git

## AI tools used
ChatGPT, Codex

## Programs/tools used
Visual Studio Code, Git, GitHub, Terminal, Swagger

## Commit
feat(jobs): add latam-focused job provider

## Next step
Push the backend changes, review the pull request, and then build a minimal frontend to search jobs, save opportunities, mark duplicates, and update application status more easily.
