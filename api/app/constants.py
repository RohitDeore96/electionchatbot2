"""
Global constants for the Election Assistant API.
Centralized repository for all magic strings and numbers to ensure DRY compliance.
"""

MODEL_NAME = "gemini-2.5-flash"
CACHE_CONTROL_PUBLIC = "public, max-age=300"
RATE_LIMIT_CHAT = "10/minute"
FIRESTORE_COLLECTION = "chat_logs"
MOCK_FIRESTORE_ENV = "MOCK_FIRESTORE"
TRUE_STR = "true"
MAPS_API_ENV_KEY = "Maps_API_KEY"
CIVIC_INFO_API_ENV_KEY = "CIVIC_INFO_API_KEY"
DEFAULT_PORT = 8000
API_TITLE = "Election Assistant API"
GZIP_MIN_SIZE = 1000
