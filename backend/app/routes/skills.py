from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.database import get_db
from app.models.skill import Skill
from app.schemas.skill import SkillResponse

router = APIRouter(prefix="/api/v1/skills", tags=["skills"])

@router.get("", response_model=List[SkillResponse])
async def get_skills(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
):
    """Get all skills, optionally filtered by category"""
    query = select(Skill)
    if category:
        query = query.where(Skill.category == category)
    
    result = await db.execute(query)
    skills = result.scalars().all()
    return skills

@router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific skill by ID"""
    result = await db.execute(select(Skill).where(Skill.id == skill_id))
    skill = result.scalar_one_or_none()
    if not skill:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill
