"""Data models and schemas for API."""

from pydantic import BaseModel
from typing import Optional


class ChatMessage(BaseModel):
    """Chat message schema."""
    video_id: str
    message: str


class ChatResponse(BaseModel):
    """Chat response schema."""
    status: str
    message: str
    video_id: str
    output_path: Optional[str] = None
    operation: Optional[str] = None


class UploadResponse(BaseModel):
    """Upload response schema."""
    video_id: str
    filename: str
    size: int
    message: str


class StatusResponse(BaseModel):
    """Status response schema."""
    video_id: str
    status: str
    progress: float
    current_operation: Optional[str] = None


class TranscriptSegment(BaseModel):
    """Transcript segment."""
    start: float
    end: float
    text: str
    confidence: float


class TranscriptResponse(BaseModel):
    """Transcript response."""
    video_id: str
    transcript: list[TranscriptSegment]
    language: str
