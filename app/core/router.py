from app.routes.UserRoute import user_router as user_router
from app.routes.RecipeRoute import recipe_router as recipe_router
from app.routes.LikeRoute import like_router as like_router
from app.routes.LoginUser import login_router as login_router

def registerRouter(app):
    app.include_router(user_router, prefix="/user", tags=["users"])
    app.include_router(recipe_router, prefix="/recipe", tags=["recipes"])
    app.include_router(like_router, prefix="/like", tags=["likes"])
    app.include_router(login_router, prefix="/auth", tags=["auth"])

    

