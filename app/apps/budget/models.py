from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class BudgetAllocation(Base):
    __tablename__ = "budget_allocations"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), nullable=False)
    category = Column(String, index=True, nullable=False) # e.g. 'Rent', 'Food', 'Transport'
    allocated_amount = Column(Float, nullable=False)
    spent_amount = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
