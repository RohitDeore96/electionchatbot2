from app.services.vertex_ai_agent import VertexAIAgent
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


def generate_ai_response(ai_agent: VertexAIAgent, message: str) -> str:
    """
    Generate an AI response using the provided agent and message.

    Args:
        ai_agent (VertexAIAgent): The AI agent instance.
        message (str): The user's input message.

    Returns:
        str: The generated response.

    Raises:
        HTTPException: If generating the AI response fails.
    """
    try:
        return ai_agent.get_response(message)
    except Exception as e:
        logger.error(f"Failed to generate AI response: {e}")
        raise HTTPException(
            status_code=500, detail=f"Failed to generate response: {str(e)}"
        )
