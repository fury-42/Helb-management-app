from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from .repository import PaymentRepository
from .service import PaymentService

def get_payment_repository(db: Session = Depends(get_db)) -> PaymentRepository:
    return PaymentRepository(db)

def get_payment_service(repository: PaymentRepository = Depends(get_payment_repository)) -> PaymentService:
    return PaymentService(repository)
