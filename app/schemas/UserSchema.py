from pydantic import BaseModel, EmailStr, field_validator
from enum import Enum
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
    email: EmailStr
    password: str

class LoginRequest(BaseModel):
    email: EmailStr
    password:str


    class Config:
        from_attributes = True

class UserPatch(UserBase):
    username: str | None = None
    email: EmailStr | None = None
    role: UserRole | None = None

class UserOut(UserBase):
    id: int
    password: str

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    message: str
    code: int
    user: UserOut | None

    class Config:
        from_attributes = True