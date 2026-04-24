from fastapi import Request


async def add_security_headers(request: Request, call_next):
    """Adds strict security headers to the response."""
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = "default-src 'self'; script-src 'self' https://maps.googleapis.com 'unsafe-inline' 'unsafe-eval'; img-src 'self' https://maps.gstatic.com https://*.googleapis.com data:;"
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    return response
