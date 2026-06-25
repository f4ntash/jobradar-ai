Hoy fue el Day 2 construyendo JobRadar AI.

Trabajé en: Added Get on Board as the primary LATAM-focused job search provider, improved normalized job search results, kept Remotive as a fallback provider, and tested the search flow with real developer queries.

El objetivo del día era: Improve the job search workflow by replacing the generic provider with a LATAM-focused search source so JobRadar AI can return more useful opportunities for Argentina and Latin America.

La parte más importante no fue solo avanzar, sino entender esto: I learned that choosing the right data source is a product decision, not only a technical one. A job search tool for LATAM developers needs providers that match the user's market, otherwise the backend can work technically but still be useless in practice.

También hubo algo que no salió perfecto: The first provider returned mostly US-focused jobs and some unrelated results, which made the search experience poor for a LATAM developer. I also noticed repeated results, which shows that the next step needs better duplicate handling and a usable frontend.

Tecnologías y herramientas usadas:
- Python, FastAPI, SQLAlchemy, SQLite, Pytest, HTTP requests, Git
- AI tools: ChatGPT, Codex
- Programas/tools: Visual Studio Code, Git, GitHub, Terminal, Swagger

Lo próximo: Push the backend changes, review the pull request, and then build a minimal frontend to search jobs, save opportunities, mark duplicates, and update application status more easily.

Estoy construyendo este proyecto en público, con foco en aprender bien, documentar el proceso y convertir JobRadar AI en un producto real para desarrolladores que buscan trabajo.

#BuildInPublic #Python #FastAPI #SoftwareDevelopment #OpenSource #JobSearch #LearningInPublic
