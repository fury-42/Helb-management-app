from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .models import PaymentStatus, PaymentProvider

class STKPushRequest(BaseModel):
    phone_number: str = Field(..., example="254712345678")
    amount: float = Field(..., gt=0)
    description: Optional[str] = "HELB Payment"

class BankTransferRequest(BaseModel):
    amount: float = Field(..., gt=0)
    reference: str = Field(..., example="TRX123456789")
    description: Optional[str] = "Bank Transfer for HELB"

class TransactionBase(BaseModel):
    amount: float
    status: PaymentStatus
    provider: PaymentProvider
    reference: Optional[str] = None
    description: Optional[str] = None

class TransactionRead(TransactionBase):
    id: int
    user_id: int
    phone_number: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class MpesaCallback(BaseModel):
    # This is a simplified version of the Mpesa callback structure
    # Daraja sends a complex nested JSON; the service will parse it.
    Body: dict
