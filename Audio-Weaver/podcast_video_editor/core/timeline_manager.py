class TimelineManager:
    def __init__(self):
        self.segments = [] # List of {'start': float, 'end': float, 'priority': str}

    def add_segment(self, start, end, priority):
        if end <= start:
            print("Error: End time must be after start time.")
            return False
        
        self.segments.append({
            'start': start,
            'end': end,
            'priority': priority
        })
        self.segments.sort(key=lambda x: x['start'])
        return True

    def get_segments(self):
        return self.segments

    def clear(self):
        self.segments = []
