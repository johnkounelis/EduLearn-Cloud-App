from fastapi import APIRouter, HTTPException
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["api"])

# Legacy endpoints for backward compatibility
@router.get("/courses")
async def get_courses():
    """Get list of courses (legacy - use /career-paths instead)"""
    logger.info("Fetching courses")
    # Mock data for backward compatibility
    courses = [
        {"id": 1, "title": "Introduction to Python", "description": "Learn Python basics"},
        {"id": 2, "title": "Web Development", "description": "Build modern web applications"},
        {"id": 3, "title": "Cloud Computing", "description": "Master cloud technologies"}
    ]
    return {"courses": courses, "count": len(courses)}

@router.get("/courses/{course_id}")
async def get_course(course_id: int):
    """Get a specific course by ID (legacy - use /career-paths/{id} instead)"""
    logger.info(f"Fetching course {course_id}")
    if course_id < 1:
        raise HTTPException(status_code=400, detail="Course ID must be positive")
    
    # Mock data
    course = {
        "id": course_id,
        "title": f"Course {course_id}",
        "description": f"Description for course {course_id}",
        "lessons": []
    }
    return course
