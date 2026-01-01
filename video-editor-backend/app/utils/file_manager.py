"""File management utilities."""

import os
import uuid
from pathlib import Path


class FileManager:
    """Handles file operations."""
    
    UPLOAD_DIR = "uploads"
    OUTPUT_DIR = "outputs"
    ALLOWED_EXTENSIONS = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv'}
    
    @staticmethod
    def generate_video_id() -> str:
        """Generate unique video ID."""
        return str(uuid.uuid4())
    
    @staticmethod
    def ensure_directories():
        """Ensure upload and output directories exist."""
        os.makedirs(FileManager.UPLOAD_DIR, exist_ok=True)
        os.makedirs(FileManager.OUTPUT_DIR, exist_ok=True)
    
    @staticmethod
    def get_upload_path(video_id: str, filename: str) -> str:
        """Get full path for uploaded video."""
        return os.path.join(FileManager.UPLOAD_DIR, f"{video_id}_{filename}")
    
    @staticmethod
    def get_output_path(video_id: str, operation: str) -> str:
        """Get output path for processed video."""
        return os.path.join(FileManager.OUTPUT_DIR, f"{video_id}_{operation}.mp4")
    
    @staticmethod
    def get_temp_path(video_id: str, suffix: str) -> str:
        """Get temporary file path."""
        return os.path.join(FileManager.OUTPUT_DIR, f"{video_id}_{suffix}.tmp")
    
    @staticmethod
    def validate_video_file(filename: str) -> bool:
        """Validate if file is a video."""
        ext = Path(filename).suffix.lower()
        return ext in FileManager.ALLOWED_EXTENSIONS
    
    @staticmethod
    def file_exists(path: str) -> bool:
        """Check if file exists."""
        return os.path.isfile(path)
    
    @staticmethod
    def get_file_size(path: str) -> int:
        """Get file size in bytes."""
        if os.path.exists(path):
            return os.path.getsize(path)
        return 0
    
    @staticmethod
    def cleanup_file(path: str) -> bool:
        """Delete a file."""
        try:
            if os.path.exists(path):
                os.remove(path)
            return True
        except Exception:
            return False
    
    @staticmethod
    def list_outputs(video_id: str) -> list[str]:
        """List all outputs for a video."""
        outputs = []
        if os.path.exists(FileManager.OUTPUT_DIR):
            for file in os.listdir(FileManager.OUTPUT_DIR):
                if file.startswith(video_id):
                    outputs.append(os.path.join(FileManager.OUTPUT_DIR, file))
        return outputs
