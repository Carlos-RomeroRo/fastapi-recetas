from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"mensaje": "Bebé como estás acabó de aterrizar en medallo"}

@app.get("/saludo/{nombre}")
def read_item(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a FastAPI 🚀"}
