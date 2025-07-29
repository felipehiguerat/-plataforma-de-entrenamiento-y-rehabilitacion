# microservicios/auth-service/app/config.py
import os
from datetime import timedelta

# Clave secreta para firmar los JWTs. ¡CAMBIA ESTO EN PRODUCCIÓN!
# Puedes generar una con: openssl rand -hex 32
SECRET_KEY = os.getenv("SECRET_KEY", "8b2b7bd1ea2fc45d4fc8c7068a1d3f20316f487b807f3ab1118f063605079174")
ALGORITHM = "HS256" # Algoritmo de hashing para JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30 # Tiempo de expiración del token de acceso
REFRESH_TOKEN_EXPIRE_DAYS = 7 # Tiempo de expiración del token de refresco (opcional para un flujo completo)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/auth_db")
