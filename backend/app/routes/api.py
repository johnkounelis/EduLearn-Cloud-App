from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["api"])

# Legacy endpoints for backward compatibility
@router.get("/courses")
async def get_courses():
    """Get list of courses (legacy - use /career-paths instead)"""
    try:
        logger.info("Fetching courses")
        # Mock data for backward compatibility
        courses = [
            {"id": 1, "title": "Introduction to Python", "description": "Learn Python basics"},
            {"id": 2, "title": "Web Development", "description": "Build modern web applications"},
            {"id": 3, "title": "Cloud Computing", "description": "Master cloud technologies"}
        ]
        return {"courses": courses, "count": len(courses)}
    except Exception as e:
        logger.error(f"Error fetching courses: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": "Failed to fetch courses", "detail": str(e)}
        )

@router.get("/courses/{course_id}")
async def get_course(course_id: int):
    """Get a specific course by ID (legacy - use /career-paths/{id} instead)"""
    try:
        logger.info(f"Fetching course {course_id}")
        if course_id < 1:
            raise HTTPException(status_code=400, detail="Course ID must be positive")
        if course_id > 1000:
            raise HTTPException(status_code=404, detail=f"Course {course_id} not found")

        # Mock data
        course = {
            "id": course_id,
            "title": f"Course {course_id}",
            "description": f"Description for course {course_id}",
            "lessons": []
        }
        return course
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching course {course_id}: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to fetch course {course_id}", "detail": str(e)}
        )

@router.get("/status")
async def api_status():
    """Check API status and return version info"""
    return {
        "status": "operational",
        "version": "1.0.0",
        "endpoints": {
            "courses": "/api/v1/courses",
            "career_paths": "/api/v1/career-paths",
            "auth": "/api/v1/auth",
            "progress": "/api/v1/progress"
        }
    }
