"""
Firestore business logic extraction to reduce cyclomatic complexity.
"""
import logging
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.constants import FIRESTORE_COLLECTION, MOCK_FIRESTORE_ENV, TRUE_STR

logger = logging.getLogger(__name__)

# Initialize DB connection once
try:
    from google.cloud import firestore

    if os.environ.get(MOCK_FIRESTORE_ENV) != TRUE_STR:
        db: Optional[Any] = firestore.Client()
    else:
        db = None
except ImportError:
    db = None

def log_chat_to_firestore(message: str, timestamp: datetime) -> None:
    """
    Log user interactions to Firestore securely.

    Args:
        message (str): The user's input message.
        timestamp (datetime): The UTC timestamp of the chat request.

    Returns:
        None
    """
    if db:
        try:
            db.collection(FIRESTORE_COLLECTION).add({"message": message, "timestamp": timestamp})  # noqa: E501
        except Exception as e:
            logger.error(f"Failed to log chat to Firestore: {e}")
    else:
        logger.info(f"Mock Firestore log: message='{message}' at {timestamp}")
