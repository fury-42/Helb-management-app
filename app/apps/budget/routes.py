from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import BudgetAllocate, BudgetLimitUpdate, BudgetAllocationResponse, BurnRateResponse
from .providers import get_budget_service
from app.core.database import get_db
from app.core.security import get_current_student
from app.apps.users.models import User

router = APIRouter(prefix="/budget", tags=["Budget"])

@router.post("/allocate", response_model=BudgetAllocationResponse)
def allocate_funds(
    data: BudgetAllocate,
    db: Session = Depends(get_db),
    service = Depends(get_budget_service),
    current_user: User = Depends(get_current_student)
):
    """Breaks down the lump sum into key areas (e.g., Rent, Food)."""
    return service.allocate_funds(db, current_user.id, data)

@router.put("/limits", response_model=BudgetAllocationResponse)
def update_limits(
    data: BudgetLimitUpdate,
    db: Session = Depends(get_db),
    service = Depends(get_budget_service),
    current_user: User = Depends(get_current_student)
):
    """Allows students to adjust category limits."""
    return service.update_limits(db, current_user.id, data)

@router.get("/burn-rate", response_model=BurnRateResponse)
def get_burn_rate(
    db: Session = Depends(get_db),
    service = Depends(get_budget_service),
    current_user: User = Depends(get_current_student)
):
    """
    Calculates the recommended weekly spending limit based on remaining balance and time.
    The 'financial heart' of the application.
    """
    return service.calculate_burn_rate(db, current_user.id)
