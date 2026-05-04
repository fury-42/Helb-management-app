from sqlalchemy.orm import Session
from .schemas import EmergencyReserve, EmergencyBalance
from app.apps.semester.repository import SemesterRepository
from app.shared.exceptions import AppException

class EmergencyService:
    def __init__(self, repo, semester_repo):
        self.repo = repo
        self.semester_repo = semester_repo

    def _get_active_semester(self, db: Session, user_id: int):
        semester = self.semester_repo.get_latest(db, user_id)
        if not semester:
            raise AppException(status_code=404, message="No active semester found.")
        return semester

    def reserve_funds(self, db: Session, user_id: int, data: EmergencyReserve) -> EmergencyBalance:
        semester = self._get_active_semester(db, user_id)
        
        if semester.remaining_balance < data.amount:
            raise AppException(status_code=400, message="Insufficient funds in the active semester to reserve this amount.")
            
        # Deduct from semester balance
        self.semester_repo.update_balance(db, semester, semester.remaining_balance - data.amount)
        
        # Add to emergency fund
        fund = self.repo.create_or_get_fund(db, semester.id)
        fund = self.repo.add_reserve(db, fund, data.amount)
        
        return self._format_response(fund)

    def get_balance(self, db: Session, user_id: int) -> EmergencyBalance:
        semester = self._get_active_semester(db, user_id)
        fund = self.repo.create_or_get_fund(db, semester.id)
        return self._format_response(fund)

    def _format_response(self, fund) -> EmergencyBalance:
        return EmergencyBalance(
            id=fund.id,
            semester_id=fund.semester_id,
            locked_amount=fund.locked_amount,
            spent_amount=fund.spent_amount,
            available_balance=fund.locked_amount - fund.spent_amount
        )
