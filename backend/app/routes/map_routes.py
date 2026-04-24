from fastapi import APIRouter
import os

router = APIRouter()


@router.get("/key")
async def get_map_key() -> dict:
    """Returns the Google Maps API key securely at runtime."""
    return {"key": os.environ.get("Maps_API_KEY", "")}

@router.get("/geocode")
async def geocode_address(address: str) -> dict:
    """Geocode address using Google Maps API."""
    # Placeholder: Will be wired to Maps API
    return {"lat": 0.0, "lng": 0.0}
