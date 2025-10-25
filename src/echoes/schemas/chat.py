"""Schemas for chat data."""

from pydantic import BaseModel

class ChatRequest(BaseModel):
    """Request for interactive chat about a story."""
    story_context: str
    question: str

class ChatResponse(BaseModel):
    """Response with answer to user's question."""
    answer: str