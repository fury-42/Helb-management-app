from pydantic import BaseModel, Field

class EmergencyReserve(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to lock into the contingency fund")

class EmergencyBalance(BaseModel):
    id: int
    semester_id: int
    locked_amount: float
    spent_amount: float
    available_balance: float

    class Config:
        from_attributes = True
