from pydantic import BaseModel
from typing import Optional, List, Dict

class QuestionCreate(BaseModel):
    question_text: str
    question_type: str
    options: Optional[Dict] = None
    correct_answer: str
    points: int = 1

class AssessmentCreate(BaseModel):
    title: str
    description: Optional[str] = None
    career_path_id: int
    time_limit: Optional[int] = None
    questions: List[QuestionCreate] = []

class AssessmentResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    career_path_id: int
    time_limit: Optional[int]
    
    class Config:
        from_attributes = True

class UserAssessmentSubmit(BaseModel):
    assessment_id: int
    answers: Dict[str, str]  # question_id: answer
