from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.routes import civic_routes, ai_routes, map_routes
from app.utils.security import add_security_headers

app = FastAPI(title="Election Assistant API")

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
