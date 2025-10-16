# EduLearn Cloud App Startup Script
$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduLearn Cloud App - Starting..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.11+ and add it to your PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if Node.js is available
try {
    $nodeVersion = node --version 2>&1
    Write-Host "[OK] Node.js found: $nodeVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Node.js is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Node.js 18+ and add it to your PATH" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

# Check directory structure
if (-not (Test-Path "backend")) {
    Write-Host "[ERROR] Backend directory not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

if (-not (Test-Path "frontend")) {
    Write-Host "[ERROR] Frontend directory not found!" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check for existing services
Write-Host ""
Write-Host "Checking for existing services..." -ForegroundColor Yellow

$backendRunning = $false
$frontendRunning = $false

$backendPort = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backendPort) {
    Write-Host "[WARNING] Port 8000 is already in use (Backend may already be running)" -ForegroundColor Yellow
    $backendRunning = $true
}

$frontendPort = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($frontendPort) {
    Write-Host "[WARNING] Port 3000 is already in use (Frontend may already be running)" -ForegroundColor Yellow
    $frontendRunning = $true
}

# Check dependencies
Write-Host ""
Write-Host "Checking dependencies..." -ForegroundColor Yellow

# Check frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "[WARNING] Frontend dependencies not installed!" -ForegroundColor Yellow
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Push-Location frontend
    npm install
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Failed to install frontend dependencies" -ForegroundColor Red
        Pop-Location
        Read-Host "Press Enter to exit"
        exit 1
    }
    Pop-Location
    Write-Host "[OK] Frontend dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[OK] Frontend dependencies found" -ForegroundColor Green
}

# Check Python packages
Push-Location backend
try {
    python -c "import fastapi, uvicorn" 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[WARNING] Python packages may not be installed" -ForegroundColor Yellow
        Write-Host "Installing Python dependencies..." -ForegroundColor Cyan
        pip install -q -r requirements.txt
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[ERROR] Failed to install Python dependencies" -ForegroundColor Red
            Pop-Location
            Read-Host "Press Enter to exit"
            exit 1
        }
        Write-Host "[OK] Python dependencies installed" -ForegroundColor Green
    } else {
        Write-Host "[OK] Python packages found" -ForegroundColor Green
    }
} catch {
    Write-Host "[ERROR] Error checking Python packages: $_" -ForegroundColor Red
}
Pop-Location

# Start backend
Write-Host ""
if (-not $backendRunning) {
    Write-Host "[1/2] Starting Backend API (FastAPI)..." -ForegroundColor Yellow
    $backendScript = "cd '$PSScriptRoot\backend'; Write-Host 'Starting EduLearn Backend API...' -ForegroundColor Green; python -m uvicorn app.main:app --host 127.0.0.1 --port 8000"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendScript
    Start-Sleep -Seconds 3
    Write-Host "[OK] Backend starting..." -ForegroundColor Green
} else {
    Write-Host "[SKIP] Backend already running on port 8000" -ForegroundColor Yellow
}

# Start frontend
if (-not $frontendRunning) {
    Write-Host "[2/2] Starting Frontend (React)..." -ForegroundColor Yellow
    $frontendScript = "cd '$PSScriptRoot\frontend'; Write-Host 'Starting EduLearn Frontend...' -ForegroundColor Green; npm start"
    Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendScript
    Write-Host "[OK] Frontend starting..." -ForegroundColor Green
} else {
    Write-Host "[SKIP] Frontend already running on port 3000" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Services are starting!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API:  http://127.0.0.1:8000" -ForegroundColor White
Write-Host "API Docs:     http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "Frontend:     http://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "Two PowerShell windows have opened - one for backend, one for frontend" -ForegroundColor Yellow
Write-Host "The frontend may take 30-60 seconds to compile on first run" -ForegroundColor Yellow
Write-Host ""
Write-Host "You can close this window - services will keep running" -ForegroundColor Gray
Write-Host "To stop services, run stop-app.bat or stop-app.ps1" -ForegroundColor Gray
Write-Host ""
Read-Host "Press Enter to exit"