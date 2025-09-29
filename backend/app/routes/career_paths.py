import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from app.database import get_db
from app.models.career_path import CareerPath, CareerPathSkill
from app.models.skill import Skill
from app.schemas.career_path import CareerPathResponse, CareerPathDetail, CareerPathCreate
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/career-paths", tags=["career-paths"])

@router.get("", response_model=List[CareerPathResponse])
async def get_career_paths(
    category: Optional[str] = Query(None, description="Filter by category"),
    db: AsyncSession = Depends(get_db)
):
    """Get all career paths, optionally filtered by category"""
    query = select(CareerPath)
    if category:
        query = query.where(CareerPath.category == category)

    result = await db.execute(query)
    career_paths = result.scalars().all()
    return career_paths

@router.get("/categories/list", response_model=List[str])
async def get_categories(db: AsyncSession = Depends(get_db)):
    """Get all available career path categories"""
    result = await db.execute(select(CareerPath.category).distinct())
    categories = [row[0] for row in result.all()]
    return categories

@router.get("/{path_id}", response_model=CareerPathDetail)
async def get_career_path(
    path_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get detailed information about a specific career path"""
    result = await db.execute(
        select(CareerPath)
        .options(selectinload(CareerPath.skills).selectinload(CareerPathSkill.skill))
        .where(CareerPath.id == path_id)
    )
    career_path = result.scalar_one_or_none()

    if not career_path:
        raise HTTPException(status_code=404, detail="Career path not found")

    # Build skills list
    skills_info = []
    for cp_skill in career_path.skills:
        skills_info.append({
            "id": cp_skill.skill.id,
            "name": cp_skill.skill.name,
            "description": cp_skill.skill.description,
            "level": cp_skill.skill.level.value if cp_skill.skill.level else "beginner"
        })

    # Parse learning_content from JSON string
    learning_content = None
    if career_path.learning_content:
        try:
            learning_content = json.loads(career_path.learning_content)
        except (json.JSONDecodeError, TypeError):
            learning_content = None

    return {
        **{c.name: getattr(career_path, c.name) for c in career_path.__table__.columns},
        "skills": skills_info,
        "learning_content": learning_content
    }
