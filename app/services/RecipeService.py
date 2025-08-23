from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.RecipeModel import RecipeModel
from schemas.RecipeSchema import RecipeCreate, RecipeOut, RecipePatch, RecipeResponse 
from fastapi import HTTPException

class RecipeService:
    def __init__(self, db: Session):
        self.db = db
    
    def create_recipe(self, recipe: RecipeCreate, user_id: int) -> RecipeResponse:
        new_recipe = RecipeModel(
            title = recipe.title,
            ingredients = recipe.ingredients,
            instructions = recipe.instructions,
            preparation_time = recipe.preparation_time,
            created_at = recipe.created_at,
            photo = recipe.photo,
            user_id = user_id
        )

        try:
            self.db.add(new_recipe)
            self.db.commit()
            self.db.refresh(new_recipe)
            return RecipeResponse(
                message = "Receta creada exitosamente",
                code = 201,
                recipe = RecipeOut.model_validate(new_recipe)
            )
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail="La receta ya existe con ese título"
            )
        except Exception as e:
            self.db.rollback()
            raise HTTPException(
                status_code=500,
                detail=f"Error al crear la receta: {str(e)}"
            )

    def patch_recipe (self, recipe_id: int, recipe: RecipePatch) -> RecipeResponse:
        db_recipe = self.get_recipe_or_404(recipe_id)
        update_data = recipe.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_recipe, key, value)

        self.db.commit()
        self.db.refresh(db_recipe)

        return RecipeResponse( message="Receta actualizada correctamente", 
                                        code=200, 
                                        recipe=RecipeOut.model_validate(db_recipe))
    
    def delete_recipe(self, recipe_id: int) -> RecipeResponse:
        db_recipe = self.get_recipe_or_404(recipe_id)
        self.db.delete(db_recipe)
        self.db.commit()
        return RecipeResponse(message="Receta eliminada correctamente", code=200, recipe=None)
    
    def get_recipe_by_id(self, recipe_id: int) -> RecipeResponse:
        db_recipe = self.get_recipe_or_404(recipe_id)
        return RecipeResponse(message="Receta encontrada correctamente", code=200, recipe=RecipeOut.model_validate(db_recipe))
    
    def get_all_recipes(self) -> RecipeResponse:
        db_recipes = self.db.query(RecipeModel).all()
        recipes_out = [RecipeOut.model_validate(recipe) for recipe in db_recipes]
        return RecipeResponse(message="Recetas obtenidas correctamente", code=200, recipe=recipes_out)
    
    def get_recipe_or_404 (self, recipe_id: int) -> RecipeModel:
        db_recipe = self.db.query(RecipeModel).filter(RecipeModel.id==recipe_id).first()
        if not db_recipe:
            raise HTTPException(status_code=404, detail="Receta no encontrada")
        
        return db_recipe