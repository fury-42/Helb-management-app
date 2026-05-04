from sqlalchemy.orm import Session
from app.apps.users.models import User

class AuthRepository:
    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()
