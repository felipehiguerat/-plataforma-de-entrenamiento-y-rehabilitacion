import os
from typing import Generator
from sqlmodel import create_engine, Session, SQLModel

# Importar la URL de la base de datos desde el archivo de configuración
from app.core.config import DATABASE_URL

# Crear el motor de la base de datos
engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    """
    Crea las tablas de la base de datos a partir de los modelos SQLModel.
    """
    SQLModel.metadata.create_all(engine)


def get_db() -> Generator[Session, None, None]:
    """
    Función de dependencia para obtener una sesión de la base de datos.
    Crea una nueva sesión por cada solicitud y la cierra al finalizar.
    """
    with Session(engine) as session:
        yield session