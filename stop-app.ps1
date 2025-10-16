# EduLearn Cloud App Stop Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduLearn Cloud App - Stopping..." -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Stopping Python processes (Backend)..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.MainWindowTitle -like "*EduLearn*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process | Where-Object {$_.ProcessName -eq "python" -and $_.CommandLine -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Write-Host "Stopping Node processes (Frontend)..." -ForegroundColor Yellow
Get-Process | Where-Object {$_.ProcessName -eq "node" -and $_.MainWindowTitle -like "*EduLearn*"} | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process | Where-Object {$_.ProcessName -eq "node" -and $_.CommandLine -like "*react-scripts*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

Write-Host ""
Write-Host "Services stopped!" -ForegroundColor Green
Write-Host ""
Read-Host "Press Enter to exit"
