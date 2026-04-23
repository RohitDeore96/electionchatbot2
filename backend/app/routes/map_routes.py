from fastapi import APIRouter

router = APIRouter()


@router.get("/geocode")
async def geocode_address(address: str):
    """Geocode address using Google Maps API."""
    # Placeholder: Will be wired to Maps API
    return {"lat": 0.0, "lng": 0.0}
