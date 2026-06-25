"""LinkedIn draft generation for JobRadar AI."""

from __future__ import annotations

from pathlib import Path

from utils import LINKEDIN_DIR, slugify


def linkedin_markdown(data: dict[str, str]) -> str:
    return f"""Hoy fue el Day {data["day"]} construyendo JobRadar AI.

Trabaje en: {data["changes"]}

El objetivo del dia era: {data["goal"]}

La parte mas importante no fue solo avanzar, sino entender esto: {data["learnings"]}

Tambien hubo algo que no salio perfecto: {data["went_wrong"]}

Tecnologias y herramientas usadas:
- {data["technologies"]}
- AI tools: {data["ai_tools"]}
- Programas/tools: {data["programs"]}

Lo proximo: {data["next_step"]}

Estoy construyendo este proyecto en publico, con foco en aprender bien, documentar el proceso y convertir JobRadar AI en un producto real para desarrolladores que buscan trabajo.

#BuildInPublic #Python #FastAPI #SoftwareDevelopment #OpenSource #JobSearch #LearningInPublic
"""


def save_linkedin_draft(data: dict[str, str]) -> Path:
    safe_slug = slugify(data["slug"])
    file_name = f"{data['day']}-{safe_slug}.md"

    LINKEDIN_DIR.mkdir(parents=True, exist_ok=True)
    path = LINKEDIN_DIR / file_name
    path.write_text(linkedin_markdown(data), encoding="utf-8")
    return path
