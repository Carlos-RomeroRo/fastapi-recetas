from app.models.RecipeModel import RecipeModel
from app.repository.BaseRepository import BaseRepository
from sqlalchemy.orm import Session

class RecipeRepository (BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, RecipeModel)