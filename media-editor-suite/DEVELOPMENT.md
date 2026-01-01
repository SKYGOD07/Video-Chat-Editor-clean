# Media Editor Suite Development Guide

## Quick Start

### 1. Setup Python Environment
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install Python dependencies
pip install ffmpeg-python openai-whisper torch
```

### 2. Install Project Dependencies
```bash
# Install root dependencies (optional, for workspace management)
npm install

# Install video editor dependencies
cd video-editor
npm install
cd ..

# Install audio editor dependencies
cd audio-editor
npm install
cd ..
```

### 3. Start Development

**Terminal 1 - Video Editor:**
```bash
cd video-editor
npm run dev
```

**Terminal 2 - Audio Editor:**
```bash
cd audio-editor
npm run dev
```

## Project Organization

Both projects are now organized as separate modules within the unified suite, with:
- Shared Python virtual environment (`.venv/`)
- Independent Node package installations
- Separate databases (configure in each project's drizzle.config.ts)
- Shared development tooling

## Common Tasks

### Type Checking
```bash
npm run check:video  # Check Video Editor types
npm run check:audio  # Check Audio Editor types
```

### Database Migrations
```bash
npm run db:push:video  # Push Video Editor schema
npm run db:push:audio  # Push Audio Editor schema
```

### Building for Production
```bash
npm run build:video  # Build Video Editor
npm run build:audio  # Build Audio Editor
```

## File Structure

```
media-editor-suite/
├── .venv/                    # Python virtual environment
├── video-editor/             # Video editing application
│   ├── client/
│   │   ├── src/
│   │   │   ├── App.tsx
│   │   │   ├── main.tsx
│   │   │   ├── components/
│   │   │   ├── hooks/
│   │   │   ├── pages/
│   │   │   └── lib/
│   │   └── index.html
│   ├── server/
│   │   ├── index.ts
│   │   ├── routes.ts
│   │   ├── db.ts
│   │   ├── py/
│   │   │   └── processor.py  # Python video processing
│   │   └── static.ts
│   ├── shared/
│   ├── script/
│   └── package.json
├── audio-editor/             # Audio editing application
│   ├── client/
│   ├── server/
│   ├── shared/
│   ├── script/
│   └── package.json
├── README.md
├── package.json
└── media-editor-suite.code-workspace
```

## Troubleshooting

### FFmpeg Not Found
Ensure FFmpeg is installed and in your system PATH:
- Download from [ffmpeg.org](https://ffmpeg.org/download.html)
- Add to Windows PATH environment variable

### Python Dependencies
If Python packages fail to install:
```bash
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install ffmpeg-python openai-whisper torch
```

### Port Conflicts
If development servers fail to start:
- Video Editor typically runs on port 5173 (Vite) and 3000 (server)
- Audio Editor typically runs on port 5174 (Vite) and 3001 (server)
- Check ports are available or modify vite.config.ts
