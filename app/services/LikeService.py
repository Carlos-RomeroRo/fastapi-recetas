from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.LikeModel import LikeModel
from app.schemas.LikeSchema import LikeCreate, LikeOut, LikeResponse, get_like_by_id
from fastapi import HTTPException
from app.repository.LikeRepository import LikeRepository
from app.repository.RecipeRepository import RecipeRepository
from app.repository.UserRepository import UserRepository

class LikeService:
    def __init__(self, db: Session):
        self.repo = LikeRepository(db)
        self.user_repo = UserRepository(db)
        self.recipe_repo = RecipeRepository(db)

    def create_like(self, recipe_id:int, user_id:int) -> LikeResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail=f"El usuario con el ID {user_id}no existe")
        recipe = self.recipe_repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(status_code=404, detail=f"La receta con el ID {recipe_id}no existe")
        
        new_like = LikeModel(user_id=user_id, recipe_id=recipe_id)

        try:
            self.repo.create(new_like)
            return LikeResponse(
                message="Like creado correctamente",
                code=201,
                like=LikeOut.model_validate(new_like)
            )
        except IntegrityError:
            self.repo.db.rollback()
            raise HTTPException(status_code=409, detail="El like ya existe para este usuario y receta")
            
        except Exception as e:
            self.repo.db.rollback()
            raise HTTPException(status_code=500, detail=f"Error al crear el like: {str(e)}")
        




    def get_like_by_id(self, user_id:int, recipe_id:int) -> LikeResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"El usuario con id {user_id} no existe"
            )
        recipe = self.recipe_repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=404,
                detail=f"La receta con id {recipe_id} no existe"
            )
        like = self.repo.get_by_user_and_recipe(user_id, recipe_id)
        if not like:
            raise HTTPException(
                status_code=404,
                detail="Like no encontrado para este usuario y receta"
            )
        return LikeResponse(
            message="Like encontrado",
            code=200,
            like=LikeOut.model_validate(like)
        )
        
    
    def get_all_likes(self) ->list[LikeOut]:
        likes = self.repo.get_all()
        return [LikeOut.model_validate(like) for like in likes]
   
   
    def delete_like (self, recipe_id:int, user_id:int) -> LikeResponse:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=404,
                detail=f"El usuario con id {user_id} no existe"
            )
        recipe = self.recipe_repo.get_by_id(recipe_id)
        if not recipe:
            raise HTTPException(
                status_code=404,
                detail=f"La receta con id {recipe_id} no existe"
            )
        like_model = self.repo.get_by_user_and_recipe(user_id,recipe_id)
        if not like_model:
            raise HTTPException(
                status_code=404,
                detail="Like no encontrado pa este usuario y receta"
            )
        self.repo.delete_by_like_model(like_model)
        return LikeResponse(message="Like eliminado correctamente", code=200, like=LikeOut.model_validate(like_model))


    