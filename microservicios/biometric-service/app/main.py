from fastapi import FastAPI
from app.api.routers.biometrics_routes import router as biometric_router
from app.core.database import engine
from app.domain.models import Base

# Crear todas las tablas al iniciar la app
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Performance Biometrics Microservice",
    description="Microservicio para gestionar datos biométricos de rendimiento.",
    version="1.0.0",
)

# Incluir el objeto router
app.include_router(biometric_router)

@app.get("/", tags=["Root"])
def read_root():
    return {"message": "Bienvenido al Microservicio de Biometría de Performance"}