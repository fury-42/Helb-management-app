from sqlalchemy.orm import Session, joinedload
from .models import User
from typing import Optional

class UserRepository:
    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, email: str, hashed_password: str, role: str, phone_number: Optional[str] = None) -> User:
        user = User(
            email=email,
            phone_number=phone_number,
            hashed_password=hashed_password,
            role=role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def get_all_with_semesters(self, db: Session):
        """Fetches all users, their semesters, and their loans in a single efficient query."""
        return db.query(User).options(
            joinedload(User.semesters),
            joinedload(User.loans)
        ).all()
