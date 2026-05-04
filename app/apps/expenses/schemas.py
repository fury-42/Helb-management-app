from pydantic import BaseModel, Field
from datetime import datetime
from typing import List

class ExpenseLog(BaseModel):
    category: str = Field(..., description="Budget category (e.g., Food, Transport, Rent)")
    description: str = Field(..., description="Short description of what was bought")
    amount: float = Field(..., gt=0, description="Amount spent")
    expense_type: str = Field(..., description="Must be 'Fixed' or 'Flexible'")

class ExpenseResponse(BaseModel):
    id: int
    semester_id: int
    category: str
    description: str
    amount: float
    expense_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class CategorySummary(BaseModel):
    category: str
    total_spent: float
    allocated_amount: float
    percentage_used: float

class ExpenseSummaryResponse(BaseModel):
    total_spent_this_semester: float
    category_summaries: List[CategorySummary]

class ExpenseAlertResponse(BaseModel):
    alerts: List[str]
