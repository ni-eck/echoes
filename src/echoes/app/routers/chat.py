"""Router for chat interactions."""

from fastapi import APIRouter, HTTPException
from agents import Runner
from ...schemas.chat import ChatRequest, ChatResponse
from ...agents.qa_agent import build_qa_agent
from ...app.settings import MODEL

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Interactive chat about a historical story.
    
    Takes a story context and a user question, then uses the QA agent
    to provide an informed answer based on the context.
    
    Args:
        request: ChatRequest with story_context and question fields
    
    Returns:
        ChatResponse with the answer
    """
    try:
        # Instantiate QA agent
        qa = build_qa_agent(MODEL)
        
        # Build prompt with context and question
        prompt = f"""Context:
{request.story_context}

Q: {request.question}
A:"""
        
        # Get answer from agent
        answer = str((await Runner.run(qa, prompt)).final_output)
        
        return ChatResponse(answer=answer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process chat: {str(e)}")