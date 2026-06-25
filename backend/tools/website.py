"""Static HTML generation for the developer journal."""

from __future__ import annotations

import html
import re
from pathlib import Path

from utils import DAILY_DIR, JOURNAL_INDEX


def section_value(text: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(.*?)(?=\n## |\Z)"
    match = re.search(pattern, text, flags=re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def parse_daily_file(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    title = text.splitlines()[0].removeprefix("# ").strip()
    day_match = re.search(r"Day\s+(\d+)", title, flags=re.IGNORECASE)
    day = day_match.group(1) if day_match else "0"
    slug = title.split(" - ", 1)[1] if " - " in title else path.stem

    return {
        "day": day,
        "slug": slug,
        "goal": section_value(text, "Goal"),
        "learnings": section_value(text, "Learnings"),
        "technologies": section_value(text, "Technologies used"),
        "ai_tools": section_value(text, "AI tools used"),
        "commit": section_value(text, "Commit"),
    }


def render_journal_item(item: dict[str, str]) -> str:
    return f"""<article>
  <h2>Day {html.escape(item["day"])} - {html.escape(item["slug"])}</h2>
  <p><strong>Goal:</strong> {html.escape(item["goal"])}</p>
  <p><strong>Learnings:</strong> {html.escape(item["learnings"])}</p>
  <p><strong>Technologies:</strong> {html.escape(item["technologies"])}</p>
  <p><strong>AI tools:</strong> {html.escape(item["ai_tools"])}</p>
  <p><strong>Commit:</strong> <code>{html.escape(item["commit"])}</code></p>
</article>"""


def build_index_html(items: list[dict[str, str]]) -> str:
    body = "\n".join(render_journal_item(item) for item in items)
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>JobRadar AI Dev Journal</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 2rem; line-height: 1.5; }}
    main {{ max-width: 860px; margin: 0 auto; }}
    article {{ border-bottom: 1px solid #ddd; padding: 1rem 0; }}
    code {{ background: #f4f4f4; padding: 0.1rem 0.3rem; }}
  </style>
</head>
<body>
  <main>
    <h1>JobRadar AI Dev Journal</h1>
    {body}
  </main>
</body>
</html>
"""


def update_journal_index() -> Path:
    JOURNAL_INDEX.parent.mkdir(parents=True, exist_ok=True)

    items = [parse_daily_file(path) for path in DAILY_DIR.glob("*.md")]
    items.sort(key=lambda item: int(item["day"]))

    JOURNAL_INDEX.write_text(build_index_html(items), encoding="utf-8")
    return JOURNAL_INDEX
