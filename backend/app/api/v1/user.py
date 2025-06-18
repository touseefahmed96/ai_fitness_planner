from app.core.security import (
    get_current_user,
    get_password_hash,
    login_user,
)
from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

router = APIRouter()


@router.get("/me")
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "goal": current_user.goal,
    }


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=get_password_hash(user.password),
        weight=user.weight,
        height=user.height,
        goal=user.goal,
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}


@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    token, user = login_user(form_data, db)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "goal": user.goal,
        "access_token": token,
        "token_type": "bearer",
    }
