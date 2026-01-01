"""Command parser for natural language video editing."""

import re
from typing import Optional


class CommandParser:
    """Parses natural language commands into video operations."""
    
    @staticmethod
    def parse(command: str) -> dict:
        """
        Parse user command and extract operation.
        
        Args:
            command: User text input
            
        Returns:
            Dictionary with operation type and parameters
        """
        command = command.strip().lower()
        
        # Remove silence
        if any(phrase in command for phrase in ['remove silence', 'remove quiet', 'cut silence', 'silence removal']):
            return {'operation': 'remove_silence'}
        
        # Cut segment
        cut_match = re.search(r'cut from\s+(\d{1,2}):(\d{2}):?(\d{2})?\s+to\s+(\d{1,2}):(\d{2}):?(\d{2})?', command)
        if cut_match:
            start = CommandParser._parse_time(cut_match.group(1), cut_match.group(2), cut_match.group(3))
            end = CommandParser._parse_time(cut_match.group(4), cut_match.group(5), cut_match.group(6))
            return {'operation': 'cut_segment', 'start': start, 'end': end}
        
        # Trim to duration
        trim_match = re.search(r'trim to\s+(\d+)\s*(?:seconds|secs|s)?', command)
        if trim_match:
            duration = int(trim_match.group(1))
            return {'operation': 'trim', 'duration': duration}
        
        # Speed up/down
        speed_match = re.search(r'(?:speed up|slow down|change speed)\s+(?:to\s+)?(\d+\.?\d*)\s*x', command)
        if speed_match:
            speed = float(speed_match.group(1))
            return {'operation': 'change_speed', 'speed': speed}
        
        # Add subtitles
        if any(phrase in command for phrase in ['add subtitles', 'add captions', 'generate subtitles', 'add subs']):
            return {'operation': 'add_subtitles'}
        
        # Get transcript
        if any(phrase in command for phrase in ['transcribe', 'get transcript', 'extract text', 'speech to text']):
            return {'operation': 'transcribe'}
        
        # Resize
        resize_match = re.search(r'resize to\s+(\d+)x(\d+)', command)
        if resize_match:
            width = int(resize_match.group(1))
            height = int(resize_match.group(2))
            return {'operation': 'resize', 'width': width, 'height': height}
        
        # Reverse
        if 'reverse' in command:
            return {'operation': 'reverse'}
        
        # Merge videos
        if any(phrase in command for phrase in ['merge', 'combine', 'concatenate']):
            return {'operation': 'concatenate'}
        
        # Unknown command
        return {'operation': 'unknown', 'raw_command': command}
    
    @staticmethod
    def _parse_time(hours: str, minutes: str, seconds: str = None) -> float:
        """Parse time string to seconds."""
        h = int(hours)
        m = int(minutes)
        s = int(seconds) if seconds else 0
        return h * 3600 + m * 60 + s
    
    @staticmethod
    def explain_operation(operation: dict) -> str:
        """Generate human-readable explanation of parsed operation."""
        op = operation.get('operation')
        
        if op == 'remove_silence':
            return "Will remove silence from the video"
        elif op == 'cut_segment':
            start = operation.get('start', 0)
            end = operation.get('end', 0)
            return f"Will cut segment from {start}s to {end}s"
        elif op == 'trim':
            duration = operation.get('duration', 0)
            return f"Will trim video to first {duration} seconds"
        elif op == 'change_speed':
            speed = operation.get('speed', 1)
            return f"Will change speed to {speed}x"
        elif op == 'add_subtitles':
            return "Will add subtitles to video"
        elif op == 'transcribe':
            return "Will transcribe audio to text"
        elif op == 'resize':
            width = operation.get('width')
            height = operation.get('height')
            return f"Will resize video to {width}x{height}"
        elif op == 'reverse':
            return "Will reverse the video"
        else:
            return "Unknown operation"
