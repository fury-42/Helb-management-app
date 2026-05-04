from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from .schemas import SemesterSetup, SemesterUpdateFunds, SemesterStatus
from .providers import get_semester_service
from app.core.database import get_db
from app.core.security import get_current_student
from app.apps.users.models import User
from app.core.rate_limiter import limiter
from fastapi import Request
from app.shared.idempotency import check_idempotency

router = APIRouter(prefix="/semester", tags=["Semester"])

@router.post("/setup", response_model=SemesterStatus)
def setup_semester(
    data: SemesterSetup,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    service = Depends(get_semester_service),
    current_user: User = Depends(get_current_student),
    idempotency_key: str = Depends(check_idempotency)
):
    """Initialize the semester by inputting the total HELB funds and the duration."""
    return service.setup_semester(db, current_user, data, background_tasks)

@router.get("/status", response_model=SemesterStatus)
@limiter.limit("5/minute")
def get_semester_status(
    request: Request,
    db: Session = Depends(get_db),
    service = Depends(get_semester_service),
    current_user: User = Depends(get_current_student)
):
    """Returns the Balance Overview, including total remaining balance and weeks left."""
    return service.get_status(db, current_user.id)

@router.patch("/update-funds", response_model=SemesterStatus)
def update_funds(
    data: SemesterUpdateFunds,
    db: Session = Depends(get_db),
    service = Depends(get_semester_service),
    current_user: User = Depends(get_current_student)
):
    """Adjusts the balance if additional funds are received or if initial estimates change."""
    return service.update_funds(db, current_user.id, data)
