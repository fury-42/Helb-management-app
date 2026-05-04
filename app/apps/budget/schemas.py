from pydantic import BaseModel, Field
from typing import Optional

class BudgetAllocate(BaseModel):
    category: str = Field(..., description="Category like 'Rent', 'Food'")
    amount: float = Field(..., gt=0, description="Amount allocated to this category")

class BudgetLimitUpdate(BaseModel):
    category: str = Field(..., description="Category to update")
    new_limit: float = Field(..., gt=0, description="New allocated limit")

class BudgetAllocationResponse(BaseModel):
    id: int
    semester_id: int
    category: str
    allocated_amount: float
    spent_amount: float
    
    class Config:
        from_attributes = True

class BurnRateResponse(BaseModel):
    total_remaining: float
    weeks_left: int
    recommended_weekly_spend: float
    recommended_daily_spend: float
    status: str # e.g., 'On Track', 'Warning', 'Danger'
