"""
Tests for API routes.
"""
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient


def test_health_check(client: TestClient) -> None:
    """
    Test the health check endpoint.

    Args:
        client (TestClient): The test client.
    """
    response = client.get("/health")
    assert response.status_code == 200


def test_get_voter_info(client: TestClient) -> None:
    """
    Test the voter info endpoint.

    Args:
        client (TestClient): The test client.
    """
    response = client.get("/api/civic/voter-info?address=123+Main+St")
    assert response.status_code == 200
    assert "address" in response.json()


@patch("app.routes.ai_routes.ai_agent.get_response")
def test_chat_with_agent(mock_get_response: MagicMock, client: TestClient) -> None:
    """
    Test the AI chat endpoint.

    Args:
        mock_get_response (MagicMock): The mocked get_response method.
        client (TestClient): The test client.
    """
    mock_get_response.return_value = "how to vote response"
    response = client.post("/api/ai/chat", json={"message": "how to vote?"})
    assert response.status_code == 200
    assert "how to vote response" in response.json()["response"]


def test_geocode_address(client: TestClient) -> None:
    """
    Test the geocode endpoint.

    Args:
        client (TestClient): The test client.
    """
    response = client.get("/api/map/geocode?address=123+Main+St")
    assert response.status_code == 200
    assert "lat" in response.json()


def test_get_map_key(client: TestClient) -> None:
    """
    Test the map key endpoint.

    Args:
        client (TestClient): The test client.
    """
    response = client.get("/api/map/key")
    assert response.status_code == 200
    assert "key" in response.json()


@patch("app.routes.ai_routes.ai_agent.get_response")
def test_chat_with_agent_exception(mock_get_response: MagicMock, client: TestClient) -> None:
    """
    Test the AI chat endpoint exception handling.

    Args:
        mock_get_response (MagicMock): The mocked get_response method.
        client (TestClient): The test client.
    """
    mock_get_response.side_effect = Exception("Test exception")
    response = client.post("/api/ai/chat", json={"message": "how to vote?"})
    assert response.status_code == 500
    assert "Test exception" in response.json()["detail"]


def test_chat_with_agent_empty_message(client: TestClient) -> None:
    """
    Test the AI chat endpoint with an empty message.

    Args:
        client (TestClient): The test client.
    """
    response = client.post("/api/ai/chat", json={"message": ""})
    assert response.status_code == 422


@patch("app.routes.ai_routes.ai_agent.get_response")
def test_chat_rate_limit(mock_get_response: MagicMock, client: TestClient) -> None:
    """
    Test the rate limiting of the AI chat endpoint.

    Args:
        mock_get_response (MagicMock): The mocked get_response method.
        client (TestClient): The test client.
    """
    mock_get_response.return_value = "response"
    for _ in range(10):
        client.post("/api/ai/chat", json={"message": "hi"})
    response = client.post("/api/ai/chat", json={"message": "hi"})
    assert response.status_code == 429
