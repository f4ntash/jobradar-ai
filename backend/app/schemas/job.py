from pydantic import BaseModel, ConfigDict
from typing import Literal, Optional
from datetime import datetime


JobStatus = Literal["saved", "applied", "interview", "rejected", "offer"]
ALLOWED_JOB_STATUSES = ("saved", "applied", "interview", "rejected", "offer")
DEFAULT_JOB_STATUS = "saved"


class JobCreate(BaseModel):
    title: str
    url: str
    company: Optional[str] = None
    location: Optional[str] = None
    remote: Optional[bool] = None
    portal: Optional[str] = None
    stack: Optional[str] = None
    match_score: Optional[int] = None
    status: Optional[str] = DEFAULT_JOB_STATUS
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
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    company: Optional[str] = None
    location: Optional[str] = None
    remote: bool
    url: str
    portal: Optional[str] = None
    stack: Optional[str] = None
    match_score: int
    status: JobStatus
    notes: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class SearchRequest(BaseModel):
    query: str
    location: Optional[str] = None
    max_results: Optional[int] = 20


class SearchAndSaveResponse(BaseModel):
    found: int
    created: int
    duplicates: int
    jobs: list[JobResponse]
