from pydantic import BaseModel
from typing import Optional

class SkillCreate(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None
    level: str = "beginner"

class SkillResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    category: Optional[str]
    level: str
    
    class Config:
        from_attributes = True
