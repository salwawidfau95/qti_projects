from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.utils.auth import hash_password, verify_password, create_access_token
from app.crud import user as user_crud

router = APIRouter(tags=["Auth"])  # <- ini optional buat grouping

@router.post("/auth/register", response_model=UserResponse)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    existing_user = user_crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    user_data.password = hash_password(user_data.password)
    new_user = user_crud.create_user(db, user_data)
    return {"message": "Registration successful", "user": new_user}

@router.post("/auth/login")
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = user_crud.get_user_by_username(db, user_data.username)
    if not user or not verify_password(user_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"user_id": user.id})
    return {
        "access_token": token,
        "token_type": "bearer"
    }
