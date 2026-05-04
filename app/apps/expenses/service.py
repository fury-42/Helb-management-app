from sqlalchemy.orm import Session
from .schemas import ExpenseLog, ExpenseResponse, ExpenseSummaryResponse, CategorySummary, ExpenseAlertResponse
from app.apps.semester.repository import SemesterRepository
from app.apps.budget.repository import BudgetRepository
from app.shared.exceptions import AppException

class ExpenseService:
    def __init__(self, repo, semester_repo, budget_repo):
        self.repo = repo
        self.semester_repo = semester_repo
        self.budget_repo = budget_repo

    def _get_active_semester(self, db: Session, user_id: int):
        semester = self.semester_repo.get_latest(db, user_id)
        if not semester:
            raise AppException(status_code=404, message="No active semester found.")
        return semester

    def log_expense(self, db: Session, user_id: int, data: ExpenseLog) -> ExpenseResponse:
        semester = self._get_active_semester(db, user_id)
        
        # 1. Log the expense
        expense = self.repo.log_expense(
            db, semester.id, data.category, data.description, data.amount, data.expense_type
        )
        
        # 2. Update Semester remaining balance
        if semester.remaining_balance < data.amount:
            raise AppException(status_code=400, message="Insufficient funds in the semester balance.")
        self.semester_repo.update_balance(db, semester, semester.remaining_balance - data.amount)
        
        # 3. Update Budget Allocation spent amount if it exists
        allocation = self.budget_repo.get_allocation_by_category(db, semester.id, data.category)
        if allocation:
            allocation.spent_amount += data.amount
            db.commit()

        return expense

    def generate_summary(self, db: Session, user_id: int) -> ExpenseSummaryResponse:
        semester = self._get_active_semester(db, user_id)
        
        allocations = self.budget_repo.get_all_allocations(db, semester.id)
        
        summaries = []
        total_spent = 0.0
        
        for allocation in allocations:
            percentage = (allocation.spent_amount / allocation.allocated_amount) * 100 if allocation.allocated_amount > 0 else 0
            summaries.append(CategorySummary(
                category=allocation.category,
                total_spent=allocation.spent_amount,
                allocated_amount=allocation.allocated_amount,
                percentage_used=round(percentage, 2)
            ))
            total_spent += allocation.spent_amount
            
        return ExpenseSummaryResponse(
            total_spent_this_semester=total_spent,
            category_summaries=summaries
        )

    def check_alerts(self, db: Session, user_id: int) -> ExpenseAlertResponse:
        semester = self._get_active_semester(db, user_id)
        allocations = self.budget_repo.get_all_allocations(db, semester.id)
        
        alerts = []
        for allocation in allocations:
            if allocation.allocated_amount > 0:
                percentage = (allocation.spent_amount / allocation.allocated_amount) * 100
                if percentage >= 100:
                    alerts.append(f"CRITICAL: Category '{allocation.category}' is exhausted (100% spent).")
                elif percentage >= 80:
                    alerts.append(f"WARNING: Category '{allocation.category}' is nearly exhausted ({round(percentage, 1)}% spent).")
                    
        if semester.total_funds > 0:
            total_percentage = ((semester.total_funds - semester.remaining_balance) / semester.total_funds) * 100
            if total_percentage >= 90:
                alerts.append("CRITICAL: Total HELB funds are 90% depleted.")
                
        return ExpenseAlertResponse(alerts=alerts)
