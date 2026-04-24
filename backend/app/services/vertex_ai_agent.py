import vertexai
from vertexai.generative_models import GenerativeModel
import os


class VertexAIAgent:
    def __init__(self):
        self.project = os.environ.get("VERTEX_AI_PROJECT_ID") or os.environ.get("GOOGLE_CLOUD_PROJECT", "electionchatbot2")
        self.location = os.environ.get("VERTEX_AI_LOCATION", "us-central1")
        self.system_instruction = (
            "You are an official Election Assistant. You help users "
            "understand the election process, voting timelines, and polling "
            "locations. You must refuse to answer any questions unrelated "
            "to voting or elections.")
        self.model = None
        self.init_error = None

    def _init_model(self):
        if not self.model:
            try:
                vertexai.init(project=self.project, location=self.location)
                self.model = GenerativeModel(
                    "gemini-1.5-flash-002",
                    system_instruction=[self.system_instruction]
                )
            except Exception as e:
                print(f"Warning: Failed to initialize Vertex AI: {e}")
                self.init_error = str(e)
                self.model = None

    def get_response(self, query: str) -> str:
        self._init_model()
        if not self.model:
            return f"Vertex AI Init Error: {self.init_error}"
        try:
            chat = self.model.start_chat()
            response = chat.send_message(query)
            return response.text
        except Exception as e:
            return f"Error: {str(e)}"
