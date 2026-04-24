from app.services.firestore_client import FirestoreClient
from app.services.vertex_ai_agent import VertexAIAgent
from app.services.translation_svc import TranslationService
from unittest.mock import MagicMock, patch


def test_firestore_client():
    client = FirestoreClient()
    assert client.get_user_preferences("user1") == {"language": "en"}
    client.save_chat_history("session1", "hello")


@patch("app.services.vertex_ai_agent.vertexai")
@patch("app.services.vertex_ai_agent.GenerativeModel")
def test_vertex_ai_agent(mock_gen_model, mock_vertexai):
    # Mock the chat response
    mock_chat = MagicMock()
    mock_chat.send_message.return_value.text = "test response"
    mock_gen_model.return_value.start_chat.return_value = mock_chat

    agent = VertexAIAgent()
    assert agent.get_response("test") == "test response"

    # Test fallback initialization
    agent.model = None
    agent.project = None
    assert agent.get_response("test") == "test response"


def test_translation_svc():
    svc = TranslationService()
    assert svc.translate_text("hello", "es") == "hello"


@patch("app.services.vertex_ai_agent.vertexai")
@patch("app.services.vertex_ai_agent.GenerativeModel")
def test_vertex_ai_agent_exceptions(mock_gen_model, mock_vertexai):
    agent = VertexAIAgent()
    agent.project = "test_proj"

    # Test initialization exception
    mock_vertexai.init.side_effect = Exception("init error")
    assert "I'm sorry" in agent.get_response("test")

    # Test chat exception
    mock_vertexai.init.side_effect = None
    mock_chat = MagicMock()
    mock_chat.send_message.side_effect = Exception("chat error")
    mock_gen_model.return_value.start_chat.return_value = mock_chat

    agent.model = None  # Force reinit
    assert "Error: chat error" in agent.get_response("test")
