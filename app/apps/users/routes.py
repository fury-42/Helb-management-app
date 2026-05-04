from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse, UserWithSemestersResponse
from .providers import get_user_service
from app.core.database import get_db
from app.core.security import get_current_admin

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=UserResponse)
def register(
    data: UserCreate,
    db: Session = Depends(get_db),
    service = Depends(get_user_service)
):
    """Register a new user (student, admin, officer)."""
    return service.register_user(db, data)

@router.get("/admin/students", response_model=list[UserWithSemestersResponse])
def get_all_students(
    db: Session = Depends(get_db),
    service = Depends(get_user_service),
    admin = Depends(get_current_admin)
):
    """Admin only: Fetches all students and their semester history using eager loading (prevents N+1)."""
    return service.get_all_with_semesters(db)
