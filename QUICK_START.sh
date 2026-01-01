#!/bin/bash
# Video Chat Editor - Quick Start Guide

# WINDOWS USERS - RUN ONE OF THESE:
# Option 1: Double-click START_ALL.bat
# Option 2: Run in PowerShell: .\START_ALL.ps1
# Option 3: Run in Command Prompt:
#   cd video-editor-backend
#   set PYTHONPATH=%CD%
#   python run.py
#
#   (in another terminal)
#   cd Video-Chat-Editor
#   npx vite --port 5000

# LINUX/MAC USERS - RUN THESE:
#!/bin/bash

# Terminal 1:
cd video-editor-backend
export PYTHONPATH=$PWD
python3 run.py

# Terminal 2:
cd Video-Chat-Editor
npx vite --port 5000

# ACCESS THE APPLICATION:
# Frontend: http://127.0.0.1:5000
# Backend: http://127.0.0.1:8000
# API Docs: http://127.0.0.1:8000/docs
