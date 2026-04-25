"""
Standardized error formatting utility to ensure DRY compliance.
"""
from typing import Dict, Any
from fastapi import HTTPException

def build_error_response(status_code: int, message: str) -> Dict[str, Any]:
    """
    Construct a standardized error dictionary.

    Args:
        status_code (int): The HTTP status code.
        message (str): The error details.

    Returns:
        Dict[str, Any]: A JSON-serializable error structure.

    Raises:
        HTTPException: Always raises to halt the request lifecycle.
    """
    raise HTTPException(status_code=status_code, detail=message)
