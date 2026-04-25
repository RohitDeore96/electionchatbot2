"""
Router defining logic for Vertex AI conversation endpoints.
Acts as the communication bridge between user prompts and Gemini models.
"""
from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel, Field
from app.services.vertex_ai_agent import VertexAIAgent
from app.utils.limiter import limiter
import logging
from datetime import datetime, timezone
import os
from typing import Dict
from app.utils.ai_helper import generate_ai_response

RATE_LIMIT_CHAT = "10/minute"
from app.services.firestore_service import log_chat_to_firestore

logger = logging.getLogger(__name__)

router = APIRouter()
ai_agent = VertexAIAgent()

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)




@router.post("/chat")
@limiter.limit(RATE_LIMIT_CHAT)
async def chat_with_agent(
    request: Request, payload: ChatRequest, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """
    Process incoming chat messages via Gemini 1.5 Flash and trigger background logging.

    Args:
        request (Request): The incoming FastAPI request.
        payload (ChatRequest): The chat request payload containing the message.
        background_tasks (BackgroundTasks): FastAPI background tasks.

    Returns:
        Dict[str, str]: A dictionary containing the AI response.

    Raises:
        HTTPException: If generating the AI response fails.
    """
    background_tasks.add_task(
        log_chat_to_firestore, payload.message, datetime.now(timezone.utc)
    )
    response_text = generate_ai_response(ai_agent, payload.message)
    return {"response": response_text}
