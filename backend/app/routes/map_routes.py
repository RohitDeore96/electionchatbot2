from fastapi import APIRouter, Response
import os
from typing import Dict

router = APIRouter()


@router.get("/key")
async def get_map_key(response: Response) -> Dict[str, str]:
    """
    Returns the Google Maps API key securely at runtime.

    Args:
        response (Response): The FastAPI response object.

    Returns:
        Dict[str, str]: A dictionary containing the Google Maps API key.
    """
    response.headers["Cache-Control"] = "public, max-age=300"
    return {"key": os.environ.get("Maps_API_KEY", "")}


@router.get("/geocode")
async def geocode_address(address: str, response: Response) -> Dict[str, float]:  # noqa: E501
    """
    Geocode address using Google Maps API.

    Args:
        address (str): The address to geocode.
        response (Response): The FastAPI response object.

    Returns:
        Dict[str, float]: A dictionary containing latitude and longitude.
    """
    response.headers["Cache-Control"] = "public, max-age=300"
    # Placeholder: Will be wired to Maps API
    return {"lat": 0.0, "lng": 0.0}
