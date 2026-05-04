from sqlalchemy.orm import Session
from .schemas import DebtLog, DebtResponse
from app.apps.semester.repository import SemesterRepository
from app.shared.exceptions import AppException

class DebtService:
    def __init__(self, repo, semester_repo):
        self.repo = repo
        self.semester_repo = semester_repo

    def _get_active_semester(self, db: Session, user_id: int):
        semester = self.semester_repo.get_latest(db, user_id)
        if not semester:
            raise AppException(status_code=404, message="No active semester found.")
        return semester

    def log_debt(self, db: Session, user_id: int, data: DebtLog) -> DebtResponse:
        semester = self._get_active_semester(db, user_id)
        
        debt = self.repo.log_debt(
            db, semester.id, data.creditor_name, data.amount, data.due_date
        )
        
        return debt

    def get_all_debts(self, db: Session, user_id: int):
        semester = self._get_active_semester(db, user_id)
        return self.repo.get_debts_by_semester(db, semester.id)
