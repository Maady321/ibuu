import sys
import os

# Add Backend to path
backend_root = os.path.dirname(os.path.abspath(__file__))
if backend_root not in sys.path:
    sys.path.insert(0, backend_root)

from sqlalchemy.orm import Session
from db.database import SessionLocal, engine, Base
from models.users import User
from schemas.user_schema import UserRegister
from pwd_utils import hash_password

import logging
logging.basicConfig(level=logging.INFO)

def test_registration_logic():
    print("Starting manual registration test...")
    db = SessionLocal()
    try:
        # Check if tables exist
        print("Checking tables...")
        from sqlalchemy import inspect
        inspector = inspect(engine)
        print(f"Tables in DB: {inspector.get_table_names()}")

        user_data = UserRegister(
            name="Test User",
            email="test@example.com",
            password="testpassword",
            phone="9876543210",
            address="Test Address"
        )
        
        print(f"Hashing password...")
        hashed = hash_password(user_data.password)
        print(f"Hashed: {hashed}")

        print(f"Creating User object...")
        new_user = User(
            name=user_data.name,
            email=user_data.email,
            password=hashed,
            phone=user_data.phone,
            address=user_data.address,
            role="user"
        )
        
        print("Saving to DB...")
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"SUCCESS: Created user with ID {new_user.id}")
        
        # Cleanup
        db.delete(new_user)
        db.commit()
        print("Cleanup successful.")

    except Exception as e:
        print(f"FAILURE: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_registration_logic()
