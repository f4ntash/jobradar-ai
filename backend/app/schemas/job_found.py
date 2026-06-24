from dataclasses import dataclass
from typing import Optional


@dataclass
class JobFound:
    """Modelo para resultados de búsqueda de ofertas laborales"""
    title: str
    company: Optional[str] = None
    url: str = ""
    portal: str = ""
    location: Optional[str] = None
    remote: bool = False
    stack: list[str] = None
    snippet: Optional[str] = None

    def __post_init__(self):
        if self.stack is None:
            self.stack = []
