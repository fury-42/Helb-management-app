from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import EmergencyReserve, EmergencyBalance
from .providers import get_emergency_service
from app.core.database import get_db
from app.core.security import get_current_student
from app.apps.users.models import User

router = APIRouter(prefix="/emergency", tags=["Emergency"])

@router.post("/reserve", response_model=EmergencyBalance)
def reserve_funds(
    data: EmergencyReserve,
    db: Session = Depends(get_db),
    service = Depends(get_emergency_service),
    current_user: User = Depends(get_current_student)
):
    """Sets aside a specific portion of HELB funds as a 'locked' contingency fund."""
    return service.reserve_funds(db, current_user.id, data)

@router.get("/balance", response_model=EmergencyBalance)
def get_emergency_balance(
    db: Session = Depends(get_db),
    service = Depends(get_emergency_service),
    current_user: User = Depends(get_current_student)
):
    """Views funds available for unexpected costs like medical bills."""
    return service.get_balance(db, current_user.id)
