"""Daily developer journal generation."""

from __future__ import annotations

from pathlib import Path

from utils import DAILY_DIR, slugify


def daily_markdown(data: dict[str, str], commit: str) -> str:
    return f"""# Day {data["day"]} - {data["slug"]}

## Goal
{data["goal"]}

## Changes
{data["changes"]}

## What went wrong
{data["went_wrong"]}

## Learnings
{data["learnings"]}

## Technologies used
{data["technologies"]}

## AI tools used
{data["ai_tools"]}

## Programs/tools used
{data["programs"]}

## Commit
{commit}

## Next step
{data["next_step"]}
"""


def save_daily_journal(data: dict[str, str], commit: str) -> Path:
    safe_slug = slugify(data["slug"])
    data["slug"] = safe_slug
    file_name = f"{data['day']}-{safe_slug}.md"

    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    path = DAILY_DIR / file_name
    path.write_text(daily_markdown(data, commit), encoding="utf-8")
    return path
