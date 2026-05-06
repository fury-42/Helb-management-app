from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from .schemas import Token
from .providers import get_auth_service
from app.core.rate_limiter import limiter, POST_LIMIT

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
@limiter.limit(POST_LIMIT)
def login(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    service = Depends(get_auth_service)
):
    """Login endpoint to retrieve a JWT access token."""
    return service.authenticate(db, form_data)
