import enum
from sqlalchemy import Column, Integer, String, Enum
from ...config import Base

class UserRole(enum.Enum):
    LIDER = "lider"
    ADMINISTRADOR = "administrador"
    USUARIO = "usuario"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(Enum(UserRole), default=UserRole.USUARIO)

def __repr__(self):
    return f"User(id={self.id}, username={self.username}, email={self.email}, role={self.value})"

