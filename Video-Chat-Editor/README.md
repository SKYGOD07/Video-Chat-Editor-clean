# AI Video Editor MVP

## Description
A chat-based video editing tool. Upload a video, then use natural language commands to edit it.

## Features
- **Upload**: Upload video files to the server.
- **Chat Interface**: Send commands like "remove silence", "add subtitles", "cut from 00:00 to 00:10".
- **AI Processing**: Uses Python (FFmpeg, Whisper) to process videos.
- **Real-time Status**: Polls for processing updates.

## Tech Stack
- **Frontend**: React + TypeScript (Vite, Shadcn UI)
- **Backend**: Node.js/Express (API Gateway) + Python (Video Processing)
- **Database**: PostgreSQL (via Drizzle ORM)
- **Tools**: FFmpeg, OpenAI Whisper

## Usage
1.  Run `npm run dev` to start the application.
2.  Open browser (port 5000).
3.  Upload a video.
4.  In the editor, type commands.

## Python Requirements
The server tries to use `openai-whisper` and `ffmpeg-python`. If not installed, it falls back to a mock implementation (copying the video).
To install real deps:
```bash
pip install openai-whisper ffmpeg-python torch numpy
```
(Note: `numba` requires Python < 3.10, so you might need a specific python environment).
