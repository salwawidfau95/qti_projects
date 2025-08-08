from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    user = "user"
    admin = "admin"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: RoleEnum

    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(BaseModel):
    message: str
    user: UserOut

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserCreateAdmin(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: RoleEnum

class UserUpdateAdmin(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[RoleEnum] = None  