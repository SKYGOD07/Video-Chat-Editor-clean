import re

def parse_time_string(time_str: str) -> float:
    """
    Parses a time string in HH:MM:SS, MM:SS, or SS format into seconds.
    """
    time_str = time_str.strip()
    if not time_str:
        return 0.0
    
    parts = time_str.split(':')
    seconds = 0.0
    
    try:
        if len(parts) == 3: # HH:MM:SS
            seconds += int(parts[0]) * 3600
            seconds += int(parts[1]) * 60
            seconds += float(parts[2])
        elif len(parts) == 2: # MM:SS
            seconds += int(parts[0]) * 60
            seconds += float(parts[1])
        elif len(parts) == 1: # SS
            seconds = float(parts[0])
        else:
            raise ValueError
    except ValueError:
        raise ValueError("Invalid time format. Use HH:MM:SS, MM:SS, or seconds.")
        
    return seconds

def seconds_to_hms(seconds: float) -> str:
    """Formats seconds to HH:MM:SS."""
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    return "{:02d}:{:02d}:{:05.2f}".format(int(h), int(m), s)
