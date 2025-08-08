from sqlalchemy.orm import Session
from app.models.content import Content
from app.schemas.content import ContentCreate, ContentUpdate

def create_content(db: Session, content_data: ContentCreate, user_id: int):
    new_content = Content(**content_data.dict(), owner_id=user_id)
    db.add(new_content)
    db.commit()
    db.refresh(new_content)
    return new_content

def get_all_content(db: Session):
    return db.query(Content).all()

def get_content_by_id(db: Session, content_id: int):
    return db.query(Content).filter(Content.id == content_id).first()

def update_content(db: Session, content_id: int, content_data: ContentUpdate):
    content = get_content_by_id(db, content_id)
    if not content:
        return None
    if content_data.title:
        content.title = content_data.title
    if content_data.body:
        content.body = content_data.body
    db.commit()
    db.refresh(content)
    return content

def delete_content(db: Session, content_id: int):
    content = get_content_by_id(db, content_id)
    if not content:
        return None
    db.delete(content)
    db.commit()
    return True
