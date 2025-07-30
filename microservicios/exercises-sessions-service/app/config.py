# microservicios/exercises-sessions-service/app/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # ¡Asegúrate que esta URL apunte al nuevo servicio de DB!
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/exercises_db")
    # Si estás en desarrollo local sin Docker Compose, usaría localhost:5433 o localhost:5432
    # Pero dentro de Docker Compose, el nombre del servicio es clave.

settings = Settings()