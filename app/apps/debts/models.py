from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Date
from sqlalchemy.sql import func
from app.core.database import Base

class Debt(Base):
    __tablename__ = "debts"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    creditor_name = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=True)
    status = Column(String, nullable=False, default="Unpaid") # e.g. 'Unpaid', 'Paid'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
