from .service import LoanService
from .repository import LoanRepository

def get_loan_service():
    return LoanService(LoanRepository())
