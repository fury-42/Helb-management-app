from sqlalchemy.orm import Session
from .models import Loan, LoanStatus

class LoanRepository:
    def create(self, db: Session, user_id: int, amount: float, description: str = None) -> Loan:
        loan = Loan(user_id=user_id, amount=amount, description=description)
        db.add(loan)
        db.commit()
        db.refresh(loan)
        return loan

    def get_by_id(self, db: Session, loan_id: int) -> Loan:
        return db.query(Loan).filter(Loan.id == loan_id).first()

    def update_status(self, db: Session, loan: Loan, status: LoanStatus) -> Loan:
        loan.status = status
        db.commit()
        db.refresh(loan)
        return loan

    def get_all_by_user(self, db: Session, user_id: int):
        return db.query(Loan).filter(Loan.user_id == user_id).all()
