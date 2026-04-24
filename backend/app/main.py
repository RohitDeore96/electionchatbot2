import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import civic_routes, ai_routes, map_routes
from app.utils.security import add_security_headers

app = FastAPI(title="Election Assistant API")

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


@app.middleware("http")
async def secure_headers(request: Request, call_next):
    return await add_security_headers(request, call_next)

# Include Routes
app.include_router(civic_routes.router, prefix="/api/civic", tags=["Civic"])
app.include_router(ai_routes.router, prefix="/api/ai", tags=["AI Chatbot"])
app.include_router(map_routes.router, prefix="/api/map", tags=["Maps"])


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Election Assistant Backend Active"}

if __name__ == "__main__":
    import os
    import uvicorn
    # Cloud Run provides the port via environment variable. Default to 8080.
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
