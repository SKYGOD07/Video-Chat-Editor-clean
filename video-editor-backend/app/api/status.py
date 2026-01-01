"""Status endpoint."""

from fastapi import APIRouter, HTTPException
import os

from app.models.schemas import StatusResponse
from app.utils.file_manager import FileManager


router = APIRouter(prefix="/api", tags=["status"])

# Global status tracking
processing_status = {}


@router.get("/status/{video_id}", response_model=StatusResponse)
async def get_status(video_id: str):
    """Get processing status of a video."""
    
    # Check if video exists
    FileManager.ensure_directories()
    
    video_exists = False
    for file in os.listdir(FileManager.UPLOAD_DIR):
        if file.startswith(video_id):
            video_exists = True
            break
    
    if not video_exists and video_id not in processing_status:
        raise HTTPException(status_code=404, detail=f"Video {video_id} not found")
    
    # Get status
    status = processing_status.get(video_id, {
        'status': 'ready',
        'progress': 0,
        'operation': None
    })
    
    return StatusResponse(
        video_id=video_id,
        status=status.get('status', 'unknown'),
        progress=status.get('progress', 0),
        current_operation=status.get('operation')
    )
