from fastapi import APIRouter, Depends, Body, Request
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from .schemas import STKPushRequest, BankTransferRequest, TransactionRead, MpesaCallback
from .providers import get_payment_service

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/mpesa/stk-push", response_model=TransactionRead)
async def initiate_stk_push(
    request: STKPushRequest,
    current_user = Depends(get_current_user),
    service = Depends(get_payment_service)
):
    """Initiate Mpesa STK Push for a user."""
    return await service.initiate_mpesa_stk_push(current_user.id, request)

@router.post("/mpesa/callback")
async def mpesa_callback(
    data: dict = Body(...),
    service = Depends(get_payment_service)
):
    """Callback endpoint for Mpesa Daraja API."""
    await service.process_mpesa_callback(data)
    return {"ResultCode": 0, "ResultDesc": "Success"}

@router.post("/bank/record", response_model=TransactionRead)
def record_bank_payment(
    request: BankTransferRequest,
    current_user = Depends(get_current_user),
    service = Depends(get_payment_service)
):
    """Record a manual bank transfer integration."""
    return service.record_bank_transfer(current_user.id, request)

@router.get("/history", response_model=List[TransactionRead])
def get_payment_history(
    current_user = Depends(get_current_user),
    service = Depends(get_payment_service)
):
    """Get the transaction history for the current user."""
    return service.get_history(current_user.id)
