"""Silence detection and removal."""

import subprocess
import os


class SilenceRemover:
    """Detects and removes silence from audio."""
    
    @staticmethod
    def remove_silence(input_path: str, output_path: str, 
                      threshold_db: int = -40,
                      min_duration_ms: int = 500) -> bool:
        """
        Remove silence from video using FFmpeg.
        
        Args:
            input_path: Input video path
            output_path: Output video path
            threshold_db: Silence threshold in dB
            min_duration_ms: Minimum silent duration to remove
        """
        # Use FFmpeg's silenceremove filter
        filter_str = (
            f"silenceremove=1:0:{threshold_db}dB:1:{min_duration_ms/1000}:{threshold_db}dB,"
            "silencedetect=n={threshold_db}dB:d=1"
        )
        
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-af', f'silenceremove=1:0:{threshold_db}dB:1:{min_duration_ms/1000}:{threshold_db}dB',
            '-y',
            output_path
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to remove silence: {e.stderr.decode()}")
    
    @staticmethod
    def detect_silence(input_path: str, threshold_db: int = -40) -> list[tuple[float, float]]:
        """
        Detect silent regions in video.
        
        Args:
            input_path: Input video path
            threshold_db: Silence threshold in dB
            
        Returns:
            List of (start_time, end_time) tuples for silent regions
        """
        cmd = [
            'ffmpeg',
            '-i', input_path,
            '-af', f'silencedetect=n={threshold_db}dB:d=0.1',
            '-f', 'null',
            '-'
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            stderr = result.stderr
            
            # Parse silence regions from output
            silence_regions = []
            import re
            
            # Pattern: silencedetect outputs "silence_start: X" and "silence_end: Y"
            for match in re.finditer(r'silence_start:\s+([\d.]+)', stderr):
                start = float(match.group(1))
                # Find corresponding silence_end
                end_match = re.search(r'silence_end:\s+([\d.]+)', stderr[match.end():])
                if end_match:
                    end = float(end_match.group(1))
                    silence_regions.append((start, end))
            
            return silence_regions
        except Exception as e:
            raise RuntimeError(f"Failed to detect silence: {e}")
    
    @staticmethod
    def create_silence_report(input_path: str) -> dict:
        """Generate silence analysis report."""
        try:
            regions = SilenceRemover.detect_silence(input_path)
            total_silent_time = sum(end - start for start, end in regions)
            
            return {
                'total_silent_regions': len(regions),
                'total_silent_time': total_silent_time,
                'regions': regions
            }
        except Exception as e:
            return {'error': str(e)}
