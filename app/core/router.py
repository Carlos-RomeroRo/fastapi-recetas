from app.routes.UserRoute import router as user_router

def registerRouter(app):
    app.include_router(user_router, prefix="/user", tags=["users"])