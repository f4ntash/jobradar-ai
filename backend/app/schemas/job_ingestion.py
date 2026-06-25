from pydantic import BaseModel
from typing import Optional


class RawJobIngestion(BaseModel):
    title: str
    url: str
    company: Optional[str] = None
    location: Optional[str] = None
