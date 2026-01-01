@echo off
REM Batch script to run both projects

echo ======================================
echo Media Editor Suite - Project Launcher
echo ======================================
echo.

REM Check if both projects exist
if not exist "video-editor" (
    echo ERROR: video-editor folder not found!
    exit /b 1
)

if not exist "audio-editor" (
    echo ERROR: audio-editor folder not found!
    exit /b 1
)

echo Opening both projects in separate terminals...
echo.

REM Start Video Editor in new terminal
echo Starting Video Editor on port 5173 (frontend) and 3000 (backend)...
start "Video Editor" cmd /k "cd video-editor && npm run dev"

timeout /t 2 /nobreak

REM Start Audio Editor in new terminal
echo Starting Audio Editor on port 5174 (frontend) and 3001 (backend)...
start "Audio Editor" cmd /k "cd audio-editor && npm run dev"

echo.
echo ======================================
echo Both projects are starting!
echo ======================================
echo.
echo Video Editor:  http://localhost:5173
echo Audio Editor:  http://localhost:5174
echo.
echo Press Ctrl+C in each terminal to stop the respective server
echo.
pause
