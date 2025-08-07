from fastapi import FastAPI
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlmodel import SQLModel, create_engine

# Importaciones de tu microservicio de autenticación
from app.api.routes import routes as auth_router
from app.core.database import get_db
from app.core.config import DATABASE_URL

# ---------------------
# Configuración de la base de datos
# ---------------------

engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    """
    Crea las tablas de la base de datos a partir de los modelos de SQLModel.
    """
    print("Creando tablas de la base de datos para el servicio de autenticación...")
    SQLModel.metadata.create_all(engine)
    print("Tablas creadas con éxito.")

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Función de ciclo de vida para la aplicación FastAPI.
    Se ejecuta al iniciar la aplicación.
    """
    create_db_and_tables()
    yield

# ---------------------
# Inicialización de la aplicación
# ---------------------

app = FastAPI(
    title="Auth Microservice",
    description="Microservicio para la autenticación y gestión de usuarios.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------
# Inclusión de rutas
# ---------------------

app.include_router(auth_router.router, prefix="/api/v1/auth")

# ---------------------
# Ruta principal
# ---------------------

@app.get("/", tags=["Root"])
def read_root():
    """
    Ruta de bienvenida del servicio.
    """
    return {"message": "Bienvenido al Microservicio de Autenticación"}
