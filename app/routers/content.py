from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas import content as content_schema
from app.crud import content as content_crud
from app.utils.auth import get_current_user
from app.models.user import RoleEnum, User

router = APIRouter(prefix="/content", tags=["Content"])

@router.post("/", response_model=content_schema.ContentResponse)
def create(content: content_schema.ContentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_content = content_crud.create_content(db, content, current_user.id)
    return {"message": "Content created successfully", "content": new_content}

@router.get("/", response_model=List[content_schema.ContentOut])
def read_all(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if current_user.role == RoleEnum.admin:
        return content_crud.get_all_content(db)
    return [c for c in content_crud.get_all_content(db) if c.owner_id == current_user.id]

@router.get("/{content_id}", response_model=content_schema.ContentOut)
def read_by_id(content_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    content = content_crud.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if current_user.role != RoleEnum.admin and content.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this content")
    return content

@router.put("/{content_id}", response_model=content_schema.ContentResponse)
def update(content_id: int, update_data: content_schema.ContentUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    content = content_crud.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if current_user.role != RoleEnum.admin and content.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this content")
    updated = content_crud.update_content(db, content_id, update_data)
    return {"message": "Content updated successfully", "content": updated}

@router.delete("/{content_id}")
def delete(content_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    content = content_crud.get_content_by_id(db, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Content not found")
    if current_user.role != RoleEnum.admin and content.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this content")
    content_crud.delete_content(db, content_id)
    return {"message": "Content deleted successfully"}
