@echo off
echo ========================================
echo   EduLearn App - Status Check
echo ========================================
echo.

echo Checking Backend (port 8000)...
netstat -ano | findstr ":8000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [OFFLINE] Backend is not running
) else (
    echo [ONLINE] Backend is running
    echo Testing backend health...
    curl -s http://127.0.0.1:8000/health >nul 2>&1
    if errorlevel 1 (
        echo          Health check failed
    ) else (
        echo          Health check passed
    )
)

echo.
echo Checking Frontend (port 3000)...
netstat -ano | findstr ":3000.*LISTENING" >nul 2>&1
if errorlevel 1 (
    echo [OFFLINE] Frontend is not running
) else (
    echo [ONLINE] Frontend is running
)

echo.
echo Process Check:
tasklist | findstr /I "python.exe node.exe" 2>nul
if errorlevel 1 (
    echo No Python or Node processes found
)

echo.
echo ========================================
pause
