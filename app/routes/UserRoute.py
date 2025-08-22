from fastapi import APIRouter, Depends, HTTPException, JSONResponse
from sqlalchemy.orm import Session
from ...config import get_db
from ..schemas.UserSchema import UserCreate, UserResponse, UserUpdate, UserPatch
from ..services.UserService import UserService

router = APIRouter(prefix="/users", tags=["users"])

#Create Users

@router.post("/create", response_model=UserResponse)
def createUser(User: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(User)
   
@router.get("/{user_id}", response_model=UserResponse)
def getUser(user_id:int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)

@router.put("/{user_id}",response_model=UserResponse)
def updateUser(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.update_user(user_id, user)
    

    