import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes import civic_routes, ai_routes, map_routes
from app.utils.security import add_security_headers
from app.utils.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

app = FastAPI(title="Election Assistant API")
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# Gracefully handle missing environment variables to prevent startup crashes
port = int(os.environ.get("PORT", 8080))
maps_api_key = os.environ.get("Maps_API_KEY", "")
civic_info_api_key = os.environ.get("CIVIC_INFO_API_KEY", "")

# Security: Strict CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://0.0.0.0:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


from typing import Callable, Awaitable, Dict
from fastapi import Response

@app.middleware("http")
async def secure_headers(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    """
    Middleware to apply strict security headers to all HTTP responses.
    
    Args:
        request (Request): The incoming FastAPI request.
        call_next (Callable): The next middleware or route handler.
        
    Returns:
        Response: The modified response containing security headers.
    """
    return await add_security_headers(request, call_next)

# Include Routes
app.include_router(civic_routes.router, prefix="/api/civic", tags=["Civic"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Chatbot"])
app.include_router(map_routes.router, prefix="/api/map", tags=["Maps"])


@app.get("/health")
def health_check() -> Dict[str, str]:
    """
    Perform a health check to verify the API is active.
    
    Returns:
        Dict[str, str]: A dictionary containing the health status and a message.
    """
    return {
        "status": "healthy",
        "message": "Election Assistant Backend Active"}

# Mount React Frontend (MUST be after API routes to avoid catching /api requests)
frontend_path = "../frontend/dist"
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")

if __name__ == "__main__":  # pragma: no cover
    import os
    import uvicorn
    # Hardcode bind to 0.0.0.0:8080 as requested to avoid Cloud Run conflicts
    uvicorn.run(app, host="0.0.0.0", port=8080)
