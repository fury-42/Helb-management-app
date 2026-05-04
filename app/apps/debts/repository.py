from sqlalchemy.orm import Session
from .models import Debt
from typing import List

class DebtRepository:
    def log_debt(self, db: Session, semester_id: int, creditor_name: str, amount: float, due_date) -> Debt:
        debt = Debt(
            semester_id=semester_id,
            creditor_name=creditor_name,
            amount=amount,
            due_date=due_date
        )
        db.add(debt)
        db.commit()
        db.refresh(debt)
        return debt

    def get_debts_by_semester(self, db: Session, semester_id: int) -> List[Debt]:
        return db.query(Debt).filter(Debt.semester_id == semester_id).all()
