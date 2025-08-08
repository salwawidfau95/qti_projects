from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.utils.auth import get_current_user, hash_password
from app.schemas.user import UserOut, UserUpdate, UserResponse, UserCreateAdmin, UserUpdateAdmin
from app.crud import user as user_crud
from app.utils.auth import is_admin, is_self_or_admin
from typing import List
from app.models.user import User

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

@router.get("/profile", response_model=UserOut)
def get_profile(current_user: UserOut = Depends(get_current_user)):
    return current_user

@router.patch("/profile", response_model=UserResponse)
def update_profile(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: UserOut = Depends(get_current_user)
):
    if user_update.password:
        user_update.password = hash_password(user_update.password)
    updated_user = user_crud.update_profile(db, current_user.id, user_update)
    return {"message": "Profile updated", "user": updated_user}

@router.delete("/profile")
def delete_own_profile(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    success = user_crud.delete_user(db, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")
    return {"message": "Akun Anda berhasil dihapus."}

@router.get("/", response_model=List[UserOut])
def get_all_users(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa melihat semua user.")
    return user_crud.get_all_users(db)

@router.post("/", response_model=UserResponse)
def create_user(
    user_data: UserCreateAdmin, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Only admin can create users")
    existing_user = user_crud.get_user_by_username(db, user_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already taken")
        
    user_data.password = hash_password(user_data.password)
    created_user = user_crud.create_user_by_admin(db, user_data)
    return {
        "message": "User created by admin successfully",
        "user": created_user
    }

@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not is_self_or_admin(current_user, user_id):
        raise HTTPException(status_code=403, detail="Tidak punya akses ke data user ini.")
    user = user_crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")
    return user

@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdateAdmin, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa mengubah user.")
    user = user_crud.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if not is_admin(current_user):
        raise HTTPException(status_code=403, detail="Hanya admin yang bisa menghapus user.")
    success = user_crud.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User tidak ditemukan.")
    return {"message": "User berhasil dihapus."}