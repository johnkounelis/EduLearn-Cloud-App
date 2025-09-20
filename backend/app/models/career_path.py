from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class CareerPath(Base):
    __tablename__ = "career_paths"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=False)  # "Cloud", "DevOps", "Software Development", etc.
    estimated_time = Column(String, nullable=True)  # e.g., "6-12 months"
    difficulty = Column(String, nullable=True)  # "Beginner", "Intermediate", "Advanced"
    job_market_info = Column(Text, nullable=True)
    salary_range = Column(String, nullable=True)
    learning_content = Column(Text, nullable=True)  # JSON string with structured learning content

    # Relationships
    skills = relationship("CareerPathSkill", back_populates="career_path")
    assessments = relationship("Assessment", back_populates="career_path")

class CareerPathSkill(Base):
    __tablename__ = "career_path_skills"
    
    id = Column(Integer, primary_key=True, index=True)
    career_path_id = Column(Integer, ForeignKey("career_paths.id"), nullable=False)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    is_required = Column(Boolean, default=True)
    priority = Column(Integer, default=0)  # Order/priority of skills
    
    # Relationships
    career_path = relationship("CareerPath", back_populates="skills")
    skill = relationship("Skill", back_populates="career_path_skills")
