from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class DebtLog(BaseModel):
    creditor_name: str = Field(..., description="Who you owe money to")
    amount: float = Field(..., gt=0, description="Amount owed")
    due_date: Optional[date] = Field(None, description="When the debt is due")

class DebtResponse(BaseModel):
    id: int
    semester_id: int
    creditor_name: str
    amount: float
    due_date: Optional[date]
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
