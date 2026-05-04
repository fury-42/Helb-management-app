from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .schemas import DebtLog, DebtResponse
from .providers import get_debt_service
from app.core.database import get_db
from app.core.security import get_current_student
from app.apps.users.models import User

router = APIRouter(prefix="/debts", tags=["Debts"])

@router.post("/log", response_model=DebtResponse)
def log_debt(
    data: DebtLog,
    db: Session = Depends(get_db),
    service = Depends(get_debt_service),
    current_user: User = Depends(get_current_student)
):
    """Tracks peer-to-peer borrowing so students can plan to settle debts."""
    return service.log_debt(db, current_user.id, data)

@router.get("/", response_model=List[DebtResponse])
def get_debts(
    db: Session = Depends(get_db),
    service = Depends(get_debt_service),
    current_user: User = Depends(get_current_student)
):
    """Retrieve all logged debts for the active semester."""
    return service.get_all_debts(db, current_user.id)
