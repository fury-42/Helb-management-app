from sqlalchemy.orm import Session
from typing import List, Optional
from .models import Transaction, PaymentStatus
from .schemas import TransactionBase 

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, transaction_data: dict) -> Transaction:
        db_transaction = Transaction(**transaction_data)
        self.db.add(db_transaction)
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def get_transaction_by_checkout_id(self, checkout_request_id: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.checkout_request_id == checkout_request_id).first()

    def get_transaction_by_reference(self, reference: str) -> Optional[Transaction]:
        return self.db.query(Transaction).filter(Transaction.reference == reference).first()

    def update_transaction_status(self, transaction: Transaction, status: PaymentStatus, reference: Optional[str] = None) -> Transaction:
        transaction.status = status
        if reference:
            transaction.reference = reference
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_user_transactions(self, user_id: int) -> List[Transaction]:
        return self.db.query(Transaction).filter(Transaction.user_id == user_id).order_by(Transaction.created_at.desc()).all()
