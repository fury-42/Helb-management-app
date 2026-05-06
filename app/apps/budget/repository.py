from sqlalchemy.orm import Session
from .models import BudgetAllocation
from typing import List, Optional

class BudgetRepository:
    def create_allocation(self, db: Session, semester_id: int, category: str, amount: float) -> BudgetAllocation:
        allocation = BudgetAllocation(
            semester_id=semester_id,
            category=category,
            allocated_amount=amount
        )
        db.add(allocation)
        db.commit()
        db.refresh(allocation)
        return allocation

    def get_allocation_by_category(self, db: Session, semester_id: int, category: str) -> Optional[BudgetAllocation]:
        return db.query(BudgetAllocation).filter(
            BudgetAllocation.semester_id == semester_id,
            BudgetAllocation.category == category
        ).first()

    def get_all_allocations(self, db: Session, semester_id: int) -> List[BudgetAllocation]:
        return db.query(BudgetAllocation).filter(
            BudgetAllocation.semester_id == semester_id
        ).all()

    def update_allocation_limit(self, db: Session, allocation: BudgetAllocation, new_limit: float) -> BudgetAllocation:
        allocation.allocated_amount = new_limit
        db.commit()
        db.refresh(allocation)
        return allocation

    def increment_spent_amount(self, db: Session, allocation: BudgetAllocation, amount: float) -> BudgetAllocation:
        allocation.spent_amount += amount
        db.commit()
        db.refresh(allocation)
        return allocation
