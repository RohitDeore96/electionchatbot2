"""
Core entry point for the backend server logic.
Bootstraps the FastAPI framework, networking rules, and sub-routers.
"""
import os
import logging
from typing import Callable, Awaitable, Dict
from fastapi import FastAPI, Request, Response
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.routes import civic_routes, ai_routes, map_routes
from app.utils.security import add_security_headers
from app.utils.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

API_TITLE = "Election Assistant API"
GZIP_MIN_SIZE = 1000
DEFAULT_PORT = 8000
ALLOWED_ORIGINS = ["http://localhost:5173", "https://YOUR_ACTUAL_FRONTEND_URL"]

app = FastAPI(
    title=API_TITLE, docs_url=None, redoc_url=None, openapi_url=None
)  # noqa: E501
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(GZipMiddleware, minimum_size=GZIP_MIN_SIZE)


try:
    import google.cloud.logging

    client = google.cloud.logging.Client()
    client.setup_logging()
except ImportError:
    logging.basicConfig(level=logging.INFO)

# Fail-safe variable parsing to avoid immediate boot panics
port = int(os.environ.get("PORT", DEFAULT_PORT))
maps_api_key = os.environ.get("Maps_API_KEY", "")
civic_info_api_key = os.environ.get("CIVIC_INFO_API_KEY", "")

# Security: Strict CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def secure_headers(
    request: Request, call_next: Callable[[Request], Awaitable[Response]]
) -> Response:
    """
    HTTP response middleware to inject mandatory OWASP security headers.

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
    Verification endpoint to ensure the system is operational.

    Returns:
        Dict[str, str]: A dictionary containing the health status and a message.  # noqa: E501
    """
    return {"status": "healthy", "message": "Election Assistant Backend Active"}


# Serve Static Application Files (executed after API routes to avoid greedy catching)  # noqa: E501
frontend_path = "../client/dist"
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="static")  # noqa: E501

if __name__ == "__main__":  # pragma: no cover
    import os
    import uvicorn

    # Hardcode bind to BIND_HOST as requested to avoid Cloud Run conflicts  # noqa: E501
    BIND_HOST = "0.0.0.0"
    uvicorn.run(app, host=BIND_HOST, port=port)
