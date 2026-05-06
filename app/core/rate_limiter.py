from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

# Initialize Limiter
# Using in-memory storage for now. In production, use Redis: "redis://localhost:6379"
limiter = Limiter(key_func=get_remote_address)

# Default limits
POST_LIMIT = "3/minute"

async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    """Custom handler for rate limit exceeded errors."""
    return JSONResponse(
        status_code=429,
        content={
            "detail": "Rate limit exceeded. Please wait for a minute before trying again.",
            "error": "too_many_requests"
        },
    )

def init_rate_limiting(app: FastAPI):
    """Initialize rate limiting for the application."""
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, rate_limit_exceeded_handler)
