from sqlalchemy.orm import Session
from datetime import date
import math
from .schemas import SemesterSetup, SemesterUpdateFunds, SemesterStatus
from app.shared.exceptions import AppException
from app.shared.notifications import notification_service
from fastapi import BackgroundTasks

class SemesterService:
    def __init__(self, repo):
        self.repo = repo

    def setup_semester(self, db: Session, user, data: SemesterSetup, background_tasks: BackgroundTasks) -> SemesterStatus:
        if data.start_date >= data.end_date:
            raise AppException(status_code=400, message="End date must be after start date")
        
        # Check if an active semester already exists for this user
        existing = self.repo.get_latest(db, user.id)
        if existing and existing.end_date >= date.today():
            raise AppException(status_code=400, message="An active semester already exists")

        semester = self.repo.create(db, user.id, data.total_funds, data.start_date, data.end_date)
        
        # Trigger background task for SMS
        if user.phone_number:
            background_tasks.add_task(
                notification_service.send_sms, 
                user.phone_number, 
                f"Hello {user.email}, your HELB semester setup for {semester.total_funds} is successful!"
            )
            
        return self._format_status(semester)

    def get_status(self, db: Session, user_id: int) -> SemesterStatus:
        semester = self._get_active_semester(db, user_id)
        return self._format_status(semester)

    def update_funds(self, db: Session, user_id: int, data: SemesterUpdateFunds) -> SemesterStatus:
        semester = self._get_active_semester(db, user_id)
        
        new_balance = semester.remaining_balance + data.amount
        if new_balance < 0:
            raise AppException(status_code=400, message="Insufficient funds. Balance cannot be negative.")
            
        updated_semester = self.repo.update_balance(db, semester, new_balance)
        return self._format_status(updated_semester)

    def _get_active_semester(self, db: Session, user_id: int):
        semester = self.repo.get_latest(db, user_id)
        if not semester:
            raise AppException(status_code=404, message="No semester setup found. Please setup a semester first.")
        return semester

    def _format_status(self, semester) -> SemesterStatus:
        # Calculate weeks left
        today = date.today()
        
        if today > semester.end_date:
            weeks_left = 0
        else:
            days = (semester.end_date - today).days
            weeks_left = math.ceil(days / 7)
            
        return SemesterStatus(
            id=semester.id,
            total_funds=semester.total_funds,
            remaining_balance=semester.remaining_balance,
            start_date=semester.start_date,
            end_date=semester.end_date,
            weeks_left=weeks_left,
            created_at=semester.created_at
        )
