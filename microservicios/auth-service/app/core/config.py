import os
from datetime import timedelta

# Clave secreta para firmar los JWTs
SECRET_KEY = os.getenv("SECRET_KEY", "8b2b7bd1ea2fc45d4fc8c7068a1d3f20316f487b807f3ab1118f063605079174")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7

# Configuración de la base de datos
DB_USER = os.getenv("POSTGRES_USER", "user")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "password")
DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "auth_db")

# Construir la URL de la base de datos
# Esta URL usará 'db' como host por defecto, lo que permite la comunicación entre contenedores
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"