from slowapi import Limiter
from slowapi.util import get_remote_address

# Initialize Limiter
# Using in-memory storage for now. In production, use Redis: "redis://localhost:6379"
limiter = Limiter(key_func=get_remote_address)
