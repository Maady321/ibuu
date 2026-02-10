from sqlalchemy.orm import Session
from db.database import SessionLocal
from fastapi import Depends, HTTPException, status, Header
from models.users import User
from models.providers import Provider
from typing import Optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(
    db: Session = Depends(get_db),
    user_id: Optional[str] = Header(None, alias="X-User-ID"),
):
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="User ID missing in headers"
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found"
        )
    return user

def get_current_provider(
    db: Session = Depends(get_db),
    provider_id: Optional[str] = Header(None, alias="X-Provider-ID"),
):
    if not provider_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Provider ID missing in headers",
        )
    
    provider = db.query(Provider).filter(Provider.id == int(provider_id)).first()
    if not provider:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Provider not found"
        )
    return provider
