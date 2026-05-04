from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token
from app.shared.exceptions import AppException
from .schemas import Token

class AuthService:
    def __init__(self, repo):
        self.repo = repo

    def authenticate(self, db: Session, form_data: OAuth2PasswordRequestForm) -> Token:
        user = self.repo.get_user_by_email(db, form_data.username)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise AppException(status_code=401, message="Incorrect email or password")
            
        if not user.is_active:
            raise AppException(status_code=400, message="Inactive user")
            
        access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
        return Token(access_token=access_token, token_type="bearer")
