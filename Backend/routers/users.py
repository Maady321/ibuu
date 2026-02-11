from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from models.users import User
from models.providers import Provider
from schemas.user_schema import UserRegister, UserLogin, UserProfileUpdate, UserOut
from pwd_utils import hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user(user: UserRegister, db: Session = Depends(get_db)):
    print(f"DEBUG: Registering user: {user.email}", flush=True)
    try:
        normalized_email = user.email.lower().strip()
        if db.query(User).filter(User.email == normalized_email).first():
            print(f"DEBUG: Email already exists: {normalized_email}", flush=True)
            raise HTTPException(status_code=400, detail="Email already registered")

        if db.query(User).filter(User.phone == user.phone).first():
            print(f"DEBUG: Phone already exists: {user.phone}", flush=True)
            raise HTTPException(status_code=400, detail="Phone number already registered")

        new_user = User(
            name=user.name,
            email=normalized_email,
            password=hash_password(user.password),
            phone=user.phone,
            address=user.address,
            role="user",
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        print(f"DEBUG: User created successfully: {new_user.id}", flush=True)

        return {
            "message": "User registered successfully", 
            "user_id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL ERROR IN REGISTER: {str(e)}", flush=True)
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    print(f"Login attempt for: {user.email}", flush=True)

    try:
        normalized_email = user.email.lower().strip()
        db_user = db.query(User).filter(User.email == normalized_email).first()

        if not db_user:
            print(f"FAILED: User not found: {normalized_email}", flush=True)
            raise HTTPException(
                status_code=401, detail=f"Account with email '{normalized_email}' not found"
            )

        if not verify_password(user.password, db_user.password):
            print(f"FAILED: Password mismatch for {normalized_email}", flush=True)
            raise HTTPException(
                status_code=401, detail="Incorrect password. Please check and try again."
            )

        print(f"SUCCESS: Login successful for {normalized_email}", flush=True)
        return {
            "message": "Login successful",
            "user_id": db_user.id,
            "user_name": db_user.name,
            "email": db_user.email,
            "role": "user"
        }
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"CRITICAL ERROR IN LOGIN: {e}", flush=True)
        raise HTTPException(status_code=500, detail="Internal Server Error during login processing")


@router.post("/unified_login")
def unified_login(user: UserLogin, db: Session = Depends(get_db)):
    print(f"Unified Login attempt for: {user.email}", flush=True)
    
    # 1. Check for Admin (Hardcoded)
    if user.email == "admin@homebuddy.com" and user.password == "admin123":
        return {
            "message": "Login successful",
            "role": "admin",
            "redirect": "Frontend/html/admin/admin-dashboard.html"
        }

    # 2. Check for User
    db_user = db.query(User).filter(User.email == user.email.lower().strip()).first()
    if db_user and verify_password(user.password, db_user.password):
        return {
            "message": "Login successful",
            "role": "user",
            "user_id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "redirect": "Frontend/html/user/dashboard.html"
        }

    # 3. Check for Provider
    db_provider = db.query(Provider).filter(Provider.email == user.email).first()
    if db_provider and verify_password(user.password, db_provider.password):
        return {
            "message": "Login successful",
            "role": "provider",
            "provider_id": db_provider.id,
            "user_id": db_provider.user_id,
            "name": db_provider.full_name,
            "email": db_provider.email,
            "redirect": "Frontend/html/provider/provider-dashboard.html"
        }

    raise HTTPException(status_code=401, detail="Invalid email or password")


@router.post("/provider/login")
def login_provider(user: UserLogin, db: Session = Depends(get_db)):
    # Legacy endpoint kept for compatibility, but unified_login is preferred
    print(f"DEBUG: Provider Login attempt for email: '{user.email}'", flush=True)

    try:
        db_provider = db.query(Provider).filter(Provider.email == user.email).first()

        if not db_provider:
            print(f"DEBUG: No provider found with email: '{user.email}'", flush=True)
            raise HTTPException(status_code=401, detail="Invalid email or password")

        if not verify_password(user.password, db_provider.password):
            print(f"DEBUG: Password mismatch for provider: '{user.email}'", flush=True)
            raise HTTPException(status_code=401, detail="Invalid email or password")

        print(
            f"DEBUG: Login successful for provider: '{user.email}', ID: {db_provider.id}",
            flush=True,
        )
        return {
            "message": "Login successful",
            "provider_id": db_provider.id,
            "user_id": db_provider.user_id,
            "full_name": db_provider.full_name,
        }
    except Exception as e:
        print(f"DEBUG: Exception during login: {str(e)}", flush=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    return db.query(User).all()


@router.get("/profile", response_model=UserOut)
def get_profile(current_user: User = Depends(get_current_user)):
    return current_user


@router.put("/profile", response_model=UserOut)
def update_profile(
    user_update: UserProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    current_user.name = user_update.name
    current_user.email = user_update.email.lower().strip()
    current_user.phone = user_update.phone
    current_user.address = user_update.address

    db.commit()
    db.refresh(current_user)
    return current_user
