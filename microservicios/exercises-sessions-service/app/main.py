from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from app.api.routes import routes_exercise, routes_session
from app.core.database import engine
from app.domain.models.models import Base

# Esta función se ejecutará al iniciar la aplicación y al detenerla.
# Es el lugar ideal para inicializar recursos como la base de datos.
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Gestiona el ciclo de vida de la aplicación.
    - Se ejecuta antes de que la aplicación comience a recibir solicitudes.
    - Se ejecuta después de que la aplicación termina de procesar solicitudes.
    """
    print("Creando tablas de la base de datos...")
    Base.metadata.create_all(bind=engine)
    yield
    print("Cerrando la aplicación...")


app = FastAPI(lifespan=lifespan)

# Incluir rutas de API
app.include_router(routes_exercise.router)
app.include_router(routes_session.router)