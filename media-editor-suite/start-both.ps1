#!/bin/bash
# Windows PowerShell script to run both projects

Write-Host "======================================"
Write-Host "Media Editor Suite - Project Launcher"
Write-Host "======================================"
Write-Host ""

# Check if both projects exist
if (-not (Test-Path "video-editor")) {
    Write-Host "ERROR: video-editor folder not found!" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "audio-editor")) {
    Write-Host "ERROR: audio-editor folder not found!" -ForegroundColor Red
    exit 1
}

Write-Host "Opening both projects in separate terminals..." -ForegroundColor Green
Write-Host ""

# Start Video Editor in new PowerShell window
Write-Host "Starting Video Editor on port 5173 (frontend) and 3000 (backend)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD/video-editor'; npm run dev"

# Wait a bit before starting second terminal
Start-Sleep -Seconds 2

# Start Audio Editor in new PowerShell window
Write-Host "Starting Audio Editor on port 5174 (frontend) and 3001 (backend)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD/audio-editor'; npm run dev"

Write-Host ""
Write-Host "======================================"
Write-Host "Both projects are starting!"
Write-Host "======================================"
Write-Host ""
Write-Host "Video Editor:  http://localhost:5173"
Write-Host "Audio Editor:  http://localhost:5174"
Write-Host ""
Write-Host "Press Ctrl+C in each terminal to stop the respective server"
Write-Host ""
