@echo off
REM Start Backend and Frontend servers for Video Chat Editor

setlocal enabledelayedexpansion

echo ============================================
echo Video Chat Editor - Full Stack Startup
echo ============================================
echo.

REM Start Backend in new window
echo [1/2] Starting FastAPI Backend on http://127.0.0.1:8000...
cd /d "%~dp0video-editor-backend"
set PYTHONPATH=%CD%
start "Backend Server" python run.py

timeout /t 3

REM Start Frontend in new window
echo [2/2] Starting React Frontend on http://127.0.0.1:5000...
cd /d "%~dp0Video-Chat-Editor"
start "Frontend Server" cmd /k "npx vite --port 5000"

echo.
echo ============================================
echo ✓ Both servers are starting...
echo ============================================
echo Frontend:  http://127.0.0.1:5000
echo Backend:   http://127.0.0.1:8000
echo ============================================
echo.
echo Close either window to stop that server
pause
