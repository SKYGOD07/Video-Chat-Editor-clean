"""Time parsing utilities for HH:MM:SS format."""

import re


def parse_time_to_seconds(time_str: str) -> int:
    """
    Convert HH:MM:SS format to seconds.
    
    Args:
        time_str: Time in HH:MM:SS or MM:SS format
        
    Returns:
        Total seconds as integer
        
    Raises:
        ValueError: If format is invalid
    """
    time_str = time_str.strip()
    
    # Match HH:MM:SS or MM:SS format
    match = re.match(r'^(\d{1,2}):(\d{2}):(\d{2})$|^(\d{1,2}):(\d{2})$', time_str)
    
    if not match:
        raise ValueError(f"Invalid time format: {time_str}. Use HH:MM:SS or MM:SS")
    
    groups = match.groups()
    
    if groups[0] is not None:  # HH:MM:SS format
        hours = int(groups[0])
        minutes = int(groups[1])
        seconds = int(groups[2])
    else:  # MM:SS format
        hours = 0
        minutes = int(groups[3])
        seconds = int(groups[4])
    
    if minutes >= 60 or seconds >= 60:
        raise ValueError("Minutes and seconds must be less than 60")
    
    total_seconds = hours * 3600 + minutes * 60 + seconds
    return total_seconds


def seconds_to_time(seconds: int) -> str:
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Total seconds
        
    Returns:
        Time string in HH:MM:SS format
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def validate_time_range(start_str: str, end_str: str, max_duration: int) -> tuple[int, int]:
    """
    Validate and parse time range.
    
    Args:
        start_str: Start time string
        end_str: End time string
        max_duration: Maximum video duration in seconds
        
    Returns:
        Tuple of (start_seconds, end_seconds)
        
    Raises:
        ValueError: If times are invalid or out of range
    """
    start = parse_time_to_seconds(start_str)
    end = parse_time_to_seconds(end_str)
    
    if start >= end:
        raise ValueError("Start time must be less than end time")
    
    if end > max_duration:
        raise ValueError(f"End time {end_str} exceeds video duration")
    
    return start, end
