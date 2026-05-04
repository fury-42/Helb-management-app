from sqlalchemy.orm import Session
from .models import Semester
from typing import Optional

class SemesterRepository:
    def create(self, db: Session, user_id: int, total_funds: float, start_date, end_date) -> Semester:
        semester = Semester(
            user_id=user_id,
            total_funds=total_funds,
            remaining_balance=total_funds,
            start_date=start_date,
            end_date=end_date
        )
        db.add(semester)
        db.commit()
        db.refresh(semester)
        return semester

    def get_latest(self, db: Session, user_id: int) -> Optional[Semester]:
        # Get the latest active semester for this specific user
        return db.query(Semester).filter(Semester.user_id == user_id).order_by(Semester.id.desc()).first()

    def update_balance(self, db: Session, semester: Semester, new_balance: float) -> Semester:
        semester.remaining_balance = new_balance
        db.commit()
        db.refresh(semester)
        return semester
