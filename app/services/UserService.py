from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.UserModel import UserModel
from app.schemas.UserSchema import UserCreate, UserResponse, UserPatch, UserOut
from fastapi import HTTPException
from passlib.context import CryptContext
from app.repository.UserRepository import UserRepository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)
    
    def create_user(self, user: UserCreate) -> UserResponse:
        hashed_password = pwd_context.hash(user.password)
        new_user = UserModel(
            username=user.username,
            email=user.email,
            role=user.role.value,
            password=hashed_password
        ) 
        try:
            create_user = self.repo.create(new_user)
            return UserResponse(
                message = "Usuario creado exitosamente",
                code = 201,
                user = UserOut.model_validate(create_user)
            )
        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="El usuario ya existe con ese nombre de usuario o correo electrónico"
            )
        except Exception as e:
            self.repo.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear el usuario: {str(e)}"
            )
    
    def user_patch(self, user_id: int, user: UserPatch) -> UserResponse:
        user_model = self.get_user_or_404(user_id)
        patch_data = user.model_dump(exclude_unset=True)

        for key,value in patch_data.items():
            setattr(user_model, key, value)

        self.repo.update(user_model) # update method from BaseRepository
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
        self.repo.delete(user_model)
        
        return UserResponse( message="Usuario eliminado correctamente", 
                                        code=200, 
                                        user=None) 
    
    def get_all_users(self) -> list[UserOut]:
        users = self.repo.get_all()
        return [UserOut.model_validate(user) for user in users]  



    def get_user_or_404 (self, user_id: int) -> UserModel:
        user = self.repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return user