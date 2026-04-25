"""
Global constants for the Election Assistant API.
Centralized repository for all magic strings and numbers to ensure DRY compliance.
"""

MODEL_NAME: str = "gemini-2.5-flash"
CACHE_CONTROL_PUBLIC: str = "public, max-age=300"
RATE_LIMIT_CHAT: str = "10/minute"
FIRESTORE_COLLECTION: str = "chat_logs"
MOCK_FIRESTORE_ENV: str = "MOCK_FIRESTORE"
TRUE_STR: str = "true"
MAPS_API_ENV_KEY: str = "Maps_API_KEY"
CIVIC_INFO_API_ENV_KEY: str = "CIVIC_INFO_API_KEY"
DEFAULT_PORT: int = 8000
API_TITLE: str = "Election Assistant API"
GZIP_MIN_SIZE: int = 1000
