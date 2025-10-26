"""Schemas for story data."""

from pydantic import BaseModel
from typing import List, Union

class StoryRequest(BaseModel):
    """Request to generate a historical story."""
    topic: str

class StoryResponse(BaseModel):
    """Complete story experience with all generated content."""
    topic: str
    brief: str
    story: str
    system_prompt: str
    faq: Union[List[str], str]  # Allow list or stringified JSON
    audio_url: str
    video_url: str