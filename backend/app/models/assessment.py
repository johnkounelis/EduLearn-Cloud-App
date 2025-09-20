from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    time_limit = Column(Integer, nullable=True)  # minutes
    
    # Relationships
    career_path = relationship("CareerPath", back_populates="assessments")
    questions = relationship("AssessmentQuestion", back_populates="assessment")
    user_assessments = relationship("UserAssessment", back_populates="assessment")

class AssessmentQuestion(Base):
    __tablename__ = "assessment_questions"
    
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # "multiple_choice", "true_false", "text"
    options = Column(Text, nullable=True)  # JSON string for multiple choice options
    correct_answer = Column(Text, nullable=False)
    points = Column(Integer, default=1)
    
    # Relationships
    assessment = relationship("Assessment", back_populates="questions")

class UserAssessment(Base):
    __tablename__ = "user_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    assessment_id = Column(Integer, ForeignKey("assessments.id"), nullable=False)
    score = Column(Integer, nullable=True)
    max_score = Column(Integer, nullable=True)
    percentage = Column(Integer, nullable=True)
    completed_at = Column(DateTime(timezone=True), server_default=func.now())
    answers = Column(Text, nullable=True)  # JSON string with user answers
    
    # Relationships
    user = relationship("User", back_populates="assessments")
    assessment = relationship("Assessment", back_populates="user_assessments")
