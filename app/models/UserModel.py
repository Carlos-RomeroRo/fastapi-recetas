from sqlalchemy import Column, Integer, String
from sqlalchemy.types import Enum as SQLEnum
from config import Base
from enum import Enum 

class UserRole(str,Enum):
    LIDER = "lider"
    ADMINISTRADOR = "administrador"
    USUARIO = "usuario"


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(SQLEnum(UserRole), default=UserRole.USUARIO)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username}, email={self.email}, role={self.role})"



