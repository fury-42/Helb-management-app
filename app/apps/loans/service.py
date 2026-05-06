from sqlalchemy.orm import Session
from fastapi import BackgroundTasks
from .schemas import LoanCreate, LoanUpdateStatus
from .models import Loan, LoanStatus
from app.shared.exceptions import AppException
from app.shared.notifications import notification_service

class LoanService:
    def __init__(self, repo):
        self.repo = repo

    def apply_for_loan(self, db: Session, user_id: int, data: LoanCreate) -> Loan:
        return self.repo.create(db, user_id, data.amount, data.description)

    def approve_loan(self, db: Session, loan_id: int, background_tasks: BackgroundTasks) -> Loan:
        loan = self.repo.get_by_id(db, loan_id)
        if not loan:
            raise AppException(status_code=404, message="Loan not found")
        
        if loan.status != LoanStatus.PENDING:
            raise AppException(status_code=400, message=f"Loan is already {loan.status.value}")

        updated_loan = self.repo.update_status(db, loan, LoanStatus.APPROVED)
        
        # Trigger background task for SMS
        user = updated_loan.user
        if user and user.phone_number:
            message = f"Congratulations {user.email}! Your HELB loan of KES {loan.amount} has been APPROVED. Funds will be disbursed shortly."
            background_tasks.add_task(
                notification_service.send_sms, 
                user.phone_number, 
                message
            )
            
        return updated_loan

    def get_user_loans(self, db: Session, user_id: int):
        return self.repo.get_all_by_user(db, user_id)
