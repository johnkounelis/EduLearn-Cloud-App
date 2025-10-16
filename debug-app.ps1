# EduLearn App Debugging Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduLearn App - Debug Information" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "Python Check:" -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "  Version: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Python not found" -ForegroundColor Red
}

# Check Node.js
Write-Host ""
Write-Host "Node.js Check:" -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>&1
    $npmVersion = npm --version 2>&1
    Write-Host "  Node version: $nodeVersion" -ForegroundColor Green
    Write-Host "  NPM version: $npmVersion" -ForegroundColor Green
} catch {
    Write-Host "  [ERROR] Node.js/NPM not found" -ForegroundColor Red
}

# Check Backend
Write-Host ""
Write-Host "Backend Check:" -ForegroundColor Yellow
if (Test-Path "backend") {
    Write-Host "  [OK] Backend directory exists" -ForegroundColor Green
    
    if (Test-Path "backend\app\main.py") {
        Write-Host "  [OK] main.py exists" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] main.py not found" -ForegroundColor Red
    }
    
    if (Test-Path "backend\requirements.txt") {
        Write-Host "  [OK] requirements.txt exists" -ForegroundColor Green
    } else {
        Write-Host "  [WARNING] requirements.txt not found" -ForegroundColor Yellow
    }
    
    Push-Location backend
    try {
        python -c "import fastapi; import uvicorn; print('Packages OK')" 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Python packages installed" -ForegroundColor Green
        } else {
            Write-Host "  [WARNING] Python packages may be missing" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "  [ERROR] Could not verify Python packages" -ForegroundColor Red
    }
    Pop-Location
} else {
    Write-Host "  [ERROR] Backend directory not found" -ForegroundColor Red
}

# Check Frontend
Write-Host ""
Write-Host "Frontend Check:" -ForegroundColor Yellow
if (Test-Path "frontend") {
    Write-Host "  [OK] Frontend directory exists" -ForegroundColor Green
    
    if (Test-Path "frontend\package.json") {
        Write-Host "  [OK] package.json exists" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] package.json not found" -ForegroundColor Red
    }
    
    if (Test-Path "frontend\node_modules") {
        $nodeModulesCount = (Get-ChildItem "frontend\node_modules" -Directory -ErrorAction SilentlyContinue).Count
        Write-Host "  [OK] node_modules exists ($nodeModulesCount packages)" -ForegroundColor Green
    } else {
        Write-Host "  [WARNING] node_modules not found - run 'npm install' in frontend directory" -ForegroundColor Yellow
    }
    
    if (Test-Path "frontend\src\App.js") {
        Write-Host "  [OK] App.js exists" -ForegroundColor Green
    } else {
        Write-Host "  [ERROR] App.js not found" -ForegroundColor Red
    }
} else {
    Write-Host "  [ERROR] Frontend directory not found" -ForegroundColor Red
}

# Check Ports
Write-Host ""
Write-Host "Port Status:" -ForegroundColor Yellow
$backendPort = Get-NetTCPConnection -LocalPort 8000 -ErrorAction SilentlyContinue
if ($backendPort) {
    Write-Host "  [RUNNING] Backend on port 8000" -ForegroundColor Green
    try {
        $response = Invoke-WebRequest -Uri http://127.0.0.1:8000/health -UseBasicParsing -TimeoutSec 2
        Write-Host "    Health check: OK" -ForegroundColor Green
    } catch {
        Write-Host "    Health check: FAILED" -ForegroundColor Red
    }
} else {
    Write-Host "  [OFFLINE] Backend not running on port 8000" -ForegroundColor Red
}

$frontendPort = Get-NetTCPConnection -LocalPort 3000 -ErrorAction SilentlyContinue
if ($frontendPort) {
    Write-Host "  [RUNNING] Frontend on port 3000" -ForegroundColor Green
} else {
    Write-Host "  [OFFLINE] Frontend not running on port 3000" -ForegroundColor Red
}

# Check Processes
Write-Host ""
Write-Host "Running Processes:" -ForegroundColor Yellow
$pythonProcesses = Get-Process python -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "  Python processes: $($pythonProcesses.Count)" -ForegroundColor Green
    foreach ($proc in $pythonProcesses) {
        Write-Host "    PID: $($proc.Id) - Started: $($proc.StartTime)" -ForegroundColor Gray
    }
} else {
    Write-Host "  No Python processes found" -ForegroundColor Yellow
}

$nodeProcesses = Get-Process node -ErrorAction SilentlyContinue
if ($nodeProcesses) {
    Write-Host "  Node processes: $($nodeProcesses.Count)" -ForegroundColor Green
    foreach ($proc in $nodeProcesses) {
        Write-Host "    PID: $($proc.Id) - Started: $($proc.StartTime)" -ForegroundColor Gray
    }
} else {
    Write-Host "  No Node processes found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Read-Host "Press Enter to exit"
