from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config import Base

class LikeModel(Base):
    __tablename__ = "likes"

    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"), primary_key=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    
    user = relationship("UserModel", back_populates="likes")
    recipe = relationship("RecipeModel", back_populates="likes")

    def __repr__(self):
        return f"Like(user_id={self.user_id}, recipe_id={self.recipe_id}, created_at={self.created_at})"

