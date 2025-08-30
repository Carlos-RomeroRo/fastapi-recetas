from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserCreate, UserResponse, UserPatch, UserOut
from fastapi import HTTPException
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_user(self, user: UserCreate) -> UserResponse:
        hashed_password = pwd_context.hash(user.password)
        new_user = UserModel(
            username=user.username,
            email=user.email,
            role=user.role.value,
            password=hashed_password
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
    
    def user_patch(self, user_id: int, user: UserPatch) -> UserResponse:
        user_model = self.get_user_or_404(user_id)
        
        patch_data = user.model_dump(exclude_unset=True)

        for key,value in patch_data.items():
            setattr(user_model, key, value)

        self.db.commit()
        self.db.refresh(user_model)

        return UserResponse( message="Usuario actualizado correctamente", 
                                        code=200, 
                                        user=UserOut.model_validate(user_model)) 
    



    def get_user_by_id(self, user_id: int) -> UserResponse:
        user_model = self.get_user_or_404(user_id)
        return UserResponse( message="Usuario encontrado correctamente por ID", 
                                        code=200, 
                                        user=UserOut.model_validate(user_model)) 

    def delete_user (self, user_id:int) -> UserResponse:
        user_model = self.get_user_or_404(user_id)
        self.db.delete(user_model)
        self.db.commit()
        
        return UserResponse( message="Usuario eliminado correctamente", 
                                        code=200, 
                                        user=None) 
    
    def get_all_users(self) -> list[UserOut]:
        users = self.db.query(UserModel).all()
        return [UserOut.model_validate(user) for user in users]  



    def get_user_or_404 (self, user_id: int) -> UserModel:
        user = self.db.query(UserModel).filter(UserModel.id==user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        return user