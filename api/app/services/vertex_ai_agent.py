"""
Service for interacting with Google Cloud Vertex AI.
Provides the VertexAIAgent class for handling chatbot interactions.
"""
import vertexai
from vertexai.generative_models import GenerativeModel
from typing import Optional, List, Dict, Any, Union, Callable
import os
import logging

logger = logging.getLogger(__name__)

from app.constants import MODEL_NAME
LOCATION = os.environ.get("VERTEX_AI_LOCATION", "us-central1")


class VertexAIAgent:
    """
    Agent for communicating with Vertex AI models.
    """

    def __init__(self) -> None:
        """
        Initialize the Vertex AI agent with configuration.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        self.project = os.environ.get("VERTEX_AI_PROJECT_ID") or os.environ.get(  # noqa: E501
            "GOOGLE_CLOUD_PROJECT", "electionchatbot2"
        )
        self.location = LOCATION
        self.system_instruction = (
            "You are an official Election Assistant. You help users "
            "understand the election process, voting timelines, and polling "
            "locations. You must refuse to answer any questions unrelated "
            "to voting or elections."
        )
        self.model: Optional[GenerativeModel] = None
        self.init_error: Optional[str] = None

    def _init_model(self) -> None:
        """
        Initialize the GenerativeModel if not already loaded.

        Args:
            None

        Returns:
            None

        Raises:
            Exception: Caught internally if model initialization fails.
        """
        if not self.model:
            try:
                vertexai.init(project=self.project, location=self.location)
                self.model = GenerativeModel(
                    MODEL_NAME, system_instruction=[self.system_instruction]
                )
            except Exception as e:
                logger.error(f"Failed to initialize Vertex AI: {e}")
                self.init_error = str(e)
                self.model = None

    def get_response(self, query: str) -> str:
        """
        Get a response from the Vertex AI model.

        Args:
            query (str): The user's input query.

        Returns:
            str: The AI model's response or an error message.

        Raises:
            None
        """
        self._init_model()
        if not self.model:
            return f"Vertex AI Init Error: {self.init_error}"
        try:
            chat = self.model.start_chat()
            response = chat.send_message(query)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
