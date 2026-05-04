from .service import BudgetService
from .repository import BudgetRepository
from app.apps.semester.repository import SemesterRepository

def get_budget_service():
    return BudgetService(BudgetRepository(), SemesterRepository())
