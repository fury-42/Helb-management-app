from fastapi import Request, Header
from app.shared.exceptions import AppException
from loguru import logger

# Simple in-memory storage for demonstration. 
# In production, use Redis with an expiration time.
IDEMPOTENCY_KEYS = {}

def check_idempotency(x_idempotency_key: str = Header(None)):
    if not x_idempotency_key:
        return None
    
    if x_idempotency_key in IDEMPOTENCY_KEYS:
        logger.warning(f"Duplicate request detected for key: {x_idempotency_key}")
        raise AppException(status_code=400, message="Duplicate request. This operation has already been processed.")
    
    # Store the key
    IDEMPOTENCY_KEYS[x_idempotency_key] = True
    logger.info(f"Idempotency key registered: {x_idempotency_key}")
    return x_idempotency_key
