"""Download endpoint."""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import os

from ..utils.file_manager import FileManager


router = APIRouter(prefix="/api", tags=["download"])


@router.get("/download/{video_id}")
async def download_video(video_id: str):
    """
    Download processed video.
    
    Returns the latest processed output video.
    """
    FileManager.ensure_directories()
    
    # Find latest output file
    outputs = FileManager.list_outputs(video_id)
    
    if not outputs:
        raise HTTPException(status_code=404, detail=f"No output found for video {video_id}")
    
    # Get most recent file
    latest = max(outputs, key=os.path.getctime)
    
    if not os.path.exists(latest):
        raise HTTPException(status_code=404, detail="Output file not found")
    
    return FileResponse(
        path=latest,
        media_type='video/mp4',
        filename=os.path.basename(latest)
    )


@router.get("/outputs/{video_id}")
async def list_outputs(video_id: str):
    """List all output files for a video."""
    
    FileManager.ensure_directories()
    
    outputs = FileManager.list_outputs(video_id)
    
    return {
        'video_id': video_id,
        'outputs': [
            {
                'filename': os.path.basename(f),
                'size': FileManager.get_file_size(f)
            }
            for f in outputs
        ]
    }
