from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum

class UserRole(str,Enum):
    LIDER = "lider"
    ADMINISTRADOR = "administrador"
    USUARIO = "usuario"

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole = UserRole.USUARIO

    @field_validator('role', mode="before")
    def normalize_role(cls, value):
        if isinstance(value, str):
            return value.lower()
        return value

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass

    class Config:
        from_attributes = True

class UserPatch(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None

class UserOut(UserBase):
    id: int

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    message: str
    code: int
    user: UserOut | None

    class Config:
        from_attributes = True