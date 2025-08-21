from sqlalchemy.orm import Session
from ..models.UserModel import UserModel
from ..schemas.UserSchema import UserCreate, UserResponse, UserUpdate, UserPatch

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserCreate) -> UserResponse:
        new_user = UserModel(
            username=user.username,
            email=user.email,
            role=user.role,
            password=user.password 
        ) 
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return {
            "message": "Usuario creado exitosamente",
            "user": UserResponse.model_validate(new_user)
        }
    
    def update_user(self, user_id: int, user: UserUpdate) -> dict | None:
        #1). Search user
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        
        # 2). Update data user
        db_user.username = user.username
        db_user.email = user.email
        db_user.role = user.role
        
        #3). Commit in the database
        self.db.commit()
        self.db.refresh(db_user)

        #4). return user with new information and message success
        return {
            "message": "Usuario actualizado exitosamente",
            "user": UserResponse.model_validate(db_user)
        }
    
    def UserPatch(self, user_id: int, user: UserPatch) -> dict | None:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            return None
        
        patch_data = user.model_dump(exclude_unset=True)

        for key,value in patch_data.items():
            setattr(db_user, key, value)

         
        
        self.db.commit()
        self.db.refresh(db_user)

        return {
            "message": "Usuario actualizado parcialmente exitosamente",
            "user": UserResponse.model_validate(db_user)
        }


    def get_user(self, user_id: int) -> UserResponse | None:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if user:
            return UserResponse.model_validate(user)
        return None
