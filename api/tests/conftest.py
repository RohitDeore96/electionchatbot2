"""
Pytest configuration and fixtures.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Provide a FastAPI test client.

    Returns:
        TestClient: The FastAPI test client.
    """
    return TestClient(app)
