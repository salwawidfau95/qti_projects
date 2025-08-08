from pydantic import BaseModel, ConfigDict
from typing import Optional

class ContentBase(BaseModel):
    title: str
    body: str

class ContentCreate(ContentBase):
    pass

class ContentUpdate(BaseModel):
    title: Optional[str]
    body: Optional[str]

class ContentOut(ContentBase):
    id: int
    owner_id: int

    model_config = ConfigDict(from_attributes=True)

class ContentResponse(BaseModel):
    message: str
    content: ContentOut
