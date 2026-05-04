from .service import ExpenseService
from .repository import ExpenseRepository
from app.apps.semester.repository import SemesterRepository
from app.apps.budget.repository import BudgetRepository

def get_expense_service():
    return ExpenseService(ExpenseRepository(), SemesterRepository(), BudgetRepository())
