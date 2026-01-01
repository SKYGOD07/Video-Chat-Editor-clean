# Video Chat Editor - Complete Setup Guide

## ✅ Project Structure

```
Video-Chat-Editor-clean/
├── Video-Chat-Editor/          # Full-stack application
│   ├── client/                 # React frontend (Vite)
│   ├── server/                 # TypeScript server
│   ├── shared/                 # Shared types/schemas
│   ├── vite.config.ts          # Frontend Vite config
│   ├── package.json            # Node dependencies
│   └── ...other configs
│
├── video-editor-backend/       # Python FastAPI backend
│   ├── app/
│   │   ├── api/                # API endpoints (upload, chat, download, status)
│   │   ├── core/               # Core engines (FFmpeg, Whisper, Command Parser)
│   │   ├── models/             # Pydantic schemas
│   │   ├── utils/              # File management utilities
│   │   └── main.py             # FastAPI application
│   ├── run.py                  # Server launcher
│   ├── requirements.txt        # Python dependencies
│   ├── outputs/                # Processed video outputs
│   └── uploads/                # Uploaded video files
│
├── START_ALL.bat               # Windows startup script
├── START_ALL.ps1               # PowerShell startup script
└── README.md                   # This file
```

## 🚀 Quick Start

### Option 1: Using PowerShell (Recommended)
```powershell
# From project root
.\START_ALL.ps1
```

### Option 2: Using Command Prompt
```batch
# From project root
START_ALL.bat
```

### Option 3: Manual Start

**Terminal 1 - Backend:**
```bash
cd video-editor-backend
set PYTHONPATH=%CD%
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd Video-Chat-Editor
npx vite --port 5000
```

## 📡 Server URLs

- **Frontend (React + Vite)**: http://127.0.0.1:5000
- **Backend API (FastAPI)**: http://127.0.0.1:8000
- **API Docs**: http://127.0.0.1:8000/docs (Swagger UI)

## 🔧 System Requirements

- **Node.js** 18+ (for frontend)
- **Python** 3.10+ (for backend)
- **FFmpeg** (optional, for video processing)
  - Windows: `choco install ffmpeg -y`
  - macOS: `brew install ffmpeg`
  - Linux: `sudo apt-get install ffmpeg`

## 📦 Dependencies

### Backend
```
fastapi
uvicorn
python-multipart
ffmpeg-python
openai-whisper
silero-vad
torch
numpy
pydantic
python-dotenv
```

### Frontend
- React 18
- TypeScript
- Tailwind CSS
- Vite
- Shadcn/UI components
- Wouter (routing)
- Lucide icons

## 🎯 Features

### Frontend
- ✅ Video upload with drag-and-drop
- ✅ Chat interface for editing commands
- ✅ Quick command templates
- ✅ Real-time message display
- ✅ Download processed videos
- ✅ Loading states and error handling

### Backend
- ✅ Video upload endpoint (`POST /api/upload`)
- ✅ Chat processing endpoint (`POST /api/chat`)
- ✅ Status tracking (`GET /api/status/{video_id}`)
- ✅ Video download (`GET /api/download/{video_id}`)
- ✅ FFmpeg integration (cut, trim, speed, resize)
- ✅ Whisper transcription
- ✅ Silence detection and removal
- ✅ CORS enabled for frontend integration

## 🛠️ Configuration

### Backend Configuration
- **Host**: 127.0.0.1 (localhost only)
- **Port**: 8000
- **Upload directory**: `video-editor-backend/uploads/`
- **Output directory**: `video-editor-backend/outputs/`

### Frontend Configuration
- **Host**: 127.0.0.1
- **Port**: 5000
- **Backend API**: http://127.0.0.1:8000

## 📝 API Examples

### Upload Video
```bash
curl -X POST "http://127.0.0.1:8000/api/upload" \
  -F "file=@video.mp4"
```

### Send Chat Command
```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "your-video-id",
    "message": "remove silence"
  }'
```

### Check Status
```bash
curl "http://127.0.0.1:8000/api/status/your-video-id"
```

### Download Result
```bash
curl "http://127.0.0.1:8000/api/download/your-video-id" \
  -o output.mp4
```

## 🐛 Troubleshooting

### Backend won't start
- Ensure Python 3.10+ is installed
- Check PYTHONPATH is set to backend directory
- Verify all dependencies: `pip install -r requirements.txt`

### Frontend won't start
- Clear node_modules: `rm -r node_modules && npm install`
- Ensure Node.js 18+ is installed
- Check port 5000 is not in use

### FFmpeg not found
- Backend will show warning but continue
- Video processing will fail until FFmpeg is installed
- This is optional for API testing

### CORS errors
- Backend has CORS enabled for all origins
- Check if both servers are running
- Verify API URLs match in frontend code

## 🔌 Environment Variables

### Backend
- `PYTHONPATH`: Points to project root (set automatically by `run.py`)

### Frontend
- No additional environment variables needed
- Backend API URL: `http://127.0.0.1:8000` (configured in editor.tsx)

## 📚 File Structure Reference

### Key Backend Files
- `app/main.py` - FastAPI app setup
- `app/api/upload.py` - Video upload handler
- `app/api/chat.py` - Chat command processor
- `app/core/command_parser.py` - Natural language to commands
- `app/core/ffmpeg_engine.py` - FFmpeg operations
- `app/core/whisper_engine.py` - Transcription

### Key Frontend Files
- `client/src/App.tsx` - Main router
- `client/src/pages/home.tsx` - Landing page
- `client/src/pages/editor.tsx` - Video editor interface
- `vite.config.ts` - Vite configuration

## 🎬 Supported Video Formats
- MP4
- AVI
- MOV
- MKV
- WebM
- FLV

## ✨ Supported Editing Operations
1. **Remove Silence** - Automatically detects and removes silent sections
2. **Cut Segment** - Cut video from X to Y seconds
3. **Trim** - Keep first N seconds
4. **Change Speed** - Speed up or slow down playback
5. **Transcribe** - Generate transcript using Whisper AI
6. **Add Subtitles** - Create subtitle file from transcription
7. **Resize** - Change video dimensions
8. **Reverse** - Play video in reverse

## 📖 Next Steps

1. **Run both servers** using startup scripts
2. **Open frontend** at http://127.0.0.1:5000
3. **Upload a test video** using the interface
4. **Send editing commands** via chat
5. **Download the processed video**

## 🤝 Integration Points

The frontend and backend communicate via:
- **REST API** with JSON payloads
- **File uploads** via multipart/form-data
- **CORS** enabled for cross-origin requests
- **Automatic video_id** tracking for all operations

## 📞 Support

If you encounter issues:
1. Check both servers are running (8000 and 5000)
2. Verify Python and Node.js versions
3. Clear caches and reinstall dependencies
4. Check FFmpeg installation for video processing
5. Review error messages in server terminals

---

**Version**: 1.0  
**Last Updated**: January 1, 2026  
**Status**: ✅ Ready for Testing
