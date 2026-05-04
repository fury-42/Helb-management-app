from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from .models import Expense
from typing import List

class ExpenseRepository:
    def log_expense(self, db: Session, semester_id: int, category: str, description: str, amount: float, expense_type: str) -> Expense:
        expense = Expense(
            semester_id=semester_id,
            category=category,
            description=description,
            amount=amount,
            expense_type=expense_type
        )
        db.add(expense)
        db.commit()
        db.refresh(expense)
        return expense

    def get_expenses_by_semester(self, db: Session, semester_id: int) -> List[Expense]:
        return db.query(Expense).filter(Expense.semester_id == semester_id).all()
