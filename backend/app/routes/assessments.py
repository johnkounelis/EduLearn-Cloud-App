from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List
import json
from app.database import get_db
from app.models.assessment import Assessment, AssessmentQuestion, UserAssessment
from app.schemas.assessment import AssessmentResponse, UserAssessmentSubmit
from app.models.user import User
from app.auth import get_current_user

router = APIRouter(prefix="/api/v1/assessments", tags=["assessments"])

@router.get("/career-path/{career_path_id}", response_model=List[AssessmentResponse])
async def get_assessments_by_career_path(
    career_path_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get all assessments for a specific career path"""
    result = await db.execute(
        select(Assessment).where(Assessment.career_path_id == career_path_id)
    )
    assessments = result.scalars().all()
    return assessments

@router.get("/{assessment_id}", response_model=dict)
async def get_assessment(
    assessment_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Get assessment details with questions"""
    result = await db.execute(
        select(Assessment)
        .options(selectinload(Assessment.questions))
        .where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    questions = []
    for q in assessment.questions:
        question_data = {
            "id": q.id,
            "question_text": q.question_text,
            "question_type": q.question_type,
            "points": q.points
        }
        if q.options:
            try:
                question_data["options"] = json.loads(q.options)
            except:
                question_data["options"] = q.options
        questions.append(question_data)
    
    return {
        "id": assessment.id,
        "title": assessment.title,
        "description": assessment.description,
        "career_path_id": assessment.career_path_id,
        "time_limit": assessment.time_limit,
        "questions": questions
    }

@router.post("/{assessment_id}/submit")
async def submit_assessment(
    assessment_id: int,
    submission: UserAssessmentSubmit,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Submit assessment answers and get score"""
    # Get assessment with questions
    result = await db.execute(
        select(Assessment)
        .options(selectinload(Assessment.questions))
        .where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(status_code=404, detail="Assessment not found")
    
    # Calculate score
    total_score = 0
    max_score = 0
    
    for question in assessment.questions:
        max_score += question.points
        user_answer = submission.answers.get(str(question.id))
        if user_answer and user_answer == question.correct_answer:
            total_score += question.points
    
    percentage = int((total_score / max_score * 100) if max_score > 0 else 0)
    
    # Save user assessment
    user_assessment = UserAssessment(
        user_id=current_user.id,
        assessment_id=assessment_id,
        score=total_score,
        max_score=max_score,
        percentage=percentage,
        answers=json.dumps(submission.answers)
    )
    db.add(user_assessment)
    await db.commit()
    await db.refresh(user_assessment)
    
    return {
        "score": total_score,
        "max_score": max_score,
        "percentage": percentage,
        "assessment_id": user_assessment.id
    }

@router.get("/user/history")
async def get_user_assessments(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get user's assessment history"""
    result = await db.execute(
        select(UserAssessment)
        .where(UserAssessment.user_id == current_user.id)
        .order_by(UserAssessment.completed_at.desc())
    )
    assessments = result.scalars().all()
    
    return [
        {
            "id": a.id,
            "assessment_id": a.assessment_id,
            "score": a.score,
            "max_score": a.max_score,
            "percentage": a.percentage,
            "completed_at": a.completed_at
        }
        for a in assessments
    ]
