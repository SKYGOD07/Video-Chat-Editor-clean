"""Upload endpoint."""

from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os

from ..models.schemas import UploadResponse
from ..utils.file_manager import FileManager


router = APIRouter(prefix="/api", tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_video(file: UploadFile = File(...)):
    """
    Upload a video file.
    
    Returns:
        UploadResponse with video_id
    """
    # Validate file
    if not FileManager.validate_video_file(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(FileManager.ALLOWED_EXTENSIONS)}"
        )
    
    # Generate video ID
    video_id = FileManager.generate_video_id()
    
    # Save file
    FileManager.ensure_directories()
    file_path = FileManager.get_upload_path(video_id, file.filename)
    
    try:
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)
        
        file_size = len(content)
        
        return UploadResponse(
            video_id=video_id,
            filename=file.filename,
            size=file_size,
            message=f"Video uploaded successfully. ID: {video_id}"
        )
    except Exception as e:
        # Clean up on error
        if os.path.exists(file_path):
            os.remove(file_path)
        
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")
