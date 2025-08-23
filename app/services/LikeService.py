from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.LikeModel import LikeModel
from schemas.LikeSchema import LikePatch, LikeCreate, LikeOut, LikeResponse
from fastapi import HTTPException

class LikeService:
    def __init__(self, db: Session):
        self.db = db

    def create_like(self, like: LikeCreate) -> LikeResponse:
        new_like = LikeModel(
            user_id=like.user_id,
            recipe_id=like.recipe_id
        )
        try:
            self.db.add(new_like)
            self.db.commit()
            self.db.refresh(new_like)
            return LikeResponse(
                message="Like creado exitosamente",
                code=201,
                like=LikeOut.model_validate(new_like)
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="El like ya existe para este usuario y receta"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear el like: {str(e)}"
            )
    
    def like_patch(self, like_id: int, like: LikePatch) -> LikeResponse:
        like_model = self.get_like_or_404(like_id)
        
        patch_data = like.model_dump(exclude_unset=True)

        for key,value in patch_data.items():
            setattr(like_model, key, value)

        self.db.commit()
        self.db.refresh(like_model)

        return LikeResponse( message="Like actualizado correctamente", 
                                        code=200, 
                                        like=LikeOut.model_validate(like_model))
    
    def get_like_by_id(self, like_id: int) -> LikeResponse:
        like_model = self.get_like_or_404(like_id)
        return LikeResponse( message="Like encontrado correctamente por ID", 
                                        code=200, 
                                        like=LikeOut.model_validate(like_model))