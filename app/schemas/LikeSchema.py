from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LikeBase(BaseModel):
    pass

class LikeCreate(LikeBase):
    pass

class LikePatch(LikeBase):
    pass

class LikeOut(LikeBase):
    id: int
    user_id: int
    recipe_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class LikeResponse(BaseModel):
    message: str
    code: int
    like: Optional[LikeOut] | None
    

