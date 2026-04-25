"""
Civic Information routes for the Election Assistant API.
Provides endpoints for fetching voter information.
"""
from fastapi import APIRouter, Response
from typing import Dict, Any

CACHE_CONTROL = "public, max-age=300"

router = APIRouter()


@router.get("/voter-info")
async def get_voter_info(address: str, response: Response) -> Dict[str, Any]:
    """
    Fetch voter info from Google Civic API.

    Args:
        address (str): The address of the voter.
        response (Response): The FastAPI response object.

    Returns:
        Dict[str, Any]: A dictionary containing voter info.
    """
    response.headers["Cache-Control"] = CACHE_CONTROL
    # Placeholder: Will be wired to Google Civic Information API
    return {"status": "success", "address": address, "elections": []}
