from .repository import AuthRepository
from .service import AuthService

def get_auth_service():
    repo = AuthRepository()
    return AuthService(repo)
