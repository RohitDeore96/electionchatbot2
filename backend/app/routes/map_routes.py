from fastapi import APIRouter
import os
from typing import Dict

router = APIRouter()


@router.get("/key")
async def get_map_key() -> Dict[str, str]:
    """
    Returns the Google Maps API key securely at runtime.
    
    Returns:
        Dict[str, str]: A dictionary containing the Google Maps API key.
    """
    return {"key": os.environ.get("Maps_API_KEY", "")}

@router.get("/geocode")
async def geocode_address(address: str) -> Dict[str, float]:
    """
    Geocode address using Google Maps API.
    
    Args:
        address (str): The address to geocode.
        
    Returns:
        Dict[str, float]: A dictionary containing latitude and longitude.
    """
    # Placeholder: Will be wired to Maps API
    return {"lat": 0.0, "lng": 0.0}
