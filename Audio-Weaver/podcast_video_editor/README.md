# podcast_video_editor/README.md
# Terminal-Based Podcast Video Editor

A CLI tool to edit podcast videos by syncing audio/video and cutting based on user input or audio analysis.

## Prerequisites

- Python 3.10+
- FFmpeg installed and in system PATH

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the program:
```bash
python main.py
```

Follow the interactive prompts to:
1. Select input video and audio tracks.
2. Define timeline segments.
3. Choose audio prioritization (Speaker A, Speaker B, or Mix).
4. Export the final video.

## Features

- Multi-track audio analysis
- Silence removal
- FFmpeg-based rendering
- Podcast-style cuts
