from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import ExpenseLog, ExpenseResponse, ExpenseSummaryResponse, ExpenseAlertResponse
from .providers import get_expense_service
from app.core.database import get_db
from app.core.security import get_current_student
from app.apps.users.models import User

router = APIRouter(prefix="/expenses", tags=["Expenses"])

@router.post("/log", response_model=ExpenseResponse)
def log_expense(
    data: ExpenseLog,
    db: Session = Depends(get_db),
    service = Depends(get_expense_service),
    current_user: User = Depends(get_current_student)
):
    """Records an expense and updates the active semester balance and category budget."""
    return service.log_expense(db, current_user.id, data)

@router.get("/summary", response_model=ExpenseSummaryResponse)
def get_expense_summary(
    db: Session = Depends(get_db),
    service = Depends(get_expense_service),
    current_user: User = Depends(get_current_student)
):
    """Generates reports showing where money is going."""
    return service.generate_summary(db, current_user.id)

@router.get("/alerts", response_model=ExpenseAlertResponse)
def get_expense_alerts(
    db: Session = Depends(get_db),
    service = Depends(get_expense_service),
    current_user: User = Depends(get_current_student)
):
    """Checks if any category is approaching its threshold."""
    return service.check_alerts(db, current_user.id)
