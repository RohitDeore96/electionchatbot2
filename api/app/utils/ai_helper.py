"""
AI Helper utility.
Provides functions for formatting and generating AI responses.
"""
from app.services.vertex_ai_agent import VertexAIAgent
from app.utils.error_utils import build_error_response
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
        build_error_response(500, f"Failed to generate response: {str(e)}")
        return ""

from typing import Dict

def format_ai_payload(response_text: str) -> Dict[str, str]:
    """
    Format the AI response into a standardized JSON payload.

    Args:
        response_text (str): The raw text response from the AI.

    Returns:
        Dict[str, str]: The formatted dictionary payload.
        
    Raises:
        None
    """
    return {"response": response_text}
