from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.progress import UserProgress
from app.models.user import User
from app.auth import get_current_user
from app.schemas.progress import ProgressResponse, ProgressUpdate

router = APIRouter(prefix="/api/v1/progress", tags=["progress"])

@router.get("", response_model=List[ProgressResponse])
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's progress across all career paths"""
    result = await db.execute(
        select(UserProgress).where(UserProgress.user_id == current_user.id)
    )
    progress_items = result.scalars().all()
    return progress_items

@router.post("/career-path/{career_path_id}")
async def update_career_path_progress(
    career_path_id: int,
    data: ProgressUpdate = Body(...),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update or create progress for a career path"""
    result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == current_user.id,
            UserProgress.career_path_id == career_path_id
        )
    )
    progress = result.scalar_one_or_none()

    pct = min(100, max(0, data.progress_percentage))

    if progress:
        progress.progress_percentage = pct
        progress.is_completed = pct == 100
        if progress.is_completed and not progress.completed_at:
            from datetime import datetime
            progress.completed_at = datetime.utcnow()
    else:
        progress = UserProgress(
            user_id=current_user.id,
            career_path_id=career_path_id,
            progress_percentage=pct,
            is_completed=pct == 100
        )
        db.add(progress)

    await db.commit()
    await db.refresh(progress)

    return {
        "id": progress.id,
        "career_path_id": progress.career_path_id,
        "progress_percentage": progress.progress_percentage,
        "is_completed": progress.is_completed
    }
