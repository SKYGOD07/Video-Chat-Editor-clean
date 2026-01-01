# Quick Start Guide

## Media Editor Suite - Running Both Projects

### Prerequisites Checklist

- ✅ Node.js 18+ installed
- ✅ Python 3.11+ installed  
- ✅ FFmpeg installed and in PATH
- ✅ PostgreSQL running (optional, for database features)

## Option 1: Run Both Projects Together (Recommended)

### Windows - Double-click to launch:
```
start-both.bat
```

**Or from PowerShell:**
```bash
.\start-both.ps1
```

This will open two separate terminal windows:
- **Video Editor**: http://localhost:5173
- **Audio Editor**: http://localhost:5174

---

## Option 2: Run Projects Individually

### Video Editor Only

```bash
cd video-editor
npm run dev
```

**Starts on:**
- Frontend: http://localhost:5173
- Backend: http://localhost:3000

### Audio Editor Only

```bash
cd audio-editor
npm run dev
```

**Starts on:**
- Frontend: http://localhost:5174
- Backend: http://localhost:3001

---

## Option 3: Run from Root Directory

### Both projects with single commands:

```bash
# Terminal 1 - Video Editor
npm run dev:video

# Terminal 2 - Audio Editor (in another terminal)
npm run dev:audio
```

---

## First Time Setup

### 1. Install Python Dependencies (One Time)

```bash
# Activate shared virtual environment
.\.venv\Scripts\Activate.ps1

# Install Python packages
pip install ffmpeg-python openai-whisper torch
```

### 2. Install Node Dependencies (One Time)

```bash
# Video Editor
cd video-editor
npm install
cd ..

# Audio Editor
cd audio-editor
npm install
cd ..
```

---

## Available Commands

### From Root Directory (media-editor-suite/)

```bash
# Development
npm run dev:video          # Start Video Editor
npm run dev:audio          # Start Audio Editor

# Build
npm run build:video        # Build Video Editor
npm run build:audio        # Build Audio Editor

# Type checking
npm run check:video        # Check Video Editor types
npm run check:audio        # Check Audio Editor types

# Database
npm run db:push:video      # Push Video Editor schema
npm run db:push:audio      # Push Audio Editor schema
```

### From Project Directory (video-editor/ or audio-editor/)

```bash
npm run dev                # Start development server
npm run build              # Build for production
npm start                  # Start production server
npm run check              # Type check
npm run db:push            # Push database schema
```

---

## Port Assignments

| Component | Port | URL |
|-----------|------|-----|
| Video Editor Frontend | 5173 | http://localhost:5173 |
| Video Editor Backend | 3000 | http://localhost:3000 |
| Audio Editor Frontend | 5174 | http://localhost:5174 |
| Audio Editor Backend | 3001 | http://localhost:3001 |

---

## Project Structure

```
media-editor-suite/
├── .venv/                        # Shared Python environment
├── video-editor/                 # Video editing application
│   ├── client/                  # React frontend (port 5173)
│   ├── server/                  # Express backend (port 3000)
│   └── package.json
├── audio-editor/                 # Audio editing application
│   ├── client/                  # React frontend (port 5174)
│   ├── server/                  # Express backend (port 3001)
│   └── package.json
├── start-both.bat               # Windows batch launcher
├── start-both.ps1               # PowerShell launcher
├── package.json                 # Root workspace config
└── README.md                    # Main documentation
```

---

## Troubleshooting

### Port Already in Use

If you get a "port already in use" error:

**Option 1:** Stop the process using the port
```bash
# Find what's using the port (PowerShell)
Get-Process | Where-Object {$_.Name -like "*node*"}
```

**Option 2:** Change ports in `vite.config.ts`
```typescript
server: {
  port: 5175,  // Change this number
  proxy: {
    '/api': 'http://localhost:3002'  // Update backend port too
  }
}
```

### FFmpeg Not Found

```bash
# Verify FFmpeg is installed
ffmpeg -version

# If not installed:
# Windows: Download from https://ffmpeg.org/download.html
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

### Python Dependency Issues

```bash
# Reinstall Python packages
pip install --upgrade ffmpeg-python openai-whisper torch

# Or if above fails, try:
pip install --force-reinstall ffmpeg-python openai-whisper torch
```

### Database Connection Error

```bash
# Ensure PostgreSQL is running, then:
cd video-editor
npm run db:push

cd ../audio-editor
npm run db:push
```

---

## Development Tips

1. **Use VS Code workspace** for better multi-project experience:
   ```bash
   code media-editor-suite.code-workspace
   ```

2. **Keep terminal windows open** to see real-time logs

3. **Hot reload enabled** - Changes auto-refresh in browser (Vite)

4. **TypeScript checking** - Run `npm run check` before committing

5. **File uploads** go to:
   - Video Editor: `video-editor/uploads/`
   - Audio Editor: `audio-editor/uploads/`

---

## Next Steps

- 📖 Read [README.md](README.md) for detailed documentation
- 📚 Check [DEVELOPMENT.md](DEVELOPMENT.md) for advanced setup
- 🎬 Open Video Editor: http://localhost:5173
- 🎙️ Open Audio Editor: http://localhost:5174

---

**Enjoy editing!** 🚀
