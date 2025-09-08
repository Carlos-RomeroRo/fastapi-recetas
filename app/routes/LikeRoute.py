from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import get_db
from app.schemas.LikeSchema import LikeCreate, LikeResponse, LikeOut
from app.services.LikeService import LikeService
from app.auth.authGet import get_current_user

like_router = APIRouter()

@like_router.post("/create", response_model=LikeResponse)
def createLike(Like: LikeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = LikeService(db)
    return service.create_like(recipe_id=Like.recipe_id,user_id=current_user.id)

@like_router.get("/{recipe_id}", response_model=LikeResponse)
def getLikeById(recipe_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = LikeService(db)
    return service.get_like_by_id(recipe_id=recipe_id, user_id=current_user.id)

@like_router.delete("/{recipe_id}", response_model=LikeResponse)
def deleteLike(recipe_id:int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = LikeService(db)
    return service.delete_like(recipe_id=recipe_id, user_id=current_user.id)

@like_router.get("/", response_model=list[LikeOut])
def getAllLikes(db: Session = Depends(get_db)):
    service = LikeService(db)
    return service.get_all_likes()
