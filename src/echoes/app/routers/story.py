"""Router for story generation."""

from fastapi import APIRouter, HTTPException
from ...schemas.story import StoryRequest, StoryResponse
from ...workflows.story_pipeline import generate_story_experience
from ...app.settings import MODEL

router = APIRouter()

@router.post("/story", response_model=StoryResponse)
async def generate_story(request: StoryRequest):
    """
    Generate a complete historical story experience.
    
    Takes a historical topic and orchestrates multiple AI agents to create:
    - Research brief with facts and timeline
    - Engaging narrative story (60-120 seconds)
    - Related FAQ questions and answers
    - Audio narration URL (mocked)
    - Video animation URL (mocked)
    
    Args:
        request: StoryRequest with topic field
    
    Returns:
        StoryResponse with all generated content and media URLs
    """
    try:
        result = await generate_story_experience(request.topic, MODEL)
        return StoryResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate story: {str(e)}")