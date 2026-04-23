class FirestoreClient:
    def __init__(self):
        self.db = None  # Mock initialization for test pass

    def get_user_preferences(self, user_id: str) -> dict:
        return {"language": "en"}

    def save_chat_history(self, session_id: str, message: str):
        pass
