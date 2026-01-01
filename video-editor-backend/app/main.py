"""FastAPI main application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from .api import upload, chat, status, download
from .core.ffmpeg_engine import FFmpegEngine
from .utils.file_manager import FileManager


# Initialize FastAPI app
app = FastAPI(
    title="Video Editor API",
    description="Chat-based AI video editing backend",
    version="1.0.0"
)

# Enable CORS for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(upload.router)
app.include_router(chat.router)
app.include_router(status.router)
app.include_router(download.router)


@app.on_event("startup")
async def startup_event():
    """Initialize on startup."""
    FileManager.ensure_directories()
    
    # Check FFmpeg
    if not FFmpegEngine.check_installed():
        print("⚠️  FFmpeg not installed. Install it to use video processing features.")
    else:
        print("✓ FFmpeg is available")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Video Editor API",
        "endpoints": {
            "upload": "POST /api/upload",
            "chat": "POST /api/chat",
            "status": "GET /api/status/{video_id}",
            "download": "GET /api/download/{video_id}",
            "outputs": "GET /api/outputs/{video_id}"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "ffmpeg_installed": FFmpegEngine.check_installed()
    }


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
