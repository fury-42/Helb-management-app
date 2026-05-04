from sqlalchemy.orm import Session
from datetime import date
import math
from .schemas import BudgetAllocate, BudgetLimitUpdate, BudgetAllocationResponse, BurnRateResponse
from app.apps.semester.repository import SemesterRepository
from app.shared.exceptions import AppException

class BudgetService:
    def __init__(self, repo, semester_repo):
        self.repo = repo
        self.semester_repo = semester_repo

    def _get_active_semester(self, db: Session, user_id: int):
        semester = self.semester_repo.get_latest(db, user_id)
        if not semester:
            raise AppException(status_code=404, message="No active semester found. Please set one up first.")
        return semester

    def allocate_funds(self, db: Session, user_id: int, data: BudgetAllocate) -> BudgetAllocationResponse:
        semester = self._get_active_semester(db, user_id)
        
        # Check if already allocated
        existing = self.repo.get_allocation_by_category(db, semester.id, data.category)
        if existing:
            raise AppException(status_code=400, message=f"Category '{data.category}' is already allocated. Use the limits update endpoint instead.")
            
        # Check if amount exceeds remaining total funds
        all_allocations = self.repo.get_all_allocations(db, semester.id)
        total_allocated = sum(a.allocated_amount for a in all_allocations)
        
        if total_allocated + data.amount > semester.total_funds:
            raise AppException(status_code=400, message="Allocation exceeds total HELB funds for this semester.")
            
        allocation = self.repo.create_allocation(db, semester.id, data.category, data.amount)
        return allocation

    def update_limits(self, db: Session, user_id: int, data: BudgetLimitUpdate) -> BudgetAllocationResponse:
        semester = self._get_active_semester(db, user_id)
        
        allocation = self.repo.get_allocation_by_category(db, semester.id, data.category)
        if not allocation:
            raise AppException(status_code=404, message=f"Allocation for category '{data.category}' not found.")
            
        # Re-verify total funds constraint
        all_allocations = self.repo.get_all_allocations(db, semester.id)
        total_allocated_others = sum(a.allocated_amount for a in all_allocations if a.id != allocation.id)
        
        if total_allocated_others + data.new_limit > semester.total_funds:
             raise AppException(status_code=400, message="New limit exceeds total available HELB funds.")
             
        updated = self.repo.update_allocation_limit(db, allocation, data.new_limit)
        return updated

    def calculate_burn_rate(self, db: Session, user_id: int) -> BurnRateResponse:
        """
        Calculates the recommended weekly and daily spending limit based on the remaining balance and time.
        This serves as the 'financial heart' of the app.
        """
        semester = self._get_active_semester(db, user_id)
        today = date.today()
        
        # 1. Calculate time remaining
        if today > semester.end_date:
            raise AppException(status_code=400, message="Semester has already ended.")
            
        start_tracking_date = max(today, semester.start_date)
        days_left = (semester.end_date - start_tracking_date).days
        
        if days_left <= 0:
            days_left = 1 # Avoid division by zero on the last day
            
        weeks_left = math.ceil(days_left / 7.0)
        
        # 2. Calculate funds available (flexible funds)
        # Ideally, we subtract fixed expenses (Rent, etc.) to give a flexible burn rate.
        # For now, we calculate burn rate based on total unspent balance.
        # In the future, this can be refined to exclude "Fixed" budget categories.
        
        remaining = semester.remaining_balance
        
        # 3. Calculate rates
        daily_spend = remaining / days_left
        weekly_spend = remaining / weeks_left if weeks_left > 0 else remaining
        
        # 4. Determine status
        status = "On Track"
        # Logic for warning/danger can be expanded based on user's actual expense velocity
        if daily_spend < 100: # Arbitrary threshold, can be configured
            status = "Danger - Severely low funds"
        elif daily_spend < 300:
            status = "Warning - Adjust spending"
            
        return BurnRateResponse(
            total_remaining=remaining,
            weeks_left=weeks_left,
            recommended_weekly_spend=round(weekly_spend, 2),
            recommended_daily_spend=round(daily_spend, 2),
            status=status
        )
