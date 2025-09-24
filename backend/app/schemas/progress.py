from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProgressUpdate(BaseModel):
    progress_percentage: int


class ProgressResponse(BaseModel):
    id: int
    career_path_id: int
    skill_id: Optional[int]
    progress_percentage: int
    is_completed: bool
    started_at: Optional[datetime]
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True
