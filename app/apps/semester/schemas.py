from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

class SemesterSetup(BaseModel):
    total_funds: float = Field(..., gt=0, description="Total HELB funds received")
    start_date: date = Field(..., description="Start date of the semester")
    end_date: date = Field(..., description="End date of the semester")

class SemesterUpdateFunds(BaseModel):
    amount: float = Field(..., description="Amount to add (positive) or remove (negative)")

class SemesterStatus(BaseModel):
    id: int
    total_funds: float
    remaining_balance: float
    start_date: date
    end_date: date
    weeks_left: int
    created_at: datetime
    
    class Config:
        from_attributes = True
