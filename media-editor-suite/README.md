# Media Editor Suite

A unified project containing two complementary media editing applications:

## Projects

### 1. Video Editor (`video-editor/`)
A full-featured video editing application with support for:
- Video processing and manipulation
- Silence removal
- Subtitle generation using Whisper AI
- Video cutting and trimming
- FFmpeg-based video operations

### 2. Audio Editor (`audio-editor/`)
A podcast and audio editing application with capabilities for:
- Audio processing
- Podcast optimization
- Voice processing
- Audio-video synchronization

## Project Structure

```
media-editor-suite/
├── .venv/                 # Shared Python virtual environment
├── video-editor/          # Video editing application
│   ├── client/           # React frontend
│   ├── server/           # Node.js/Express backend
│   ├── shared/           # Shared types and schemas
│   └── package.json
├── audio-editor/          # Audio editing application
│   ├── client/           # React frontend
│   ├── server/           # Node.js/Express backend
│   ├── shared/           # Shared types and schemas
│   └── package.json
└── README.md             # This file
```

## Quick Start

**For a fast setup guide, see [QUICKSTART.md](QUICKSTART.md)**

### Fastest Way to Run Both:

**Windows:**
```bash
.\start-both.bat
```

**PowerShell:**
```bash
.\start-both.ps1
```

This opens both projects in separate windows with one command!

---

## Setup

### Prerequisites
- Node.js 18+
- Python 3.11+
- FFmpeg (for video processing)
- PostgreSQL (optional, for database)

### Installation

1. **Install Python dependencies (one time):**
   ```bash
   .\.venv\Scripts\Activate.ps1
   pip install ffmpeg-python openai-whisper torch
   ```

2. **Install Node dependencies:**
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

## Development

### Start Both Projects Together
```bash
.\start-both.bat    # Windows
# OR
.\start-both.ps1    # PowerShell
```

**Access:**
- Video Editor: http://localhost:5173
- Audio Editor: http://localhost:5174

### Run Individual Projects

**Video Editor:**
```bash
cd video-editor
npm run dev
```

**Audio Editor:**
```bash
cd audio-editor
npm run dev
```

### From Root Directory

```bash
npm run dev:video    # Video Editor
npm run dev:audio    # Audio Editor
npm run build:video  # Build Video Editor
npm run build:audio  # Build Audio Editor
```

## Database

Both projects use Drizzle ORM. To push schema changes:

```bash
cd video-editor
npm run db:push

# or

cd audio-editor
npm run db:push
```

## License

MIT
