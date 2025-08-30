from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from config import get_db
from app.models.UserModel import UserModel
from app.core.Security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db))-> UserModel:
    user_id = verify_access_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user