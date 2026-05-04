from sqlalchemy.orm import Session
from .models import EmergencyFund
from typing import Optional

class EmergencyRepository:
    def create_or_get_fund(self, db: Session, semester_id: int) -> EmergencyFund:
        fund = db.query(EmergencyFund).filter(EmergencyFund.semester_id == semester_id).first()
        if not fund:
            fund = EmergencyFund(semester_id=semester_id, locked_amount=0.0, spent_amount=0.0)
            db.add(fund)
            db.commit()
            db.refresh(fund)
        return fund

    def add_reserve(self, db: Session, fund: EmergencyFund, amount: float) -> EmergencyFund:
        fund.locked_amount += amount
        db.commit()
        db.refresh(fund)
        return fund
