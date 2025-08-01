from fastapi import FastAPI
from app.routes import router
from app.database import engine
from app.models import Base

app = FastAPI()

# Crear todas las tablas definidas en los modelos al iniciar la app
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(router)
