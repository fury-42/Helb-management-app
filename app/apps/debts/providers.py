from .service import DebtService
from .repository import DebtRepository
from app.apps.semester.repository import SemesterRepository

def get_debt_service():
    return DebtService(DebtRepository(), SemesterRepository())
