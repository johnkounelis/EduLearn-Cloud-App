from pydantic import BaseModel
from typing import Optional, List, Any

class SkillInfo(BaseModel):
    id: int
    name: str
    description: Optional[str]
    level: str

class CareerPathResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    category: str
    estimated_time: Optional[str]
    difficulty: Optional[str]
    
    class Config:
        from_attributes = True

class CareerPathDetail(CareerPathResponse):
    job_market_info: Optional[str]
    salary_range: Optional[str]
    skills: List[SkillInfo] = []
    learning_content: Optional[Any] = None

class CareerPathCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    estimated_time: Optional[str] = None
    difficulty: Optional[str] = None
    job_market_info: Optional[str] = None
    salary_range: Optional[str] = None
