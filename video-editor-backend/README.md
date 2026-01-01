# Video Editor Backend API

A **FastAPI-based backend** for chat-driven video editing. This backend processes natural language commands to edit videos using FFmpeg, Whisper, and AI analysis.

## Features

✅ **Video Upload** - Upload MP4, AVI, MOV, MKV, WebM files  
✅ **Chat-based Editing** - Natural language commands like "remove silence" or "cut from 00:01:20 to 00:02:10"  
✅ **Operations Supported**:
- Remove silence from video
- Cut/trim segments
- Change playback speed
- Add subtitles (via Whisper transcription)
- Transcribe audio to text
- Resize video
- Reverse video

✅ **Status Tracking** - Monitor processing progress  
✅ **Download Results** - Retrieve processed videos  
✅ **CORS Enabled** - Works with external frontends

## Installation

### 1. Install Dependencies

```bash
# Install Python packages
pip install -r requirements.txt

# Install FFmpeg (required for video processing)
# Windows (using chocolatey):
choco install ffmpeg

# macOS:
brew install ffmpeg

# Linux (Ubuntu/Debian):
sudo apt-get install ffmpeg
```

### 2. Verify FFmpeg Installation

```bash
ffmpeg -version
ffprobe -version
```

## Quick Start

```bash
# Run the backend server
python -m app.main

# Or using Uvicorn directly:
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Server will start at: **http://127.0.0.1:8000**

## API Usage

### 1. Upload Video

```bash
curl -X POST http://127.0.0.1:8000/api/upload \
  -F "file=@your_video.mp4"
```

Response:
```json
{
  "video_id": "550e8400-e29b-41d4-a716-446655440000",
  "filename": "your_video.mp4",
  "size": 104857600,
  "message": "Video uploaded successfully. ID: 550e8400-..."
}
```

### 2. Send Editing Command

```bash
curl -X POST http://127.0.0.1:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "video_id": "550e8400-e29b-41d4-a716-446655440000",
    "message": "remove silence"
  }'
```

Supported commands:
- `"remove silence"` - Remove silent parts
- `"cut from 00:01:20 to 00:02:10"` - Cut specific segment
- `"trim to 60 seconds"` - Keep first N seconds
- `"speed up 1.5x"` - Change playback speed
- `"add subtitles"` - Generate subtitles
- `"transcribe"` - Convert audio to text
- `"resize to 1280x720"` - Resize video

Response:
```json
{
  "status": "success",
  "message": "Silence removed successfully",
  "video_id": "550e8400-...",
  "output_path": "outputs/550e8400-..._no_silence.mp4",
  "operation": "remove_silence"
}
```

### 3. Check Status

```bash
curl http://127.0.0.1:8000/api/status/550e8400-e29b-41d4-a716-446655440000
```

Response:
```json
{
  "video_id": "550e8400-...",
  "status": "complete",
  "progress": 100,
  "current_operation": "remove_silence"
}
```

### 4. Download Result

```bash
curl -o edited_video.mp4 \
  http://127.0.0.1:8000/api/download/550e8400-e29b-41d4-a716-446655440000
```

### 5. List All Outputs

```bash
curl http://127.0.0.1:8000/api/outputs/550e8400-e29b-41d4-a716-446655440000
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API info and available endpoints |
| GET | `/health` | Health check |
| POST | `/api/upload` | Upload video file |
| POST | `/api/chat` | Send editing command |
| GET | `/api/status/{video_id}` | Get processing status |
| GET | `/api/download/{video_id}` | Download processed video |
| GET | `/api/outputs/{video_id}` | List output files |

## Project Structure

```
video-editor-backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── api/
│   │   ├── upload.py          # Upload endpoint
│   │   ├── chat.py            # Chat/edit endpoint
│   │   ├── status.py          # Status endpoint
│   │   └── download.py        # Download endpoint
│   ├── core/
│   │   ├── command_parser.py   # Parse natural language
│   │   ├── ffmpeg_engine.py    # Video processing
│   │   ├── whisper_engine.py   # Speech-to-text
│   │   └── silence_remover.py  # Silence detection
│   ├── models/
│   │   └── schemas.py          # Pydantic models
│   └── utils/
│       └── file_manager.py     # File operations
├── uploads/                    # Uploaded videos
├── outputs/                    # Processed videos
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Environment Variables

Create a `.env` file (optional):

```env
# API Configuration
HOST=127.0.0.1
PORT=8000

# Whisper Model (tiny, base, small, medium, large)
WHISPER_MODEL=base
```

## Frontend Integration

### JavaScript Example

```javascript
// Upload video
const formData = new FormData();
formData.append('file', videoFile);

const uploadRes = await fetch('http://127.0.0.1:8000/api/upload', {
  method: 'POST',
  body: formData
});

const { video_id } = await uploadRes.json();

// Send editing command
const chatRes = await fetch('http://127.0.0.1:8000/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    video_id,
    message: 'remove silence'
  })
});

const result = await chatRes.json();
console.log(result);
```

## Troubleshooting

### FFmpeg Not Found
```bash
# Install FFmpeg or add to PATH
# Windows: choco install ffmpeg
# macOS: brew install ffmpeg
# Linux: sudo apt-get install ffmpeg
```

### Whisper Model Too Large
The first time you use Whisper, it downloads a model (~140MB for 'base'). This is normal.

Use smaller model:
```python
# In app/core/whisper_engine.py
MODEL = "tiny"  # 39MB, faster
```

### CORS Errors
Already configured for all origins. If issues persist, check frontend URL.

## Performance Tips

1. **Optimize Input Videos** - Use MP4 with H.264 codec
2. **Reduce Resolution** - Resize before processing
3. **Use Smaller Whisper Model** - `tiny` or `base` for speed
4. **Async Processing** - Redesign for background tasks (Celery/RQ)

## Future Enhancements

- [ ] Background task processing (Celery/Redis)
- [ ] Batch operations
- [ ] Video effects (blur, filters)
- [ ] Audio mixing/ducking
- [ ] Real-time preview
- [ ] Database storage (PostgreSQL)
- [ ] User authentication
- [ ] S3 integration for large files

## License

MIT

## Support

For issues or questions, check the API docs at: **http://127.0.0.1:8000/docs**

This includes an interactive Swagger UI for testing all endpoints!
