from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from app.services.vertex_ai_agent import VertexAIAgent

router = APIRouter()
ai_agent = VertexAIAgent()


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


@router.post("/chat")
async def chat_with_agent(request: ChatRequest):
    """Interact with Vertex AI Gemini 1.5 Flash."""
    try:
        response_text = ai_agent.get_response(request.message)
        return {"response": response_text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate response: {str(e)}")
