from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import get_db
from app.schemas.UserSchema import UserCreate, UserResponse, UserPatch, UserOut
from app.services.UserService import UserService

user_router = APIRouter()

#Create Users

@user_router.post("/create", response_model=UserResponse)
def createUser(User: UserCreate, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.create_user(User)
   
@user_router.get("/{user_id}", response_model=UserResponse)
def getUserById(user_id:int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_user_by_id(user_id)

@user_router.patch("/{user_id}", response_model=UserResponse)
def patchUser(user_id: int, user: UserPatch, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.user_patch(user_id, user)

@user_router.delete("/{user_id}", response_model=UserResponse)
def deleteUser(user_id: int, db: Session = Depends(get_db)):
    service = UserService(db)
    return service.delete_user(user_id)

@user_router.get("/", response_model=list[UserOut])
def getAllUsers(db: Session = Depends(get_db)):
    service = UserService(db)
    return service.get_all_users()