from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from .schemas import LoanCreate, LoanRead, LoanUpdateStatus
from .providers import get_loan_service

router = APIRouter(prefix="/loans", tags=["Loans"])

@router.post("/", response_model=LoanRead)
def apply_for_loan(
    data: LoanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    service = Depends(get_loan_service)
):
    """Apply for a new HELB loan."""
    return service.apply_for_loan(db, current_user.id, data)

@router.get("/", response_model=List[LoanRead])
def get_my_loans(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    service = Depends(get_loan_service)
):
    """Get all loan applications for the current user."""
    return service.get_user_loans(db, current_user.id)

@router.patch("/{loan_id}/approve", response_model=LoanRead)
def approve_loan(
    loan_id: int,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    service = Depends(get_loan_service)
):
    """Approve a loan application (Admin/Officer only)."""
    # In a real app, check for admin/officer role here
    if current_user.role not in ["admin", "officer"]:
        from app.shared.exceptions import AppException
        raise AppException(status_code=403, message="Only admins or officers can approve loans")
        
    return service.approve_loan(db, loan_id, background_tasks)
