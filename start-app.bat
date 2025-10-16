@echo off
setlocal enabledelayedexpansion

echo ========================================
echo   EduLearn Cloud App - Starting...
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.11+ and add it to your PATH
    pause
    exit /b 1
)
echo [OK] Python found

REM Check if Node.js is available
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Node.js is not installed or not in PATH
    echo Please install Node.js 18+ and add it to your PATH
    pause
    exit /b 1
)
echo [OK] Node.js found

REM Check if backend directory exists
if not exist "backend" (
    echo [ERROR] Backend directory not found!
    pause
    exit /b 1
)

REM Check if frontend directory exists
if not exist "frontend" (
    echo [ERROR] Frontend directory not found!
    pause
    exit /b 1
)

REM Check for existing services on ports
echo.
echo Checking for existing services...
netstat -ano | findstr ":8000" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 8000 is already in use (Backend may already be running)
    echo Skipping backend startup...
    set BACKEND_SKIP=1
) else (
    set BACKEND_SKIP=0
)

netstat -ano | findstr ":3000" >nul 2>&1
if not errorlevel 1 (
    echo [WARNING] Port 3000 is already in use (Frontend may already be running)
    echo Skipping frontend startup...
    set FRONTEND_SKIP=1
) else (
    set FRONTEND_SKIP=0
)

REM Check backend dependencies
echo.
echo Checking dependencies...
if not exist "backend\app\__init__.py" (
    echo [WARNING] Backend app structure may be incomplete
)

REM Check frontend dependencies
if not exist "frontend\node_modules" (
    echo [WARNING] Frontend dependencies not installed!
    echo Installing frontend dependencies...
    cd frontend
    call npm install
    if errorlevel 1 (
        echo [ERROR] Failed to install frontend dependencies
        cd ..
        pause
        exit /b 1
    )
    cd ..
    echo [OK] Frontend dependencies installed
) else (
    echo [OK] Frontend dependencies found
)

REM Check Python packages
cd backend
python -c "import fastapi, uvicorn" >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Python packages may not be installed
    echo Installing Python dependencies...
    call pip install -q -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install Python dependencies
        cd ..
        pause
        exit /b 1
    )
    echo [OK] Python dependencies installed
) else (
    echo [OK] Python packages found
)
cd ..

REM Start backend if not already running
echo.
if "!BACKEND_SKIP!"=="0" (
    echo [1/2] Starting Backend API (FastAPI)...
    start "EduLearn Backend" cmd /k "cd /d %~dp0backend && echo Starting EduLearn Backend API... && python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
    timeout /t 3 /nobreak >nul
    echo [OK] Backend starting...
) else (
    echo [SKIP] Backend already running on port 8000
)

REM Start frontend if not already running
if "!FRONTEND_SKIP!"=="0" (
    echo [2/2] Starting Frontend (React)...
    start "EduLearn Frontend" cmd /k "cd /d %~dp0frontend && echo Starting EduLearn Frontend... && npm start"
    echo [OK] Frontend starting...
) else (
    echo [SKIP] Frontend already running on port 3000
)

echo.
echo ========================================
echo   Services are starting!
echo ========================================
echo.
echo Backend API:  http://127.0.0.1:8000
echo API Docs:     http://127.0.0.1:8000/docs
echo Frontend:     http://localhost:3000
echo.
echo Two windows have opened - one for backend, one for frontend
echo The frontend may take 30-60 seconds to compile on first run
echo.
echo You can close this window - services will keep running
echo To stop services, run stop-app.bat
echo.
timeout /t 5 /nobreak >nul