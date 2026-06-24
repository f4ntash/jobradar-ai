import re
from typing import Optional
import requests
from bs4 import BeautifulSoup
from app.schemas.job_found import JobFound


class JobScraper:
    """Servicio independiente para buscar ofertas laborales en múltiples portales"""

    GREENHOUSE_URL = "https://boards.greenhouse.io/embed/job_board/jobs"
    LEVER_URL = "https://api.lever.co/v0/postings/search"

    TECH_STACK = {
        "react": ["react", "reactjs"],
        "next.js": ["next.js", "nextjs", "next"],
        "react native": ["react native", "react-native"],
        "typescript": ["typescript", "ts"],
        "node.js": ["node.js", "nodejs", "node", "express"],
        "python": ["python"],
        "fastapi": ["fastapi"],
        "ai": ["ai", "artificial intelligence", "machine learning", "ml"],
        "llm": ["llm", "large language model", "gpt", "openai"],
    }

    def search(self, query: str, max_results: int = 20) -> list[JobFound]:
        """
        Busca ofertas laborales en múltiples portales.
        
        Args:
            query: Término de búsqueda
            max_results: Número máximo de resultados
            
        Returns:
            Lista de JobFound sin duplicados
        """
        results = []

        # Buscar en cada portal
        results.extend(self._search_greenhouse(query, max_results))
        results.extend(self._search_lever(query, max_results))

        # Limpiar y deduplicar
        results = self._clean_results(results)
        results = self._remove_duplicates(results)

        return results[:max_results]

    def _search_greenhouse(self, query: str, max_results: int) -> list[JobFound]:
        """Buscar en portales Greenhouse"""
        results = []
        try:
            # Buscar boards públicos de Greenhouse (simulado)
            # En producción, se consultarían boards específicos de empresas
            search_url = f"{self.GREENHOUSE_URL}?search={query}"

            response = requests.get(search_url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                jobs = soup.select(".opening")[:max_results]

                for job in jobs:
                    title_elem = job.select_one(".opening__title")
                    company_elem = job.select_one(".opening__company")
                    url_elem = job.select_one("a")

                    if title_elem and url_elem:
                        job_found = JobFound(
                            title=title_elem.get_text(strip=True),
                            company=company_elem.get_text(
                                strip=True
                            ) if company_elem else None,
                            url=url_elem.get("href", ""),
                            portal="Greenhouse",
                            snippet=None,
                        )
                        results.append(job_found)
        except Exception:
            pass

        return results

    def _search_lever(self, query: str, max_results: int) -> list[JobFound]:
        """Buscar en portales Lever"""
        results = []
        try:
            # Lever API para búsqueda públicas
            params = {"search": query}
            response = requests.get(self.LEVER_URL, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                postings = data.get("postings", [])[:max_results]

                for posting in postings:
                    job_found = JobFound(
                        title=posting.get("title", ""),
                        company=posting.get("company", {}).get("name"),
                        url=posting.get("hostedUrl", ""),
                        portal="Lever",
                        location=self._extract_location(
                            posting.get("locations", [])
                        ),
                        snippet=posting.get("text", "")[:200],
                    )
                    results.append(job_found)
        except Exception:
            pass

        return results

    def _clean_results(self, jobs: list[JobFound]) -> list[JobFound]:
        """Procesar y enriquecer cada job encontrado"""
        for job in jobs:
            job.stack = self._detect_stack(job.title, job.snippet)
            job.remote = self._detect_remote(
                job.title, job.location, job.snippet
            )

        return jobs

    def _remove_duplicates(self, jobs: list[JobFound]) -> list[JobFound]:
        """Remover jobs duplicados por URL"""
        seen = set()
        unique = []

        for job in jobs:
            if job.url and job.url not in seen:
                seen.add(job.url)
                unique.append(job)

        return unique

    def _detect_stack(self, title: str, snippet: Optional[str] = None) -> list[str]:
        """Detectar tecnologías mencionadas"""
        text = f"{title} {snippet or ''}".lower()
        detected = []

        for tech, keywords in self.TECH_STACK.items():
            if any(keyword in text for keyword in keywords):
                detected.append(tech)

        return list(set(detected))

    def _detect_remote(
        self, title: str, location: Optional[str], snippet: Optional[str]
    ) -> bool:
        """Detectar si el trabajo es remoto"""
        text = f"{title} {location or ''} {snippet or ''}".lower()
        remote_keywords = [
            "remote",
            "work from home",
            "wfh",
            "distributed",
            "anywhere",
        ]

        return any(keyword in text for keyword in remote_keywords)

    def _extract_location(self, locations: list[dict]) -> Optional[str]:
        """Extraer ubicación desde lista de diccionarios"""
        if locations:
            loc = locations[0]
            return f"{loc.get('city', '')}, {loc.get('country', '')}".strip(
                ", "
            )
        return None
