# Video Chat Editor - Full Stack Startup Script

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Video Chat Editor - Full Stack Startup" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

$scriptPath = Split-Path -Parent -Path $MyInvocation.MyCommand.Definition
$backendPath = Join-Path $scriptPath "video-editor-backend"
$frontendPath = Join-Path $scriptPath "Video-Chat-Editor"

# Start Backend
Write-Host "[1/2] Starting FastAPI Backend..." -ForegroundColor Yellow
Push-Location $backendPath
$env:PYTHONPATH = $backendPath

# Start backend in a separate PowerShell window
$backendArgs = @(
    "-NoExit"
    "-Command"
    "cd '$backendPath'; `$env:PYTHONPATH='$backendPath'; python run.py"
)
Start-Process powershell -ArgumentList $backendArgs -WindowStyle Normal

Start-Sleep -Seconds 3

# Start Frontend
Write-Host "[2/2] Starting React Frontend..." -ForegroundColor Yellow
Push-Location $frontendPath

$frontendArgs = @(
    "-NoExit"
    "-Command"
    "cd '$frontendPath'; npx vite --port 5000"
)
Start-Process powershell -ArgumentList $frontendArgs -WindowStyle Normal

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "✓ Both servers are starting..." -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:  http://127.0.0.1:5000" -ForegroundColor Cyan
Write-Host "Backend:   http://127.0.0.1:8000" -ForegroundColor Cyan
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Waiting for servers to start..." -ForegroundColor Yellow

# Wait and check if servers are running
$maxWait = 30
$elapsed = 0
$backendReady = $false
$frontendReady = $false

while (($elapsed -lt $maxWait) -and (-not $backendReady -or -not $frontendReady)) {
    Start-Sleep -Seconds 1
    $elapsed += 1
    
    # Check backend
    $backendTest = Test-NetConnection -ComputerName 127.0.0.1 -Port 8000 -InformationLevel Quiet 2>&1 | Select-String "True" -Quiet
    if ($backendTest) { $backendReady = $true }
    
    # Check frontend
    $frontendTest = Test-NetConnection -ComputerName 127.0.0.1 -Port 5000 -InformationLevel Quiet 2>&1 | Select-String "True" -Quiet
    if ($frontendTest) { $frontendReady = $true }
}

Write-Host ""
if ($backendReady) {
    Write-Host "✓ Backend is ready at http://127.0.0.1:8000" -ForegroundColor Green
} else {
    Write-Host "⚠ Backend may still be starting..." -ForegroundColor Yellow
}

if ($frontendReady) {
    Write-Host "✓ Frontend is ready at http://127.0.0.1:5000" -ForegroundColor Green
} else {
    Write-Host "⚠ Frontend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Opening application in browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 2
Start-Process "http://127.0.0.1:5000"
