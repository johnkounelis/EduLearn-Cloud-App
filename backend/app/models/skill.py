from sqlalchemy import Column, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class SkillLevel(str, enum.Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Skill(Base):
    __tablename__ = "skills"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    category = Column(String, nullable=True)  # e.g., "Programming", "DevOps", "Cloud"
    level = Column(Enum(SkillLevel), default=SkillLevel.BEGINNER)
    
    # Relationships
    career_path_skills = relationship("CareerPathSkill", back_populates="skill")
