from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class Expense(Base):
    __tablename__ = "expenses"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    category = Column(String, index=True, nullable=False)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    expense_type = Column(String, nullable=False) # e.g. 'Fixed', 'Flexible'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
