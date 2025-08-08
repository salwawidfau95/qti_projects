from sqlalchemy import Column, Integer, String, Enum
from app.db.database import Base
import enum
from sqlalchemy.orm import relationship

# Definisi Enum Role
class RoleEnum(str, enum.Enum):
    user = "user"
    admin = "admin"

# Model SQLAlchemy untuk tabel users
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.user)

    contents = relationship("Content", back_populates="owner", cascade="all, delete")
