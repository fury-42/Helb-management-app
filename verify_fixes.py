from app.core.database import SessionLocal, Base, engine
from app.apps.users.repository import UserRepository
from app.apps.users.models import User
from app.apps.semester.models import Semester
import uuid

def test_user_creation_with_phone():
    db = SessionLocal()
    repo = UserRepository()
    
    email = f"test_{uuid.uuid4().hex[:6]}@example.com"
    phone = "+254700000000"
    
    print(f"Creating user with email: {email} and phone: {phone}")
    
    try:
        user = repo.create(db, email, "hashed_password", "student", phone)
        print(f"User created: ID={user.id}, Email={user.email}, Phone={user.phone_number}")
        
        # Verify from DB
        db_user = db.query(User).filter(User.id == user.id).first()
        if db_user.phone_number == phone:
            print("SUCCESS: Phone number correctly persisted in DB.")
        else:
            print(f"FAILURE: Phone number in DB is {db_user.phone_number}")
            
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_user_creation_with_phone()
