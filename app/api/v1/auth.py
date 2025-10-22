from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from ...core.database import get_db
from ...core.security import verify_password, get_password_hash, create_access_token
from ...core.config import settings
from ...models.user import User
from ...schemas.user import UserCreate, UserResponse
from ...schemas.auth import Token, LoginRequest

router = APIRouter()

@router.post("/register",response_model=UserResponse)
def register(user: UserCreate, db:Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==user.email).first()
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    hashed_password=get_password_hash(user.password)
    new_user=User(
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=user.phone
    )
    db.add(new_user) 
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("login",response_model=Token)
def login(login_data: LoginRequest, db: Session=Depends(get_db)):
    db_user=db.query(User).filter(User.email==login_data.email).first()
    if not db_user or not verify_password(login_data.password,db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token_expxires=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token=create_access_token(data={"sub":str(db_user.id)}, expires_delta=access_token_expxires)

    return {"access_token":access_token, "token_type":"bearer"}