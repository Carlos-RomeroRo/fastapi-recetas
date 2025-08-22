from pydantic import BaseModel, EmailStr
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
    user: UserOut

    class Config:
        from_attributes = True