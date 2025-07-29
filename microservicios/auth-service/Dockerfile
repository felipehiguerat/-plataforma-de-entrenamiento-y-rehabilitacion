# microservicios/auth-service/Dockerfile

# Usamos una imagen base oficial de Python
# python:3.12-slim-bookworm es una versión ligera basada en Debian Bookworm
FROM python:3.12-slim-bookworm

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos de configuración de Poetry
# La copia se hace antes de instalar las dependencias para aprovechar el cache de Docker
COPY pyproject.toml poetry.lock ./

# Instala Poetry
RUN pip install poetry==1.8.2

# Configura Poetry para no crear entornos virtuales dentro del proyecto
# Esto es importante para que las dependencias se instalen directamente en el entorno del contenedor
RUN poetry config virtualenvs.create false

# Instala las dependencias del proyecto usando poetry
RUN poetry install --no-root --no-dev

# Copia el resto del código de la aplicación
# .dockerignore debe excluir .venv, __pycache__, etc.
COPY . .

# Expone el puerto en el que la aplicación va a escuchar (el mismo que usas en Uvicorn)
EXPOSE 8001

# Comando para ejecutar la aplicación cuando el contenedor se inicie
# Usamos Gunicorn con Uvicorn workers para un entorno de producción más robusto
# 'main:app' se refiere al archivo main.py y la instancia de FastAPI 'app'
# --host 0.0.0.0 es crucial para que la aplicación sea accesible desde fuera del contenedor
# --port 8001 es el puerto interno del contenedor
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]