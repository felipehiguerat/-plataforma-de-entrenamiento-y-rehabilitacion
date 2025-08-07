from fastapi import FastAPI
from app.routes import router
from app.core.database import engine
from app.domain.models.models import Base

app = FastAPI()

# Crear todas las tablas definidas en los modelos al iniciar la app
Base.metadata.create_all(bind=engine)

# Incluir rutas
app.include_router(router)
