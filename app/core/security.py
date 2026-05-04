from datetime import datetime, timedelta
from typing import Optional
import jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.settings import settings
from app.core.database import get_db
from app.shared.exceptions import AppException

# We will import User dynamically or use a service to avoid circular imports.
# For simplicity in this architectural pattern, we will fetch the user directly.

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")
ph = PasswordHasher()

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        return ph.verify(hashed_password, plain_password)
    except VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.apps.users.models import User # Import here to avoid circular dependencies
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise AppException(status_code=401, message="Could not validate credentials")
    except jwt.PyJWTError:
        raise AppException(status_code=401, message="Could not validate credentials")
        
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise AppException(status_code=401, message="User not found")
    if not user.is_active:
        raise AppException(status_code=400, message="Inactive user")
    return user

def get_current_student(current_user = Depends(get_current_user)):
    if current_user.role != "student":
        raise AppException(status_code=403, message="Not enough permissions. Student role required.")
    return current_user

def get_current_admin(current_user = Depends(get_current_user)):
    if current_user.role != "admin":
        raise AppException(status_code=403, message="Not enough permissions. Admin role required.")
    return current_user
