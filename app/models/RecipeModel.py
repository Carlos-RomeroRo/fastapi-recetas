from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config import Base

class RecipeModel(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, index=True)
    ingredients = Column(Text)
    instructions = Column(Text)
    preparation_time = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey("users.id"))
    photo = Column(Text, nullable=True)

    user = relationship("UserModel", back_populates="recipes")
    likes = relationship("LikeModel", back_populates="recipe", cascade="all, delete")

    def __repr__(self):
        return f"Recipe(id={self.id}, title={self.title}, description={self.ingredients}, created_at={self.created_at}, user_id={self.user_id})"