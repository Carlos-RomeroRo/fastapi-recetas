from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..models.UserModel import UserModel
from ..schemas.UserSchema import UserCreate, UserResponse, UserUpdate, UserPatch, UserOut
from fastapi import HTTPException
class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserCreate) -> UserResponse:
        new_user = UserModel(
            username=user.username,
            email=user.email,
            role=user.role.value,
            password=user.password 
        ) 
        try:
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            return UserResponse(
                message = "Usuario creado exitosamente",
                code = 201,
                user = UserOut.model_validate(new_user)
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="El usuario ya existe con ese nombre de usuario o correo electrónico"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear el usuario: {str(e)}"
            )
    
    def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
        #1). Search user
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # 2). Update data user
        update_data = user.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_user, key, value)
        
        #3). Commit in the database
        self.db.commit()
        self.db.refresh(db_user)

        #4). return user with new information and message success
        return UserResponse( message="Usuario actualizado correctamente", 
                                        code=200, 
                                        user=UserOut.model_validate(db_user))   
    
    def user_patch(self, user_id: int, user: UserPatch) -> UserResponse:
        db_user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not db_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        patch_data = user.model_dump(exclude_unset=True)

        for key,value in patch_data.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)

        return UserResponse( message="Usuario actualizado correctamente", 
                                        code=200, 
                                        user=UserOut.model_validate(db_user)) 
    



    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado por ID")
        return UserResponse( message="Usuario encontrado correctamente por ID", 
                                        code=200, 
                                        user=UserOut.model_validate(user)) 

    def delete_user (self, user_id:int) -> UserResponse:
        user = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado para eliminar")
        
        self.db.delete(user)
        self.db.commit()
        
        return UserResponse( message="Usuario eliminado correctamente", 
                                        code=200, 
                                        user=None) 
    
    def get_all_users(self) -> list[UserOut]:
        users = self.db.query(UserModel).all()
        return [UserOut.model_validate(user) for user in users]  


        