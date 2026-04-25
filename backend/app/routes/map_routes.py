"""
Map routes for the Election Assistant API.
Provides endpoints for fetching map API keys and geocoding.
"""
from fastapi import APIRouter, Response
import os
from typing import Dict

CACHE_CONTROL = "public, max-age=300"
MAPS_API_ENV_KEY = "Maps_API_KEY"

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
    response.headers["Cache-Control"] = CACHE_CONTROL
    return {"key": os.environ.get(MAPS_API_ENV_KEY, "")}


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
    response.headers["Cache-Control"] = CACHE_CONTROL
    # Placeholder: Will be wired to Maps API
    return {"lat": 0.0, "lng": 0.0}
