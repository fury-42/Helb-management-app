from sqlalchemy.orm import Session
from .schemas import UserCreate, UserResponse
from app.core.security import hash_password
from app.shared.exceptions import AppException

class UserService:
    def __init__(self, repo):
        self.repo = repo

    def register_user(self, db: Session, data: UserCreate) -> UserResponse:
        existing = self.repo.get_by_email(db, data.email)
        if existing:
            raise AppException(status_code=400, message="Email already registered")
            
        hashed_pw = hash_password(data.password)
        user = self.repo.create(db, data.email, hashed_pw, data.role, data.phone_number)
        return user

    def get_all_with_semesters(self, db: Session):
        return self.repo.get_all_with_semesters(db)
