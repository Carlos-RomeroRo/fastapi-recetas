from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import get_db
from app.schemas.LikeSchema import LikeCreate, LikeResponse, LikeOut
from app.services.LikeService import LikeService

like_router = APIRouter()

@like_router.post("/create", response_model=LikeResponse)
def createLike(Like: LikeCreate, db: Session = Depends(get_db)):
    service = LikeService(db)
    return service.create_like(Like)

@like_router.get("/{like_id}", response_model=LikeResponse)
def getLikeById(like_id:int, db: Session = Depends(get_db)):
    service = LikeService(db)
    return service.get_like_by_id(like_id)

@like_router.delete("/{like_id}", response_model=LikeResponse)
def deleteLike(like_id: int, db: Session = Depends(get_db)):
    service = LikeService(db)
    return service.delete_like(like_id)

@like_router.get("/", response_model=list[LikeOut])
def getAllLikes(db: Session = Depends(get_db)):
    service = LikeService(db)
    return service.get_all_likes()

@like_router.patch("/{like_id}", response_model=LikeResponse)
def patchLike(like_id: int, db: Session = Depends(get_db)):
    service = LikeService(db)
    return service.like_patch(like_id)