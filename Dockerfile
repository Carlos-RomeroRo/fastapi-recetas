# Imagen base con Python
FROM python:3.11-slim

# Crear directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiar requirements primero (mejor para cache de Docker)
COPY requirements.txt .

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto que usará Uvicorn
EXPOSE 5000

# Comando para ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]
