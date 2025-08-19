from pydantic import BaseModel, EmailStr
from typing import Optional
import enum

class UserRole(enum.Enum):
    LIDER = "lider"
    ADMINISTRADOR = "administrador"
    USUARIO = "usuario"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.USUARIO

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    id:int

    class Config:
        from_attributes = True