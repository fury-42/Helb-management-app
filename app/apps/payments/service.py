import base64
from datetime import datetime
import httpx
import logging
from typing import Optional
from app.core.settings import settings
from .models import PaymentStatus, PaymentProvider
from .repository import PaymentRepository
from .schemas import STKPushRequest, BankTransferRequest

logger = logging.getLogger(__name__)

class PaymentService:
    def __init__(self, repository: PaymentRepository):
        self.repository = repository

    async def _get_mpesa_access_token(self) -> str:
        url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        auth = base64.b64encode(f"{settings.MPESA_CONSUMER_KEY}:{settings.MPESA_CONSUMER_SECRET}".encode()).decode()
        
        headers = {"Authorization": f"Basic {auth}"}
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            return response.json()["access_token"]

    async def initiate_mpesa_stk_push(self, user_id: int, request: STKPushRequest):
        access_token = await self._get_mpesa_access_token()
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{settings.MPESA_SHORTCODE}{settings.MPESA_PASSKEY}{timestamp}".encode()).decode()
        
        headers = {"Authorization": f"Bearer {access_token}"}
        
        payload = {
            "BusinessShortCode": settings.MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": int(request.amount),
            "PartyA": request.phone_number,
            "PartyB": settings.MPESA_SHORTCODE,
            "PhoneNumber": request.phone_number,
            "CallBackURL": settings.MPESA_CALLBACK_URL,
            "AccountReference": f"HELB-{user_id}",
            "TransactionDesc": request.description or "HELB Payment"
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
            res_data = response.json()
            
            if response.status_code == 200 and res_data.get("ResponseCode") == "0":
                # Create transaction record
                transaction_data = {
                    "user_id": user_id,
                    "amount": request.amount,
                    "phone_number": request.phone_number,
                    "status": PaymentStatus.PENDING,
                    "provider": PaymentProvider.MPESA,
                    "checkout_request_id": res_data.get("CheckoutRequestID"),
                    "description": request.description
                }
                return self.repository.create_transaction(transaction_data)
            else:
                logger.error(f"Mpesa STK Push failed: {res_data}")
                raise Exception(f"Mpesa initiation failed: {res_data.get('ErrorMessage', 'Unknown error')}")

    async def process_mpesa_callback(self, callback_data: dict):
        result_code = callback_data["Body"]["stkCallback"]["ResultCode"]
        checkout_request_id = callback_data["Body"]["stkCallback"]["CheckoutRequestID"]
        
        transaction = self.repository.get_transaction_by_checkout_id(checkout_request_id)
        if not transaction:
            logger.warning(f"Transaction not found for checkout_id: {checkout_request_id}")
            return
            
        if result_code == 0:
            # Success
            items = callback_data["Body"]["stkCallback"]["CallbackMetadata"]["Item"]
            receipt = next((item["Value"] for item in items if item["Name"] == "MpesaReceiptNumber"), None)
            self.repository.update_transaction_status(transaction, PaymentStatus.COMPLETED, reference=receipt)
        else:
            # Failed
            self.repository.update_transaction_status(transaction, PaymentStatus.FAILED)

    def record_bank_transfer(self, user_id: int, request: BankTransferRequest):
        transaction_data = {
            "user_id": user_id,
            "amount": request.amount,
            "status": PaymentStatus.COMPLETED, # Assuming bank transfer is recorded after confirmation
            "provider": PaymentProvider.BANK,
            "reference": request.reference,
            "description": request.description
        }
        return self.repository.create_transaction(transaction_data)

    def get_history(self, user_id: int):
        return self.repository.get_user_transactions(user_id)
