from pydantic import BaseModel
from typing import Optional

class RecipeBase(BaseModel):
    title: str
    ingredients: str
    instructions: str
    preparation_time: int
    photo: str | None = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(RecipeBase):
    pass

    class Config:
        from_attributes = True

class RecipePatch(RecipeBase):
    title: Optional[str] = None
    ingredients: Optional[str] = None
    instructions: Optional[str] = None
    preparation_time: Optional[str] = None
    photo: Optional[str] = None

class RecipeOut(RecipeBase):
    id: int
    user_id: int
    likes_count: str

    class Config:
        from_attributes = True

class RecipeResponse(BaseModel):
    message: str
    code: int
    recipe: Optional[RecipeOut] = None

    class Config:
        from_attributes = True