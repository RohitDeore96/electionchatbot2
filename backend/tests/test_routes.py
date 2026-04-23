def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200

def test_get_voter_info(client):
    response = client.get("/api/civic/voter-info?address=123+Main+St")
    assert response.status_code == 200
    assert "address" in response.json()

from unittest.mock import patch

@patch('app.routes.ai_routes.ai_agent.get_response')
def test_chat_with_agent(mock_get_response, client):
    mock_get_response.return_value = "how to vote response"
    response = client.post("/api/ai/chat", json={"message": "how to vote?"})
    assert response.status_code == 200
    assert "how to vote response" in response.json()["response"]

def test_geocode_address(client):
    response = client.get("/api/map/geocode?address=123+Main+St")
    assert response.status_code == 200
    assert "lat" in response.json()

@patch('app.routes.ai_routes.ai_agent.get_response')
def test_chat_with_agent_exception(mock_get_response, client):
    mock_get_response.side_effect = Exception("Test exception")
    response = client.post("/api/ai/chat", json={"message": "how to vote?"})
    assert response.status_code == 500
    assert "Test exception" in response.json()["detail"]
