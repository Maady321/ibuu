from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from dependencies import get_db, get_current_user
from models.providers import Provider
from models.users import User

from schemas.provider_schema import ProviderCreate, ProviderUpdate, ProviderResponse

from pwd_utils import hash_password

router = APIRouter(prefix="/api/providers", tags=["Providers"])

@router.post("/create", response_model=ProviderResponse)
def create_provider(provider: ProviderCreate, db: Session = Depends(get_db)):
    """
    Register a new service provider. Creates both a User record and a Provider profile.
    """
    logger.info(f"New provider registration attempt: {provider.email}")
    normalized_email = provider.email.lower().strip()

    try:
        # 1. Integrity Check: Check for existing User/Provider
        existing_user = db.query(User).filter(User.email == normalized_email).first()
        if existing_user:
            # Check if this user is already a provider
            existing_provider = db.query(Provider).filter(Provider.user_id == existing_user.id).first()
            if existing_provider:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="An account with this email already exists as a provider."
                )
            # If they exist but as a different role, we update their role (multi-role support foundation)
            existing_user.role = "provider"
            db_user = existing_user
        else:
            # Create new base User
            db_user = User(
                name=provider.full_name.strip(),
                email=normalized_email,
                password=hash_password(provider.password),
                phone=provider.phone.strip(),
                address=provider.address.strip(),
                role="provider",
                is_active=True
            )
            db.add(db_user)
            db.flush() # Get user ID before proceeding

        # 2. Extract provider-specific data (everything except password/email which go to User)
        p_data = provider.model_dump(exclude={"password"})
        p_data["email"] = normalized_email

        # 3. Create the Provider Profile linked to the User
        new_provider = Provider(
            user_id=db_user.id,
            **p_data
        )

        db.add(new_provider)
        db.commit()
        db.refresh(new_provider)
        
        logger.info(f"Provider registration success: ID {new_provider.id}")
        return new_provider

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"FATAL ERROR in provider registration: {str(e)}")
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create provider account. Please verify all fields are correct."
        )



@router.get("/all", response_model=list[ProviderResponse])
def get_providers(db: Session = Depends(get_db)):
    return db.query(Provider).all()


@router.get("/{provider_id}", response_model=ProviderResponse)
def get_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider


@router.put("/update/{provider_id}", response_model=ProviderResponse)
def update_provider(
    provider_id: int, update: ProviderUpdate, db: Session = Depends(get_db)
):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    for key, value in update.model_dump(exclude_unset=True).items():
        setattr(provider, key, value)

    db.commit()
    db.refresh(provider)
    return provider


@router.delete("/delete/{provider_id}")
def delete_provider(provider_id: int, db: Session = Depends(get_db)):
    provider = db.query(Provider).filter(Provider.id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")

    db.delete(provider)
    db.commit()
    return {"message": "Provider deleted successfully"}
