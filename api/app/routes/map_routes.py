"""
Spatial routing and geolocation handlers for the platform.
Delivers keys and coordinates securely.
"""
from fastapi import APIRouter, Response
import os
from typing import Dict

from app.constants import CACHE_CONTROL_PUBLIC, MAPS_API_ENV_KEY

router = APIRouter()


@router.get("/key")
async def get_map_key(response: Response) -> Dict[str, str]:
    """
    Serve the Google Maps authorization token securely during execution.

    Args:
        response (Response): The FastAPI response object.

    Returns:
        Dict[str, str]: A dictionary containing the Google Maps API key.
        
    Raises:
        None
    """
    response.headers["Cache-Control"] = CACHE_CONTROL_PUBLIC
    return {"key": os.environ.get(MAPS_API_ENV_KEY, "")}


@router.get("/geocode")
async def geocode_address(address: str, response: Response) -> Dict[str, float]:  # noqa: E501
    """
    Translate a string address into geospatial coordinates via Google Maps.

    Args:
        address (str): The address to geocode.
        response (Response): The FastAPI response object.

    Returns:
        Dict[str, float]: A dictionary containing latitude and longitude.
        
    Raises:
        None
    """
    response.headers["Cache-Control"] = CACHE_CONTROL_PUBLIC
    # Placeholder: Will be wired to Maps API
    return {"lat": 0.0, "lng": 0.0}
