from fastapi import APIRouter, Request, BackgroundTasks
from pydantic import BaseModel, Field
from app.services.vertex_ai_agent import VertexAIAgent
from app.utils.limiter import limiter
import logging
from datetime import datetime, timezone
import os
from typing import Dict
from app.utils.ai_helper import generate_ai_response

logger = logging.getLogger(__name__)

router = APIRouter()
ai_agent = VertexAIAgent()

try:
    from google.cloud import firestore

    if os.environ.get("MOCK_FIRESTORE") != "true":
        db = firestore.Client()
    else:
        db = None
except ImportError:
    db = None


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)


def log_chat_to_firestore(message: str, timestamp: datetime) -> None:
    """
    Log the user's chat prompt and timestamp to a Firestore collection.

    Args:
        message (str): The user's input message.
        timestamp (datetime): The UTC timestamp of the chat request.
    """
    if db:
        try:
            db.collection("chat_logs").add({"message": message, "timestamp": timestamp})  # noqa: E501
        except Exception as e:
            logger.error(f"Failed to log chat to Firestore: {e}")
    else:
        logger.info(f"Mock Firestore log: message='{message}' at {timestamp}")


@router.post("/chat")
@limiter.limit("10/minute")
async def chat_with_agent(
    request: Request, payload: ChatRequest, background_tasks: BackgroundTasks
) -> Dict[str, str]:
    """
    Interact with Vertex AI Gemini 1.5 Flash and log prompt to Firestore.

    Args:
        request (Request): The incoming FastAPI request.
        payload (ChatRequest): The chat request payload containing the message.
        background_tasks (BackgroundTasks): FastAPI background tasks.

    Returns:
        dict: A dictionary containing the AI response.

    Raises:
        HTTPException: If generating the AI response fails.
    """
    background_tasks.add_task(
        log_chat_to_firestore, payload.message, datetime.now(timezone.utc)
    )
    response_text = generate_ai_response(ai_agent, payload.message)
    return {"response": response_text}
