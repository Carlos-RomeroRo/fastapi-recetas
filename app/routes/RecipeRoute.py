#create recipe routes

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import get_db
from app.schemas.RecipeSchema import RecipeCreate, RecipeResponse, RecipeUpdate, RecipePatch, RecipeOut
from app.services.RecipeService import RecipeService
from app.auth.authGet import get_current_user

recipe_router = APIRouter()

@recipe_router.post("/create", response_model=RecipeResponse)
def createRecipe(recipe: RecipeCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    service = RecipeService(db)
    return service.create_recipe(recipe, current_user.id)

@recipe_router.get("/{recipe_id}", response_model=RecipeResponse)
def getRecipeById(recipe_id:int, db: Session = Depends(get_db)):
    service = RecipeService(db)
    return service.get_recipe_by_id(recipe_id)

@recipe_router.patch("/{recipe_id}", response_model=RecipeResponse)
def patchRecipe(recipe_id: int, recipe: RecipePatch, db: Session = Depends(get_db)):
    service = RecipeService(db)
    return service.recipe_patch(recipe_id, recipe)

@recipe_router.delete("/{recipe_id}", response_model=RecipeResponse)
def deleteRecipe(recipe_id: int, db: Session = Depends(get_db)):
    service = RecipeService(db)
    return service.delete_recipe(recipe_id)

@recipe_router.get("/", response_model=list[RecipeOut])
def getAllRecipes(db: Session = Depends(get_db)):
    service = RecipeService(db)
    return service.get_all_recipes()