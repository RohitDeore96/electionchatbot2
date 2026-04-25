"""
Tests for utility and helper functions.
"""
import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from datetime import datetime

from app.utils.error_utils import build_error_response
from app.utils.ai_helper import format_ai_payload, generate_ai_response
from app.services.firestore_service import log_chat_to_firestore
from app.utils.storage import upload_to_gcs
from app.utils.security import add_security_headers
from fastapi import Request, Response


def test_build_error_response() -> None:
    """Test standardized error builder raises properly shaped exception."""
    with pytest.raises(HTTPException) as exc_info:
        build_error_response(400, "Bad Request Format")
    
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Bad Request Format"


def test_format_ai_payload() -> None:
    """Test AI payload formatter returns correct schema."""
    result = format_ai_payload("hello world")
    assert result == {"response": "hello world"}


@patch("app.services.firestore_service.db")
def test_log_chat_to_firestore_success(mock_db: MagicMock) -> None:
    """Test successful firestore logging."""
    mock_collection = MagicMock()
    mock_db.collection.return_value = mock_collection
    
    timestamp = datetime.now()
    log_chat_to_firestore("test message", timestamp)
    
    mock_db.collection.assert_called_once_with("chat_logs")
    mock_collection.add.assert_called_once_with({
        "message": "test message", 
        "timestamp": timestamp
    })


@patch("app.services.firestore_service.db")
@patch("app.services.firestore_service.logger.error")
def test_log_chat_to_firestore_exception(mock_logger_error: MagicMock, mock_db: MagicMock) -> None:
    """Test firestore logging gracefully handles exceptions."""
    mock_db.collection.side_effect = Exception("DB Connection Refused")
    
    timestamp = datetime.now()
    log_chat_to_firestore("test message", timestamp)
    
    mock_logger_error.assert_called_once()
    assert "DB Connection Refused" in mock_logger_error.call_args[0][0]


@patch("app.services.firestore_service.db", None)
@patch("app.services.firestore_service.logger.info")
def test_log_chat_to_firestore_mock_mode(mock_logger_info: MagicMock) -> None:
    """Test firestore fallback logging when DB is not initialized."""
    timestamp = datetime.now()
    log_chat_to_firestore("test message", timestamp)
    
    mock_logger_info.assert_called_once()
    assert "Mock Firestore log" in mock_logger_info.call_args[0][0]


def test_generate_ai_response_success() -> None:
    """Test AI response generator success path."""
    mock_agent = MagicMock()
    mock_agent.get_response.return_value = "ai response"
    
    result = generate_ai_response(mock_agent, "hello")
    assert result == "ai response"


def test_generate_ai_response_exception() -> None:
    """Test AI response generator raises HTTP error on failure."""
    mock_agent = MagicMock()
    mock_agent.get_response.side_effect = Exception("Vertex limit")
    
    with pytest.raises(HTTPException) as exc_info:
        generate_ai_response(mock_agent, "hello")
        
    assert exc_info.value.status_code == 500
    assert "Vertex limit" in exc_info.value.detail


@patch("app.utils.storage.storage_client")
def test_upload_to_gcs_success(mock_client: MagicMock) -> None:
    """Test successful GCS upload."""
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_bucket.blob.return_value = mock_blob
    mock_client.bucket.return_value = mock_bucket
    
    assert upload_to_gcs("bucket", "file.txt", "dest.txt") is True
    mock_blob.upload_from_filename.assert_called_once_with("file.txt")


@patch("app.utils.storage.storage_client")
def test_upload_to_gcs_exception(mock_client: MagicMock) -> None:
    """Test GCS upload gracefully handles errors."""
    mock_client.bucket.side_effect = Exception("Upload failed")
    assert upload_to_gcs("bucket", "file.txt", "dest.txt") is False


@patch("app.utils.storage.storage_client", None)
def test_upload_to_gcs_no_client() -> None:
    """Test GCS upload returns false when client is missing."""
    assert upload_to_gcs("bucket", "file.txt", "dest.txt") is False


@pytest.mark.asyncio
async def test_add_security_headers() -> None:
    """Test security middleware appends correct headers."""
    mock_request = MagicMock(spec=Request)
    mock_response = Response()
    
    async def mock_call_next(req: Request) -> Response:
        return mock_response
        
    res = await add_security_headers(mock_request, mock_call_next)
    assert res.headers["X-Frame-Options"] == "DENY"
    assert res.headers["X-Content-Type-Options"] == "nosniff"
    assert res.headers["Server"] == "Hidden"
