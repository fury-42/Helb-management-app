from pydantic import BaseModel, EmailStr, Field
from datetime import datetime, date
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr = Field(..., description="User's email address")
    phone_number: Optional[str] = Field(None, description="User's phone number for SMS notifications")
    password: str = Field(..., min_length=6, description="Password (min 6 chars)")
    role: str = Field(default="student", description="Role: student, admin, officer")

class UserResponse(BaseModel):
    id: int
    email: str
    phone_number: Optional[str]
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class SemesterMinimalResponse(BaseModel):
    id: int
    total_funds: float
    remaining_balance: float
    start_date: date
    end_date: date

    class Config:
        from_attributes = True

class LoanMinimalResponse(BaseModel):
    id: int
    amount: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserWithSemestersResponse(UserResponse):
    semesters: list[SemesterMinimalResponse] = []
    loans: list[LoanMinimalResponse] = []
