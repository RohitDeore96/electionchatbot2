from fastapi import APIRouter

router = APIRouter()


@router.get("/voter-info")
async def get_voter_info(address: str):
    """Fetch voter info from Google Civic API."""
    # Placeholder: Will be wired to Google Civic Information API
    return {"status": "success", "address": address, "elections": []}
