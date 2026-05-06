from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from .models import LoanStatus

class LoanBase(BaseModel):
    amount: float
    description: Optional[str] = None

class LoanCreate(LoanBase):
    pass

class LoanUpdateStatus(BaseModel):
    status: LoanStatus

class LoanRead(LoanBase):
    id: int
    user_id: int
    status: LoanStatus
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True
