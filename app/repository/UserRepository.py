
from app.models.UserModel import UserModel
from app.repository.BaseRepository import BaseRepository
from sqlalchemy.orm import Session

class UserRepository (BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, UserModel)

        