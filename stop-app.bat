@echo off
echo ========================================
echo   EduLearn Cloud App - Stopping...
echo ========================================
echo.

REM Find and kill processes by port
echo Stopping Backend (port 8000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000.*LISTENING"') do (
    echo Killing process %%a...
    taskkill /PID %%a /F >nul 2>&1
)

echo Stopping Frontend (port 3000)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":3000.*LISTENING"') do (
    echo Killing process %%a...
    taskkill /PID %%a /F >nul 2>&1
)

REM Also kill by window title as backup
echo.
echo Checking for processes by window title...
taskkill /FI "WINDOWTITLE eq EduLearn Backend*" /T /F >nul 2>&1
taskkill /FI "WINDOWTITLE eq EduLearn Frontend*" /T /F >nul 2>&1

timeout /t 2 /nobreak >nul

REM Verify services stopped
echo.
echo Verifying services stopped...
netstat -ano | findstr ":8000" >nul 2>&1
if errorlevel 1 (
    echo [OK] Backend stopped
) else (
    echo [WARNING] Backend may still be running on port 8000
)

netstat -ano | findstr ":3000" >nul 2>&1
if errorlevel 1 (
    echo [OK] Frontend stopped
) else (
    echo [WARNING] Frontend may still be running on port 3000
)

echo.
echo Services stopped!
echo.
pause