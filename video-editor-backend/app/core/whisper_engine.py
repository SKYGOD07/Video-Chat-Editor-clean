"""Whisper speech-to-text engine."""

import subprocess
import json
import os


class WhisperEngine:
    """Handles Whisper transcription."""
    
    MODEL = "base"  # tiny, base, small, medium, large
    
    @staticmethod
    def check_installed() -> bool:
        """Check if Whisper is installed."""
        try:
            subprocess.run(['whisper', '--help'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    @staticmethod
    def transcribe(audio_path: str, output_path: str = None, language: str = "en") -> dict:
        """
        Transcribe audio file.
        
        Args:
            audio_path: Path to audio file
            output_path: Where to save transcript
            language: Language code
            
        Returns:
            Dictionary with transcript data
        """
        if not output_path:
            output_path = audio_path.replace('.mp3', '').replace('.wav', '')
        
        cmd = [
            'whisper',
            audio_path,
            '--model', WhisperEngine.MODEL,
            '--language', language,
            '--output_format', 'json',
            '--output_dir', os.path.dirname(output_path) or '.',
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            
            # Load generated JSON
            json_path = output_path + '.json'
            if os.path.exists(json_path):
                with open(json_path, 'r') as f:
                    return json.load(f)
            
            return {"text": result.stdout}
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Whisper transcription failed: {e.stderr}")
    
    @staticmethod
    def transcribe_video(video_path: str, output_path: str = None) -> dict:
        """Transcribe video by extracting audio first."""
        import tempfile
        
        # Extract audio temporarily
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
            tmp_audio = tmp.name
        
        try:
            # Extract audio
            cmd = [
                'ffmpeg',
                '-i', video_path,
                '-q:a', '9',
                '-y',
                tmp_audio
            ]
            subprocess.run(cmd, capture_output=True, check=True)
            
            # Transcribe
            result = WhisperEngine.transcribe(tmp_audio, output_path)
            return result
        finally:
            if os.path.exists(tmp_audio):
                os.remove(tmp_audio)
