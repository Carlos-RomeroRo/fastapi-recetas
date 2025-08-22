from fastapi import FastAPI
from app.core.router import registerRouter
from config import init_db

app = FastAPI() # inicializa la aplicación FastAPI
init_db()  # Inicializa las tablas en la base de datos
registerRouter(app) # Registra las rutas de la aplicación

@app.get("/")
def read_root():
    return {"mensaje": "Servidor iniciado correctamente!!"}

@app.get("/saludo/{nombre}")
def read_item(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a FastAPI 🚀"}
