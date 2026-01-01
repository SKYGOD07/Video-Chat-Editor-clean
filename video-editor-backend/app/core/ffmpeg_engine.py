"""FFmpeg video processing engine."""

import subprocess
import json
import os
from typing import Optional


class FFmpegEngine:
    """Handles all FFmpeg operations."""
    
    FFMPEG_CMD = None
    FFPROBE_CMD = None
    
    @staticmethod
    def _find_ffmpeg():
        """Find FFmpeg executable - check local installation first, then system PATH."""
        if FFmpegEngine.FFMPEG_CMD is not None:
            return
        
        # Check local installation in Video-Chat-Editor-clean folder
        local_paths = [
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "ffmpeg-8.0.1", "bin", "ffmpeg.exe"),
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "ffmpeg-8.0.1", "bin", "ffmpeg"),
        ]
        
        for path in local_paths:
            if os.path.exists(path):
                FFmpegEngine.FFMPEG_CMD = path
                ffprobe_path = path.replace("ffmpeg", "ffprobe")
                FFmpegEngine.FFPROBE_CMD = ffprobe_path
                return
        
        # Fallback to system PATH
        FFmpegEngine.FFMPEG_CMD = "ffmpeg"
        FFmpegEngine.FFPROBE_CMD = "ffprobe"
    
    @staticmethod
    def check_installed() -> bool:
        """Check if FFmpeg is installed."""
        FFmpegEngine._find_ffmpeg()
        try:
            subprocess.run([FFmpegEngine.FFMPEG_CMD, '-version'], capture_output=True, check=True)
            subprocess.run([FFmpegEngine.FFPROBE_CMD, '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def get_duration(video_path: str) -> float:
        """Get video duration in seconds."""
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFPROBE_CMD,
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return float(data['format']['duration'])
        except Exception as e:
            raise RuntimeError(f"Failed to get duration: {e}")
    
    @staticmethod
    def cut_segment(input_path: str, output_path: str, start: float, end: float) -> bool:
        """
        Cut a segment from video.
        
        Args:
            input_path: Input video
            output_path: Output video
            start: Start time in seconds
            end: End time in seconds
        """
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFMPEG_CMD,
            '-i', input_path,
            '-ss', str(start),
            '-to', str(end),
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to cut segment: {e.stderr.decode()}")
    
    @staticmethod
    def concatenate_videos(input_files: list[str], output_path: str) -> bool:
        """
        Concatenate multiple videos.
        
        Args:
            input_files: List of input video paths
            output_path: Output video path
        """
        # Create concat file
        concat_file = output_path.replace('.mp4', '_concat.txt')
        
        with open(concat_file, 'w') as f:
            for file in input_files:
                # Escape backslashes for Windows
                escaped_file = file.replace('\\', '\\\\')
                f.write(f"file '{escaped_file}'\n")
        
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFMPEG_CMD,
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            os.remove(concat_file)
            return True
        except subprocess.CalledProcessError as e:
            if os.path.exists(concat_file):
                os.remove(concat_file)
            raise RuntimeError(f"Failed to concatenate: {e.stderr.decode()}")
    
    @staticmethod
    def add_subtitles(video_path: str, subtitle_path: str, output_path: str) -> bool:
        """
        Add subtitle file to video.
        
        Args:
            video_path: Input video
            subtitle_path: Subtitle file path
            output_path: Output video
        """
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFMPEG_CMD,
            '-i', video_path,
            '-i', subtitle_path,
            '-c', 'copy',
            '-c:s', 'mov_text',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to add subtitles: {e.stderr.decode()}")
    
    @staticmethod
    def speed_video(input_path: str, output_path: str, speed: float) -> bool:
        """
        Change video speed.
        
        Args:
            input_path: Input video
            output_path: Output video
            speed: Speed multiplier (0.5 = half speed, 2.0 = double speed)
        """
        if speed <= 0:
            raise ValueError("Speed must be positive")
        
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFMPEG_CMD,
            '-i', input_path,
            '-filter:v', f'setpts=PTS/{speed}',
            '-filter:a', f'atempo={speed}',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to change speed: {e.stderr.decode()}")
    
    @staticmethod
    def extract_audio(video_path: str, output_path: str) -> bool:
        """Extract audio from video."""
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFMPEG_CMD,
            '-i', video_path,
            '-q:a', '9',
            '-n',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")
    
    @staticmethod
    def resize_video(input_path: str, output_path: str, width: int, height: int) -> bool:
        """Resize video."""
        FFmpegEngine._find_ffmpeg()
        cmd = [
            FFmpegEngine.FFMPEG_CMD,
            '-i', input_path,
            '-vf', f'scale={width}:{height}',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to resize: {e.stderr.decode()}")
