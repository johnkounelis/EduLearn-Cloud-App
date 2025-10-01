import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.database import Base, engine, AsyncSessionLocal
from app.auth import get_password_hash, create_access_token


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture(autouse=True)
async def setup_database():
    """Create tables before each test and drop them after."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def client():
    """Async HTTP client for FastAPI."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def seeded_db():
    """Seed the database with sample data and return the session."""
    from app.seed_data import seed_database
    async with AsyncSessionLocal() as db:
        await seed_database(db)


@pytest.fixture
async def registered_user(client: AsyncClient):
    """Register a test user and return user data + token."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123",
        "full_name": "Test User",
    }
    await client.post("/api/v1/auth/register", json=user_data)
    # Login to get token
    login_resp = await client.post(
        "/api/v1/auth/login",
        data={"username": "testuser", "password": "password123"},
    )
    token = login_resp.json()["access_token"]
    return {"token": token, **user_data}


def auth_header(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


# ---------------------------------------------------------------------------
# Root & Health
# ---------------------------------------------------------------------------

class TestRootEndpoints:
    async def test_read_root(self, client: AsyncClient):
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "Welcome to EduLearn API!" in data["message"]
        assert data["version"] == "1.0.0"

    async def test_health_check(self, client: AsyncClient):
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "edulearn-api"


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

class TestAuth:
    async def test_register_user(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/register",
            json={
                "email": "new@example.com",
                "username": "newuser",
                "password": "secret123",
                "full_name": "New User",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == "new@example.com"
        assert data["username"] == "newuser"
        assert "id" in data

    async def test_register_duplicate_email(self, client: AsyncClient):
        payload = {
            "email": "dup@example.com",
            "username": "user1",
            "password": "secret123",
        }
        await client.post("/api/v1/auth/register", json=payload)
        payload["username"] = "user2"
        response = await client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 400

    async def test_register_duplicate_username(self, client: AsyncClient):
        payload = {
            "email": "a@example.com",
            "username": "sameuser",
            "password": "secret123",
        }
        await client.post("/api/v1/auth/register", json=payload)
        payload["email"] = "b@example.com"
        response = await client.post("/api/v1/auth/register", json=payload)
        assert response.status_code == 400

    async def test_login_success(self, client: AsyncClient, registered_user):
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    async def test_login_wrong_password(self, client: AsyncClient, registered_user):
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "testuser", "password": "wrong"},
        )
        assert response.status_code == 401

    async def test_login_nonexistent_user(self, client: AsyncClient):
        response = await client.post(
            "/api/v1/auth/login",
            data={"username": "ghost", "password": "nope"},
        )
        assert response.status_code == 401

    async def test_get_me(self, client: AsyncClient, registered_user):
        response = await client.get(
            "/api/v1/auth/me",
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "testuser"
        assert data["email"] == "test@example.com"

    async def test_get_me_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/auth/me")
        assert response.status_code in [401, 422]

    async def test_get_me_invalid_token(self, client: AsyncClient):
        response = await client.get(
            "/api/v1/auth/me",
            headers=auth_header("invalid.token.here"),
        )
        assert response.status_code == 401


# ---------------------------------------------------------------------------
# Career Paths
# ---------------------------------------------------------------------------

class TestCareerPaths:
    async def test_list_career_paths_empty(self, client: AsyncClient):
        response = await client.get("/api/v1/career-paths")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_career_paths_seeded(self, client: AsyncClient, seeded_db):
        response = await client.get("/api/v1/career-paths")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5
        titles = {p["title"] for p in data}
        assert "Cloud Solution Architect" in titles
        assert "DevOps Engineer" in titles

    async def test_filter_by_category(self, client: AsyncClient, seeded_db):
        response = await client.get("/api/v1/career-paths?category=Cloud")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert all(p["category"] == "Cloud" for p in data)

    async def test_get_career_path_detail(self, client: AsyncClient, seeded_db):
        # Get list first to find an ID
        list_resp = await client.get("/api/v1/career-paths")
        path_id = list_resp.json()[0]["id"]
        response = await client.get(f"/api/v1/career-paths/{path_id}")
        assert response.status_code == 200
        data = response.json()
        assert "title" in data
        assert "skills" in data

    async def test_get_career_path_not_found(self, client: AsyncClient):
        response = await client.get("/api/v1/career-paths/9999")
        assert response.status_code == 404

    async def test_get_categories(self, client: AsyncClient, seeded_db):
        response = await client.get("/api/v1/career-paths/categories/list")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert "Cloud" in data


# ---------------------------------------------------------------------------
# Skills
# ---------------------------------------------------------------------------

class TestSkills:
    async def test_list_skills_empty(self, client: AsyncClient):
        response = await client.get("/api/v1/skills")
        assert response.status_code == 200
        assert response.json() == []

    async def test_list_skills_seeded(self, client: AsyncClient, seeded_db):
        response = await client.get("/api/v1/skills")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 20
        names = {s["name"] for s in data}
        assert "Docker" in names
        assert "Python" in names

    async def test_filter_skills_by_category(self, client: AsyncClient, seeded_db):
        response = await client.get("/api/v1/skills?category=Cloud")
        assert response.status_code == 200
        data = response.json()
        assert all(s["category"] == "Cloud" for s in data)

    async def test_get_skill_by_id(self, client: AsyncClient, seeded_db):
        list_resp = await client.get("/api/v1/skills")
        skill_id = list_resp.json()[0]["id"]
        response = await client.get(f"/api/v1/skills/{skill_id}")
        assert response.status_code == 200
        data = response.json()
        assert "name" in data
        assert "category" in data
        assert "level" in data

    async def test_get_skill_not_found(self, client: AsyncClient):
        response = await client.get("/api/v1/skills/9999")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Assessments
# ---------------------------------------------------------------------------

class TestAssessments:
    async def test_get_assessments_for_career_path(self, client: AsyncClient, seeded_db):
        # Get the Cloud career path ID
        paths = (await client.get("/api/v1/career-paths")).json()
        cloud_path = next(p for p in paths if p["title"] == "Cloud Solution Architect")
        response = await client.get(f"/api/v1/assessments/career-path/{cloud_path['id']}")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["title"] == "Cloud Architecture Fundamentals Assessment"

    async def test_get_assessment_detail(self, client: AsyncClient, seeded_db):
        # Find assessment
        paths = (await client.get("/api/v1/career-paths")).json()
        cloud_path = next(p for p in paths if p["title"] == "Cloud Solution Architect")
        assessments = (
            await client.get(f"/api/v1/assessments/career-path/{cloud_path['id']}")
        ).json()
        assessment_id = assessments[0]["id"]

        response = await client.get(f"/api/v1/assessments/{assessment_id}")
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        assert len(data["questions"]) == 3

    async def test_get_assessment_not_found(self, client: AsyncClient):
        response = await client.get("/api/v1/assessments/9999")
        assert response.status_code == 404

    async def test_submit_assessment(self, client: AsyncClient, seeded_db, registered_user):
        # Find assessment + questions
        paths = (await client.get("/api/v1/career-paths")).json()
        cloud_path = next(p for p in paths if p["title"] == "Cloud Solution Architect")
        assessments = (
            await client.get(f"/api/v1/assessments/career-path/{cloud_path['id']}")
        ).json()
        assessment_id = assessments[0]["id"]
        detail = (await client.get(f"/api/v1/assessments/{assessment_id}")).json()

        # Submit correct answers
        answers = {}
        for q in detail["questions"]:
            if q["question_text"].startswith("What is Infrastructure"):
                answers[str(q["id"])] = "B) Managing infrastructure through code"
            elif q["question_text"].startswith("Which AWS"):
                answers[str(q["id"])] = "B) Lambda"
            else:
                answers[str(q["id"])] = "True"

        response = await client.post(
            f"/api/v1/assessments/{assessment_id}/submit",
            json={"assessment_id": assessment_id, "answers": answers},
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["percentage"] == 100
        assert data["score"] == data["max_score"]

    async def test_submit_assessment_partial(self, client: AsyncClient, seeded_db, registered_user):
        paths = (await client.get("/api/v1/career-paths")).json()
        cloud_path = next(p for p in paths if p["title"] == "Cloud Solution Architect")
        assessments = (
            await client.get(f"/api/v1/assessments/career-path/{cloud_path['id']}")
        ).json()
        assessment_id = assessments[0]["id"]
        detail = (await client.get(f"/api/v1/assessments/{assessment_id}")).json()

        # Submit wrong answers
        answers = {str(q["id"]): "wrong answer" for q in detail["questions"]}

        response = await client.post(
            f"/api/v1/assessments/{assessment_id}/submit",
            json={"assessment_id": assessment_id, "answers": answers},
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["percentage"] == 0

    async def test_submit_assessment_unauthorized(self, client: AsyncClient, seeded_db):
        response = await client.post(
            "/api/v1/assessments/1/submit",
            json={"assessment_id": 1, "answers": {}},
        )
        assert response.status_code in [401, 422]

    async def test_user_assessment_history(self, client: AsyncClient, seeded_db, registered_user):
        response = await client.get(
            "/api/v1/assessments/user/history",
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        assert isinstance(response.json(), list)


# ---------------------------------------------------------------------------
# Progress
# ---------------------------------------------------------------------------

class TestProgress:
    async def test_get_progress_empty(self, client: AsyncClient, registered_user):
        response = await client.get(
            "/api/v1/progress",
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        assert response.json() == []

    async def test_update_progress(self, client: AsyncClient, seeded_db, registered_user):
        paths = (await client.get("/api/v1/career-paths")).json()
        path_id = paths[0]["id"]

        response = await client.post(
            f"/api/v1/progress/career-path/{path_id}",
            json={"progress_percentage": 50},
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["progress_percentage"] == 50
        assert data["is_completed"] is False

    async def test_update_progress_complete(self, client: AsyncClient, seeded_db, registered_user):
        paths = (await client.get("/api/v1/career-paths")).json()
        path_id = paths[0]["id"]

        response = await client.post(
            f"/api/v1/progress/career-path/{path_id}",
            json={"progress_percentage": 100},
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert data["progress_percentage"] == 100
        assert data["is_completed"] is True

    async def test_update_progress_clamps(self, client: AsyncClient, seeded_db, registered_user):
        paths = (await client.get("/api/v1/career-paths")).json()
        path_id = paths[0]["id"]

        response = await client.post(
            f"/api/v1/progress/career-path/{path_id}",
            json={"progress_percentage": 150},
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        assert response.json()["progress_percentage"] == 100

    async def test_get_progress_after_update(self, client: AsyncClient, seeded_db, registered_user):
        paths = (await client.get("/api/v1/career-paths")).json()
        path_id = paths[0]["id"]

        await client.post(
            f"/api/v1/progress/career-path/{path_id}",
            json={"progress_percentage": 75},
            headers=auth_header(registered_user["token"]),
        )

        response = await client.get(
            "/api/v1/progress",
            headers=auth_header(registered_user["token"]),
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["progress_percentage"] == 75

    async def test_progress_unauthorized(self, client: AsyncClient):
        response = await client.get("/api/v1/progress")
        assert response.status_code in [401, 422]


# ---------------------------------------------------------------------------
# Legacy Courses API
# ---------------------------------------------------------------------------

class TestLegacyAPI:
    async def test_get_courses(self, client: AsyncClient):
        response = await client.get("/api/v1/courses")
        assert response.status_code == 200
        data = response.json()
        assert "courses" in data
        assert "count" in data
        assert isinstance(data["courses"], list)

    async def test_get_course_by_id(self, client: AsyncClient):
        response = await client.get("/api/v1/courses/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data

    async def test_get_course_invalid_id(self, client: AsyncClient):
        response = await client.get("/api/v1/courses/0")
        assert response.status_code == 400


# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------

class TestCORS:
    async def test_cors_allowed_origin(self, client: AsyncClient):
        response = await client.options(
            "/",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET",
            },
        )
        assert response.status_code in [200, 204]
