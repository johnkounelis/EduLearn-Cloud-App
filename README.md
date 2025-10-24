# EduLearn - Cloud-Based IT Career Learning Platform

[![CI/CD Pipeline](https://github.com/johnkounelis/EduLearn-Cloud-App/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/johnkounelis/EduLearn-Cloud-App/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![React 18](https://img.shields.io/badge/react-18.2-61dafb.svg)](https://reactjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-009688.svg)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-ready-2496ED.svg)](https://www.docker.com/)
[![Terraform](https://img.shields.io/badge/terraform-aws-7B42BC.svg)](https://www.terraform.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A comprehensive cloud-native learning platform designed for IT graduates and newcomers exploring career paths in technology. Built with a modern microservices architecture using FastAPI, React, Docker, and deployed on AWS with Terraform infrastructure-as-code.

---

## Table of Contents

- [Live Demo](#live-demo)
- [Screenshots](#screenshots)
- [Architecture](#architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Docker Deployment](#docker-deployment)
- [AWS Cloud Deployment](#aws-cloud-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Testing](#testing)
- [Environment Variables](#environment-variables)
- [Contributing](#contributing)
- [License](#license)

---

## Live Demo

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | React SPA user interface |
| Backend API | http://localhost:8000 | FastAPI REST API |
| API Docs (Swagger) | http://localhost:8000/docs | Interactive API documentation |
| Health Check | http://localhost:8000/health | Service health endpoint |

**Demo Credentials:**
```
Username: demo_user
Password: Demo123!
```

---

## Screenshots

### Home Page - Career Path Discovery
> Landing page with hero section, category filters, and featured IT career paths including Cloud, DevOps, Software Development, Security, and Data Science.

![Home Page](docs/screenshots/home-page.png)

### Career Paths - Browse & Filter
> Browse all IT career paths with category filtering, search functionality, difficulty levels, salary ranges, and estimated learning timelines.

![Career Paths](docs/screenshots/career-paths.png)

### User Dashboard
> Personalized dashboard showing career path progress, completed assessments, and quick navigation.

![Dashboard](docs/screenshots/dashboard.png)

### Progress Tracking
> Track your learning journey across all career paths with completion stats, assessment scores, and visual progress indicators.

![Progress](docs/screenshots/progress.png)

### User Authentication - Login & Register
> Secure JWT-based authentication with user registration and login.

![Login](docs/screenshots/login.png)

![Register](docs/screenshots/register.png)

---

## Architecture

```
                    +------------------+
                    |   React Frontend |
                    |   (Port 3000)    |
                    +--------+---------+
                             |
                         Axios HTTP
                             |
                    +--------v---------+
                    |  FastAPI Backend  |
                    |   (Port 8000)    |
                    +--------+---------+
                             |
                      SQLAlchemy ORM
                             |
              +--------------+--------------+
              |                             |
    +---------v---------+     +-------------v-----------+
    |  SQLite (Local)   |     |  PostgreSQL (Production) |
    |  edulearn.db      |     |  AWS RDS                 |
    +-------------------+     +-------------------------+
```

### Cloud Architecture (AWS)

```
                         Internet
                            |
                    +-------v--------+
                    |   AWS ALB      |
                    | (Load Balancer)|
                    +---+--------+--+
                        |        |
              +---------v--+  +--v----------+
              | ECS Task   |  | ECS Task    |
              | (Frontend) |  | (Backend)   |
              | Nginx+React|  | FastAPI     |
              +------------+  +------+------+
                                     |
                              +------v------+
                              |   AWS RDS   |
                              | PostgreSQL  |
                              +-------------+
```

---

## Features

### Career Path Exploration
- Browse IT career paths across 5 categories: **Cloud, DevOps, Software Development, Security, Data Science**
- View detailed career information including required skills, estimated learning time, salary ranges ($80K-$200K+), and job market insights
- Filter by category and search career paths

### Skills Assessment Engine
- Interactive quizzes with timed assessments (configurable time limits)
- Multiple question types: multiple choice, true/false, and text input
- Automatic scoring with detailed results and performance tracking
- Assessment history for reviewing past attempts

### Progress Tracking
- Real-time progress monitoring per career path
- Visual progress bars and completion percentages
- Track started, in-progress, and completed career paths

### User Authentication & Authorization
- Secure registration with email/username/password
- JWT-based authentication with 30-minute token expiration
- Protected routes (Dashboard, Progress) require authentication
- Password hashing with bcrypt

### Cloud-Native Architecture
- Fully containerized with multi-stage Docker builds
- Docker Compose for local development orchestration
- AWS ECS Fargate deployment with auto-scaling
- Infrastructure as Code with Terraform
- CI/CD pipeline with GitHub Actions

---

## Tech Stack

### Backend
| Technology | Purpose | Version |
|-----------|---------|---------|
| FastAPI | Async web framework with auto-generated docs | 0.104+ |
| SQLAlchemy | Async ORM with relationship support | 2.0+ |
| Pydantic | Data validation and serialization | v2 |
| python-jose | JWT token creation and validation | - |
| passlib | Password hashing (bcrypt) | - |
| Uvicorn | ASGI server | - |
| SQLite / PostgreSQL | Database (dev / production) | - |

### Frontend
| Technology | Purpose | Version |
|-----------|---------|---------|
| React | Component-based UI library | 18.2 |
| React Router | Client-side routing (SPA) | v6 |
| Axios | HTTP client for API calls | - |
| CSS3 | Custom styling | - |

### DevOps & Infrastructure
| Technology | Purpose |
|-----------|---------|
| Docker | Containerization (multi-stage builds) |
| Docker Compose | Local multi-container orchestration |
| Nginx | Frontend reverse proxy (production) |
| Terraform | AWS infrastructure as code |
| GitHub Actions | CI/CD automation |
| AWS ECS Fargate | Serverless container orchestration |
| AWS RDS | Managed PostgreSQL database |
| AWS ALB | Application load balancing |
| AWS ECR | Docker image registry |

---

## Getting Started

### Prerequisites

- **Python 3.11+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Docker & Docker Compose** (optional) - [Download](https://www.docker.com/)

### Quick Start (Windows)

The fastest way to run everything:

```batch
start-app.bat
```

This script automatically:
1. Checks Python 3.11+ and Node.js 18+ are installed
2. Verifies required directories exist
3. Checks if ports 8000 and 3000 are available
4. Installs missing dependencies
5. Opens separate terminal windows for backend and frontend

Or use PowerShell with colored output:
```powershell
.\start-app.ps1
```

To stop the app:
```batch
stop-app.bat
```

### Manual Setup

#### 1. Clone the Repository
```bash
git clone https://github.com/johnkounelis/EduLearn-Cloud-App.git
cd EduLearn-Cloud-App
```

#### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
source venv/bin/activate        # Linux/macOS
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

The backend will:
- Create the SQLite database automatically
- Seed it with sample career paths, skills, and assessments
- Serve the API at http://127.0.0.1:8000

#### 3. Frontend Setup
```bash
cd frontend
npm install
npm start
```

The React dev server starts at http://localhost:3000 with hot reload.

#### 4. Verify Everything Works
```bash
# Health check
curl http://localhost:8000/health
# Expected: {"status":"ok","service":"edulearn-api"}

# List career paths
curl http://localhost:8000/api/v1/career-paths

# Register a test user
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","username":"testuser","password":"Test123!","full_name":"Test User"}'
```

---

## API Documentation

### Interactive Docs

Visit http://localhost:8000/docs for the full Swagger UI with try-it-out functionality.

### Endpoints Summary

#### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/api/v1/auth/register` | No | Register a new user |
| POST | `/api/v1/auth/login` | No | Login (returns JWT token) |
| GET | `/api/v1/auth/me` | Yes | Get current user profile |

#### Career Paths
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/career-paths` | No | List all career paths (optional `?category=` filter) |
| GET | `/api/v1/career-paths/{id}` | No | Get career path with skills |
| GET | `/api/v1/career-paths/categories/list` | No | Get all categories |

#### Skills
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/skills` | No | List all skills |
| GET | `/api/v1/skills/{id}` | No | Get skill details |

#### Assessments
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/assessments/career-path/{id}` | No | Get assessments for a career path |
| GET | `/api/v1/assessments/{id}` | No | Get assessment with questions |
| POST | `/api/v1/assessments/{id}/submit` | Yes | Submit assessment answers |
| GET | `/api/v1/assessments/user/history` | Yes | Get user's assessment history |

#### Progress Tracking
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/v1/progress` | Yes | Get all progress for current user |
| POST | `/api/v1/progress/career-path/{id}` | Yes | Update progress for a career path |

#### System
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API welcome message and version |
| GET | `/health` | Health check (used by Docker/ALB) |

---

## Project Structure

```
EduLearn-Cloud-App/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                 # FastAPI app: CORS, routes, startup, error handling
│   │   ├── database.py             # SQLAlchemy async engine & session factory
│   │   ├── auth.py                 # JWT creation/validation, password hashing
│   │   ├── seed_data.py            # Initial data: career paths, skills, assessments
│   │   ├── models/
│   │   │   ├── user.py             # User model (email, username, hashed_password)
│   │   │   ├── career_path.py      # CareerPath + CareerPathSkill junction
│   │   │   ├── skill.py            # Skill model (name, category, level)
│   │   │   ├── assessment.py       # Assessment + AssessmentQuestion models
│   │   │   └── progress.py         # UserProgress + UserAssessment models
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   │   ├── user.py
│   │   │   ├── career_path.py
│   │   │   ├── skill.py
│   │   │   ├── assessment.py
│   │   │   └── progress.py
│   │   └── routes/
│   │       ├── auth.py             # Register, login, get-me endpoints
│   │       ├── career_paths.py     # CRUD + category filtering
│   │       ├── skills.py           # Skill listing
│   │       ├── assessments.py      # Quiz retrieval + submission + scoring
│   │       ├── progress.py         # Progress tracking
│   │       └── api.py              # General API routes
│   ├── test_main.py                # Backend tests
│   ├── pytest.ini                  # Test configuration
│   ├── requirements.txt            # Python dependencies
│   ├── Dockerfile                  # Python 3.11-slim container
│   ├── .dockerignore
│   └── .env.example                # Environment variable template
│
├── frontend/
│   ├── public/
│   │   ├── index.html              # HTML template
│   │   └── favicon.ico
│   ├── src/
│   │   ├── index.js                # React DOM mount point
│   │   ├── App.js                  # Root component: routing, auth state
│   │   ├── App.css                 # Global styles
│   │   ├── pages/
│   │   │   ├── Home.js             # Landing page with hero + career cards
│   │   │   ├── Home.css
│   │   │   ├── Login.js            # Login form
│   │   │   ├── Login.css
│   │   │   ├── Register.js         # Registration form
│   │   │   ├── Register.css
│   │   │   ├── Dashboard.js        # User dashboard (protected)
│   │   │   ├── Dashboard.css
│   │   │   ├── CareerPaths.js      # Browse/filter career paths
│   │   │   ├── CareerPaths.css
│   │   │   ├── CareerPathDetail.js # Single career path view
│   │   │   ├── CareerPathDetail.css
│   │   │   ├── Assessment.js       # Take quizzes (protected)
│   │   │   ├── Assessment.css
│   │   │   ├── Skills.js           # Browse all skills
│   │   │   ├── Skills.css
│   │   │   ├── Progress.js         # Learning progress (protected)
│   │   │   └── Progress.css
│   │   └── components/
│   │       ├── Navbar.js           # Navigation bar with auth state
│   │       ├── Navbar.css
│   │       ├── SearchBar.js        # Search component
│   │       ├── ProgressTracker.js  # Visual progress bars
│   │       ├── CodeBlock.js        # Code syntax highlighting
│   │       ├── TryItSection.js     # Interactive learning sections
│   │       ├── LessonSection.js    # Lesson content display
│   │       └── TutorialNavigation.js
│   ├── package.json                # Node dependencies & scripts
│   ├── Dockerfile                  # Multi-stage: Node build + Nginx serve
│   ├── .dockerignore
│   └── .env.example
│
├── terraform/                      # AWS Infrastructure as Code
│   ├── main.tf                     # Provider config, Terraform settings
│   ├── variables.tf                # Input variables
│   ├── outputs.tf                  # Output values (ALB URL, etc.)
│   ├── network.tf                  # VPC, subnets, internet gateway
│   ├── security.tf                 # Security groups, IAM roles
│   ├── ecr.tf                      # ECR repositories for Docker images
│   ├── ecs.tf                      # ECS cluster, task definitions, services
│   ├── rds.tf                      # RDS PostgreSQL instance
│   ├── alb.tf                      # Application Load Balancer + listeners
│   └── data.tf                     # Data sources (availability zones)
│
├── .github/workflows/
│   └── ci-cd.yml                   # GitHub Actions: test, build, deploy
│
├── docker-compose.yml              # Local dev: backend + frontend + healthchecks
├── start-app.bat                   # Windows: auto-start both servers
├── start-app.ps1                   # PowerShell: auto-start with colored output
├── stop-app.bat                    # Stop running servers
├── stop-app.ps1                    # PowerShell stop script
├── check-status.bat                # Check if servers are running
├── DEPLOYMENT.md                   # Production deployment guide
├── README-START.md                 # Quick start reference
└── README.md                       # This file
```

---

## Docker Deployment

### Local Development with Docker Compose

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up --build -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

### Production Docker Builds

```bash
# Build optimized backend image
docker build -t edulearn-backend ./backend

# Build optimized frontend image (multi-stage: Node build + Nginx)
docker build -t edulearn-frontend ./frontend

# Run individually
docker run -p 8000:8000 edulearn-backend
docker run -p 80:80 edulearn-frontend
```

---

## AWS Cloud Deployment

### Infrastructure Overview

The Terraform configuration provisions:
- **VPC** with public/private subnets across 2 availability zones
- **ECS Fargate** cluster with backend and frontend services
- **RDS PostgreSQL** instance in private subnets
- **Application Load Balancer** with health checks
- **ECR** repositories for Docker images
- **Security groups** with least-privilege access
- **IAM roles** for ECS task execution

### Deploy Step-by-Step

#### 1. Configure Variables
```bash
cd terraform
cat > terraform.tfvars << EOF
aws_region         = "eu-central-1"
environment        = "dev"
project_name       = "edulearn"
db_password        = "YourSecurePassword123!"
backend_image_tag  = "latest"
frontend_image_tag = "latest"
EOF
```

#### 2. Initialize and Apply
```bash
terraform init
terraform plan      # Review changes
terraform apply     # Deploy infrastructure
```

#### 3. Push Docker Images to ECR
```bash
# Authenticate with ECR
aws ecr get-login-password --region eu-central-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.eu-central-1.amazonaws.com

# Build, tag, and push backend
docker build -t edulearn-backend ./backend
docker tag edulearn-backend:latest <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-backend:latest
docker push <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-backend:latest

# Build, tag, and push frontend
docker build -t edulearn-frontend ./frontend
docker tag edulearn-frontend:latest <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-frontend:latest
docker push <account-id>.dkr.ecr.eu-central-1.amazonaws.com/edulearn-frontend:latest
```

#### 4. Deploy to ECS
```bash
aws ecs update-service --cluster edulearn-cluster --service edulearn-backend-service --force-new-deployment
aws ecs update-service --cluster edulearn-cluster --service edulearn-frontend-service --force-new-deployment
```

---

## CI/CD Pipeline

The GitHub Actions workflow (`.github/workflows/ci-cd.yml`) automates:

| Stage | Trigger | Actions |
|-------|---------|---------|
| Test | Push / PR to main | Run backend pytest, lint checks |
| Build | Push to main | Build Docker images, push to ECR |
| Deploy | Push to main (optional) | Terraform apply, ECS service update |

### Required GitHub Secrets

| Secret | Description |
|--------|-------------|
| `AWS_ACCESS_KEY_ID` | AWS IAM access key |
| `AWS_SECRET_ACCESS_KEY` | AWS IAM secret key |

---

## Testing

### Backend Tests
```bash
cd backend
pip install pytest pytest-asyncio httpx
pytest -v
```

### Frontend Tests
```bash
cd frontend
npm test
```

### API Testing with curl
```bash
# Register
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","username":"testuser","password":"Test123!","full_name":"Test User"}'

# Login (returns JWT token)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -d "username=testuser&password=Test123!"

# Use token for authenticated endpoints
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer <your-token>"
```

---

## Environment Variables

### Backend (`backend/.env`)
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/edulearn  # Production
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend (`frontend/.env`)
```env
REACT_APP_API_URL=http://localhost:8000
```

See `backend/.env.example` and `frontend/.env.example` for templates.

---

## Screen Recording Guide

To create a demo video of the application:

### Using Windows Built-in Tools
1. **Xbox Game Bar** (Win + G): Press `Win + Alt + R` to start/stop recording
2. **Snipping Tool** (Windows 11): Open Snipping Tool > Record > New

### Using OBS Studio (Free)
1. Download [OBS Studio](https://obsproject.com/)
2. Add a "Window Capture" source pointing to your browser
3. Set output to MP4, 1080p, 30fps
4. Click "Start Recording"

### Recommended Demo Flow
1. **Home Page** - Show the hero section and career path cards
2. **Career Paths** - Filter by category (Cloud, DevOps, etc.)
3. **Career Path Detail** - Click into "Cloud Solution Architect", show skills and salary info
4. **Register** - Create a new account
5. **Login** - Sign in with credentials
6. **Dashboard** - Show the personalized dashboard
7. **Assessment** - Take a quiz, submit answers, view score
8. **Progress** - Show progress tracking across career paths
9. **API Docs** - Quick look at http://localhost:8000/docs
10. **Skills Page** - Browse available skills

### Taking Screenshots
```bash
# Create screenshots directory
mkdir -p docs/screenshots

# Recommended: Use browser DevTools (F12) to set viewport to 1280x720
# Then use Win+Shift+S (Snipping Tool) to capture each page
```

---

## Database Schema

```
users                    career_paths              skills
├── id (PK)              ├── id (PK)               ├── id (PK)
├── email (unique)       ├── title (unique)        ├── name (unique)
├── username (unique)    ├── description           ├── description
├── hashed_password      ├── category              ├── category
├── full_name            ├── estimated_time        └── level
├── is_active            ├── difficulty
├── is_admin             ├── job_market_info       career_path_skills
├── created_at           └── salary_range          ├── id (PK)
└── updated_at                                     ├── career_path_id (FK)
                                                   ├── skill_id (FK)
assessments              assessment_questions       ├── is_required
├── id (PK)              ├── id (PK)               └── priority
├── title                ├── assessment_id (FK)
├── description          ├── question_text         user_progress
├── career_path_id (FK)  ├── question_type         ├── id (PK)
└── time_limit           ├── options (JSON)        ├── user_id (FK)
                         ├── correct_answer        ├── career_path_id (FK)
user_assessments         └── points                ├── skill_id (FK)
├── id (PK)                                        ├── progress_percentage
├── user_id (FK)                                   ├── is_completed
├── assessment_id (FK)                             ├── started_at
├── score                                          ├── completed_at
├── max_score                                      └── last_updated
├── percentage
├── completed_at
└── answers (JSON)
```

---

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Authors

John Kounelis

---

**Built with modern cloud-native technologies for IT career exploration and skill development.**
