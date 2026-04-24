from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, Field
from app.services.vertex_ai_agent import VertexAIAgent
from app.utils.limiter import limiter
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
ai_agent = VertexAIAgent()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

@router.post("/chat")
@limiter.limit("10/minute")
async def chat_with_agent(request: Request, payload: ChatRequest) -> dict:
    """Interact with Vertex AI Gemini 1.5 Flash."""
    try:
        response_text = ai_agent.get_response(payload.message)
        return {"response": response_text}
    except Exception as e:
        logger.error(f"Failed to generate AI response: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}"
        )