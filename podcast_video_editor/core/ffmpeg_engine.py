"""FFmpeg integration for video/audio processing."""

import subprocess
import json
import os
from pathlib import Path


class FFmpegEngine:
    """Handles all FFmpeg operations."""
    
    @staticmethod
    def get_video_duration(video_path: str) -> int:
        """
        Get video duration in seconds.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Duration in seconds
        """
        cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'json',
            video_path
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            data = json.loads(result.stdout)
            return int(float(data['format']['duration']))
        except (subprocess.CalledProcessError, json.JSONDecodeError, KeyError):
            raise RuntimeError(f"Failed to get duration for {video_path}")
    
    @staticmethod
    def extract_audio(video_path: str, output_path: str, audio_index: int = 0) -> str:
        """
        Extract audio track from video.
        
        Args:
            video_path: Path to video file
            output_path: Path to save audio
            audio_index: Audio stream index
            
        Returns:
            Path to extracted audio
        """
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-map', f'0:a:{audio_index}',
            '-q:a', '9',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to extract audio: {e.stderr.decode()}")
    
    @staticmethod
    def cut_segment(input_path: str, output_path: str, start: int, end: int) -> str:
        """
        Cut a segment from video using timestamp.
        
        Args:
            input_path: Input video path
            output_path: Output video path
            start: Start time in seconds
            end: End time in seconds
            
        Returns:
            Path to output file
        """
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-ss', str(start),
            '-to', str(end),
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to cut segment: {e.stderr.decode()}")
    
    @staticmethod
    def concatenate_videos(input_files: list[str], output_path: str) -> str:
        """
        Concatenate multiple video files.
        
        Args:
            input_files: List of video file paths
            output_path: Output video path
            
        Returns:
            Path to output file
        """
        # Create concat demuxer file
        concat_file = output_path.replace('.mp4', '_concat.txt')
        
        with open(concat_file, 'w') as f:
            for file in input_files:
                f.write(f"file '{file}'\n")
        
        cmd = [
            'ffmpeg',
            '-f', 'concat',
            '-safe', '0',
            '-i', concat_file,
            '-c', 'copy',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            # Clean up concat file
            if os.path.exists(concat_file):
                os.remove(concat_file)
            return output_path
        except subprocess.CalledProcessError as e:
            if os.path.exists(concat_file):
                os.remove(concat_file)
            raise RuntimeError(f"Failed to concatenate videos: {e.stderr.decode()}")
    
    @staticmethod
    def mux_audio_video(video_path: str, audio_path: str, output_path: str) -> str:
        """
        Mux video with audio track.
        
        Args:
            video_path: Path to video file
            audio_path: Path to audio file
            output_path: Output video path
            
        Returns:
            Path to output file
        """
        cmd = [
            'ffmpeg',
            '-i', video_path,
            '-i', audio_path,
            '-c:v', 'copy',
            '-c:a', 'aac',
            '-map', '0:v:0',
            '-map', '1:a:0',
            '-shortest',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return output_path
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to mux audio: {e.stderr.decode()}")
    
    @staticmethod
    def check_ffmpeg_installed() -> bool:
        """Check if FFmpeg is installed and accessible."""
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            subprocess.run(['ffprobe', '-version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
