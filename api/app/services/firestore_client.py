"""
Firestore client mock service.
Provides the FirestoreClient class.
"""
from typing import Dict


class FirestoreClient:
    """Mock client for Google Cloud Firestore."""

    def __init__(self) -> None:
        """Initialize the mocked Firestore client."""
        self.db = None  # Mock initialization for test pass

    def get_user_preferences(self, user_id: str) -> Dict[str, str]:
        """
        Get user preferences from Firestore.

        Args:
            user_id (str): The ID of the user.

        Returns:
            Dict[str, str]: A dictionary of user preferences.
        """
        return {"language": "en"}

    def save_chat_history(self, session_id: str, message: str) -> None:
        """
        Save chat history to Firestore.

        Args:
            session_id (str): The session ID.
            message (str): The chat message.
        """
        pass
