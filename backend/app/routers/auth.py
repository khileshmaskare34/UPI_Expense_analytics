from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.models.user import User
from app.db.session import SessionLocal

from app.schemas.user import UserCreate, UserResponse
from app.crud.user import create_user, get_user_by_email

from app.core.deps import get_current_user
from app.schemas.user import UserResponse

from app.schemas.auth import LoginRequest, TokenResponse
from app.core.security import verify_password
from app.core.jwt import create_access_token


router = APIRouter(prefix="/auth", tags=["Auth"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    print("email and password_:", user)
    existing = get_user_by_email(db, user.email)

    if existing:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = create_user(db, user)
    return new_user

@router.get("/users", response_model=List[UserResponse])
def get_alluser(db:Session = Depends(get_db)):
    users = db.query(User).all()
    return users



@router.post("/login", response_model=TokenResponse)
def login_user(data: LoginRequest, db: Session = Depends(get_db)):
    user = get_user_by_email(db, data.email)

    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    if not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    token = create_access_token({"sub": str(user.id)})

    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user