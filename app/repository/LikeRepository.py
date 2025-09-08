from app.models.LikeModel import LikeModel
from app.repository.BaseRepository import BaseRepository
from sqlalchemy.orm import Session

class LikeRepository (BaseRepository):
    def __init__(self, db: Session):
        self.db = db
        super().__init__(db, LikeModel)
        
    def get_by_user_and_recipe(self, user_id: int, recipe_id: int) -> LikeModel | None:
        return self.db.query(LikeModel).filter_by(user_id=user_id, recipe_id=recipe_id).first()

    def delete_by_like_model(self,like:LikeModel):
        try:
            self.db.delete(like)
            self.db.commit()
        except:
            self.db.rollback()
            raise