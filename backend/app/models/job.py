from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.core.database import Base
from datetime import datetime


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=True)
    location = Column(String, nullable=True)
    remote = Column(Boolean, default=False)
    url = Column(String, nullable=False, unique=True, index=True)
    portal = Column(String, nullable=True)
    stack = Column(String, nullable=True)
    match_score = Column(Integer, default=0)
    status = Column(String, default="saved")
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=True)
