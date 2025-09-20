import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="EduLearn API",
    description="Cloud-based Learning Platform API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global exception handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP exception: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"error": "Validation error", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "message": "An unexpected error occurred"}
    )

@app.get("/")
def read_root():
    logger.info("Root endpoint accessed")
    return {"message": "Welcome to EduLearn API!", "version": "1.0.0"}

@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "ok", "service": "edulearn-api"}

# Include API routes
from app.routes import api, auth, career_paths, skills, assessments, progress
app.include_router(api.router)
app.include_router(auth.router)
app.include_router(career_paths.router)
app.include_router(skills.router)
app.include_router(assessments.router)
app.include_router(progress.router)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    from app.database import init_db, AsyncSessionLocal
    from app.seed_data import seed_database
    
    await init_db()
    logger.info("Database initialized")
    
    # Seed initial data
    async with AsyncSessionLocal() as db:
        try:
            await seed_database(db)
            logger.info("Database seeded with initial data")
        except Exception as e:
            logger.error(f"Error seeding database: {e}")
