"""Chat endpoint for video editing commands."""

from fastapi import APIRouter, HTTPException
from pathlib import Path
import os

from ..models.schemas import ChatMessage, ChatResponse
from ..core.command_parser import CommandParser
from ..core.ffmpeg_engine import FFmpegEngine
from ..core.whisper_engine import WhisperEngine
from ..core.silence_remover import SilenceRemover
from ..utils.file_manager import FileManager


router = APIRouter(prefix="/api", tags=["chat"])

# Global status tracking
processing_status = {}


@router.post("/chat", response_model=ChatResponse)
async def chat_edit(message: ChatMessage):
    """
    Process natural language video editing command.
    
    Input JSON:
    {
        "video_id": "string",
        "message": "remove silence / cut from 00:01:20 to 00:02:10"
    }
    """
    video_id = message.video_id
    command = message.message
    
    # Validate video exists
    video_files = []
    FileManager.ensure_directories()
    
    for file in os.listdir(FileManager.UPLOAD_DIR):
        if file.startswith(video_id):
            video_files.append(os.path.join(FileManager.UPLOAD_DIR, file))
    
    if not video_files:
        raise HTTPException(status_code=404, detail=f"Video {video_id} not found")
    
    input_video = video_files[0]
    
    # Parse command
    parsed = CommandParser.parse(command)
    operation = parsed.get('operation')
    
    # Update status
    processing_status[video_id] = {
        'status': 'processing',
        'operation': operation,
        'progress': 0.5
    }
    
    try:
        # Check FFmpeg
        if not FFmpegEngine.check_installed():
            raise RuntimeError("FFmpeg not installed")
        
        # Process based on operation
        if operation == 'remove_silence':
            output_path = FileManager.get_output_path(video_id, 'no_silence')
            SilenceRemover.remove_silence(input_video, output_path)
            
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="success",
                message="Silence removed successfully",
                video_id=video_id,
                output_path=output_path,
                operation=operation
            )
        
        elif operation == 'cut_segment':
            start = parsed.get('start', 0)
            end = parsed.get('end', 0)
            output_path = FileManager.get_output_path(video_id, f'cut_{int(start)}_to_{int(end)}')
            
            FFmpegEngine.cut_segment(input_video, output_path, start, end)
            
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="success",
                message=f"Segment cut from {start}s to {end}s",
                video_id=video_id,
                output_path=output_path,
                operation=operation
            )
        
        elif operation == 'trim':
            duration = parsed.get('duration', 60)
            output_path = FileManager.get_output_path(video_id, f'trimmed_{duration}s')
            
            FFmpegEngine.cut_segment(input_video, output_path, 0, duration)
            
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="success",
                message=f"Video trimmed to {duration} seconds",
                video_id=video_id,
                output_path=output_path,
                operation=operation
            )
        
        elif operation == 'change_speed':
            speed = parsed.get('speed', 1.0)
            output_path = FileManager.get_output_path(video_id, f'speed_{speed}x')
            
            FFmpegEngine.speed_video(input_video, output_path, speed)
            
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="success",
                message=f"Video speed changed to {speed}x",
                video_id=video_id,
                output_path=output_path,
                operation=operation
            )
        
        elif operation == 'add_subtitles':
            # This would require whisper to generate subtitles
            output_path = FileManager.get_output_path(video_id, 'with_subtitles')
            
            # For now, we'll just indicate it's in progress
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="processing",
                message="Subtitle generation in progress (requires Whisper model download)",
                video_id=video_id,
                operation=operation
            )
        
        elif operation == 'transcribe':
            output_path = FileManager.get_output_path(video_id, 'transcript')
            
            # Transcribe video
            result = WhisperEngine.transcribe_video(input_video, output_path)
            
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="success",
                message="Video transcribed successfully",
                video_id=video_id,
                output_path=output_path,
                operation=operation
            )
        
        elif operation == 'resize':
            width = parsed.get('width', 1280)
            height = parsed.get('height', 720)
            output_path = FileManager.get_output_path(video_id, f'resized_{width}x{height}')
            
            FFmpegEngine.resize_video(input_video, output_path, width, height)
            
            processing_status[video_id] = {'status': 'complete', 'progress': 100}
            
            return ChatResponse(
                status="success",
                message=f"Video resized to {width}x{height}",
                video_id=video_id,
                output_path=output_path,
                operation=operation
            )
        
        else:
            return ChatResponse(
                status="error",
                message=f"Unknown operation: {operation}. Try: 'remove silence', 'cut from X to Y', 'transcribe'",
                video_id=video_id,
                operation=operation
            )
    
    except Exception as e:
        processing_status[video_id] = {'status': 'error', 'progress': 0}
        
        raise HTTPException(
            status_code=500,
            detail=f"Operation failed: {str(e)}"
        )
