from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from config import get_db
from app.models.UserModel import UserModel
from app.core.Security import create_access_token
from app.schemas.UserSchema import LoginRequest

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
login_router = APIRouter()

@login_router.post("/login")
def login(request: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == request.email).first()
    if not user or not pwd_context.verify(request.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub":str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}