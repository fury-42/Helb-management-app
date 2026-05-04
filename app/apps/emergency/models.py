from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base

class EmergencyFund(Base):
    __tablename__ = "emergency_funds"
    
    id = Column(Integer, primary_key=True, index=True)
    semester_id = Column(Integer, ForeignKey("semesters.id"), unique=True, nullable=False)
    locked_amount = Column(Float, nullable=False, default=0.0)
    spent_amount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
