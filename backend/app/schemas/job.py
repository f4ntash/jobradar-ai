from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class JobCreate(BaseModel):
    title: str
    url: str
    company: Optional[str] = None
    location: Optional[str] = None
    remote: Optional[bool] = None
    portal: Optional[str] = None
    stack: Optional[str] = None
    match_score: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class JobUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    remote: Optional[bool] = None
    url: Optional[str] = None
    portal: Optional[str] = None
    stack: Optional[str] = None
    match_score: Optional[int] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class JobResponse(BaseModel):
    id: int
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    remote: bool
    url: str
    portal: Optional[str] = None
    stack: Optional[str] = None
    match_score: int
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 20


class SearchAndSaveResponse(BaseModel):
    found: int
    created: int
    duplicates: int
    jobs: list[JobResponse]
